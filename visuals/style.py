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
/* --- 1. Global Matrix Theme --- */
Screen {
    background: #000000;
    color: #00FF00;
}

/* --- 2. The Banner (Top) --- */
.banner {
    text-align: center;
    height: auto;
    padding: 1;
    background: #111111;
    color: #00FF00;
    dock: top;
}

/* --- 3. The Main Layout (Holds Chat + Sidebar) --- */
#main_layout {
    width: 100%;
    height: 1fr; /* Takes all space between Banner and Input */
}

/* --- 4. The Chat Area (Left) --- */
RichLog {
    width: 1fr;      /* Takes all remaining width */
    height: 100%;
    background: #050505;
    color: #00FF00;
    /* Base border - will be overridden by status classes below */
    border: solid #003300; 
}

/* --- 5. The Sidebar (Right) --- */
#sidebar {
    dock: right;
    width: 25;       /* Fixed width for user list */
    height: 100%;
    background: #0a0a0a;
    border-left: solid #00FF00;
}

#sidebar_title {
    text-align: center;
    background: #003300;
    color: #FFFFFF;
    text-style: bold;
    width: 100%;
    height: auto;
    padding: 1;
}

#user_list {
    height: 1fr; /* Takes remaining height in sidebar */
    border: none;
    background: #0a0a0a;
}
/* Style for individual items in the list */
ListItem {
    color: #00AA00;
    background: #0a0a0a;
    border-bottom: solid #00FF00;
}
ListItem:hover {
    background: #003300;
    color: #FFFFFF;
}

/* --- 6. The Quit Button (Sidebar Bottom) --- */
#quit_btn {
    dock: bottom;
    width: 100%;
    height: 3;
    background: #330000;
    color: #FF0000;
    /*border-top: solid #FF0000;*/
    text-style: bold;
}
#quit_btn:hover {
    background: #FF0000;
    color: #FFFFFF;
}

/* --- 7. The Input Box (Bottom) --- */
Input {
    dock: bottom;
    height: 3;
    background: #000000;
    border: solid #00FF00;
    color: #FFFFFF;
}

/* --- 8. Dynamic Status Borders (Applied to RichLog) --- */
.status-connecting {
    border: dashed #FFFF00; /* Yellow */
}
.status-connected {
    border: solid #00FF00; /* Green */
}
.status-error {
    border: heavy #FF0000; /* Red */
}
"""