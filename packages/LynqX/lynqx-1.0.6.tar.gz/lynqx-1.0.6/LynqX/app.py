#!/usr/bin/env python3
"""
P2P Chat Client with Textual TUI
"""

import asyncio
import httpx
import json
import base64
import os
import argparse
import threading
import requests
from sseclient import SSEClient
from urllib.parse import urlparse
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog, Static
from textual.containers import Vertical
from textual import events
import uuid
from datetime import datetime
from time import time, sleep
import emoji
import threading  # For synchronization
import aiofiles  # New import for async file I/O
import websockets
from websockets.exceptions import ConnectionClosedOK

# Hardcoded base URL
BASE_URL = "https://lynqx.onrender.com"
API_HOST = "lynqx.onrender.com"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsImV4cCI6MTc0Nzk4ODgyOX0._GuIVI3PUL4g1IUz-Jlu7PNiTf8fGs3o2EhEr4lsQNo"

# Credentials for token retrieval (update as needed)
USERNAME = "alice"
PASSWORD = "s3cr3t"

async def get_jwt_token(username: str, password: str) -> str:
    """
    Fetch a Bearer JWT from the /token endpoint.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://{API_HOST}/token",
            data={"username": username, "password": password},
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

class LynqX(App):
    """Textual app for P2P chat client."""
    CSS = """
    RichLog {
        height: 60%;
        border: solid green;
    }
    Static#progress_label {
        height: 5%;
        color: yellow;
    }
    Input {
        height: 20%;
        border: solid blue;
    }
    Static#status {
        height: 15%;
        background: grey;
        color: black;
        padding: 1;
    }
    """

    CHUNK_SIZE = 262144  # 256 KB

    def __init__(self, room_id, **kwargs):
        super().__init__(**kwargs)
        self.room_id = room_id
        self.base_url = BASE_URL
        self.client_id = str(uuid.uuid4())
        self.nickname = "Anonymous"
        self.connection_status = "Connecting..."
        self.file_progress = {}  # {filename: (total_size, current_size)}
        self.reconnect_attempts = 0
        self.typing_task = None
        self.typing_users = {}  # {nickname: timeout_task}
        self.progress_lock = threading.Lock()  # For synchronizing file_progress updates
        self.active_clients_count = 1  # Track the number of clients in the room
        self.cancel_file_transfer = False  # Flag to stop file transfer
        self.current_file = None  # Track the currently transferring file
        self.file_transfer_state = {}  # {filename: {"path": str, "total_size": int, "current_size": int}}

    def compose(self) -> ComposeResult:
        """Create the TUI layout."""
        yield Header(show_clock=True)
        yield Vertical(
            RichLog(id="chat_log", wrap=True, markup=True),
            Static("", id="progress_label"),
            Input(placeholder="Type a message, /file, or /help", id="input"),
            Static(f"Room: {self.room_id} | Nickname: {self.nickname} | Status: {self.connection_status}", id="status"),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Start the receive loop."""
        self.query_one("#progress_label", Static).visible = False
        threading.Thread(target=self.start_receive_loop, daemon=True).start()

    def check_network(self) -> bool:
        """Check if the network is available by pinging the server's health endpoint."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    async def check_ongoing_transfers(self):
        """Check with the server for any ongoing file transfers and resume them."""
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
            try:
                response = await client.get(f"{self.base_url}/rooms/{self.room_id}/get_file_progress?client_id={self.client_id}")
                if response.status_code == 200:
                    ongoing_transfers = response.json().get("ongoing_transfers", {})
                    for filename, server_current_size in ongoing_transfers.items():
                        if filename in self.file_transfer_state:
                            # Update the local state with the server's progress
                            state = self.file_transfer_state[filename]
                            state["current_size"] = server_current_size
                            self.add_message(f"[yellow][{self.get_timestamp()}] Resuming file transfer for '{filename}' from {server_current_size} bytes...[/]")
                            # Resume the file transfer
                            await self.resume_file_transfer(filename, state["path"], state["total_size"], server_current_size)
            except httpx.RequestError as e:
                self.add_message(f"[red][{self.get_timestamp()}] Error checking ongoing transfers: {e}[/]")

    async def resume_file_transfer(self, filename: str, file_path: str, total_size: int, start_position: int):
        """Resume a file transfer from the given position."""
        send_url = f"{self.base_url}/rooms/{self.room_id}/send"
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
            self.current_file = filename
            self.cancel_file_transfer = False
            with self.progress_lock:
                self.file_progress[filename] = (total_size, start_position)
            self.start_file_progress(filename, total_size)
            try:
                with open(file_path, 'rb') as f:
                    f.seek(start_position)  # Move to the last sent position
                    while chunk := f.read(8192):
                        if self.cancel_file_transfer:
                            self.add_message(f"[red][{self.get_timestamp()}] File transfer for '{filename}' canceled.[/]")
                            self.end_file_progress(filename)
                            return
                        b64 = base64.b64encode(chunk).decode()
                        with self.progress_lock:
                            total_size, current_size = self.file_progress[filename]
                            current_size += len(chunk)
                            self.file_progress[filename] = (total_size, current_size)
                            self.file_transfer_state[filename]["current_size"] = current_size
                        self.update_file_progress(filename)
                        await client.post(send_url, json={
                            'type': 'file-chunk',
                            'filename': filename,
                            'data': b64,
                            'client_id': self.client_id,
                            'nickname': self.nickname
                        })
                if self.cancel_file_transfer:
                    self.add_message(f"[red][{self.get_timestamp()}] File transfer for '{filename}' canceled.[/]")
                    self.end_file_progress(filename)
                    return
                await client.post(send_url, json={
                    'type': 'file-end',
                    'filename': filename,
                    'data': '',
                    'client_id': self.client_id,
                    'nickname': self.nickname
                })
                self.add_message(f"[blue][{self.get_timestamp()}] Sent file '{filename}'[/]")
                self.current_file = None
                self.file_transfer_state.pop(filename, None)
                self.end_file_progress(filename)
            except Exception as e:
                self.add_message(f"[red][{self.get_timestamp()}] Error resuming file '{filename}': {e}[/]")
                self.current_file = None
                self.file_transfer_state.pop(filename, None)
                self.end_file_progress(filename)

    def start_receive_loop(self):
        """Receive messages and files via SSE with auto-reconnection logic."""
        url = f"{self.base_url}/rooms/{self.room_id}/stream?client_id={self.client_id}"
        self.call_from_thread(self.add_message, f"[yellow][{self.get_timestamp()}] Welcome to room {self.room_id}! Type /help for commands.[/]")
        while True:  # Loop indefinitely until the user exits
            try:
                self.call_from_thread(self.update_status, "Connecting to stream...")
                # Retry connecting to the stream up to 3 times if a 404 is encountered
                connect_attempts = 3
                for attempt in range(connect_attempts):
                    response = requests.get(url, stream=True)
                    if response.status_code == 404:
                        if attempt < connect_attempts - 1:
                            self.call_from_thread(self.add_message, f"[yellow][{self.get_timestamp()}] Room {self.room_id} not found, retrying ({attempt + 1}/{connect_attempts})...[/]")
                            sleep(1)
                            continue
                        else:
                            self.call_from_thread(self.update_status, f"Room {self.room_id} not found.")
                            self.call_from_thread(self.add_message, f"[red][{self.get_timestamp()}] Room {self.room_id} not found after {connect_attempts} attempts.[/]")
                            return
                    break  # If successful, break out of the retry loop
                self.call_from_thread(self.update_status, "Connected to stream.")
                self.call_from_thread(self.add_message, f"[yellow][{self.get_timestamp()}] Successfully connected to the room.[/]")
                # Check for ongoing file transfers and resume them
                self.run_worker(self.check_ongoing_transfers(), exclusive=False)
                self.reconnect_attempts = 0
                client = SSEClient(response)
            except Exception as e:
                self.reconnect_attempts += 1
                self.call_from_thread(self.update_status, f"Connection failed: {e}. Reconnecting (attempt {self.reconnect_attempts})...")
                self.call_from_thread(self.add_message, f"[red][{self.get_timestamp()}] Connection lost: {e}. Attempting to reconnect...[/]")
                # Wait for network recovery with exponential backoff
                while not self.check_network():
                    self.call_from_thread(self.update_status, f"Network unavailable. Waiting to reconnect (attempt {self.reconnect_attempts})...")
                    sleep(min(2 ** self.reconnect_attempts, 30))  # Cap backoff at 30 seconds
                sleep(min(2 ** self.reconnect_attempts, 30))  # Additional delay after network recovery
                continue

            fobj = None
            filename = None

            try:
                for event in client.events():
                    msg = json.loads(event.data)
                    t = msg.get('type')
                    if t == 'client_count':
                        self.active_clients_count = msg.get('count', 1)
                        self.call_from_thread(self.update_status, self.connection_status)  # Update status bar with new client count
                    elif t == 'message':
                        if msg.get('client_id') != self.client_id:
                            nick = msg.get('nickname', 'Peer')
                            text = emoji.emojize(msg['data'], language='alias')
                            self.call_from_thread(self.add_message, f"[green][{self.get_timestamp()}] {nick}:[/] {text}")
                    elif t == 'typing':
                        if msg.get('client_id') != self.client_id:
                            nick = msg.get('nickname', 'Peer')
                            self.call_from_thread(self.update_typing, nick, True)
                    elif t == 'file':
                        filename = msg['filename']
                        with self.progress_lock:
                            self.file_progress[filename] = (msg['size'], 0)
                        # If the file already exists (from a previous partial transfer), open in append mode
                        fobj = open(filename, 'ab')
                        self.current_file = filename  # Track the current file
                        self.call_from_thread(self.start_file_progress, filename, msg['size'])
                    elif t == 'file-chunk' and fobj:
                        chunk = base64.b64decode(msg['data'])
                        fobj.write(chunk)
                        with self.progress_lock:
                            total_size, _ = self.file_progress.get(filename, (0, 0))
                            current_size = msg.get('current_size') or 0
                            self.file_progress[filename] = (total_size, current_size)
                        self.call_from_thread(self.update_file_progress, filename)
                    elif t == 'file-end' and fobj:
                        fobj.close()
                        self.current_file = None
                        self.call_from_thread(self.add_message, f"[green][{self.get_timestamp()}] Received file '{filename}'[/]")
                        self.call_from_thread(self.end_file_progress, filename)
                    elif t == 'file-cancel' and fobj:
                        fobj.close()
                        os.remove(filename)  # Delete the partially transferred file
                        self.current_file = None
                        self.call_from_thread(self.add_message, f"[red][{self.get_timestamp()}] File transfer for '{msg['filename']}' canceled.[/]")
                        self.call_from_thread(self.end_file_progress, msg['filename'])
            except Exception as e:
                self.reconnect_attempts += 1
                self.call_from_thread(self.update_status, f"Stream disconnected: {e}. Reconnecting (attempt {self.reconnect_attempts})...")
                self.call_from_thread(self.add_message, f"[red][{self.get_timestamp()}] Stream disconnected: {e}. Attempting to reconnect...[/]")
                if fobj:
                    fobj.close()
                    self.current_file = None
                # Wait for network recovery with exponential backoff
                while not self.check_network():
                    self.call_from_thread(self.update_status, f"Network unavailable. Waiting to reconnect (attempt {self.reconnect_attempts})...")
                    sleep(min(2 ** self.reconnect_attempts, 30))  # Cap backoff at 30 seconds
                sleep(min(2 ** self.reconnect_attempts, 30))  # Additional delay after network recovery
                continue

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        text = event.value.strip()
        if not text:
            return
        self.query_one("#input", Input).value = ""

        # Handle commands
        if text == '/help':
            self.add_message(
                "[yellow]Commands:[/]\n"
                "  /help - Show this help\n"
                "  /nick <name> - Set your nickname\n"
                "  /file <path> - Send a file\n"
                "  /stop - Stop an ongoing file transfer\n"
                "  /clear - Clear chat log\n"
                "  /exit - Exit the app"
            )
            return
        elif text.startswith('/nick '):
            new_nick = text.split(' ', 1)[1].strip()
            if new_nick:
                self.nickname = new_nick
                self.add_message(f"[yellow][{self.get_timestamp()}] Nickname set to '{new_nick}'[/]")
                self.update_status(self.connection_status)
            return
        elif text == '/clear':
            self.query_one("#chat_log", RichLog).clear()
            return
        elif text == '/stop':
            if not self.current_file:
                self.add_message(f"[yellow][{self.get_timestamp()}] No file transfer in progress.[/]")
                return
            # Cancel the file transfer
            self.cancel_file_transfer = True
            filename = self.current_file
            send_url = f"{self.base_url}/rooms/{self.room_id}/send"
            async def send_cancel():
                async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                    try:
                        await client.post(send_url, json={
                            'type': 'file-cancel',
                            'filename': filename,
                            'data': '',
                            'client_id': self.client_id,
                            'nickname': self.nickname
                        })
                    except Exception as e:
                        self.add_message(f"[red][{self.get_timestamp()}] Error canceling file transfer: {e}[/]")
            self.run_worker(send_cancel(), exclusive=False)
            self.file_transfer_state.pop(filename, None)  # Remove from state
            return
        elif text == '/exit':
            self.exit()
            return

        send_url = f"{self.base_url}/rooms/{self.room_id}/send"
        async def send():
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
                if text.startswith('/file '):
                    path = text.split(' ', 1)[1]
                    if not os.path.isfile(path):
                        self.add_message(f"[red]File not found: {path}[/]")
                        return
                    filename = os.path.basename(path)
                    room = self.room_id
                    # 1) retrieve fresh JWT
                    try:
                        token = await get_jwt_token(USERNAME, PASSWORD)
                    except Exception as e:
                        self.add_message(f"[red]Auth failed: {e}[/]")
                        return
                    uri = f"wss://{API_HOST}/ws/{room}"
                    headers = [("Authorization", f"Bearer {token}")]
                    self.add_message(f"[green]Starting file transfer: {filename}[/]")
                    try:
                        # 1 WebSocket → true streaming
                        async with websockets.connect(uri, extra_headers=headers) as ws:
                            with open(path, "rb") as f:
                                while chunk := f.read(64 * 1024):
                                    await ws.send(chunk)
                        # clean close signals file-end
                        self.add_message(f"[green]File transfer complete: {filename}[/]")
                    except ConnectionClosedOK:
                        self.add_message(f"[green]File transfer complete: {filename}[/]")
                    except Exception as e:
                        self.add_message(f"[red]File transfer failed: {e}[/]")
                    return
                else:
                    try:
                        await client.post(send_url, json={
                            'type': 'message',
                            'data': text,
                            'client_id': self.client_id,
                            'nickname': self.nickname
                        })
                        text_emojized = emoji.emojize(text, language='alias')
                        self.add_message(f"[blue][{self.get_timestamp()}] You: {text_emojized}[/]")
                    except Exception as e:
                        self.add_message(f"[red][{self.get_timestamp()}] Error sending message: {e}[/]")

        self.run_worker(send(), exclusive=False)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle typing events."""
        if event.value and not self.typing_task:
            self.typing_task = self.run_worker(self.send_typing(), exclusive=False)

    async def send_typing(self):
        """Send typing event to server."""
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
            try:
                await client.post(
                    f"{self.base_url}/rooms/{self.room_id}/typing",
                    json={
                        'type': 'typing',
                        'data': '',
                        'client_id': self.client_id,
                        'nickname': self.nickname
                    }
                )
            except Exception as e:
                self.add_message(f"[red][{self.get_timestamp()}] Error sending typing event: {e}[/]")
        await asyncio.sleep(5)
        self.typing_task = None

    def update_typing(self, nickname: str, is_typing: bool) -> None:
        """Update typing indicators with timeout."""
        if is_typing:
            if nickname in self.typing_users:
                self.typing_users[nickname].cancel()
            self.typing_users[nickname] = self.run_worker(self.remove_typing(nickname), exclusive=False)
        else:
            if nickname in self.typing_users:
                self.typing_users[nickname].cancel()
                del self.typing_users[nickname]

        if self.typing_users:
            typing_text = f"[yellow]{', '.join(self.typing_users.keys())} {'is' if len(self.typing_users) == 1 else 'are'} typing...[/]"
            self.query_one("#status", Static).update(
                f"Room: {self.room_id} | Nickname: {self.nickname} | Clients: {self.active_clients_count} | Join: lynqx -j {self.room_id} | Status: {self.connection_status}\n{typing_text}"
            )
        else:
            self.update_status(self.connection_status)

    async def remove_typing(self, nickname: str):
        """Remove typing indicator after timeout."""
        await asyncio.sleep(5)
        if nickname in self.typing_users:
            del self.typing_users[nickname]
        if self.typing_users:
            typing_text = f"[yellow]{', '.join(self.typing_users.keys())} {'is' if len(self.typing_users) == 1 else 'are'} typing...[/]"
            self.query_one("#status", Static).update(
                f"Room: {self.room_id} | Nickname: {self.nickname} | Clients: {self.active_clients_count} | Join:lynqx -j {self.room_id} | Status: {self.connection_status}\n{typing_text}"
            )
        else:
            self.update_status(self.connection_status)

    def add_message(self, message: str) -> None:
        """Add a message to the chat log."""
        self.query_one("#chat_log", RichLog).write(message)

    def update_status(self, status: str) -> None:
        """Update the status bar with room info."""
        self.connection_status = status
        self.query_one("#status", Static).update(
            f"Room: {self.room_id} | Nickname: {self.nickname} | Clients: {self.active_clients_count} | Join: lynqx -j {self.room_id} | Status: {status}"
        )

    def get_timestamp(self) -> str:
        """Get current timestamp in HH:MM format."""
        return datetime.now().strftime("%H:%M")

    def start_file_progress(self, filename: str, total_size: int) -> None:
        """Start file transfer progress indication."""
        progress_label = self.query_one("#progress_label", Static)
        progress_label.update(f"Transferring '{filename}' (0/{total_size} bytes)")
        progress_label.visible = True

    def update_file_progress(self, filename: str) -> None:
        """Update file transfer progress indication."""
        with self.progress_lock:
            total_size, current_size = self.file_progress.get(filename, (0, 0))
        progress_label = self.query_one("#progress_label", Static)
        progress_label.update(f"Transferring '{filename}' ({current_size}/{total_size} bytes)")

    def end_file_progress(self, filename: str) -> None:
        """End file transfer progress indication."""
        progress_label = self.query_one("#progress_label", Static)
        progress_label.visible = False
        with self.progress_lock:
            self.file_progress.pop(filename, None)

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts."""
        if event.key == "ctrl+c" or event.key == "escape":
            self.exit()

    async def file_chunk_generator(self, path):
        async with aiofiles.open(path, 'rb') as f:
            while True:
                chunk = await f.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk

    async def stream_file_upload(self, path, filename):
        url = f"{self.base_url}/upload"
        headers = {
            "Content-Type": "application/octet-stream",
            "X-Filename": filename
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                data=self.file_chunk_generator(path),
                headers=headers
            )
            return response

def main():
    asyncio.run(run())

async def run():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--create', action='store_true', help='Create room')
    group.add_argument('-j', '--join', metavar='ROOM_ID', help='Join room')
    args = parser.parse_args()

    async with httpx.AsyncClient() as client:
        if args.create:
            resp = await client.post(f"{BASE_URL}/create")
            data = resp.json()
            rid = data['room_id']
        else:
            rid = args.join
            try:
                check = await client.get(f"{BASE_URL}/rooms/{rid}")
                if check.status_code == 404:
                    print(f"Room {rid} not found.")
                    return
            except httpx.RequestError as e:
                print(f"Error checking room: {e}")
                return

    app = LynqX(room_id=rid)
    await app.run_async()

if __name__ == "__main__":
    main()
