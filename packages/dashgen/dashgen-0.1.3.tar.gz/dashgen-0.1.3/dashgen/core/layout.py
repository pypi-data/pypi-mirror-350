from dashgen.core.components import render_card, render_table, render_chart

class Column:
    def __init__(self, width=12):
        self.width = width
        self.content = []

    def add_card(self, *args, **kwargs):
        self.content.append(render_card(*args, **kwargs))
        return self

    def add_table(self, *args, **kwargs):
        self.content.append(render_table(*args, **kwargs))
        return self

    def add_chart(self, *args, **kwargs):
        self.content.append(render_chart(*args, **kwargs))
        return self

    def render(self):
        return f'<div class="col col-{self.width}">{"".join(self.content)}</div>'

class Row:
    def __init__(self, *columns):
        self.columns = columns

    def render(self):
        return f'<div class="row">{"".join(col.render() for col in self.columns)}</div>'