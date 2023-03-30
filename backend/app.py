
import os
import openai
from flask import Flask, jsonify, request
import psycopg2
import pandas as pd
from sql_formatter.core import format_sql

from flask_cors import CORS

openai.api_key = "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"

app = Flask(__name__)
CORS(app)

@app.route('/generate_sql_query', methods=['POST'])
def generate_query_endpoint():
    question = request.json['prompt']
    # question = request.json["question"]
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            # prompt=f"### Postgres SQL tables, with their properties:\n#\n# view_gen_hearings_component(arbitration_id, container_name, matter_number, experts_id, type_of_hearing, start_date, end_date , exclude_weekend, hsf_internal_advocates, external_advocates,hearing_format, virtual_hearing, bundle_used, hsf_involved_bundle, bundle_type, hearing_services_used, experts_who_gave_evidence_at_hearing, created_by, updated_by)\n\n# view_gen_end_of_matter_assessment_component(arbitration_id ,known_as as container_name ,matter_number ,end_of_matter_id ,file_closed_date ,how_compl x_was_the_matter  ,key_matter_takeway_points ,formal_debrief_client ,client_feedback ,client_responsiveness ,counterparty_difficulty  ,coclaimant_corespondent_difficulty  ,total_hours_recorded_matter_code, total_billable_hours_on_arbitration ,total_revenue_matter ,actual_revenue_reason ,contribution_margin_matter ,total_billed_hours_on_arbitration ,technology_used  ,out_of_house_services  ,created_by ,updated_by)\n\n# Salary_Payments(id, employee_id, amount, date)\n#\n\n### {question}\n\nSelect ",
            prompt="### Postgres SQL tables, with their properties:\n#\n# view_gen_hearings_component(arbitration_id, container_name, matter_number, experts_id, type_of_hearing, start_date, end_date , exclude_weekend, hsf_internal_advocates, external_advocates,hearing_format, virtual_hearing, bundle_used, hsf_involved_bundle, bundle_type, hearing_services_used, experts_who_gave_evidence_at_hearing, created_by, updated_by)\n\n# view_gen_end_of_matter_assessment_component(arbitration_id ,known_as as container_name ,matter_number ,end_of_matter_id ,file_closed_date ,how_compl x_was_the_matter  ,key_matter_takeway_points ,formal_debrief_client ,client_feedback ,client_responsiveness ,counterparty_difficulty  ,coclaimant_corespondent_difficulty  ,total_hours_recorded_matter_code, total_billable_hours_on_arbitration ,total_revenue_matter ,actual_revenue_reason ,contribution_margin_matter ,total_billed_hours_on_arbitration ,technology_used  ,out_of_house_services  ,created_by ,updated_by)\n\n# view_gen_settlements_component(\tarbitration_id, known_as as container_name, matter_number, settlements_id, is_adr_process, if_so_which_adr_process, settlement_date, hsf_assessment_success, client_assessment_success, settlement_amount_usd, settlement_amount_local, local_currency_name , further_details, created_by, updated_by)\n\n# view_gen_claim_and_counterclaim_component(arbitration_id, known_as as container_name, matter_number, claim_counterclaim_id, value_of_claims_local, local_currency_name, declaratory_relief, value_of_claims_usd, value_of_counterclaims_usd, value_of_counterclaims_local, additional_information_claims  , created_by, updated_by )\n\n#\n\n### Question : A Postgresql query to list all hearing that we did in the last year from 2022, from table view_gen_hearings_component taking column start_date \nAnswer : SELECT * FROM view_gen_hearings_component WHERE start_date >= '2022-01-01;\n\n\n### Question : A Postgresql query to list all top 10 revenue generating matters, from table view_gen_end_of_matter_assessment_component taking column total_revenue_matter - \nAnswer : SELECT arbitration_id, container_name, matter_number, total_revenue_matter\nFROM view_gen_end_of_matter_assessment_component WHERE total_revenue_matter IS NOT NULL ORDER BY total_revenue_matter DESC LIMIT 10;\n\n\n### Question : A Postgresql query to average settlement values, from table gen_settlements_component taking column settlement_amount_usd\n\n\n### Question : A Postgresql query to list the arbitrations that have the 10 highest claim values from table view_gen_claim_and_counterclaim_component -\nAnswer :  SELECT arbitration_id, container_name, matter_number, value_of_claims_usd FROM view_gen_claim_and_counterclaim_component WHERE value_of_claims_usd IS NOT NULL ORDER BY value_of_claims_usd DESC LIMIT 10;\n\n\n\n### Question : A Postgresql query to list all the settlements that we have done in the last year 2022 from table view_gen_settlements_component - \nAnswer : SELECT * FROM view_gen_settlements_component WHERE date_trunc('year', settlement_date) = '2022-01-01';\n\n### Question : Show me all hearing in the past year 5 - \nAnswer: SELECT arbitration_id, container_name, matter_number, experts_id, type_of_hearing, start_date, end_date, hsf_internal_advocates, external_advocates, hearing_format, virtual_hearing, bundle_used, hsf_involved_bundle, bundle_type, hearing_services_used, experts_who_gave_evidence_at_hearing, created_by, updated_by FROM view_gen_hearings_component\nWHERE start_date >= (NOW() - INTERVAL '5 years');\n\n\n\n\n\nquestion: "+ question + "\n\n",
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            # stop=["#", ";"]
        )
        
    except Exception as e:
        #if error occours
        print("sgnons erorr : ",str(e))
        query = format_sql("""openai API Error""")
    
        return jsonify({"query":query, 'error_details':str(e), 'is_run':False})
    
    query = response.choices[0].text
    # query = query.replace("*", "SELECT *")
    # if not query.startswith("SELECT"):
    #     query = "SELECT " + query
    #     print(query)
    try:
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='postgres',
            database='postgres',
            port="5440"
        )
    except Exception as e:
        return jsonify({'query':format_sql(query), 'error_details':str(e), 'is_run':False})

    query = query.replace(";","")

    def replace_string(input_string):
        input_string = input_string.replace("Answer", "")
        return input_string.replace(":", "")


    query = replace_string(query)
    query = query.strip()
    # Create a cursor object
    cur = conn.cursor()
    cur1 = conn.cursor()
    print("\n\n\n\nquery : "+"select json_agg(to_json(d)) from ("+ query + ") as d")
    # Execute the query
    try:
        cur1.execute("""select json_agg(to_json(d)) from ("""+ query + """) as d""")
    except Exception as e:
        #if error occours
        print("sgnons erorr : ",str(e))
        
        return jsonify({'query':format_sql(query), 'error_details':str(e), 'is_run':False})


    
    cur.execute(query)

    # Fetch the result
    result = cur.fetchall()
    json_ans = cur1.fetchall()
    print(json_ans)
    if (json_ans[0][0][0]):
        print(json_ans[0][0][0])
    else:    
        print("sgnons null value")
        return jsonify({'query':format_sql(query), 'error_details':'No SQl data', 'is_run':False})

    return jsonify({'query':format_sql(query), 'result':result, 'jsonresult': json_ans , 'is_run':True})


if __name__ == "__main__":
    app.run(debug=True)

