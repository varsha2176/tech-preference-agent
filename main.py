# main.py
import requests

def get_github_data(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    data = response.json()
    
    repos = []
    for repo in data:
        repos.append({
            "name": repo['name'],
            "description": repo['description'],
            "language": repo['language']
        })
    return repos

def extract_text_from_github(repos):
    texts = []
    for repo in repos:
        if repo['description']:
            texts.append(repo['description'])
        if repo['language']:
            texts.append(repo['language'])
    return " ".join(texts)

def get_preferences(text):
    keywords = {
        'AI/ML': ['machine learning', 'deep learning', 'tensorflow', 'pytorch'],
        'Web Development': ['react', 'angular', 'javascript', 'html', 'css'],
        'Data Science': ['pandas', 'numpy', 'matplotlib', 'jupyter'],
        'Cloud': ['aws', 'gcp', 'azure', 'docker', 'kubernetes'],
        'Mobile Dev': ['flutter', 'android', 'swift']
    }
    
    preferences = []
    for area, words in keywords.items():
        for word in words:
            if word.lower() in text.lower():
                preferences.append(area)
                break
    return preferences

# ------- Run the Program -------
username = input("Enter GitHub username: ")
repos = get_github_data(username)
github_text = extract_text_from_github(repos)
prefs = get_preferences(github_text)

print("\n🔍 Technical Preferences found:")
for p in prefs:
    print(f"✅ {p}")
