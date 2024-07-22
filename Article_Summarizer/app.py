# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import fitz  # PyMuPDF

# Define login credentials
USERNAME = "user"
PASSWORD = "password"

# Streamlit app
def login_page():
    st.title('Login')
    
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        if username == USERNAME and password == PASSWORD:
            st.session_state['logged_in'] = True
            st.session_state['show_login'] = False
        else:
            st.error('Incorrect username or password')

def main_page():
    st.title('Summarization Tool for Articles, Newspapers, and Research Papers')
    
    # User inputs
    url = st.text_input("Enter the URL of the article, newspaper, research paper, or PDF:")
    source_type = st.selectbox("Select the type of content", ["Article", "Newspaper", "Research Paper", "PDF"])
    
    if st.button('Process'):
        if url:
            if source_type == "Article":
                process_article(url)
            elif source_type == "Newspaper":
                process_newspaper(url)
            elif source_type == "Research Paper" and url.lower().endswith(".pdf"):
                process_research_paper(url)
            elif source_type == "PDF" and url.lower().endswith(".pdf"):
                process_pdf(url)
            else:
                st.warning("Please provide a valid URL and select the appropriate type of content.")
        else:
            st.warning("Please enter a URL.")

def process_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        
        st.subheader("Article Details")
        st.write("*Title:*", article.title)
        st.write("*Authors:*", article.authors)
        st.write("*Publish Date:*", article.publish_date)
        if article.top_image:
            st.image(article.top_image, caption="Top Image", use_column_width=True)
        st.write("*Article Text:*", article.text)
        st.write("*Article Summary:*", article.summary)
    except Exception as e:
        st.error(f"An error occurred while processing the article: {e}")

def process_newspaper(url):
    try:
        process_article(url)  # Newspapers are processed similarly to articles
    except Exception as e:
        st.error(f"An error occurred while processing the newspaper: {e}")

def process_research_paper(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Open the PDF
        pdf_file = fitz.open(stream=response.content, filetype="pdf")
        text = ""
        
        # Extract text from each page
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
        
        if text.strip() == "":
            st.warning("No text found in the research paper.")
        else:
            st.subheader("Research Paper Details")
            st.write("*Text from Research Paper:*", text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the PDF: {e}")
    except fitz.FitzError as e:
        st.error(f"An error occurred while processing the PDF: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def process_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Open the PDF
        pdf_file = fitz.open(stream=response.content, filetype="pdf")
        text = ""
        
        # Extract text from each page
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
        
        if text.strip() == "":
            st.warning("No text found in the PDF.")
        else:
            st.subheader("PDF Document Details")
            st.write("*Text from PDF:*", text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the PDF: {e}")
    except fitz.FitzError as e:
        st.error(f"An error occurred while processing the PDF: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Main logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['show_login'] = True

if st.session_state['show_login']:
    login_page()
else:
    main_page()
