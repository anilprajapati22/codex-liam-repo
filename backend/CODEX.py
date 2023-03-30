import os
import openai
from flask import Flask, jsonify, request, render_template
import psycopg2
import pandas as pd
from sql_formatter.core import format_sql
from flask_cors import CORS
from chart_code_formator import get_code
from chart_html_code_get import get_div
import os
import multiprocessing
openai.api_key = "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"

app = Flask(__name__)
CORS(app)


@app.route('/chart')
def chart():
   return render_template('chart.html', chart_div = get_div())    

def run_chart():
    print("**********************")
    print("\n\n\n running chart")
    # run the chart file that created by the code page
    os.system("python3 chart_code_run.py")

@app.route('/login', methods=['POST'])
def login():
    user = request.json['user']
    password = request.json['password']
    print(user,password)
    if user == 'liam' and password == 'massiveGLiam':
        return jsonify({'auth': True})
    else:
        return jsonify({ 'auth' : False} )

@app.route('/generate_sql_query', methods=['POST'])
def generate_query_endpoint():
    question = request.json['prompt']
    # question = request.json["question"]
    is_chart_in_ans = False
    response = openai.Completion.create(
                model="text-davinci-003",
                prompt="### Postgres SQL tables, with their properties:\n\nTable 1:  view_gen_hearings_component(arbitration_id, container_name, matter_number, experts_id, type_of_hearing, start_date, end_date , exclude_weekend, hsf_internal_advocates, external_advocates,hearing_format, virtual_hearing, bundle_used, hsf_involved_bundle, bundle_type, hearing_services_used, experts_who_gave_evidence_at_hearing, created_by, updated_by)\n\nTable 2: view_gen_end_of_matter_assessment_component(arbitration_id ,known_as as container_name ,matter_number ,end_of_matter_id ,file_closed_date ,how_compl x_was_the_matter  ,key_matter_takeway_points ,formal_debrief_client ,client_feedback ,client_responsiveness ,counterparty_difficulty  ,coclaimant_corespondent_difficulty  ,total_hours_recorded_matter_code, total_billable_hours_on_arbitration ,total_revenue_matter ,actual_revenue_reason ,contribution_margin_matter ,total_billed_hours_on_arbitration ,technology_used  ,out_of_house_services  ,created_by ,updated_by)\n\nTable 3: view_gen_settlements_component(arbitration_id, container_name, matter_number, settlements_id, is_adr_process, if_so_which_adr_process, settlement_date, hsf_assessment_success, client_assessment_success, settlement_amount_usd, settlement_amount_local, local_currency_name , further_details, created_by, updated_by)\\n\\n# view_gen_claim_and_counterclaim_component(arbitration_id, known_as as container_name, matter_number, claim_counterclaim_id, value_of_claims_local, local_currency_name, declaratory_relief, value_of_claims_usd, value_of_counterclaims_usd, value_of_counterclaims_local, additional_information_claims  , created_by, updated_by )\n\n Question : A Postgresql query to list all hearing that we did in the last year from 2022, from table view_gen_hearings_component taking column start_date \\nAnswer : SELECT * FROM view_gen_hearings_component WHERE start_date >= '2022-01-01';\n\nQuestion : A Postgresql query to list all top 10 revenue generating matters, from table view_gen_end_of_matter_assessment_component taking column total_revenue_matter - \\nAnswer : SELECT arbitration_id, container_name, matter_number, total_revenue_matter\\nFROM view_gen_end_of_matter_assessment_component WHERE total_revenue_matter IS NOT NULL ORDER BY total_revenue_matter DESC LIMIT 10;\n\npython bar chart visualization code for list all top 10 revenue generating matters:\n\nimport plotly.express as px\nimport pandas as pd\n\n# query the database\ndf = pd.read_sql_query(\"SELECT container_name, total_revenue_matter FROM view_gen_end_of_matter_assessment_component WHERE total_revenue_matter IS NOT NULL ORDER BY total_revenue_matter DESC LIMIT 10;\", conn)\n\n# create the bar chart\nfig = px.bar(df, x='container_name', y='total_revenue_matter', color='container_name')\n\n# update the layout\nfig.update_layout(\n    title='Top 10 containers by total revenue matter',\n    plot_bgcolor='rgba(0,0,0,0)',\n    paper_bgcolor='rgba(0,0,0,0)',\n    font=dict(\n        family=\"Arial\",\n        size=14,\n        color=\"#7f7f7f\"\n    ),\n    showlegend=False\n)\n\n# show the chart\nfig.show()\n\n\nQuestion : A Postgresql query to average settlement values, from table gen_settlements_component taking column settlement_amount_usd\n\nQuestion : A Postgresql query to list the arbitrations that have the 10 highest claim values from table view_gen_claim_and_counterclaim_component -\\nAnswer :  SELECT arbitration_id, container_name, matter_number, value_of_claims_usd FROM view_gen_claim_and_counterclaim_component WHERE value_of_claims_usd IS NOT NULL ORDER BY value_of_claims_usd DESC LIMIT 10;\n\nQuestion : A Postgresql query to list all the settlements that we have done in the last year 2022 from table view_gen_settlements_component - \\nAnswer : SELECT settlement_date, container_name FROM view_gen_settlements_component WHERE date_trunc('year', settlement_date) = '2022-01-01';\n\npython bar chart visualization code for list all the settlements that we have done in the last year:\nimport plotly.express as px\nimport pandas as pd\n\n# query the database\ndf = pd.read_sql_query(\"SELECT * FROM view_gen_settlements_component WHERE date_trunc('year', settlement_date) >= (NOW() - INTERVAL '5 years');\", conn)\n\n# create the bar chart\nfig = px.bar(df, x='settlement_date', y='settlement_amount_usd', barmode='group')\n\n# update the layout\nfig.update_layout(\n    title='Settlement Amounts (USD) by Year',\n    xaxis_title='Settlement Date',\n    yaxis_title='Settlement Amount (USD)',\n    xaxis_tickangle=-45,\n    plot_bgcolor='rgba(0,0,0,0)',\n    paper_bgcolor='rgba(0,0,0,0)',\n    font=dict(\n        family=\"Arial\",\n        size=14,\n        color=\"#7f7f7f\"\n    ),\n    showlegend=False\n)\n\nQuestion : Show me all hearing in the past year 5 - \\nAnswer: SELECT arbitration_id, container_name, matter_number, experts_id, type_of_hearing, start_date, end_date, hsf_internal_advocates, external_advocates, hearing_format, virtual_hearing, bundle_used, hsf_involved_bundle, bundle_type, hearing_services_used, experts_who_gave_evidence_at_hearing, created_by, updated_by FROM view_gen_hearings_component\\nWHERE start_date >= (NOW() - INTERVAL '5 years');\n\nFrom the given tables above write a postgresql query:\n\n" + question + "\n\nIdentigy if there are multiple questions in one input, separate them for clarity if there are.\n\n\nStart the answers with 'A no.:' for consistency.\n\nOnly display the answers and no other explanations or random text.\n\n",
                temperature=0.15,
                max_tokens=1646,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0

                )

    try:
        response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="### Postgres SQL tables, with their properties:\n\nTable 1:  view_gen_hearings_component(arbitration_id, container_name, matter_number, experts_id, type_of_hearing, start_date, end_date , exclude_weekend, hsf_internal_advocates, external_advocates,hearing_format, virtual_hearing, bundle_used, hsf_involved_bundle, bundle_type, hearing_services_used, experts_who_gave_evidence_at_hearing, created_by, updated_by)\n\nTable 2: view_gen_end_of_matter_assessment_component(arbitration_id ,known_as as container_name ,matter_number ,end_of_matter_id ,file_closed_date ,how_compl x_was_the_matter  ,key_matter_takeway_points ,formal_debrief_client ,client_feedback ,client_responsiveness ,counterparty_difficulty  ,coclaimant_corespondent_difficulty  ,total_hours_recorded_matter_code, total_billable_hours_on_arbitration ,total_revenue_matter ,actual_revenue_reason ,contribution_margin_matter ,total_billed_hours_on_arbitration ,technology_used  ,out_of_house_services  ,created_by ,updated_by)\n\nTable 3: view_gen_settlements_component(arbitration_id, container_name, matter_number, settlements_id, is_adr_process, if_so_which_adr_process, settlement_date, hsf_assessment_success, client_assessment_success, settlement_amount_usd, settlement_amount_local, local_currency_name , further_details, created_by, updated_by)\\n\\n# view_gen_claim_and_counterclaim_component(arbitration_id, known_as as container_name, matter_number, claim_counterclaim_id, value_of_claims_local, local_currency_name, declaratory_relief, value_of_claims_usd, value_of_counterclaims_usd, value_of_counterclaims_local, additional_information_claims  , created_by, updated_by )\n\n Question : A Postgresql query to list all hearing that we did in the last year from 2022, from table view_gen_hearings_component taking column start_date \\nAnswer : SELECT * FROM view_gen_hearings_component WHERE start_date >= '2022-01-01';\n\nQuestion : A Postgresql query to list all top 10 revenue generating matters, from table view_gen_end_of_matter_assessment_component taking column total_revenue_matter - \\nAnswer : SELECT arbitration_id, container_name, matter_number, total_revenue_matter\\nFROM view_gen_end_of_matter_assessment_component WHERE total_revenue_matter IS NOT NULL ORDER BY total_revenue_matter DESC LIMIT 10;\n\npython bar chart visualization code for list all top 10 revenue generating matters:\n\nimport plotly.express as px\nimport pandas as pd\n\n# query the database\ndf = pd.read_sql_query(\"SELECT container_name, total_revenue_matter FROM view_gen_end_of_matter_assessment_component WHERE total_revenue_matter IS NOT NULL ORDER BY total_revenue_matter DESC LIMIT 10;\", conn)\n\n# create the bar chart\nfig = px.bar(df, x='container_name', y='total_revenue_matter', color='container_name')\n\n# update the layout\nfig.update_layout(\n    title='Top 10 containers by total revenue matter',\n    plot_bgcolor='rgba(0,0,0,0)',\n    paper_bgcolor='rgba(0,0,0,0)',\n    font=dict(\n        family=\"Arial\",\n        size=14,\n        color=\"#7f7f7f\"\n    ),\n    showlegend=False\n)\n\n# show the chart\nfig.show()\n\n\nQuestion : A Postgresql query to average settlement values, from table gen_settlements_component taking column settlement_amount_usd\n\nQuestion : A Postgresql query to list the arbitrations that have the 10 highest claim values from table view_gen_claim_and_counterclaim_component -\\nAnswer :  SELECT arbitration_id, container_name, matter_number, value_of_claims_usd FROM view_gen_claim_and_counterclaim_component WHERE value_of_claims_usd IS NOT NULL ORDER BY value_of_claims_usd DESC LIMIT 10;\n\nQuestion : A Postgresql query to list all the settlements that we have done in the last year 2022 from table view_gen_settlements_component - \\nAnswer : SELECT settlement_date, container_name FROM view_gen_settlements_component WHERE date_trunc('year', settlement_date) = '2022-01-01';\n\npython bar chart visualization code for list all the settlements that we have done in the last year:\nimport plotly.express as px\nimport pandas as pd\n\n# query the database\ndf = pd.read_sql_query(\"SELECT * FROM view_gen_settlements_component WHERE date_trunc('year', settlement_date) >= (NOW() - INTERVAL '5 years');\", conn)\n\n# create the bar chart\nfig = px.bar(df, x='settlement_date', y='settlement_amount_usd', barmode='group')\n\n# update the layout\nfig.update_layout(\n    title='Settlement Amounts (USD) by Year',\n    xaxis_title='Settlement Date',\n    yaxis_title='Settlement Amount (USD)',\n    xaxis_tickangle=-45,\n    plot_bgcolor='rgba(0,0,0,0)',\n    paper_bgcolor='rgba(0,0,0,0)',\n    font=dict(\n        family=\"Arial\",\n        size=14,\n        color=\"#7f7f7f\"\n    ),\n    showlegend=False\n)\n\nQuestion : Show me all hearing in the past year 5 - \\nAnswer: SELECT arbitration_id, container_name, matter_number, experts_id, type_of_hearing, start_date, end_date, hsf_internal_advocates, external_advocates, hearing_format, virtual_hearing, bundle_used, hsf_involved_bundle, bundle_type, hearing_services_used, experts_who_gave_evidence_at_hearing, created_by, updated_by FROM view_gen_hearings_component\\nWHERE start_date >= (NOW() - INTERVAL '5 years');\n\nFrom the given tables above write a postgresql query:\n\n" + question + "\n\nIdentigy if there are multiple questions in one input, separate them for clarity if there are.\n\n\nStart the answers with 'A no.:' for consistency.\n\nOnly display the answers and no other explanations or random text.\n\n",
                    temperature=0.15,
                    max_tokens=1646,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
  
                    )
        
    except Exception as e:
        #if error occours
        print("sgnons erorr : ",str(e))
        query = format_sql("""Open API Error""")

        return jsonify({"query":query, 'error_details':str(e), 'is_run':False, 'is_chart_in_ans' : is_chart_in_ans})
    
    query = response.choices[0].text
    # query = query.replace("*", "SELECT *")
    # if not query.startswith("SELECT"):
    #     query = "SELECT " + query
    #     print(query)
    print("\n\n\n\n\n\n\n line 66",query,"\n\n\n\n\n\n\n")
     
    if "A1:" in query:

        index1 = query.index("A1:")
        if "A1:" in query and "A2:" in query:
            index2 = query.index("A2:")
            answer1 = query[:index2].replace("A1:", "").strip()
            answer2 = query[index2:].replace("A2:", "").strip()
            is_chart_in_ans = True
            # answer2 = query[index2:].replace("A2: python bar chart  visualization code for list all the settlements that we have done in the last year:", "").strip()

            print("ans1 A1: : \n",answer1)
            print("ans2 A1: : \n",answer2)
        else:
            answer1 = query[index1:].replace("A1:", "").strip()
            print("else ans3 : \n",answer1)
            is_chart_in_ans = False
    if "a1:" in query:

        index1 = query.index("a1:")
        if "a1:" in query and "a2:" in query:
            index2 = query.index("a2:")
            answer1 = query[:index2].replace("a1:", "").strip()
            answer2 = query[index2:].replace("a2:", "").strip()
            is_chart_in_ans = True
            # answer2 = query[index2:].replace("A2: python bar chart  visualization code for list all the settlements that we have done in the last year:", "").strip()

            print("ans1 a1: : \n",answer1)
            print("ans2 a1: : \n",answer2)
        else:
            answer1 = query[index1:].replace("a1:", "").strip()
            print("else ans3 : \n",answer1)
            is_chart_in_ans = False
    elif "A 1:" in query :
        index1 = query.index("A 1:")
        if "A 1:" in query and "A 2:" in query:
            index2 = query.index("A 2:")
            answer1 = query[:index2].replace("A 1:", "").strip()
            answer2 = query[index2:].replace("A 2:", "").strip()
            is_chart_in_ans = True
            # answer2 = query[index2:].replace("A 2: python bar chart  visualization code for list all the settlements that we have done in the last year:", "").strip()

            print("ans1 A 1: : \n",answer1)
            print("ans2 A 1: : \n",answer2)
        else:
            answer1 = query[index1:].replace("A 1:", "").strip()
            print("else ans3 : \n",answer1)
            is_chart_in_ans = False
    elif "a 1:" in query :
        index1 = query.index("a 1:")
        if "a 1:" in query and "a 2:" in query:
            index2 = query.index("a 2:")
            answer1 = query[:index2].replace("a 1:", "").strip()
            answer2 = query[index2:].replace("a 2:", "").strip()
            is_chart_in_ans = True
            # answer2 = query[index2:].replace("A 2: python bar chart  visualization code for list all the settlements that we have done in the last year:", "").strip()

            print("ans1 a 1: : \n",answer1)
            print("ans2 a 1: : \n",answer2)
        else:
            answer1 = query[index1:].replace("a 1:", "").strip()
            print("else ans3 : \n",answer1)
            is_chart_in_ans = False
    elif "A 1.:" in query :
        index1 = query.index("A 1.:")
        if "A 1.:" in query and "A 2.:" in query:
            index2 = query.index("A 2.:")
            answer1 = query[:index2].replace("A 1.:", "").strip()
            answer2 = query[index2:].replace("A 2.:", "").strip()
            is_chart_in_ans = True
            # answer2 = query[index2:].replace("A 2: python bar chart  visualization code for list all the settlements that we have done in the last year:", "").strip()

            print("ans1 A 1.: : \n",answer1)
            print("ans2 A 1.: : \n",answer2)
        else:
            answer1 = query[index1:].replace("A 1.:", "").strip()
            print("else ans3 : \n",answer1)
            is_chart_in_ans = False
    elif "a 1.:" in query :
        index1 = query.index("a 1.:")
        if "a 1.:" in query and "a 2.:" in query:
            index2 = query.index("a 2.:")
            answer1 = query[:index2].replace("a 1.:", "").strip()
            answer2 = query[index2:].replace("a 2.:", "").strip()
            is_chart_in_ans = True
            # answer2 = query[index2:].replace("A 2: python bar chart  visualization code for list all the settlements that we have done in the last year:", "").strip()

            print("ans1 a 1.: : \n",answer1)
            print("ans2 a 1.: : \n",answer2)
        else:
            answer1 = query[index1:].replace("a 1.:", "").strip()
            print("else ans3 : \n",answer1)
            is_chart_in_ans = False

    try:
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='postgres',
            database='postgres',
            port="5440"
        )
    except Exception as e:
        return jsonify({'query':format_sql(query), 'error_details':str(e), 'is_run':False, 'is_chart_in_ans' : is_chart_in_ans})
    # if chart is inside the ans only run this html file genration code
    if is_chart_in_ans:
        # write inside python3 file
        chart_file = open("chart_code_run.py","w")
        print("write inside the chart file")            
        chart_file.write(get_code(answer2.strip()))
        chart_file.close()

        # will cretae thred and run the run_chart function
        thread = multiprocessing.Process(target=run_chart, args=())
        thread.start()


    answer1 = answer1.replace(";","")

    def replace_string(input_string):
        input_string = input_string.replace("Answer", "")
        return input_string.replace(":", "")


    answer1 = replace_string(answer1)
    answer1 = answer1.replace("\n"," ")
    print("\n\nreplaced new line char\n",str(answer1))
    answer1 = answer1.strip()
    # Create a cursor object
    cur = conn.cursor()
    cur1 = conn.cursor()
    print("\n\n\n\nquery line 123: "+"select json_agg(to_json(d)) from ("+ answer1 + ") as d")
    # Execute the query
    try:
        cur1.execute("""select json_agg(to_json(d)) from ("""+ answer1 + """) as d""")
    except Exception as e:
        #if error occours
        print("sgnons erorr : ",str(e))
        
        return jsonify({'query':format_sql(query), 'error_details':str(e), 'is_run':False, 'is_chart_in_ans' : is_chart_in_ans})


    
    cur.execute(answer1)

    # Fetch the result
    result = cur.fetchall()
    json_ans = cur1.fetchall()
    # print("\njsonans : \n",json_ans)
    if (json_ans[0][0][0]):
        print(json_ans[0][0][0])
    else:    
        print("sgnons null value")
        return jsonify({'query':format_sql(answer1), 'error_details':'No SQl data', 'is_run':False, 'is_chart_in_ans' : is_chart_in_ans})

    
    return jsonify({'query':format_sql(answer1), 'result':result, 'jsonresult': json_ans , 'is_run':True, 'is_chart_in_ans' : is_chart_in_ans})


@app.route('/get_div', methods=['GET'])
def get_div_from_html():
    return jsonify({
        'sgnons' : 'jkhjamjbm',
        'div' : get_div()
    })


if __name__ == "__main__":
    app.run(debug=True)

