LOGIN_CSS = """
    LoginScreen {
        align: center middle;
        background: #000000;
    }
    #login-container {
        width: 60;
        height: auto;
        border: solid #00FF00;
        padding: 2;
        background: #111111;
    }
    Label { color: #00FF00; margin-top: 1; }
    Input { border: solid #00AA00; }
    Button { width: 100%; margin-top: 2; background: #003300; color: #00FF00; }
    Button:hover { background: #00FF00; color: #000000; }
"""

MATRIX_CSS = """
Screen {
    background: #000000;
    color: #00FF00;
}

RichLog {
    background: #050505;
    border: solid #003300;
    color: #00FF00;
    height: 1fr;
}

Input {
    dock: bottom;
    background: #000000;
    border: solid #00FF00;
    color: #FFFFFF;
}

.status-connecting {
    border: dashed #FFFF00;
}
.status-connected {
    border: solid #00FF00;
}
.status-error {
    border: heavy #FF0000; /* Red */
}

.banner {
    text-align: center;
    height: auto;
    padding: 1;
    background: $surface-darken-1; 
}
"""