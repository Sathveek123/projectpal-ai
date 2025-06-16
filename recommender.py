import json

# Load the database
def load_project_db():
    with open("project_db.json", "r") as file:
        return json.load(file)

# Main project recommendation logic
def recommend_projects(skills, days, domain=None):
    db = load_project_db()
    matches = []

    for proj in db:
        print(f"\n🔍 Checking: {proj['title']}")
        print(f"Skills Required: {proj['skills']} | Duration: {proj['duration']} | Domain: {proj['domain']}")

        # 1. Check duration
        if proj['duration'] > days:
            print("❌ Skipped: duration too long.")
            continue

        # 2. Check domain (if not 'Open')
        if domain.lower() != "open" and proj['domain'].lower() != domain.lower():
            print("❌ Skipped: domain mismatch.")
            continue

        # 3. Check for skill match (case-insensitive)
        proj_skills = [s.lower() for s in proj['skills']]
        if any(skill.lower() in proj_skills for skill in skills):
            print("✅ Match found!")
            matches.append(proj)
        else:
            print("❌ Skipped: no skill match.")

    print(f"\n✅ Total matches: {len(matches)}")
    return matches[:3] if matches else ["No matching projects found."]
