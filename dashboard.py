# =========================
# 1. IMPORTS
# =========================
import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

# =========================
# 2. LOAD & PREPROCESS DATA
# =========================
def load_data():
    data = pd.read_csv('dataset.csv')

    # Clean text
    data['Illness_Frequency'] = data['Illness_Frequency'].str.strip()

    # Convert to numeric
    illness_map = {'Rare':1, 'Sometimes':2, 'Often':3}
    data['Illness_Frequency'] = data['Illness_Frequency'].map(illness_map)

    # Fill missing values
    data['Illness_Frequency'].fillna(2, inplace=True)

    # Create label column for table
    reverse_map = {1:'Rare', 2:'Sometimes', 3:'Often'}
    data['Illness_Label'] = data['Illness_Frequency'].map(reverse_map)

    return data

data = load_data()

# =========================
# 3. GRAPH FUNCTIONS
# =========================
def create_graphs(filtered):

    # Graph 1
    fig1 = px.bar(
        filtered.groupby('Exercise')['Illness_Frequency'].mean().reset_index(),
        x='Exercise',
        y='Illness_Frequency',
        title="💪 Exercise vs Illness",
        text='Illness_Frequency',
        color='Exercise'
    )

    fig1.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    # Graph 2
    fig2 = px.bar(
        filtered.groupby('Checkup')['Monthly_Expense'].mean().reset_index(),
        x='Checkup',
        y='Monthly_Expense',
        title="🏥 Checkup vs Expense",
        text='Monthly_Expense',
        color='Checkup'
    )

    fig2.update_traces(texttemplate='%{text:.0f}', textposition='outside')

    # Graph 3 (Pie)
    fig3 = px.pie(
        filtered,
        names='Diet',
        title="🥗 Diet Distribution",
        hole=0.4
    )

    return fig1, fig2, fig3

# =========================
# 4. DASH APP
# =========================
app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#0f172a', 'color': 'white'}, children=[

    html.H1("🚀 Preventive Care Dashboard", style={'textAlign': 'center'}),

    # Filter
    dcc.Dropdown(
        id='diet-filter',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Good', 'value': 'Good'},
            {'label': 'Average', 'value': 'Average'},
            {'label': 'Poor', 'value': 'Poor'},
        ],
        value='All'
    ),

    dcc.Graph(id='graph1'),
    dcc.Graph(id='graph2'),
    dcc.Graph(id='graph3'),

    html.H2("📊 Dataset Table"),

    dash_table.DataTable(
        id='table',
        columns=[
            {"name": "Age", "id": "Age"},
            {"name": "Exercise", "id": "Exercise"},
            {"name": "Checkup", "id": "Checkup"},
            {"name": "Diet", "id": "Diet"},
            {"name": "Illness Level", "id": "Illness_Label"},
            {"name": "Monthly Expense (₹)", "id": "Monthly_Expense"},
        ],
        page_size=10,
        sort_action="native",
        filter_action="native",

        style_table={'overflowX': 'auto'},

        style_cell={
            'textAlign': 'center',
            'backgroundColor': '#1e293b',
            'color': 'white',
            'padding': '8px'
        },

        style_header={
            'backgroundColor': '#334155',
            'fontWeight': 'bold',
            'color': 'white'
        }
    )
])

# =========================
# 5. CALLBACK
# =========================
@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('graph3', 'figure'),
     Output('table', 'data')],
    [Input('diet-filter', 'value')]
)
def update_dashboard(selected_diet):

    if selected_diet == 'All':
        filtered = data
    else:
        filtered = data[data['Diet'] == selected_diet]

    fig1, fig2, fig3 = create_graphs(filtered)

    return fig1, fig2, fig3, filtered.to_dict('records')

# =========================
# 6. RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)