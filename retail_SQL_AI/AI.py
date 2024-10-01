from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import sql_database
from sqlalchemy import create_engine, text
from get_api_key_from_json import get_api_key_from_json
import re
from langchain_community.utilities.sql_database import SQLDatabase


# Database connection parameters
db_user = "root"
db_password = "Aj213778*"
db_host = "localhost"
db_name = "Amv_Tshirts"

# Get the API key from the JSON file
api_key = get_api_key_from_json(r"C:\Users\AM ECOSYSTEMS\OneDrive\Documents\Chatbot\Retail AI Store Bot\Apikey.json", "api key")

# Initialize the ChatGoogleGenerativeAI with the API key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def main(query):
    try:
        # Create a SQLAlchemy engine
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

        # Create an instance of SQLDatabase
        db = SQLDatabase(engine)

        # Create the SQLDatabaseChain with the LLM
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)

        # Let the LLM generate the SQL query based on the natural language question
        response = db_chain.invoke(query+"if the query doesnt specify much data say please provide a proper query also make sure you dont create query which will update anything in database")  # Use the passed query instead of a hardcoded one

        # Attempt to extract the generated SQL query
        result_string = response.get('result', '')

        # Adjusted regex to find the SQL query in the result string
        sql_query_match = re.search(r'SQLQuery:\s*(SELECT.*)', result_string)

        if sql_query_match:
            generated_sql_query = sql_query_match.group(1).strip()  # Extract and strip the SQL query
        else:
            generated_sql_query = None  # Handle the absence of a valid query

        # Execute the generated SQL query
        if generated_sql_query:
            with engine.connect() as connection:
                result = connection.execute(text(generated_sql_query))  # Use the text wrapper for the query
                stock_quantity = result.fetchone()  # Fetch the first result
                # print("Quantity of stock Found"+str(stock_quantity[0]))

            # Print the stock quantity
            value_from_database = llm.invoke(str(stock_quantity[0])+ " is the answer to the query asked by User here is the:-"+ query+"Create a response which a saleswomen would give looking at the answer and the query and the answer which is getting generated is also by AI only query comes from user. if the answer has error word written in it please suggest it would be better asking someone in store if not dont add anything else and answer is always correct")
            response_content = value_from_database.content.strip('"')
            return response_content  # Return the stock quantity as a string
        else:
            print("No valid SQL query generated.")
            return "No valid SQL query generated."
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error for debugging
        return f"Error: {str(e)}"
