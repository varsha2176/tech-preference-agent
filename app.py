import streamlit as st
import requests
import PyPDF2
import os
from collections import Counter

# ----- Streamlit UI -----
st.set_page_config(page_title="Technical Preference Detector (GitHub + LinkedIn)", layout="centered")

st.title("Technical Preference Detector (GitHub + LinkedIn PDF)")

# GitHub input
st.header("GitHub Profile")
github_username = st.text_input("Enter GitHub Username")

# LinkedIn input
st.header("LinkedIn Profile PDF")
uploaded_file = st.file_uploader("Upload a LinkedIn PDF", type=["pdf"], help="Limit 200MB per file • PDF")

# ----- GitHub Preference Detection -----
def analyze_github(username):
    github_url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(github_url)
        if response.status_code != 200:
            return None, "Could not fetch GitHub repos. Check username or API limit."
        repos = response.json()
        lang_counter = Counter()
        for repo in repos:
            lang_url = repo.get("languages_url")
            lang_resp = requests.get(lang_url)
            if lang_resp.status_code == 200:
                lang_data = lang_resp.json()
                lang_counter.update(lang_data)
        return lang_counter, None
    except Exception as e:
        return None, str(e)

# ----- LinkedIn PDF Parsing -----
def analyze_linkedin(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        keywords = ['Data Science', 'Web Development', 'Cloud Computing', 'Cybersecurity', 'AI', 'Machine Learning', 'DevOps', 'Mobile Development', 'AR/VR', 'Blockchain']
        found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
        return found_keywords
    except Exception as e:
        return [f"Error reading PDF: {str(e)}"]

# ----- Results -----
if github_username or uploaded_file:
    if github_username:
        st.subheader("Fetching GitHub data...")
        github_prefs, error = analyze_github(github_username)
        if error:
            st.error(error)
        elif github_prefs:
            st.subheader("GitHub Preferences:")
            sorted_langs = github_prefs.most_common()
            for lang, count in sorted_langs:
                st.write(f"{lang}: {count} bytes")
            st.bar_chart(dict(sorted_langs))

    if uploaded_file:
        st.subheader(f"Analyzing LinkedIn file: {uploaded_file.name}")
        linkedin_prefs = analyze_linkedin(uploaded_file)
        st.subheader("LinkedIn Preferences:")
        if linkedin_prefs:
            for kw in linkedin_prefs:
                st.write(kw)
        else:
            st.info("No relevant tech keywords found in the PDF.")
