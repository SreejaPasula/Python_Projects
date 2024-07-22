import streamlit as st
import bcrypt
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# User credentials (for demonstration purposes, replace with a proper database in production)
username = "user"
password = "password"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def login(username_input, password_input):
    if username_input == username and bcrypt.checkpw(password_input.encode('utf-8'), hashed_password):
        return True
    return False

def predict(article):
    # Perform NER on the article text
    doc = nlp(article)

    # Extract all entities, concepts, and topics from the text
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    concepts = [(token.text, token.pos_) for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ"]]
    topics = [(token.text, token.dep_) for token in doc if token.dep_ in ["nsubj", "dobj", "iobj"]]

    # Check for red flags in the article's content
    red_flags = ["!", "?", "...", "Click here to learn more!"]
    for flag in red_flags:
        if flag in article:
            return "Unreliable"

    # Use sentiment analysis to check for sensational language
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(article)
    if sentiment['compound'] > 0.5:
        return "Unreliable"

    # Temporarily bypass the domain check to test other parts
    # try:
    #     response = requests.get("https://api.example.com/domain")
    #     response.raise_for_status()
    #     domain = response.text
    #     if domain not in ["nytimes.com", "washingtonpost.com", "bbc.com"]:
    #         return "Unreliable"
    # except requests.ConnectionError:
    #     return "Error: Unable to connect to the domain API"
    # except requests.RequestException as e:
    #     return f"Error: {e}"

    # If none of the above checks fail, mark the article as "Reliable"
    return "Reliable"

def fetch_related_info(article):
    # Generate a mock response based on the user's input
    query = " ".join(word_tokenize(article)[:10])  # Use the first 10 words for the query
    
    # Mock data for reliable information
    reliable_info = {
        "weather": [
            "Reliable Info 1: Recent studies on climate change show the impact on weather patterns.",
            "Reliable Info 2: Weather manipulation technologies are heavily regulated by international agreements."
        ],
        "government": [
            "Reliable Info 1: Government operations are subject to strict oversight and public accountability.",
            "Reliable Info 2: Recent policies aimed at transparency and integrity in government practices."
        ],
        "conspiracy": [
            "Reliable Info 1: Information on the effectiveness of whistleblower protection laws.",
            "Reliable Info 2: How investigative journalism upholds the truth in high-profile cases."
        ]
    }
    
    # Determine the relevant reliable information based on the query
    for key in reliable_info:
        if key in query.lower():
            return reliable_info[key]
    
    # Default reliable information if no relevant information is found
    return [
        "Reliable Info: Fact-checking is a crucial part of maintaining the integrity of information."
    ]

def main():
    st.title("Credibility Checker")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("Login")
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username_input, password_input):
                st.session_state.logged_in = True
                st.success("Logged in successfully")
            else:
                st.error("Invalid credentials")
    else:
        st.subheader("Article Credibility Checker")
        article = st.text_area("Enter the article text")
        if st.button("Check Credibility"):
            if article:
                result = predict(article)
                st.write(f"The article is: *{result}*")
                if result == "Unreliable":
                    st.subheader("Related Reliable Information")
                    related_info = fetch_related_info(article)
                    if related_info:
                        for info in related_info:
                            st.write(info)
                    else:
                        st.write("No related information found.")
            else:
                st.error("Please enter the article text")

        if st.button("Logout"):
            st.session_state.logged_in = False

if _name_ == "_main_":
    main()
