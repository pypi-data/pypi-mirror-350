import json
import uuid

def generate_chartjs_block(title, data, chart_type="bar", options=None):
    options = options or {}

    labels = [item['label'] for item in data]
    values = [item['value'] for item in data]

    chart_id = "chart_" + uuid.uuid4().hex[:8]
    chart_type = chart_type if chart_type in ("bar", "line") else "bar"

    # Personalizações via options
    show_legend = options.get("show_legend", False)
    show_data_labels = options.get("show_data_labels", False)
    show_x_axis = options.get("show_x_axis", True)
    show_y_axis = options.get("show_y_axis", True)
    autosize_x = options.get("autosize_x", True)
    autosize_y = options.get("autosize_y", False)
    tension = options.get("tension", 0.3)
    fill = options.get("fill", False)
    height_px = options.get("height", 300)

    bar_color = options.get("bar_color", "#73060F")
    border_color = options.get("border_color", "#73060F")

    title_visible = options.get("show_title", True)
    title_html = f'<h3 class="text-lg font-semibold mb-3">{title}</h3>' if title_visible else ""

    # Datalabels positioning
    anchor = 'end' if chart_type == 'bar' else 'center'
    align = 'top' if chart_type == 'bar' else 'bottom'

    return f'''
    <div class="bg-white rounded-lg shadow p-4 flex flex-col gap-2">
      {title_html}
      <canvas id="{chart_id}" class="{ 'w-full' if autosize_x else '' } { 'h-full' if autosize_y else '' }" height="{height_px}"></canvas>
      <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
      <script>
        const ctx_{chart_id} = document.getElementById('{chart_id}').getContext('2d');
        new Chart(ctx_{chart_id}, {{
          type: '{chart_type}',
          data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
              label: '{title if show_legend else ""}',
              data: {json.dumps(values)},
              backgroundColor: '{bar_color}',
              borderColor: '{border_color}',
              tension: {tension},
              fill: {str(fill).lower()}
            }}]
          }},
          options: {{
            responsive: false,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: {str(show_legend).lower()} }},
              datalabels: {{
                display: {str(show_data_labels).lower()},
                color: '#111',
                anchor: '{anchor}',
                align: '{align}',
                font: {{
                  size: 11,
                  weight: 'bold'
                }},
                formatter: function(value) {{
                  return value;
                }}
              }}
            }},
            scales: {{
              x: {{ display: {str(show_x_axis).lower()} }},
              y: {{ display: {str(show_y_axis).lower()} }}
            }}
          }},
          plugins: [ChartDataLabels]
        }});
      </script>
    </div>
    '''
