import os
import streamlit as st
import pickle
import time
import requests
from bs4 import BeautifulSoup
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import pathway as pw

load_dotenv()  

st.title("Your own MBBS Bot 🩺")
st.sidebar.title("Health Article URLs or Website")

input_type = st.sidebar.radio("Input Type", ("Individual URLs", "Website"))
urls = []

if input_type == "Individual URLs":
    for i in range(3):
        url = st.sidebar.text_input(f"URL {i+1}")
        if url:
            urls.append(url)
else:
    website = st.sidebar.text_input("Website URL")
    max_pages = st.sidebar.number_input("Max pages to scrape", min_value=1, max_value=50, value=20)

    if website:
        try:
            response = requests.get(website)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            base_url = website if website.endswith('/') else website + '/'
            links = [base_url + link if link.startswith('/') else link for link in links]
            urls = links[:max_pages]
        except Exception as e:
            st.sidebar.text(f"Error scraping the website: {e}")

default_urls = [
    "https://medlineplus.gov/all_healthtopics.html"
]

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()
llm = OpenAI(temperature=0.9, max_tokens=500)

if process_url_clicked:
    if not urls:
        urls = default_urls

    try:
        loader = UnstructuredURLLoader(urls=urls)
        main_placeholder.text("Data Loading...Started...✅✅✅")
        data = loader.load()

        # Use Pathway to split data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        main_placeholder.text("Text Splitter...Started...✅✅✅")
        docs = text_splitter.split_documents(data)

        if docs:
            df = pw.DataFrame(docs)

            embeddings = OpenAIEmbeddings()
            vectorstore_openai = FAISS.from_documents(df, embeddings)
            main_placeholder.text("Embedding Vector Started Building...✅✅✅")
            time.sleep(2)

            with open(file_path, "wb") as f:
                pickle.dump(vectorstore_openai, f)
        else:
            main_placeholder.text("No documents to process. Please check the URLs provided.")
    except Exception as e:
        main_placeholder.text(f"An error occurred: {e}")

query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                vectorstore = pickle.load(f)
                chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
                result = chain({"question": query}, return_only_outputs=True)

                st.header("Answer")
                st.write(result["answer"])

                sources = result.get("sources", "")
                if sources:
                    st.subheader("Sources:")
                    sources_list = sources.split("\n")
                    for source in sources_list:
                        st.write(source)
        except Exception as e:
            st.write(f"An error occurred while retrieving the answer: {e}")
    else:
        st.write("FAISS index not found. Please process the URLs first.")
