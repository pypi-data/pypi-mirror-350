import json
import uuid

def generate_chartjs_block(title, data, chart_type="bar"):
    labels = [item['label'] for item in data]
    values = [item['value'] for item in data]
    
    # ID único por gráfico
    chart_id = "chart_" + uuid.uuid4().hex[:8]

    chart_type = chart_type if chart_type in ("bar", "line") else "bar"

    return f'''
    <div class="chart-container">
      <h3>{title}</h3>
      <canvas id="{chart_id}" width="400" height="200"></canvas>
      <script>
        const ctx_{chart_id} = document.getElementById('{chart_id}').getContext('2d');
        new Chart(ctx_{chart_id}, {{
          type: '{chart_type}',
          data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
              label: '{title}',
              data: {json.dumps(values)},
              backgroundColor: '{'#73060F' if chart_type == 'bar' else 'transparent'}',
              borderColor: '#73060F',
              tension: 0.3,
              fill: false
            }}]
          }},
          options: {{
            responsive: false,
            plugins: {{ legend: {{ display: false }} }}
          }}
        }});
      </script>
    </div>
    '''
