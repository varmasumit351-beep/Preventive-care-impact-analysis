# =========================
# 1. IMPORTS
# =========================
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 2. LOAD DATA
# =========================
@st.cache_data
def load_data():
    data = pd.read_csv('dataset.csv')

    # Clean text
    data['Illness_Frequency'] = data['Illness_Frequency'].str.strip()

    # Convert to numeric
    illness_map = {'Rare':1, 'Sometimes':2, 'Often':3}
    data['Illness_Frequency'] = data['Illness_Frequency'].map(illness_map)

    # Fill missing values
    data['Illness_Frequency'].fillna(2, inplace=True)

    # Reverse label
    reverse_map = {1:'Rare', 2:'Sometimes', 3:'Often'}
    data['Illness_Label'] = data['Illness_Frequency'].map(reverse_map)

    return data

data = load_data()

# =========================
# 3. UI
# =========================
st.set_page_config(page_title="Preventive Care Dashboard", layout="wide")

st.title("🚀 Preventive Care Dashboard")

# Sidebar filter
diet_filter = st.sidebar.selectbox(
    "Select Diet",
    ['All', 'Good', 'Average', 'Poor']
)

# =========================
# 4. FILTER DATA
# =========================
if diet_filter == 'All':
    filtered = data
else:
    filtered = data[data['Diet'] == diet_filter]

# =========================
# 5. GRAPHS
# =========================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        filtered.groupby('Exercise')['Illness_Frequency'].mean().reset_index(),
        x='Exercise',
        y='Illness_Frequency',
        title="💪 Exercise vs Illness",
        text='Illness_Frequency',
        color='Exercise'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        filtered.groupby('Checkup')['Monthly_Expense'].mean().reset_index(),
        x='Checkup',
        y='Monthly_Expense',
        title="🏥 Checkup vs Expense",
        text='Monthly_Expense',
        color='Checkup'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Pie chart
fig3 = px.pie(
    filtered,
    names='Diet',
    title="🥗 Diet Distribution",
    hole=0.4
)
st.plotly_chart(fig3, use_container_width=True)
# =========================
# 5. ADVANCED GRAPHS
# =========================

st.subheader("📈 Advanced Insights")

col1, col2 = st.columns(2)

# 1. Box Plot (Distribution Insight)
with col1:
    fig_box = px.box(
        filtered,
        x="Exercise",
        y="Monthly_Expense",
        color="Exercise",
        title="💰 Expense Distribution by Exercise"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# 2. Violin Plot (Better Distribution View)
with col2:
    fig_violin = px.violin(
        filtered,
        x="Diet",
        y="Illness_Frequency",
        color="Diet",
        box=True,
        title="🥗 Diet vs Illness Distribution"
    )
    st.plotly_chart(fig_violin, use_container_width=True)

# =========================
# 3. Scatter Plot (Correlation)
# =========================
fig_scatter = px.scatter(
    filtered,
    x="Age",
    y="Monthly_Expense",
    color="Diet",
    size="Illness_Frequency",
    hover_data=["Exercise", "Checkup"],
    title="📊 Age vs Expense (Bubble shows Illness)"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# 4. Heatmap (Correlation Matrix)
# =========================
import numpy as np

numeric_cols = filtered.select_dtypes(include=np.number)

corr = numeric_cols.corr()

fig_heatmap = px.imshow(
    corr,
    text_auto=True,
    title="🔥 Correlation Heatmap"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# =========================
# 5. Sunburst Chart (Hierarchy)
# =========================
fig_sunburst = px.sunburst(
    filtered,
    path=["Diet", "Exercise", "Checkup"],
    values="Monthly_Expense",
    title="🌳 Lifestyle Impact Breakdown"
)
st.plotly_chart(fig_sunburst, use_container_width=True)

# =========================
# 6. Histogram (Frequency Analysis)
# =========================
fig_hist = px.histogram(
    filtered,
    x="Illness_Label",
    color="Diet",
    barmode="group",
    title="📊 Illness Frequency Distribution"
)
st.plotly_chart(fig_hist, use_container_width=True)

# =========================
# 6. TABLE
# =========================
st.subheader("📊 Dataset Table")

st.dataframe(filtered[[
    "Age",
    "Exercise",
    "Checkup",
    "Diet",
    "Illness_Label",
    "Monthly_Expense"
]])