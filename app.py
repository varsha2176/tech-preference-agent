import streamlit as st
import requests
import os

st.set_page_config(page_title="Tech Preference Analyzer", layout="centered")

st.title("🧠 Tech Preference Analyzer")
st.write("Analyze a user's tech preference based on their public GitHub repositories.")

# Input GitHub username
username = st.text_input("Enter GitHub username")

# Fetch token securely
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# When user submits
if st.button("Analyze") and username:
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        if not repos:
            st.info("No public repositories found for this user.")
        else:
            lang_count = {}
            for repo in repos:
                lang_url = repo.get("languages_url")
                if lang_url:
                    lang_resp = requests.get(lang_url, headers=headers)
                    if lang_resp.status_code == 200:
                        langs = lang_resp.json()
                        for lang in langs:
                            lang_count[lang] = lang_count.get(lang, 0) + langs[lang]

            if lang_count:
                sorted_langs = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)
                st.subheader("Preferred Technologies:")
                for lang, bytes_count in sorted_langs:
                    st.write(f"**{lang}**: {bytes_count} bytes")

                st.bar_chart({lang: bytes for lang, bytes in sorted_langs})
            else:
                st.warning("No language data found in the repositories.")
    else:
        st.error("Failed to fetch repositories. Check the username or API limit.")
