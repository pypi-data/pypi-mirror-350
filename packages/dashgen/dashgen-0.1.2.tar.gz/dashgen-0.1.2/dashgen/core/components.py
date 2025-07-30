from dashgen.core.utils import format_currency
from dashgen.charts.chartjs import generate_chartjs_block

def render_card(title, value, target):
    perc = int((value / target) * 100) if target else 0
    return f'''
    <div class="card">
        <h3>{title}</h3>
        <p><strong>{format_currency(value)}</strong> / {format_currency(target)} ({perc}%)</p>
        <div class="bar"><div class="fill" style="width:{min(100, perc)}%"></div></div>
    </div>
    '''

def render_table(title, data, headers):
    rows = ""
    for row in data:
        rows += "<tr>" + "".join([f"<td>{row.get(h, '')}</td>" for h in headers]) + "</tr>"
    return f'''
    <div class="table-container">
        <h3>{title}</h3>
        <table>
            <thead><tr>{''.join(f'<th>{h}</th>' for h in headers)}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    '''

def render_chart(chart_type, title, data):
    return generate_chartjs_block(title, data, chart_type=chart_type)