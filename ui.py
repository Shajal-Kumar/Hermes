import threading
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Input, RichLog, Header, Footer, Button, Label
from textual.containers import Vertical, Horizontal
from textual.suggester import SuggestFromList
from backend import IRCClient
from style import MATRIX_CSS, LOGIN_CSS
from banner import *

IRC_COMMANDS = [
    "/join", "/part", "/quit", "/nick", "/me", 
    "/msg", "/list", "/whois", "/topic", "/clear"
]

# add command autocompletion
# add ability to select nickname


class LoginScreen(Screen):
    CSS = LOGIN_CSS
    
    def compose(self):
        with Vertical(id="login-container"):
            yield Label("SERVER ADDRESS")
            yield Input(value="irc.libera.chat", id="server")
            
            yield Label("CHANNEL")
            yield Input(placeholder="Enter channel...", id="channel")
            
            yield Label("NICKNAME")
            yield Input(placeholder="Enter your nick...", id="nick")
            
            yield Button("ENTER THE MATRIX", id="connect_btn", variant="success")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "connect_btn":
            server = self.query_one("#server", Input).value.strip() or "irc.libera.chat"
            channel = self.query_one("#channel", Input).value.strip() or "#python-test-room"
            nick = self.query_one("#nick", Input).value

            channel = "#" + channel if not channel.startswith("#") else channel
            
            if not nick:
                self.notify("Nickname is required!", severity="error")
                return

            self.dismiss({
                "server": server,
                "channel": channel,
                "nick": nick
            })

class ChatScreen(Screen):
    CSS = MATRIX_CSS

    def __init__(self, server_config):
        super().__init__()
        self.server_config = server_config
    
    def compose(self) -> ComposeResult:
        yield Static(get_banner_widget("HERMES"), classes="banner")
        yield RichLog(id="chat_log", highlight=True, markup=True)
        yield Input(placeholder="Wake up, Neo...",
                    id="message_input",
                    suggester=SuggestFromList([], case_sensitive=False))
        yield Footer()

    def on_mount(self):
        self.client = IRCClient(
            self.server_config["server"],
            6667,
            self.server_config["nick"],
            self.server_config["channel"],
            callback=self.on_backend_message
        )
        self.client.connect()
        self.query_one("#message_input").focus()

    def dispatch_ui(self, func, *args):
        """
        Helper: Decides whether to run the function directly or schedule it.
        Prevents the 'RuntimeError' if called from Main Thread.
        """
        if threading.current_thread() is threading.main_thread():
            func(*args)
        else:
            self.call_from_thread(func, *args)

    def on_backend_message(self, data):
        """Called by backend. Bridges to UI thread safely."""

        if isinstance(data, dict):
            if data['type'] == 'namelist':
                self.dispatch_ui(self.update_suggester, data['names'])
                return 
        
        message_text = str(data)

        # Ignore the ISUPPORT messages
        if " 005 " in message_text: 
            return

        if "Joined" in message_text:
            self.dispatch_ui(self.set_status_border, "status-connected")
        elif "failed" in message_text or "Error" in message_text:
            self.dispatch_ui(self.set_status_border, "status-error")

        formatted_msg = message_text
        
        if "Connected" in message_text or "Joined" in message_text:
            formatted_msg = f"[bold green]{message_text}[/]"
            
        elif ":" in message_text:
            try:
                parts = message_text.split(":", 1)
                if len(parts) == 2:
                    nick, msg = parts
                    formatted_msg = f"[cyan]{nick}[/]:{msg}"
            except ValueError:
                pass

        self.dispatch_ui(self.write_to_log, formatted_msg)

    def set_status_border(self, class_name):
        """Helper to change the border color dynamically"""
        log = self.query_one("#chat_log")
        log.remove_class("status-connecting", "status-connected", "status-error")
        log.add_class(class_name)

    def update_suggester(self, names):
        try:
            inp = self.query_one(Input)
            inp.suggester = SuggestFromList(names, case_sensitive=False)
            # self.write_to_log(f"[dim]Debug: Loaded {len(names)} nicknames for autocomplete.[/]")
        except:
            pass

    def write_to_log(self, text):
        self.query_one(RichLog).write(text)

    def on_input_submitted(self, event: Input.Submitted):
        message = event.value
        if message:
            if message.strip().lower() == "/quit":
                self.client.disconnect()
                self.write_to_log(f"[bold red][-] Disconnected from {self.server_config['server']}[/]")
                self.dispatch_ui(self.set_status_border, "status-error")
                return

            self.write_to_log(f"[bold green]{self.server_config['nick']}[/]: {message}")
            self.client.send_message(message)
            event.input.value = ""

class IRCApp(App):
    def on_mount(self):
        self.push_screen(LoginScreen(), callback=self.on_login_completed)

    def on_login_completed(self, result_data):
        if result_data:
            chat_screen = ChatScreen(result_data)
            self.push_screen(chat_screen)
        else:
            self.exit()

if __name__ == "__main__":
    app = IRCApp()
    app.run()