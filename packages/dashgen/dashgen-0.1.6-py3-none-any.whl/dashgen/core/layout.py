from dashgen.core.components import render_card, render_table, render_chart

class Column:
    def __init__(self, width=12):
        self.width = width
        self.content = []
        self._types = []            # Tipos de componentes adicionados
        self._chart_heights = []    # Alturas informadas via options["height"]

    def add_card(self, title, value, target, style=None):
        self.content.append(render_card(title, value, target, style=style))
        self._types.append("card")
        return self

    def add_table(self, title, data, headers):
        self.content.append(render_table(title, data, headers))
        self._types.append("table")
        return self

    def add_chart(self, chart_type, title, data, options=None):
        self.content.append(render_chart(chart_type, title, data, options=options))
        self._types.append("chart")
        if options and "height" in options:
            self._chart_heights.append(options["height"])
        return self

    def render(self):
        return f'<div class="col-span-{self.width}">{"".join(self.content)}</div>'

    def get_component_types(self):
        return self._types

    def get_chart_heights(self):
        return self._chart_heights


class Row:
    def __init__(self, *columns):
        self.columns = columns

    def render(self):
        return f'<div class="grid grid-cols-12 gap-6 mb-6">{"".join(col.render() for col in self.columns)}</div>'

    def estimate_height(self):
        """
        Estima a altura da linha com base nos tipos de componentes.
        Considera heights personalizados de gráficos com padding compensado.
        """
        height = 0
        for col in self.columns:
            types = col.get_component_types()
            for t in types:
                if t == "card":
                    height = max(height, 180)
                elif t == "table":
                    height = max(height, 320)

            # ✅ Compensa altura extra dos gráficos (padding, título, gap)
            if hasattr(col, "get_chart_heights"):
                for h in col.get_chart_heights():
                    height = max(height, h + 96)
            elif "chart" in types:
                height = max(height, 450)  # fallback se nenhum height for passado

        return height + 40  # margem inferior entre linhas
