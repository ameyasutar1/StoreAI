from PyPDF2 import PdfReader
from langchain_groq import ChatGroq
from get_api_key_from_json import get_api_key_from_json
from ReadTxt import read_file
import getpass
import os
import re
import json

def Reader(pdf_path):

    # Open the PDF and extract text using PyPDF2
    reader = PdfReader(pdf_path)
    extracted_text = ""

    api_key = get_api_key_from_json(r"C:\Users\AM ECOSYSTEMS\OneDrive\Documents\Chatbot\Retail AI Store Bot\Apikey.json","groq_key")

    if "GROQ_API_KEY" not in os.environ:
        os.environ["GROQ_API_KEY"] = api_key

    # Iterate through each page in the PDF and extract text
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        extracted_text += page.extract_text()
        llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )
    Query = read_file(r"C:\Users\AM ECOSYSTEMS\OneDrive\Documents\Chatbot\Retail AI Store Bot\retail_SQL_AI\PromptPDF.txt")
    ai_response = llm.invoke(Query+"Further is the extracted Data From PDF Provide a Valid JSON and nothing else no preamble neither text after the response"+extracted_text)
    # print(ai_response.content)
    # Print the extracted text to the console
    json_data = ai_response.content
    return json_data

# def extract_json_objects(text):
#     # Regular expression to match the entire JSON block
#     regex = r'(\{.*\})'  # This captures everything between braces

#     # Search for the JSON string in the input
#     match = re.search(regex, text, re.DOTALL)

#     if match:
#         json_data = match.group(1)  # Extract the matched JSON string
#         print("Extracted JSON data block:", json_data)  # Debug print

#         # Attempt to parse the JSON string into a Python dictionary
#         try:
#             data = json.loads(json_data)  # Load the entire JSON block
#             # Extract the array of t-shirts
#             t_shirts = data.get("t_shirts", [])
            
#             # Prepare a list to store extracted data
#             extracted_data = []
#             for item in t_shirts:
#                 extracted_data.append(item)

#             return extracted_data  # Return the list of t-shirt dictionaries

#         except json.JSONDecodeError as e:
#             print(f"JSON decoding error: {e}")
#             print("Problematic JSON data:", json_data)
#             return []  # Return an empty list if JSON parsing fails
#     else:
#         print("No valid JSON found in the text.")
#         return []  # Return an empty list if no JSON data found

def extract_json_objects(text):
    # Regex to match JSON objects: 
    # Match balanced braces and quoted strings
    regex = r'\{(?:[^{}]|"[^"\\]*(?:\\.[^"\\]*)*")*+\}'  # Simple non-recursive JSON match
    
    # Find potential JSON objects
    potential_jsons = re.findall(regex, text)

    extracted_data = []

    for match in potential_jsons:
        print("Extracted JSON data block:", match)  # Debugging output
        
        # Attempt to parse the JSON string into a Python dictionary or list
        try:
            data = json.loads(match)
            extracted_data.append(data)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            print("Problematic JSON data:", match)
            # Attempt to fix common issues
            fixed_data = fix_and_parse_json(match)
            if fixed_data is not None:
                extracted_data.append(fixed_data)

    return {"t_shirts": extracted_data} if extracted_data else {"t_shirts": []}

def fix_and_parse_json(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        fixed_json_string = fix_common_issues(json_string)
        try:
            return json.loads(fixed_json_string)
        except json.JSONDecodeError as e:
            print(f"Failed to fix JSON: {e}")
            return None

def fix_common_issues(json_string):
    # Remove trailing commas before closing brackets
    json_string = re.sub(r',\s*([}\]])', r'\1', json_string)
    
    # Attempt to balance braces and brackets
    open_braces = json_string.count('{')
    close_braces = json_string.count('}')
    open_brackets = json_string.count('[')
    close_brackets = json_string.count(']')
    
    # Add missing closing braces or brackets
    if open_braces > close_braces:
        json_string += '}' * (open_braces - close_braces)
    if open_brackets > close_brackets:
        json_string += ']' * (open_brackets - close_brackets)

    return json_string