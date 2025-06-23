import streamlit as st
import requests
import PyPDF2
import os

# -------- GitHub Analyzer -------- #
def get_github_data(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {st.secrets['GITHUB_TOKEN']}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    repos = response.json()
    repo_data = []
    for repo in repos:
        if isinstance(repo, dict):
            repo_data.append({
                "name": repo.get('name', ''),
                "description": repo.get('description', ''),
                "topics": repo.get('topics', []),
                "language": repo.get('language', '')
            })
    return repo_data

def extract_github_preferences(repos):
    preferences = set()
    for repo in repos:
        description = repo.get('description', '') or ''
        topics = repo.get('topics', [])
        language = repo.get('language', '')

        if 'machine' in description.lower() or 'ml' in description.lower():
            preferences.add("AI/ML")
        if 'web' in description.lower() or 'html' in description.lower():
            preferences.add("Web Development")
        if 'data' in description.lower():
            preferences.add("Data Science")
        if language:
            preferences.add(language)

        for topic in topics:
            if topic.lower() in ['ai', 'ml', 'nlp']:
                preferences.add("AI/ML")
            elif topic.lower() in ['web', 'html', 'css', 'javascript']:
                preferences.add("Web Development")
            elif topic.lower() in ['data-science', 'analytics']:
                preferences.add("Data Science")

    return list(preferences)

# -------- LinkedIn Analyzer -------- #
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_linkedin_preferences(text):
    preferences = set()
    text_lower = text.lower()

    if 'machine learning' in text_lower or 'deep learning' in text_lower:
        preferences.add("AI/ML")
    if 'web development' in text_lower or 'html' in text_lower or 'css' in text_lower:
        preferences.add("Web Development")
    if 'data science' in text_lower or 'data analyst' in text_lower:
        preferences.add("Data Science")
    if 'cloud' in text_lower:
        preferences.add("Cloud Computing")
    if 'devops' in text_lower:
        preferences.add("DevOps")
    if 'android' in text_lower or 'ios' in text_lower:
        preferences.add("Mobile Development")

    return list(preferences)

# -------- UI -------- #
st.title("Technical Preference Detector (GitHub + LinkedIn PDF)")

# GitHub input
st.subheader("GitHub Profile")
github_username = st.text_input("Enter GitHub Username")

# LinkedIn PDF input
st.subheader("LinkedIn Profile PDF")
pdf_folder = "linkedin_pdfs"
os.makedirs(pdf_folder, exist_ok=True)

existing_pdfs = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
selected_pdf = st.selectbox("Select a LinkedIn PDF", options=["None"] + existing_pdfs)

st.markdown("⬇Or upload a new LinkedIn profile:")
uploaded_pdf = st.file_uploader("Upload a LinkedIn PDF", type="pdf")

linkedin_prefs = []
github_prefs = []

if st.button("Detect Preferences"):
    # GitHub
    if github_username:
        st.info("Fetching GitHub data...")
        repos = get_github_data(github_username.strip())
        if repos:
            github_prefs = extract_github_preferences(repos)
            st.success("GitHub data loaded.")
        else:
            st.warning("Could not fetch GitHub repos. Check username or API limit.")

    # LinkedIn
    if selected_pdf != "None":
        st.info(f"Analyzing LinkedIn file: {selected_pdf}")
        with open(os.path.join(pdf_folder, selected_pdf), "rb") as f:
            text = extract_text_from_pdf(f)
            linkedin_prefs = extract_linkedin_preferences(text)
            st.success(f"PDF '{selected_pdf}' loaded.")
    elif uploaded_pdf:
        filepath = os.path.join(pdf_folder, uploaded_pdf.name)
        with open(filepath, "wb") as f:
            f.write(uploaded_pdf.read())
        text = extract_text_from_pdf(open(filepath, "rb"))
        linkedin_prefs = extract_linkedin_preferences(text)
        st.success(f"PDF '{uploaded_pdf.name}' uploaded and loaded.")
    else:
        st.warning("No LinkedIn profile selected or uploaded.")

    # Output
    if github_prefs:
        st.subheader("GitHub Preferences:")
        for p in set(github_prefs):
            st.markdown(f"- **{p}**")

    if linkedin_prefs:
        st.subheader("LinkedIn Preferences:")
        for p in set(linkedin_prefs):
            st.markdown(f"- **{p}**")

    if not github_prefs and not linkedin_prefs:
        st.warning("No preferences detected.")
