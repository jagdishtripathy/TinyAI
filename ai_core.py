import re
import time
import socket
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from networkx import is_connected
from data_loader import load_data, save_json
from config import *

# Load data
user_profile, memory_facts, chat_history, df, log_df = load_data()

# Build documents
documents = [
    Document(page_content=f"{row['Field']}: {row['Value']}", metadata={"source": row['Field']})
    for _, row in df.iterrows()
] + [
    Document(
        page_content=f"LogType: {row['LogType']}\nExample: {row['Example']}\nWhatToLookFor: {row['WhatToLookFor']}",
        metadata={"source": f"log_{row['LogType']}"}
    )
    for _, row in log_df.iterrows()
]

embedding_model = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
db = FAISS.from_documents(documents, embedding_model)
retriever = db.as_retriever(search_kwargs={"top_k": 5})

llm = LlamaCpp(
    model_path=MODEL_PATH,
    temperature=0.2,
    max_tokens=4096,
    top_p=0.9,
    n_ctx=4096,
    n_batch=8,
    verbose=False,
    model_kwargs={"use_gpu": True, "gpu_layers": 40}
)

prompt_template = """
You are TinyAI, a helpful cybersecurity AI assistant created by Jagadish Tripathy. Your purpose is to assist users with questions related to cybersecurity, SIEM, and ethical hacking. You also remember facts shared by the user. Find the current things on the internet and use them to answer the question. If the user asks you to remember something, do so and confirm it.

Internet Access: {internet_status}
Current Date: {current_date}
Day: {current_day}

Latest Web Info (if any):
{web_info}

User Interests: {interests}
User Memory:
{memory}

Knowledge Base:
{summaries}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["summaries", "question", "interests", "memory", "current_date", "current_day", "internet_status", "web_info"],
    template=prompt_template,
)

qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

def detect_interest(msg):
    keywords = {
        "payload": "cybersecurity", "msfvenom": "ethical hacking",
        "wazuh": "SIEM", "burp": "web pentesting",
        "nmap": "network scanning", "osint": "open source intelligence"
    }
    for key, tag in keywords.items():
        if key in msg.lower() and tag not in user_profile["interests"]:
            user_profile["interests"].append(tag)
            save_json(PROFILE_PATH, user_profile)

def add_fact_to_memory(fact):
    memory_facts.append(fact)
    save_json(MEMORY_PATH, memory_facts)
    db.add_documents([Document(page_content=fact, metadata={"source": "memory"})])

def ask_ai(message, history):
    detect_interest(message)
    chat_history.append({"role": "user", "content": message})
    save_json(CHAT_HISTORY_PATH, chat_history)

    if (m := re.match(r"remember[:\s]*(that)?\s*(.*)", message.strip(), re.IGNORECASE)):
        fact = m.group(2).strip()
        if fact:
            add_fact_to_memory(fact)
            yield "", history + [{"role": "user", "content": message}, {"role": "assistant", "content": "I've noted that!"}]
            return

    docs = retriever.get_relevant_documents(message)
    context = "\n".join([doc.page_content for doc in docs])
    memory_context = "\n".join(memory_facts)
    now = datetime.now()
    current_date = now.strftime("%B %d, %Y")
    current_day = now.strftime("%A")
    internet_status = "Available" if check_internet_connection() else "Not Available"
    web_info = ""
    search_tool = DuckDuckGoSearchAPIWrapper()
    try:
        search_result = search_tool.run(message)
        if search_result:
            web_info = f"Internet Search Result:\n{search_result}"
            context = f"{web_info}\n\n" + context
        else:
            web_info = "No recent information available."
    except Exception as e:
        web_info = f"Web search error: {str(e)}"

    result = qa_chain({
        "summaries": context,
        "question": message,
        "interests": ", ".join(user_profile.get("interests", [])),
        "memory": memory_context,
        "current_date": current_date,
        "current_day": current_day,
        "internet_status": internet_status,
        "web_info": web_info
    })

    answer = result.get("answer", "I couldn't find an answer to that.")
    partial = ""
    for char in answer:
        partial += char
        yield "", history + [{"role": "user", "content": message}, {"role": "assistant", "content": partial}]
        time.sleep(0.03)

    chat_history.append({"role": "assistant", "content": answer})
    save_json(CHAT_HISTORY_PATH, chat_history)

def check_internet_connection():
    import socket
    try:
        socket.create_connection(("www.google.com", 80), timeout=3)
        return True
    except OSError:
        return False