import pandas as pd
import streamlit as st

@st.cache_data # Cache data loading for performance
def load_plan_type_definitions():
    """Loads dummy health insurance plan type definitions."""
    try:
        df = pd.read_csv("data/plan_type_definitions.csv")
        return df
    except FileNotFoundError:
        st.error("Error: 'data/plan_type_definitions.csv' not found. Please create it.")
        return pd.DataFrame()

@st.cache_data # Cache data loading for performance
def load_dummy_insurance_plans():
    """Loads dummy health insurance plan data."""
    try:
        df = pd.read_csv("data/dummy_insurance_plans.csv")
        return df
    except FileNotFoundError:
        st.error("Error: 'data/dummy_insurance_plans.csv' not found. Please create it.")
        return pd.DataFrame()

def get_plan_type_details(df_definitions, plan_type):
    """Retrieves details for a specific plan type."""
    details = df_definitions[df_definitions['PlanType'] == plan_type]
    if not details.empty:
        return details.iloc[0]
    return None

def filter_and_rank_plans(df_plans, preferred_type, priorities, user_conditions):
    """
    Filters and ranks dummy plans based on user preferences.
    This is a highly simplified, illustrative function.
    """
    filtered_df = df_plans.copy()

    # 1. Filter by Preferred Plan Type
    if preferred_type and preferred_type != "Any":
        filtered_df = filtered_df[filtered_df['PlanType'] == preferred_type]

    # 2. Basic Filtering by Hypothetical "GoodForConditions"
    if user_conditions:
        # This is a very crude string match. Real logic would be complex.
        condition_keywords = [c.strip().lower() for c in user_conditions.split(',')]
        filtered_df = filtered_df[
            filtered_df['GoodForConditions'].apply(lambda x: any(kw in x.lower() for kw in condition_keywords))
        ]

    # 3. Simple Ranking based on Priorities (Illustrative)
    if not filtered_df.empty and priorities:
        # Assign scores based on priorities
        filtered_df['Score'] = 0
        if 'Low Monthly Premium' in priorities:
            filtered_df['Score'] += (1000 - filtered_df['MonthlyPremium']) / 100 # Lower premium, higher score
        if 'Low Deductible' in priorities:
            filtered_df['Score'] += (5000 - filtered_df['Deductible']) / 500 # Lower deductible, higher score
        if 'Max Flexibility' in priorities:
            filtered_df['Score'] += filtered_df['FlexibilityScore'] * 10
        if 'Easy Specialist Access' in priorities:
            filtered_df['Score'] += 10 # PPO/EPO generally get a bonus
        if 'Broad Network' in priorities:
            filtered_df['Score'] += 5 # PPO/EPO generally get a bonus for larger network

        filtered_df = filtered_df.sort_values(by='Score', ascending=False)

    return filtered_df