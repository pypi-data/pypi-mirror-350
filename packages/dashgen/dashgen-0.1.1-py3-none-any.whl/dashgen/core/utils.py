import base64
from pathlib import Path

def format_currency(value):
    if value >= 1_000_000:
        return f"R$ {value / 1_000_000:.1f}M".replace(".", ",")
    elif value >= 1_000:
        return f"R$ {value / 1_000:.1f}K".replace(".", ",")
    else:
        return f"R$ {value:.0f}"

def image_to_base64(path):
    img_path = Path(path)
    if img_path.exists():
        return base64.b64encode(img_path.read_bytes()).decode("utf-8")
    return ""