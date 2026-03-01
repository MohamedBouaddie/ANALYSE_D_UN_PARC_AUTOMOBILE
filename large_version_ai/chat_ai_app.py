from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_sslify import SSLify  # not used for now
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
db = None
db2 = None
llm = None
rag_ready = False

def load_excel_to_vector(file_name):
    if not os.path.exists(file_name):
        print(f"❌ ERROR: '{file_name}' file not found!")
        return None

    df = pd.read_excel(file_name)
    text = df.to_string(index=False)

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_texts(chunks, embeddings)

    return vectordb



def initialize_ai():
    global db1, db2, llm, rag_ready

    try:
        print("\n⏳ Loading data.xlsx -> Model 1 & 3")
        db1 = load_excel_to_vector("big_data_voiture.xlsx")

        print("⏳ Loading data2.xlsx -> Model 2")
        db2 = load_excel_to_vector("data.xlsx")

        if db1 is None:
            raise Exception("data.xlsx failed to load")

        if db2 is None:
            print("⚠️ WARNING: data2.xlsx not found, Model2 will fallback to data.xlsx")
            db2 = db1

        llm = Ollama(
            model="phi3",
            num_predict=100,
num_ctx=256,
        )

        rag_ready = True
        print("✅ SYSTEM: AI Ready with 2 knowledge bases!")

    except Exception as e:
        print(f"❌ INITIALIZATION ERROR: {e}")
        rag_ready = False


# Run the initialization immediately when script starts
initialize_ai()


@app.route('/api/chat', methods=['POST'])
def chat():
    global rag_ready, db, llm

    # 1. Check if AI loaded correctly
    if not rag_ready:
        return jsonify({
            "response": "Error: Server could not load 'data.xlsx'. Please check the VPS console logs."
        })

    # 2. Get data from Website
    data = request.json or {}
    user_query = data.get('message', '')
    model_name = data.get('model', '')  # <-- front should send "model": "model1" / "model2" / "model3"

    print(f"\n📩 Received Query: {user_query}")
    print(f"🧠 Selected model: {model_name}")
    if model_name == "gpt-4":
       if db1 is None:
           return jsonify({"response": "Model 1 database not loaded"})
       current_db = db1
    elif model_name == "codex-v2":
        if db2 is None:
            return jsonify({"response": "Model 2 database (data2.xlsx) not loaded"})
        current_db = db2
    elif model_name == "creative-x":
        if db1 is None:
            return jsonify({"response": "Model 3 database not loaded"})
        current_db = db1
    try:
        # 3. Search for context (RAG)
        docs = current_db.similarity_search(user_query, k=1)
        context = docs[0].page_content if docs else "No context found."

        # 4. Choose prompt depending on model_name
        if model_name == "gpt-4":

            # 🔹 Model 1: Simple, direct assistant
            system_prompt = f"""
You are a smart, multilingual assistant.

Rules:
- If the question is simple, give a SHORT and SIMPLE answer.
- If the question is complex, give a clear but not too long explanation.
- Use natural, friendly language.
MAX 100 WORDS
            """

        elif model_name == "codex-v2":
            current_db = db1
             # 🔹 Model 2: Teacher / explainer
            system_prompt = f"""
You are an expert DATA ANALYST specialized in automotive (car) big data.

VERY IMPORTANT RULES:
- You can ONLY use the information provided in the Excel context below.
- Do NOT use external knowledge about cars.
- Do NOT invent data.
- If the answer does not exist in the data, clearly say: "Data not available in the file."

YOUR ROLE:
- Analyze the car data from the Excel file (brands, models, prices, mileage, fuel, year, performance, etc.).
- Extract insights, trends, comparisons, and statistics ONLY from the data.
- Answer with clear facts derived from the file.

YOUR CAPABILITIES (from data only):
- Find the cheapest / most expensive car
- Calculate average price, average mileage, average year
- Compare brands, models, or fuel types
- Find the best / worst values
- Detect trends (for example: price vs year if possible)
- Summarize patterns in the dataset


LANGUAGE RULE:
- Detect the user's language automatically
- Always reply in the SAME language (Arabic / French / English)

STYLE:
- Keep answers structured and clear
- Use bullet points when useful
- Focus on data insights, not storytelling

THE IMPORTANT RULE EST DE DONNER LES CALCULES EN NOMBRES
JAMAIS DONNER LE CODE PROGRAMMABLE
MAX 100 WORD
EXCEL DATA (CONTEXT):
{context}
            """

        elif model_name == "creative-x":
            current_db = db2
# 🔹 Model 3: Creative / advisor
            system_prompt = f"""
You are a DATA ASSISTANT specialized in simple calculations and basic data analysis.

IMPORTANT RULES:
- You can ONLY use the provided Excel data (context below).
- Do NOT use any external or general knowledge.
- Do NOT invent any values.
- If the data does not contain the answer, clearly say: "Data not available."

YOUR TASK:
- Perform only SIMPLE calculations (sum, average, count, min, max, percentage).
- Give simple explanations.
- When useful, show a BASIC example of Pandas or Matplotlib code.

STYLE:
- Keep answers short and clear.
- If the user is Arabic, answer in Arabic.
- If the user is French, answer in French.
- If the user is English, answer in English.

ALLOWED PANDAS FUNCTIONS (examples):
- df.head()
- df.describe()
- df['column'].sum()
- df['column'].mean()
- df['column'].min()
- df['column'].max()
- df['column'].count()
- df.groupby(...)
- df.sort_values(...)

ALLOWED MATPLOTLIB (examples):
- plt.plot()
- plt.bar()
- plt.hist()

DO NOT USE:
- Machine learning
- Complex statistics
- Deep learning
- External web data
MAX 100 WORDS
EXCEL DATA (context):
{context}
            """
              # Fallback if unknown model name


        # Final prompt sent to the LLM
        prompt = f"""{system_prompt}

User message:
{user_query}
"""

        # 5. Generate Answer
        answer = llm.invoke(prompt)

        print("📤 Sending Response...")

        # 6. Return to Website
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
    app.run(host='0.0.0.0', port=8080)
