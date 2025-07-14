import pandas as pd
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS for cross-origin requests

# Load environment variables (e.g., your Gemini API key)
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes, allowing your Vue.js frontend to make requests
CORS(app)

# --- Initialize ChromaDB and Gemini Client (once when the app starts) ---
CHROMA_PATH = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="colleges_and_programs")
print(f"ChromaDB collection '{collection.name}' initialized.")

gemini_client = genai.Client()
print("Gemini client initialized.")

@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    """
    API endpoint to receive a user query, perform RAG, and return Gemini's response.
    """
    try:
        # Get the user query from the JSON request body
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        print(f"Received query: {user_query}")

        # Perform the ChromaDB query
        results = collection.query(
            query_texts=[user_query],
            n_results=20
        )

        # Determine the type of query and construct the appropriate system prompt
        # This logic is directly from your ask.py
        if "scholarship" in user_query.lower() or "scholarships" in user_query.lower():
            system_prompt = f"""
You are a helpful assistant. The user is asking for scholarship information.
You will be provided with a list of dictionaries (JSON format), where each dictionary contains details about programs and associated scholarship links.
Your task is to extract the 'institution_name', 'program_name', 'ched_scholarship_link', 'owwa_scholarship_link', and 'dost_scholarship_link' from these dictionaries.
Present the scholarship information in a clear, structured, and bulleted list format, grouped by institution and program.
For each unique institution and program combination, list the available scholarship links.
If a scholarship link is 'N/A', do not include it in the response for that entry.

Example format:
- Institution Name: [Institution Name]
  Program: [Program Name]
  - CHED Scholarship: [Link or "N/A"]
  - OWWA Scholarship: [Link or "N/A"]
  - DOST Scholarship: [Link or "N/A"]

If you cannot find any relevant scholarship information in the provided data, respond with: "I don't know."
Do not make up information.

The data:
{json.dumps(results['metadatas'], indent=2)}
"""
        elif "resource" in user_query.lower() or "prepare" in user_query.lower() or "link" in user_query.lower():
            system_prompt = f"""
You are a helpful assistant. The user is asking for general online resources related to a program.
You will be provided with a list of dictionaries (JSON format), where each dictionary contains details about a program and associated online resources.
Your task is to extract the 'resource_name', 'resource_link', and 'resource_types' from these dictionaries.
Present the unique online resources in a numbered list, formatted as follows:

(1)
RESOURCE NAME: [Resource Name]
RESOURCE LINK: [Resource Link]
RESOURCE TYPE: [Resource Type]

(2)
...

Only provide online resources that are directly relevant to the user's query (e.g., for 'BS Biology' program).
If multiple entries refer to the exact same resource (same name and link), list it only once.
Do not include information about schools, municipalities, provinces, or scholarships unless explicitly asked.
If you cannot find any relevant online resources in the provided data, respond with: "I don't know."

The data:
{json.dumps(results['metadatas'], indent=2)}
"""
        else:
            system_prompt = f"""
You are a helpful assistant. The user will ask you for universities or colleges that offer a specific program.
You will be provided with a list of text documents, each describing a college, its program offerings, and potentially resources and scholarships.
Your task is to list all the unique institutions that offer the program the user is looking for.
Present the schools in a bulleted list, like this:

- School1
- School2
- School3
...

Do not include resource or scholarship information unless explicitly asked by the user.
If you don't know the answer based on the provided data, respond with: "I don't know."
Do not make up information.

The data:
{json.dumps(results['documents'], indent=2)}
"""

        # Generate content using Gemini
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt),
            contents=user_query
        )

        # Return the generated text from Gemini
        return jsonify({"response_text": response.text})

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
