import streamlit as st
from recommender_with_gpt import recommend_projects

st.set_page_config(page_title="ProjectPal AI", page_icon="🎮", layout="centered")

st.title("🎮 ProjectPal – AI-Powered Project Idea Recommender")
st.write("Get 3 personalized project ideas based on your skills, time, domain, and difficulty level!")

# Input section
skills_input = st.text_input("🛠 Enter your skills (comma-separated)", "Python, NLP")
days_input = st.slider("⏱ How many days do you have?", 1, 30, 5)

domain_input = st.selectbox("🌐 Choose your domain", [
    "AI/ML", "Web", "Mobile", "Game Dev", "Design",
    "Business", "Data Analytics", "Cybersecurity",
    "IoT", "Media", "Software", "Database", "Open"
])

difficulty_input = st.selectbox("🎚️ Choose Difficulty", ["Any", "Beginner", "Intermediate", "Advanced"])

# Suggest button
if st.button("Suggest Projects"):
    skills = [s.strip().lower() for s in skills_input.split(",")]
    results = recommend_projects(
        skills=skills,
        days=days_input,
        domain=domain_input,
        difficulty=difficulty_input,
        use_gpt=True  # GPT fallback enabled
    )

    # Display results
    if isinstance(results[0], str) and ("Title" in results[0] or results[0].startswith("1.")):
        st.markdown("### 🤖 GPT Suggestions")
        st.markdown(results[0])
    elif isinstance(results[0], str):
        st.warning(results[0])
    else:
        for i, proj in enumerate(results, 1):
            st.subheader(f"{i}. {proj['title']}")
            st.markdown(f"🛠 **Tools:** {', '.join(proj['tools'])}")
            st.markdown(f"🎯 **Difficulty:** {proj.get('difficulty', 'Intermediate')}")
            st.markdown(f"📄 {proj['description']}")
