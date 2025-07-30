
# Dashgen

📊 Gere **dashboards visuais como imagens (PNG)** diretamente do Python com HTML, Tailwind CSS e Chart.js.

---

## ✨ O que é?

`dashgen` é um micro-framework que permite criar dashboards dinâmicos e exportá-los como imagens de alta qualidade.

Ideal para gerar relatórios diários, KPIs, resumos visuais e compartilhar automaticamente via e-mail, WhatsApp, sistemas internos etc.

---

## 🛠 Instalação

```bash
pip install dashgen
playwright install
````

---

## 🚀 Exemplo Completo

```python
from dashgen import Dashboard
from dashgen.core.layout import Row, Column

# Criar o dashboard com altura automática, título estilizado e tema
db = Dashboard(
    title="📊 Relatório de Desempenho Comercial",
    title_style="text-3xl font-bold text-emerald-700",
    logo_path="logo.png",
    size=(1080, None),
    auto_size=True,
    theme={
        "primary": "#0f766e",
        "accent": "#22d3ee",
        "bg": "#f0fdfa",
        "text": "#082f49"
    }
)

# Linha com dois cards
db.add(Row(
    Column(6).add_card("Receita Acumulada", 9000000, 10000000),
    Column(6).add_card("Unidades Vendidas", 430, 500)
))

# Linha com tabela e gráfico de barras
dados = [
    {"Nome": "Projeto A", "Meta": "R$ 3M", "Realizado": "R$ 2.4M", "Variação": "-20%"},
    {"Nome": "Projeto B", "Meta": "R$ 5M", "Realizado": "R$ 5.2M", "Variação": "+4%"}
]

db.add(Row(
    Column(6).add_table("Desempenho por Projeto", dados, ["Nome", "Meta", "Realizado", "Variação"]),
    Column(6).add_chart(
        "bar",
        "Vendas por Mês",
        [
            {"label": "Jan", "value": 120},
            {"label": "Fev", "value": 135},
            {"label": "Mar", "value": 160},
            {"label": "Abr", "value": 110},
            {"label": "Mai", "value": 190}
        ],
        options={
            "height": 300,
            "show_data_labels": True,
            "show_legend": False,
            "show_x_axis": True,
            "show_y_axis": True,
            "autosize_x": True,
            "bar_color": "#0f766e"
        }
    )
))

# Linha com gráfico de linha (largura total)
db.add(Row(
    Column(12).add_chart(
        "line",
        "Receita Total (R$)",
        [
            {"label": "Jan", "value": 1200000},
            {"label": "Fev", "value": 1450000},
            {"label": "Mar", "value": 1600000},
            {"label": "Abr", "value": 1800000},
            {"label": "Mai", "value": 2100000}
        ],
        options={
            "height": 460,
            "show_legend": False,
            "show_x_axis": True,
            "show_y_axis": True,
            "autosize_x": True,
            "tension": 0.4,
            "fill": False,
            "border_color": "#22d3ee"
        }
    )
))

# Gerar imagem
db.generate("output_dashboard.png")
print("✅ Dashboard gerado com sucesso!")

```

---

## 🧱 Componentes Disponíveis

### 📐 Layout

* `Row(...)`: Agrupa colunas
* `Column(width=...)`: Define largura (1 a 12)

### 📦 Card (KPI)

```python
Column(6).add_card("Título", valor, meta, style={ ... })
```

Suporta personalização com:

* `title_color`, `title_size`, `text_size`
* `bar_color`, `card_class`

### 📊 Tabela

```python
Column(6).add_table("Título", data, headers)
```

* `data`: lista de dicionários
* `headers`: nomes das colunas a exibir

### 📈 Gráfico (Chart.js)

```python
Column(6).add_chart("bar" ou "line", "Título", data, options={...})
```

* `data`: lista com `label` e `value`
* `options`:

  * `height`: altura do canvas
  * `fill`: preencher área sob a linha
  * `tension`: suavidade das curvas
  * `autosize_x` / `autosize_y`: expandir horizontal/vertical
  * `show_legend`: mostrar legenda
  * `show_x_axis` / `show_y_axis`: mostrar eixos
  * `show_data_labels`: mostrar valores sobre as barras

---

## 🎨 Tema Personalizado

```python
theme = {
    "primary": "#005f73",  # Barras e títulos
    "accent": "#94d2bd",   # Detalhes
    "bg": "#fefae0",       # Fundo da imagem
    "text": "#001219"      # Cor do texto
}
```

---

## 🧠 Funcionalidades Especiais

* `auto_size=True`: ajusta altura da imagem com base no conteúdo
* Responsivo com Tailwind
* Gráficos com Chart.js
* Rótulos de valores (`chartjs-plugin-datalabels`)
* Estilização por componente (`style`, `options`)

---

## 📚 API Referência

### 📘 `Dashboard(...)`

| Parâmetro   | Tipo             | Descrição                   |
| ----------- | ---------------- | --------------------------- |
| `title`     | `str`            | Título do dashboard         |
| `logo_path` | `str` (opcional) | Caminho da logo             |
| `size`      | `(int, int)`     | Tamanho fixo da imagem      |
| `auto_size` | `bool`           | Ajuste automático de altura |
| `theme`     | `dict`           | Cores do tema               |

---

## ✅ Requisitos

* Python 3.7+
* `playwright`
* `jinja2`

```bash
pip install dashgen
playwright install
```

---

## 🖼 Gere imagens de dashboards com visual moderno, responsivo e exportável – em uma linha de código.

```
