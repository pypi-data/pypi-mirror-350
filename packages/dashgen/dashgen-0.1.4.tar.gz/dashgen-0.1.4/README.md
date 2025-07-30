
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

# Criar o dashboard com altura automática e tema
db = Dashboard(
    title="Relatório de Vendas",
    logo_path="logo.png",  # Opcional
    size=(1080, None),     # Altura automática
    auto_size=True,
    theme={
        "primary": "#005f73",
        "accent": "#94d2bd",
        "bg": "#fefae0",
        "text": "#001219"
    }
)

# Linha com dois cards lado a lado
db.add(Row(
    Column(6).add_card("Receita Acumulada", 8200000, 10000000),
    Column(6).add_card("Unidades Vendidas", 320, 400)
))

# Linha com tabela e gráfico de barras
dados = [
    {"Nome": "Projeto A", "Meta": "R$ 2M", "Realizado": "R$ 1.6M", "Variação": "-20%"},
    {"Nome": "Projeto B", "Meta": "R$ 3M", "Realizado": "R$ 3.1M", "Variação": "+3%"},
]
db.add(Row(
    Column(6).add_table("Receita por Empreendimento", dados, ["Nome", "Meta", "Realizado", "Variação"]),
    Column(6).add_chart("bar", "Vendas Mensais", [
        {"label": "Jan", "value": 120},
        {"label": "Fev", "value": 135},
        {"label": "Mar", "value": 160},
    ])
))

# Linha com gráfico de linha
db.add(Row(
    Column(12).add_chart("line", "Receita Total (R$)", [
        {"label": "Jan", "value": 1200000},
        {"label": "Fev", "value": 1450000},
        {"label": "Mar", "value": 1600000},
    ])
))

# Exportar como imagem
db.generate("output_dashboard.png")
```

---

## 🧱 Componentes Disponíveis

### 📐 Layout

* `Row(...)`: agrupa colunas lado a lado
* `Column(width=...)`: define largura (1 a 12 colunas)

### 📦 Card (KPI)

```python
Column(6).add_card("Título", valor, meta)
```

Barra de progresso com percentual atingido.

### 📊 Tabela

```python
Column(6).add_table("Título", data, headers)
```

* `data`: lista de dicionários
* `headers`: nomes das colunas a exibir

### 📈 Gráfico

```python
Column(6).add_chart("bar", "Título", data)
Column(6).add_chart("line", "Título", data)
```

* `data`: lista com `label` e `value`
* Tipos: `"bar"`, `"line"`

---

## 🎨 Tema Personalizado

Você pode customizar as cores do dashboard:

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

* `auto_size=True`: ajusta automaticamente a altura da imagem com base no conteúdo
* Suporte a `Tailwind` via CDN
* Charts renderizados com `Chart.js`
* Layout flexível com `Row` e `Column`

---

## 📚 Documentação Técnica

### 📘 `Dashboard`

```python
Dashboard(title, logo_path=None, size=(1080, 1080), theme=None, auto_size=False)
```

| Parâmetro   | Tipo             | Descrição                           |
| ----------- | ---------------- | ----------------------------------- |
| `title`     | `str`            | Título do dashboard                 |
| `logo_path` | `str` (opcional) | Caminho para a logo                 |
| `size`      | `(int, int)`     | Tamanho da imagem (largura, altura) |
| `theme`     | `dict`           | Cores personalizadas                |
| `auto_size` | `bool`           | Ativa ajuste automático de altura   |

---

### ✅ `Dashboard.add(Row(...))`

Adiciona um conjunto de colunas à imagem.

---

### ✅ `Dashboard.generate(path)`

Gera e salva a imagem final em `path`.

---

### 📘 `Row(...)`

Agrupa `Column`s horizontalmente (até 12 colunas somadas).

### 📘 `Column(width=12)`

Define a largura da coluna (de 1 a 12). Dentro dela você pode usar:

* `.add_card(...)`
* `.add_table(...)`
* `.add_chart(...)`

---

## ✅ Requisitos

* Python 3.7+
* `playwright`
* `jinja2`

Instale tudo com:

```bash
pip install dashgen
playwright install
```

---

## 🖼 Exporte dashboards com visual moderno e profissional em segundos.

