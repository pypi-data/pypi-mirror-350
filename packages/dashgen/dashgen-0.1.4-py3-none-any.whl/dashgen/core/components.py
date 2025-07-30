from dashgen.core.utils import format_currency
from dashgen.charts.chartjs import generate_chartjs_block

def render_card(title, value, target):
    perc = int((value / target) * 100) if target else 0
    return f'''
    <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-lg font-semibold mb-2">{title}</h3>
        <p class="text-sm mb-2">
            <strong>{format_currency(value)}</strong> / {format_currency(target)} ({perc}%)
        </p>
        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div class="h-full bg-[color:var(--primary)]" style="width:{min(100, perc)}%"></div>
        </div>
    </div>
    '''

def render_table(title, data, headers):
    rows = ""
    for row in data:
        row_html = "".join([f"<td class='px-3 py-2 border-b border-gray-100 text-sm'>{row.get(h, '')}</td>" for h in headers])
        rows += f"<tr>{row_html}</tr>"

    header_html = "".join([f"<th class='text-left text-[color:var(--primary)] font-semibold text-sm px-3 py-2 bg-gray-100'>{h}</th>" for h in headers])

    return f'''
    <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-lg font-semibold mb-3">{title}</h3>
        <div class="overflow-x-auto">
            <table class="w-full border-collapse">
                <thead><tr>{header_html}</tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    </div>
    '''

def render_chart(chart_type, title, data):
    return generate_chartjs_block(title, data, chart_type=chart_type)
