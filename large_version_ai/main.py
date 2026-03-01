from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

# Your specific libraries
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

app = Flask(__name__)
CORS(app)

# --- GLOBAL VARIABLES ---
# We store the AI brain here so it stays loaded in memory
db = None
llm = None
rag_ready = False

def initialize_ai():
    """
    Loads the Excel file and builds the AI model ONCE when the server starts.
    """
    global db, llm, rag_ready
    
    print("\n⏳ SYSTEM: Loading 'big_voiture.xlsx' and building Vector Database...")
    print("   (This might take a minute depending on file size)")

    # 1. Check if file exists
    if not os.path.exists("big_voiture.xlsx"):
        print("❌ ERROR: 'big_voiture.xlsx' file not found in the same directory!")
        return False

    try:
        # 2. LOAD EXCEL
        df = pd.read_excel("data.xlsx")
        text = df.to_string(index=False)

        # 3. SPLIT TEXT
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)

        # 4. EMBEDDINGS
        # Downloads model on first run, then uses cache
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # 5. VECTOR STORE
        db = FAISS.from_texts(chunks, embeddings)

        # 6. LOCAL LLM (Ollama)
        # Ensure you have run `ollama pull phi` on your VPS
        llm = Ollama(model="phi") 
        
        rag_ready = True
        print("✅ SYSTEM: AI Ready! Listening for website requests...")
        return True
        
    except Exception as e:
        print(f"❌ INITIALIZATION ERROR: {e}")
        return False

# Run the initialization immediately when script starts
initialize_ai()

@app.route('/api/chat', methods=['POST'])
def chat():
    # 1. Check if AI loaded correctly
    if not rag_ready:
        return jsonify({
            "response": "Error: Server could not load 'big_voiture.xlsx'. Please check the VPS console logs."
        })

    # 2. Get data from Website
    data = request.json
    user_query = data.get('message', '')
    
    # (Optional) You can check data.get('model') here if you want 
    # different logic for the 3 buttons, but for now we use your script for all.

    print(f"\n📩 Received Query: {user_query}")

    # 3. Your Script Logic (Search + Invoke)
    try:
        # Search for context
        docs = db.similarity_search(user_query, k=1)
        context = docs[0].page_content if docs else "No context found."

        # Create Prompt
        prompt = f"""
        You are an efficient data assistant. Answer based ONLY on the following Excel data:

        {context}

        Question: {query}
        """

        # Generate Answer
        answer = llm.invoke(prompt)
        
        print("📤 Sending Response...")
        
        # 4. Return to Website
        return jsonify({
            "response": answer
        })

    except Exception as e:
        print(f"❌ Processing Error: {e}")
        return jsonify({
            "response": "I encountered an internal error processing your request."
        })

if __name__ == '__main__':
    # host='0.0.0.0' makes it available to the public internet
    app.run(host='0.0.0.0', port=5000)

