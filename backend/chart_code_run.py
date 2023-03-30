
import psycopg2
import warnings

warnings.filterwarnings('ignore')

conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='postgres',
            database='postgres',
            port="5440"
        )    
print("Chart file created")
    
import plotly.express as px
import pandas as pd

# query the database
df = pd.read_sql_query("SELECT * FROM view_gen_settlements_component WHERE date_trunc('year', settlement_date) >= (NOW() - INTERVAL '5 years');", conn)

# create the bar chart
fig = px.bar(df, x='settlement_date', y='settlement_amount_usd', barmode='group')

# update the layout
fig.update_layout(
    title='Settlement Amounts (USD) by Year',
    xaxis_title='Settlement Date',
    yaxis_title='Settlement Amount (USD)',
    xaxis_tickangle=-45,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Arial",
        size=14,
        color="#7f7f7f"
    ),
    showlegend=False
)
fig.write_html('templates/chart.html')