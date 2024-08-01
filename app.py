# app.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from geminiAPI import*
import os,shutil
from OCR import *


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def dltfaiss():
    try:
        shutil.rmtree("faiss_index")
    except Exception as e:
        print(e)


def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    # dltfaiss()
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    # prompt_template = """
    # Context:
    # The answer to the question is found in a PDF document. Please provide the page number where the answer is located.
    # Context:\n {context}?\n
    # Question: \n{question}\n

    # Page Number:
    # """


    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):

    if os.path.exists("faiss_index"):

        embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
        
        # new_db = FAISS.load_local("faiss_index", embeddings)
        new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)  

        chain = get_conversational_chain()

        
        response = chain(
            {"input_documents":docs, "question": user_question}
            , return_only_outputs=True)

        print(response)
        # st.write("Reply: ", response["output_text"])
        return response["output_text"]
    
    else:
        return "You Did not provide any PDF, First upload the PDF"



def main():

    # if 'init' not in st.session_state:
    #     st.session_state.init = True
    #     dltfaiss()

    st.set_page_config("Chat PDF")
    st.header("Chat With PDF 🤖")
    user_question = st.chat_input("Ask a Question from the PDF Files")
    Q = str(user_question)

    if user_question:
        st.write("**👤:** "+Q)
        A = user_input(user_question)
        P = "answer is not available in the context"
        if "not" and "context" in A:
            A = A+" you can find it from-->\n"+angel(Q)
        st.write("**🤖:** ",A)


    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your readable PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        # pdf_docs = perform_ocr(pdf_docs)
        # for pdf in pdf_docs:
        #     if not is_soft_copy(pdf):
        #         # pdf_docs = perform_ocr(pdf_docs)
        #         st.error("Performing the OCR function is under maintenance.\nSome of your uploaded files are not readeble please refresh and upload again")
        #         break
            
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")



if __name__ == "__main__":
    main()
