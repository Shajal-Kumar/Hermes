import pyfiglet
from rich.text import Text
from rich.color import Color, blend_rgb
from textual.widgets import Static

def gradient_text(text: str, start_color: str, end_color: str) -> Text:
    """Render text with a smooth gradient."""
    rich_text = Text()
    start = Color.parse(start_color).triplet
    end = Color.parse(end_color).triplet
    steps = max(len(text), 1)

    for i, char in enumerate(text):
        blend = blend_rgb(start, end, i / steps)
        # hex_color = f"#{blend[0]:02x}{blend[1]:02x}{blend[2]:02x}"
        hex_color = f"#{0:02x}{min(255,int(60+i*195)):02x}{0:02x}"
        rich_text.append(char, style=f"bold {hex_color}")
    
    return rich_text

def get_banner_widget(message: str):
    ascii_art = pyfiglet.figlet_format(message, font="dos_rebel", width=120)
    
    final_banner = Text()
    
    for line in ascii_art.splitlines():
        grad_line = gradient_text(line, "#FFD700", "#00FFFF")
        final_banner.append(grad_line)
        final_banner.append("\n")
    
    return final_banner
