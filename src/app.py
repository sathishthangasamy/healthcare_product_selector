import streamlit as st
import pandas as pd
from utils import load_plan_type_definitions, load_dummy_insurance_plans, get_plan_type_details, filter_and_rank_plans

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Healthcare Plan Selector (Prototype)")

# --- Load Dummy Data ---
df_plan_types = load_plan_type_definitions()
df_dummy_plans = load_dummy_insurance_plans()

# --- Title and Disclaimers ---
st.title("⚕️ Healthcare Plan & Provider Selector (Prototype)")
st.markdown("""
Welcome to the Healthcare Plan & Provider Selector! This **prototype** aims to illustrate how you could choose
between different health insurance plan types (HMO, PPO, POS, EPO) and compare hypothetical providers
based on your needs.

**CRITICAL DISCLAIMER:**
* **ALL DATA IS DUMMY AND HYPOTHETICAL.** This app does NOT use real insurance plan data, premiums, or provider networks.
    Real plan details are proprietary, constantly change, and vary by location and personal factors.
* **NOT HIPAA COMPLIANT.** This prototype is for demonstration only and does NOT handle any Protected Health Information (PHI).
    A production application would require a robust, secure, and HIPAA-compliant backend infrastructure.
* **NOT FINANCIAL OR MEDICAL ADVICE.** Always consult with a licensed insurance agent or financial advisor for insurance decisions, and a healthcare professional for medical advice.
""")

st.subheader("1. Understand Plan Types")

selected_plan_type_overview = st.selectbox(
    "Select a Plan Type to learn more:",
    [""] + list(df_plan_types['PlanType'].unique())
)

if selected_plan_type_overview:
    details = get_plan_type_details(df_plan_types, selected_plan_type_overview)
    if details is not None:
        st.markdown(f"**{details['PlanType']}**: {details['ShortDescription']}")
        st.markdown(f"- **Key Features:** {details['KeyFeatures']}")
        st.markdown(f"- **Considerations:** {details['Considerations']}")
        st.markdown("---")

st.subheader("2. Tell us about your priorities (Hypothetical)")

col1, col2 = st.columns(2)

with col1:
    user_preferred_plan_type = st.selectbox(
        "Which plan type are you considering?",
        ["Any"] + list(df_plan_types['PlanType'].unique()),
        help="Choose a specific type or 'Any' for broad suggestions."
    )
    user_conditions_input = st.text_input(
        "Do you have any specific health conditions? (e.g., 'diabetes', 'allergies')",
        help="This helps us hypothetically filter suitable plans. (Dummy data only)."
    )

with col2:
    user_priorities = st.multiselect(
        "What are your top priorities?",
        [
            "Low Monthly Premium",
            "Low Deductible",
            "Max Flexibility (out-of-network options)",
            "Easy Specialist Access (no referrals)",
            "Broad Network of Doctors"
        ],
        help="Select factors important to you."
    )

st.subheader("3. Hypothetical Plan Recommendations & Provider Comparison")

if st.button("Find Hypothetical Plans"):
    if not df_dummy_plans.empty:
        recommended_plans = filter_and_rank_plans(
            df_dummy_plans,
            user_preferred_plan_type,
            user_priorities,
            user_conditions_input
        )

        if not recommended_plans.empty:
            st.write(f"Based on your inputs, here are some **hypothetical** plans that might fit:")

            # Display top 5 hypothetical plans
            for index, row in recommended_plans.head(5).iterrows():
                with st.expander(f"**{row['PlanName']}** by {row['Provider']} ({row['PlanType']})"):
                    st.markdown(f"**Monthly Premium:** ${row['MonthlyPremium']}")
                    st.markdown(f"**Deductible:** ${row['Deductible']}")
                    st.markdown(f"**Out-of-Pocket Max:** ${row['OOP_Max']}")
                    st.markdown(f"**Network Size:** {row['NetworkSize']}")
                    st.markdown(f"**Flexibility (1-10):** {row['FlexibilityScore']}")
                    st.markdown(f"**Specialist Access:** {row['SpecialistAccess']}")
                    st.markdown(f"**Referral Needed:** {'Yes' if row['ReferralNeeded'] else 'No'}")
                    st.markdown(f"**Good For:** {row['GoodForConditions']}")
                    st.markdown(f"**Notes:** {row['Notes']}")
                    st.caption("*(Remember, these are dummy figures. Actual plans vary significantly.)*")
                    st.write("---")

            st.markdown("### Hypothetical Providers Offering Plans")
            # Show a list of providers from the filtered plans
            st.write("Hypothetical providers with plans matching your criteria:")
            st.write(recommended_plans['Provider'].unique())
            st.info("*(In a real app, you'd click a provider to see their real plans or be directed to their site.)*")

        else:
            st.warning("No hypothetical plans found matching your criteria. Try adjusting your inputs.")
    else:
        st.error("Dummy insurance plan data not loaded. Check 'data/dummy_insurance_plans.csv'.")

st.markdown("---")
st.markdown("### Next Steps (For a Real Application):")
st.markdown("""
* **Actual Data Integration:** Securely connect to real insurance plan databases and APIs (a major, complex undertaking).
* **Advanced Matching:** Implement sophisticated algorithms for precise plan matching based on detailed user profiles and robust plan data.
* **HIPAA Compliance:** Design and deploy on a HIPAA-compliant infrastructure with strict data security measures.
* **Licensing:** Ensure all necessary insurance licensing is in place for providing real advice.
""")

st.caption("This application is for informational purposes only and does not constitute financial, insurance, or medical advice. Consult with licensed professionals.")
