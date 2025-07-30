import asyncio
from jinja2 import Template
from dashgen.core.utils import image_to_base64
from dashgen.core.renderer import render_html_to_image
from pathlib import Path

class Dashboard:
    def __init__(self, title="Dashboard", logo_path=None, size=(1080, 1080), theme=None):
        self.title = title
        self.logo_b64 = image_to_base64(logo_path) if logo_path else ""
        self.width, self.height = size
        self.components = []
        self.theme = theme or {}

    def add(self, layout):
        self.components.append(layout.render())

    def generate(self, output_path):
        base_html_path = Path(__file__).parent.parent / "templates" / "base.html"
        css_path = Path(__file__).parent.parent / "themes" / "default.css"

        with open(css_path, encoding="utf-8") as f:
            theme_css = f.read()

        custom_root = ":root {\n" + "\n".join([
            f"  --{k}: {v};" for k, v in self.theme.items()
        ]) + "\n}\n"
        
        if ":root {" in theme_css:
            theme_css = custom_root + css_path.read_text(encoding="utf-8").split("}", 1)[1]
        else:
            theme_css = custom_root + theme_css

        with open(base_html_path, encoding="utf-8") as f:
            template = Template(f.read())

        rendered_html = template.render(
            title=self.title,
            logo_b64=self.logo_b64,
            components="\n".join(self.components),
            theme_css=theme_css
        )

        asyncio.run(render_html_to_image(rendered_html, output_path, self.width, self.height))