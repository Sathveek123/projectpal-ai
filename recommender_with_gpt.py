
import json
import openai
import os

# Load local project database
def load_project_db():
    try:
        with open("project_db.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Main recommendation function with difficulty and GPT fallback
def recommend_projects(skills, days, domain=None, difficulty=None, use_gpt=False):
    db = load_project_db()
    matches = []

    for proj in db:
        proj_skills = [s.lower() for s in proj.get('skills', [])]
        proj_domain = proj.get('domain', '').lower()
        proj_diff = proj.get('difficulty', 'Intermediate').lower()

        if proj.get('duration', 999) > days:
            continue
        if domain and domain.lower() != "open" and proj_domain != domain.lower():
            continue
        if difficulty and difficulty.lower() != "any" and proj_diff != difficulty.lower():
            continue
        if any(skill.lower() in proj_skills for skill in skills):
            matches.append(proj)

    if matches:
        return matches[:3]

    # GPT fallback using OpenAI >=1.0.0 API
    if use_gpt:
        try:
            client = openai.OpenAI(api_key=os.getenv("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"))

            prompt = (
                f"Suggest 3 unique project ideas for a student with skills in {', '.join(skills)}, "
                f"who has {days} days and is interested in {domain}. "
                f"Each idea should include: Title, Tools, Difficulty, and a 2-line Description."
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )

            return [response.choices[0].message.content.strip()]
        except Exception as e:
            return [f"❌ GPT Fallback failed: {str(e)}"]

    return ["No matching projects found."]
