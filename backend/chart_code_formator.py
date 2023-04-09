import os

def get_code(code):
    print("\n\n\n\n"+str("inside the chart code formator")+"\n\n\n")
    code_with_db_con = """
import psycopg2
import warnings

warnings.filterwarnings('ignore')

conn = psycopg2.connect(
            host='""" +  os.getenv('PYTHON_DB_HOST') + """',
            user='postgres',
            password='postgres',
            database='postgres',
            port="5440"
        )    
print("Chart file created")
    """+ "\n"+ code.replace("fig.show()","") + """\nfig.write_html('templates/chart.html')"""
    return code_with_db_con