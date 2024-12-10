import streamlit as st
import requests
from newspaper import Article
import fitz  # PyMuPDF

# Define login credentials
USERNAME = ["user","anirudh","shiva","vamshi","sreeja"]
PASSWORD = ["password","anirudh","shiva","vamshi","sreeja"]
# Streamlit app
def login_page():
    st.title('Login')
    
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        if username in USERNAME and password in PASSWORD:
            if USERNAME.index(username)==PASSWORD.index(password): 
                st.session_state['logged_in'] = True
                st.session_state['show_login'] = False
        else:
            st.error('Incorrect username or password')

def main_page():
    st.title('Credibility Check for Articles, Newspapers, Research Papers, and PDFs')
    
    input_type = st.radio("Select the input type", ["URL", "Text"])
    
    if input_type == "URL":
        url = st.text_input("Enter the URL of the article, newspaper, research paper, or PDF:")
        source_type = st.selectbox("Select the type of content", ["Article", "Newspaper", "Research Paper", "PDF"])
        
        if st.button('Process URL'):
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
    
    elif input_type == "Text":
        text = st.text_area("Paste the text of the article here:")
        
        if st.button('Process Text'):
            if text:
                # Check credibility of the pasted text
                credibility = check_text_credibility(text)
                st.subheader("Text Details")
                st.write("Text:", text)
                st.write("Credibility:", credibility)
            else:
                st.warning("Please paste the text of the article.")

def process_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        st.subheader("Article Details")
        st.write("Title:", article.title)
        st.write("Authors:", article.authors)
        st.write("Publish Date:", article.publish_date)
        if article.top_image:
            st.image(article.top_image, caption="Top Image", use_column_width=True)
        st.write("Article Text:", article.text)
        
        # Check credibility
        credibility = check_credibility(article)
        st.write("Credibility:", credibility)
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
            st.write("Text from Research Paper:", text)
            
            # Check credibility
            credibility = check_research_paper_credibility(text)
            st.write("Credibility:", credibility)
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
            st.write("Text from PDF:", text)
            
            # Check credibility
            credibility = check_pdf_credibility(text)
            st.write("Credibility:", credibility)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the PDF: {e}")
    except fitz.FitzError as e:
        st.error(f"An error occurred while processing the PDF: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Credibility checking functions
def check_credibility(article):
    # Basic heuristics to determine credibility
    if article.publish_date and article.authors:
        return "Reliable"
    return "Unreliable"

def check_research_paper_credibility(text):
    # Simple example: check for the presence of keywords or structure
    if "abstract" in text.lower() and "introduction" in text.lower():
        return "Reliable"
    return "Unreliable"

def check_pdf_credibility(text):
    # Simple example: check for presence of metadata or keywords
    if "introduction" in text.lower() or "conclusion" in text.lower():
        return "Reliable"
    return "Unreliable"

def check_text_credibility(text):
    # Basic credibility check based on text content
    if "author" in text.lower() or "source" in text.lower():
        return "Reliable"
    return "Unreliable"

# Main logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['show_login'] = True

if st.session_state['show_login']:
    login_page()
else:
    main_page()
