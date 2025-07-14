import pandas as pd
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app) 

# --- Initialize ChromaDB and Gemini Client ---
CHROMA_PATH = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="colleges_and_programs")
print(f"ChromaDB collection '{collection.name}' initialized.")

gemini_client = genai.Client()
print("Gemini client initialized.")

@app.route('/generate_roadmap', methods=['POST'])
def generate_roadmap():
    """
    API endpoint to generate roadmap data for Vue Flow.
    Receives current nodes from frontend, performs RAG, and returns structured JSON labels.
    """
    try:
        data = request.json
        current_nodes_context = data.get('currentNodes', [])
        user_query = data.get('userQuery', 'Suggest a personalized learning and career roadmap in tech.')

        print(f"Received user query: {user_query}")
        print(f"Received current nodes context: {current_nodes_context}")

        # 1. Perform RAG based on the user's input/context
        print("Performing ChromaDB query...")
        results = collection.query(
            query_texts=[user_query],
            n_results=10
        )
        print("ChromaDB query complete.")
        
        rag_context = json.dumps(results['documents'], indent=2)
        print(f"RAG Context (first 200 chars): {rag_context[:200]}...")
        
        # 2. Define the JSON schema for the expected response (id and newLabel)
        roadmap_schema = {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "id": {"type": "STRING"},
                    "newLabel": {"type": "STRING"}
                },
                "required": ["id", "newLabel"]
            }
        }
        
        # 3. Construct the system instruction and context prompt
        system_instruction_text = """
        You are a helpful career and education advisor for a user in Cebu City, Philippines. 
        Your task is to populate a flowchart with a personalized roadmap based on the provided data.
        
        You have been provided with:
        1. A list of current node IDs and their existing labels in a flowchart structure.
        2. Relevant data from a database (RAG results) containing information about schools and programs in Cebu.
        
        Use the RAG data to inform the 'PROGRAM' (id: 1) node, ensuring they are specific to a school found in the database if possible.
        
        Generate relevant and specific labels for EACH node ID (1 through 15) in the provided list.
        
        * For 'PROGRAM' (id: 1), suggest a STEM related field or course that is found in the database, 
        * For 'RESOURCES' (id: 2), skip this field. Dont put anything in this field but the word "RESOURCES"
        * For 'COLLEGES' (id: 3), skip this field. Dont put anything in this field but the word "COLLEGES".
        * FOR nodes with id 4-9, fill with them with resources that can be found in the database that are related to the program suggested in id: 1.
        * FOR nodes with id 10-12, provide schools that offer the program that can be found in the database that are related to the program suggested in id: 1.
        * Fill the remaining nodes (13-15) with information regarding the schools found in nodes 10-12 respectively.
        

        Return the response ONLY as a JSON array of objects, structured exactly as required by the roadmap_schema, with 'id' and 'newLabel' for all nodes (1-15).
        """
        
        # 4. Prepare contents for Gemini API call - FIX: Added 'role': 'user'
        contents_for_gemini = [
            {"role": "user", "parts": [{"text": f"User's query/interest: {user_query}"}]},
            {"role": "user", "parts": [{"text": f"Current Node structure: {json.dumps(current_nodes_context)}"}]},
            {"role": "user", "parts": [{"text": f"Relevant RAG Data: {rag_context}"}]}
        ]

        print("Calling Gemini API...")
        # 5. Call Gemini API with structured output configuration
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction_text,
                response_mime_type="application/json",
                response_schema=roadmap_schema,
                temperature=0.8
            ),
            contents=contents_for_gemini
        )
        print("Gemini API call complete.")

        # 6. Parse and return the JSON
        # The response.text will be the JSON string output by Gemini based on the schema
        gemini_response_json = json.loads(response.text)
        print(f"Gemini response JSON: {gemini_response_json}")
        
        return jsonify(gemini_response_json)

    except Exception as e:
        print(f"Error in /generate_roadmap endpoint: {e}")
        return jsonify({"error": str(e), "message": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
