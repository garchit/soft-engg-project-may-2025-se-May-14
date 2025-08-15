import os
from flask import request, jsonify
from flask_restful import Resource
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# ----------- GLOBAL SINGLETON INITIALIZATION -----------

# Load vector store
persist_dir = "vector_store"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if os.path.exists(persist_dir) and os.listdir(persist_dir):
    print("Loading existing vector store from disk...")
    db = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
else:
    print("Creating new vector store from documents...")
    # Correctly locate the documents folder relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__)) # Gets the 'routes' directory
    project_root = os.path.dirname(base_dir) # Goes up to the 'Backend' directory
    file_path = os.path.join(project_root, 'routes', 'documents', 'examples.txt')
    
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    db = Chroma.from_documents(docs, embedding_model, persist_directory=persist_dir)
    db.persist()

# Load the model pipeline once
model_id = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
llm_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
llm = HuggingFacePipeline(pipeline=llm_pipeline)

# Set up prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are a helpful and friendly AI finance tutor. 
    You are allowed to answer both finance-related questions and casual small talk.

    If the answer can be found in the context below, use it.
    If the question is casual, respond naturally.
    If the question is completely unrelated, say: "Sorry, that's out of my scope."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
)

# Build the chain
retriever = db.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt_template}
)

# ----------- RESOURCE CLASS (USE GLOBALS) -----------

class AIChatbot(Resource):
    def post(self):
        data = request.get_json(force=True)
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "Missing 'question'"}), 400

        result = qa_chain.run(question)
        return jsonify({"question": question, "answer": self.clean_answer(result)})

    def clean_answer(self, text):
        text = text.strip()
        seen = set()
        output = []
        for line in text.splitlines():
            if line not in seen:
                seen.add(line)
                output.append(line)
        return " ".join(output[:5])