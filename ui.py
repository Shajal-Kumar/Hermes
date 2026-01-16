# ui.py
import threading  # <--- 1. ADD THIS IMPORT
from textual.app import App, ComposeResult
from textual.widgets import Input, RichLog, Header, Footer
from backend import IRCClient

class IRCApp(App):
    # ... (Keep CSS and Compose exactly the same) ...
    CSS = """
    Screen { layout: vertical; }
    RichLog { height: 1fr; border: solid green; }
    Input { dock: bottom; border: wide $accent; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="chat_log", highlight=True, markup=True)
        yield Input(placeholder="Type message...", id="message_input")
        yield Footer()

    def on_mount(self):
        # ... (Same as before) ...
        self.server_config = {
            "server": "irc.libera.chat",
            "port": 6667,
            "nick": "TextualDev01",
            "channel": "#python-test-room"
        }

        self.client = IRCClient(
            self.server_config["server"],
            self.server_config["port"],
            self.server_config["nick"],
            self.server_config["channel"],
            callback=self.on_backend_message
        )
        self.client.connect()
        self.query_one("#message_input").focus()

    def on_backend_message(self, message_text):
        """Called by backend. Bridges to UI thread safely."""
        
        # Formatting logic (Same as before)
        formatted_msg = message_text
        if "Connected" in message_text or "Joined" in message_text:
            formatted_msg = f"[bold green]{message_text}[/]"
        elif ":" in message_text:
            nick, msg = message_text.split(":", 1)
            formatted_msg = f"[cyan]{nick}[/]:{msg}"

        # --- THE FIX IS HERE ---
        # If we are ALREADY on the main thread, just write directly.
        # If we are on a background thread, use call_from_thread.
        if threading.current_thread() is threading.main_thread():
            self.write_to_log(formatted_msg)
        else:
            self.call_from_thread(self.write_to_log, formatted_msg)

    def write_to_log(self, text):
        self.query_one(RichLog).write(text)

    # ... (Keep on_input_submitted exactly the same) ...
    def on_input_submitted(self, event: Input.Submitted):
        message = event.value
        if message:
            if message.strip().lower() == "/quit":
                self.client.disconnect()
                self.exit()
                return

            self.write_to_log(f"[bold magenta]Me[/]: {message}")
            self.client.send_message(message)
            event.input.value = ""

if __name__ == "__main__":
    app = IRCApp()
    app.run()