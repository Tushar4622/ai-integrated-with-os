# AI-Integrated OS — Voice & Gesture-Controlled Assistant Platform

A Python-based voice/text assistant module and the current core of the **AI-Integrated OS** project — an initiative to build a computing experience centered on AI, voice and gesture interaction, automation, and adaptive learning. This module listens for spoken or typed commands and automates web browsing, media playback, WhatsApp Web, and desktop actions.

> This is the assistant/automation layer of the broader AI-Integrated OS vision. Future modules (gesture interaction, adaptive learning, deeper OS-level integration) will build on this foundation.

## Features

- **Voice or text input** — uses `speech_recognition` + Google Speech API when a microphone is available; falls back to typed input otherwise.
- **Text-to-speech responses** via `pyttsx3` (SAPI5 voice engine).
- **Web search** — Google, YouTube, or GitHub, based on keywords in the command.
- **Wikipedia lookups** — short summaries via the `wikipedia` package.
- **Quick site launcher** — opens YouTube, Google, GitHub, TryHackMe, ChatGPT, Smash Karts, NetMirror.
- **Ask ChatGPT** — opens ChatGPT pre-filled with a spoken/typed question.
- **YouTube playback** — uses Selenium to search YouTube and auto-play the first result.
- **NetMirror playback** — searches and plays a title on NetMirror via Selenium.
- **WhatsApp Web automation** — open WhatsApp Web, switch chats, send/type messages, delete last message, attach files, and start/end voice or video calls (via Selenium).
- **Browser/tab control** — close the current tab or browser window using `pyautogui` hotkeys.
- **Time announcement** and **graceful exit** commands.

## Requirements

- Python 3.8+
- Google Chrome installed
- A working microphone (optional — falls back to text mode if unavailable)

### Python Dependencies

```bash
pip install pyttsx3 wikipedia pyautogui SpeechRecognition selenium webdriver-manager
```

> **Note:** `os`, `sys`, `time`, `datetime`, and `urllib.parse` are part of the Python standard library and need no installation.

### ChromeDriver

- The YouTube and NetMirror playback functions expect a `chromedriver.exe` in the working directory (Windows-specific path).
- The WhatsApp automation function uses `webdriver_manager` to auto-download the correct ChromeDriver, so no manual setup is needed for that feature.

## Usage

Run the script:

```bash
python ai_integrated_os.py
```

AI-Integrated OS will greet you based on the time of day, then wait for a command (spoken or typed).

### Example Commands

| Say / Type | Action |
|---|---|
| "What can you do?" | Lists AI-Integrated OS's capabilities |
| "Search for cats" | Searches Google |
| "Search for lofi music on YouTube" | Searches and plays first YouTube result |
| "Search for react on GitHub" | Searches GitHub |
| "Wikipedia Albert Einstein" | Reads a short Wikipedia summary |
| "Open YouTube" / "Open Google" / "Open GitHub" | Opens the site |
| "Open TryHackMe" | Opens TryHackMe |
| "Open ChatGPT" | Opens ChatGPT |
| "Ask ChatGPT ..." | Prompts for a question, opens ChatGPT with it pre-filled |
| "Open NetMirror" | Opens NetMirror |
| "Play [song] on YouTube" | Plays a song on YouTube |
| "Play [title] on NetMirror" | Plays a title on NetMirror |
| "Open WhatsApp" | Launches WhatsApp Web |
| "Switch to [contact name]" | Opens a specific WhatsApp chat |
| "Send message [text]" | Sends a WhatsApp message |
| "Type [text]" | Drafts (without sending) a WhatsApp message |
| "Delete last message" | Deletes your last sent WhatsApp message |
| "Voice call" / "Video call" / "End call" | Controls WhatsApp calls |
| "Close tab" / "Close browser" | Closes the active tab or window |
| "Time" | Announces the current time |
| "Exit" / "Quit" / "Goodbye" | Shuts AI-Integrated OS down |

## Known Limitations / Notes

- `chromedriver.exe` path is hardcoded for Windows in `play_youtube_song` and `play_netmirror` — update this path (or use `webdriver_manager` like the WhatsApp function does) for cross-platform use.
- The WhatsApp Chrome profile path (`C:/AIIntegratedOSChromeProfile`) is Windows-specific; change it for macOS/Linux.
- Selenium-based automation (YouTube, NetMirror, WhatsApp) depends on the current DOM structure of those sites and may break if the sites update their layout.
- `pyautogui.FAILSAFE` is enabled — move your mouse to a screen corner to abort a stuck automation.
- Some WhatsApp command matches (e.g. `"open WhatsApp" in query`) are case-sensitive by design; ensure exact phrasing or adjust the code to use `query_lower` for consistency.

## Disclaimer

This project automates third-party websites (YouTube, WhatsApp Web, NetMirror, GitHub, ChatGPT) via browser automation. Usage should comply with each site's Terms of Service. NetMirror in particular may host content without proper licensing — use at your own discretion and risk.
