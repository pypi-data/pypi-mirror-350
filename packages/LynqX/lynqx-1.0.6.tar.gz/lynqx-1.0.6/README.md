# LynqX

**LynqX** is a terminal-based peer-to-peer chat client built using [Textual](https://textual.textualize.io/). It supports:

* Real-time messaging
* File sharing (with resume and cancel support)
* Typing indicators
* Emoji rendering
* Reconnection logic
* Custom commands

LynqX connects to a backend server (e.g., [LynqX server](https://github.com/SwagCoder18/ChatX)) for managing chat rooms and delivering messages over Server-Sent Events (SSE).

---

## 🚀 Features

* 📦 File transfers with resume capability
* 🔒 Cancel transfers anytime
* 🧠 Reconnect logic with exponential backoff
* 😃 Emoji support via `emoji` Python package
* 🧑‍💻 Typing indicators for active participants
* 📿 Textual UI for a clean terminal interface

---

## 📆 Installation

```
pip install lynqx
```

This will automatically install all required dependencies:

* `textual`
* `httpx`
* `requests`
* `sseclient`
* `emoji`

---

## 🧑‍💻 Usage

### Create a new chat room:

```
lynqx -c
```

### Join an existing room:

```
lynqx -j <room_id>
```

---

## ⚙️ Requirements

* Python 3.8+

---

## 🧠 Customization

* You can change the base server URL in `app.py` via the `BASE_URL` constant.
* For advanced use, fork or modify the [LynqX server backend](https://github.com/SwagCoder18/ChatX).

---

## 📄 License

MIT — see the [LICENSE](./LICENSE) file for details.