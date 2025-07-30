from dashgen.core.components import render_card, render_table, render_chart

class Column:
    def __init__(self, width=12):
        self.width = width
        self.content = []
        self._types = []  # Armazena tipo dos componentes adicionados

    def add_card(self, *args, **kwargs):
        self.content.append(render_card(*args, **kwargs))
        self._types.append("card")
        return self

    def add_table(self, *args, **kwargs):
        self.content.append(render_table(*args, **kwargs))
        self._types.append("table")
        return self

    def add_chart(self, *args, **kwargs):
        self.content.append(render_chart(*args, **kwargs))
        self._types.append("chart")
        return self

    def render(self):
        return f'<div class="col-span-{self.width}">{"".join(self.content)}</div>'

    def get_component_types(self):
        return self._types


class Row:
    def __init__(self, *columns):
        self.columns = columns

    def render(self):
        return f'<div class="grid grid-cols-12 gap-6 mb-6">{"".join(col.render() for col in self.columns)}</div>'

    def estimate_height(self):
        """
        Estima a altura da linha com base nos tipos de componentes.
        Cards são baixos, tabelas e gráficos são mais altos.
        """
        height = 0
        for col in self.columns:
            types = col.get_component_types()
            for t in types:
                if t == "card":
                    height = max(height, 180)
                elif t == "table":
                    height = max(height, 320)
                elif t == "chart":
                    height = max(height, 350)  # gráfico dentro de card
        return height + 40  # espaço entre linhas
