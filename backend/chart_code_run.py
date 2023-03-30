
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
df = pd.read_sql_query("SELECT arbitration_id, container_name, matter_number, experts_id, type_of_hearing, start_date, end_date, hsf_internal_advocates, external_advocates, hearing_format, virtual_hearing, bundle_used, hsf_involved_bundle, bundle_type, hearing_services_used, experts_who_gave_evidence_at_hearing, created_by, updated_by FROM view_gen_hearings_component WHERE start_date >= (NOW() - INTERVAL '3 years');", conn)

# create the bar chart
fig = px.bar(df, x='container_name', y='start_date', color='container_name')

# update the layout
fig.update_layout(
    title='Hearings in the past 3 years',
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