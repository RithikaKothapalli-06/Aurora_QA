from fastapi import FastAPI, Query
from message_fetcher import get_all_messages
from vector_store import init_vector_store, search_similar_messages
from reasoning import generate_answer
import uvicorn

# ---------------------------------------------------------
# APP INITIALIZATION
# ---------------------------------------------------------

app = FastAPI(
    title="Aurora QA System",
    description="Natural-language QA over member messages.",
    version="1.0.0"
)

# ---------------------------------------------------------
# LOAD MESSAGES + BUILD VECTOR STORE ON STARTUP
# ---------------------------------------------------------

print("Fetching messages from November API...")
messages = get_all_messages()

print(f"Loaded {len(messages)} messages.")

print("Initializing vector store...")
client, collection = init_vector_store(messages)

print("Vector store ready.")


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

@app.get("/ask")
def ask_question(question: str = Query(..., description="Your natural-language question")):

    similar = search_similar_messages(collection, question, top_k=3)
    answer = generate_answer(question, similar)
    return {"answer": answer}


@app.get("/")
def root():
    return {
        "message": "Aurora QA API is running. Use /ask?question=your_question"
    }


# ---------------------------------------------------------
# LOCAL RUN
# ---------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
