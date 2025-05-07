import streamlit as st
import random
import time
import os
import requests

# Mock Grok API (replace with real API calls in production)
def analyze_material(material):
    categories = ["agents", "processes", "problems"]
    category = random.choice(categories)
    return {"category": category, "details": f"This material is related to {category}."}

def simulate_discussion(agents, scenario):
    discussion = ""
    for agent in agents:
        discussion += f"{agent}: Based on my profile, I think we should evaluate risks and opportunities.\n"
    discussion += "Final Recommendation: Proceed with caution."
    return discussion

# Real Grok API integration (uncomment and configure in production)
# def analyze_material(material):
#     api_key = os.getenv("XAI_API_KEY")
#     response = requests.post(
#         "https://api.xai.com/grok/analyze",  # Hypothetical endpoint
#         headers={"Authorization": f"Bearer {api_key}"},
#         json={"text": material}
#     )
#     return response.json()

# Predefined agents
agents = {
    "CEO": {"role": "Chief Executive Officer", "risk_tolerance": "Moderate", "description": "Focuses on strategy and growth."},
    "CFO": {"role": "Chief Financial Officer", "risk_tolerance": "Low", "description": "Prioritizes financial stability."},
    "CMO": {"role": "Chief Marketing Officer", "risk_tolerance": "High", "description": "Drives bold marketing initiatives."},
    "COO": {"role": "Chief Operations Officer", "risk_tolerance": "Moderate", "description": "Ensures operational efficiency."}
}

# Predefined cases
predefined_cases = {
    "New Product Investment": {
        "scenario": "Should we invest in a new product line?",
        "agents": ["CEO", "CFO", "CMO"],
        "materials": {"Market research report": {"category": "problems", "details": "Indicates market demand."},
                      "Financial projections": {"category": "processes", "details": "Shows ROI potential."}},
        "discussion": """
**CEO**: Investing could make us market leaders, but it must fit our strategy.  
**CFO**: Projections are solid, but upfront costs are a concern.  
**CMO**: This could skyrocket our brand if marketed well.  
**Analysis**: CFO’s caution balances CMO’s optimism.  
**Recommendation**: Pilot the product first.
""",
        "recommendation": "Pilot the product first."
    },
    "Market Expansion": {
        "scenario": "Should we expand to a new market?",
        "agents": ["CEO", "CMO", "COO"],
        "materials": {"Competitor analysis": {"category": "problems", "details": "Shows competitive landscape."},
                      "Logistics plan": {"category": "processes", "details": "Outlines supply chain needs."}},
        "discussion": """
**CEO**: Expansion diversifies revenue but requires careful planning.  
**CMO**: A strong campaign can establish our presence fast.  
**COO**: Logistics must be flawless to succeed.  
**Analysis**: COO’s focus on operations complements CMO’s vision.  
**Recommendation**: Start with a feasibility study.
""",
        "recommendation": "Start with a feasibility study."
    }
}

# Session state initialization
if 'current_case' not in st.session_state:
    st.session_state.current_case = None

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["Home", "Problem Structuring", "Simulation", "Analysis"])

# Home Page
if page == "Home":
    st.title("DecisionTwin")
    st.markdown("Simulate and optimize organizational decisions with AI.")

    st.subheader("Previous Cases")
    for case_name in predefined_cases.keys():
        if st.button(case_name):
            st.session_state.current_case = predefined_cases[case_name]
            st.success(f"Loaded: {case_name}")

    st.subheader("New Case")
    with st.form("new_case_form"):
        case_name = st.text_input("Case Name")
        case_description = st.text_area("Case Description")
        materials = st.text_area("Materials (comma-separated)")
        submitted = st.form_submit_button("Create Case")
        if submitted:
            materials_list = [m.strip() for m in materials.split(",") if m.strip()]
            analyzed_materials = {m: analyze_material(m) for m in materials_list}
            st.session_state.current_case = {
                "name": case_name,
                "description": case_description,
                "materials": analyzed_materials,
                "agents": list(agents.keys()),
                "scenario": case_description
            }
            st.success("Case created!")

# Problem Structuring Page
elif page == "Problem Structuring":
    if st.session_state.current_case:
        case = st.session_state.current_case
        st.title(case["name"])
        st.write(case["description"])

        with st.expander("Agents"):
            for agent_name in case["agents"]:
                agent = agents[agent_name]
                st.write(f"**{agent_name}** - {agent['role']}")
                st.write(f"Risk Tolerance: {agent['risk_tolerance']}")
                st.write(agent['description'])

        with st.expander("Materials"):
            for material, analysis in case["materials"].items():
                st.write(f"**{material}**: {analysis['category']} - {analysis['details']}")

        st.subheader("Adjust Parameters")
        st.write("Future versions will allow parameter tuning here.")
    else:
        st.warning("Select or create a case first.")

# Simulation Page
elif page == "Simulation":
    if st.session_state.current_case:
        case = st.session_state.current_case
        st.title("Simulation")

        if st.button("Start Simulation"):
            with st.spinner("Simulating..."):
                if "discussion" in case:
                    discussion = case["discussion"]
                else:
                    discussion = simulate_discussion(case["agents"], case["scenario"])
                st.session_state.current_case["discussion"] = discussion
                st.session_state.current_case["recommendation"] = "Proceed with caution" if "recommendation" not in case else case["recommendation"]

            st.subheader("Discussion Transcript")
            for line in discussion.split("\n"):
                if line.strip():
                    st.write(line)
                    time.sleep(1)
    else:
        st.warning("Select or create a case first.")

# Analysis Page
elif page == "Analysis":
    if st.session_state.current_case and "discussion" in st.session_state.current_case:
        case = st.session_state.current_case
        st.title("Analysis")

        st.subheader("Recommendation")
        st.write(case["recommendation"])

        st.subheader("Insights")
        st.write("Full version will include bias detection, KPIs, and more.")

        st.subheader("Feedback")
        rating = st.slider("Rate simulation accuracy", 1, 5)
        if st.button("Submit Feedback"):
            st.success("Feedback submitted!")
    else:
        st.warning("Run a simulation first.")