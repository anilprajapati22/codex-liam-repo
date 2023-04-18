
import psycopg2
import warnings

warnings.filterwarnings('ignore')

conn = psycopg2.connect(
            host='51.142.115.5',
            user='postgres',
            password='postgres',
            database='postgres',
            port="5441"
        )    
print("Chart file created")
    
import plotly.express as px
import pandas as pd

# query the database
df = pd.read_sql_query("SELECT settlement_amount_usd FROM view_settlements_component;", conn)

# create the bar chart
fig = px.bar(df, x='settlement_amount_usd', y='count', color='settlement_amount_usd')

# update the layout
fig.update_layout(
    title='Average Settlement Amount (USD)',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Arial",
        size=14,
        color="#7f7f7f"
    ),
    showlegend=False
)

# show the chart

fig.write_html('templates/chart.html')