import streamlit as st
import pandas as pd

# --- Dummy Data (This would come from a secure, HIPAA-compliant database in a real app) ---
products_data = {
    "product_id": ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008"],
    "name": [
        "Pain Relief (Generic Ibuprofen)", "Allergy Relief (Loratadine)",
        "Blood Pressure Monitor", "Glucose Meter Kit",
        "Vitamin D Supplement", "Multivitamin (Adult)",
        "Antacid Tablets", "First Aid Kit (Basic)"
    ],
    "category": [
        "OTC Medication", "OTC Medication", "Medical Device", "Medical Device",
        "Supplement", "Supplement", "OTC Medication", "General Health"
    ],
    "suitable_for_conditions": [
        "Pain, Fever, Inflammation", "Allergies, Hay Fever",
        "High Blood Pressure", "Diabetes",
        "Vitamin D Deficiency", "General Wellness",
        "Heartburn, Indigestion", "Minor Cuts, Scrapes"
    ],
    "general_price_range": [
        "$5 - $15", "$10 - $25", "$30 - $60", "$40 - $80",
        "$8 - $20", "$15 - $30", "$6 - $18", "$12 - $30"
    ],
    "description": [
        "Common non-steroidal anti-inflammatory drug (NSAID) for pain and fever.",
        "Non-drowsy antihistamine for 24-hour allergy symptom relief.",
        "Digital monitor for home use to track blood pressure readings.",
        "Kit includes meter, test strips, lancets for blood glucose monitoring.",
        "Essential vitamin for bone health and immune support.",
        "Comprehensive blend of vitamins and minerals for daily nutritional needs.",
        "Chewable tablets for fast relief from stomach acid.",
        "Essential supplies for treating minor injuries at home."
    ]
}
df_products = pd.DataFrame(products_data)

# --- Streamlit App Layout ---

st.set_page_config(layout="wide", page_title="Healthcare Product Selector (Prototype)")

st.title("💡 Healthcare Product Selector (Prototype)")
st.markdown("""
Welcome to the Healthcare Product Selector! This is a **prototype** to demonstrate how an app can help
U.S. residents find suitable healthcare products based on their needs.

**Important Note:** This prototype uses **dummy data** and **does not handle any real Protected Health Information (PHI)**.
For a production application involving real patient data, strict HIPAA compliance and secure infrastructure are mandatory.
Always consult a healthcare professional for medical advice.
""")

st.subheader("Tell us about your needs (Dummy Input)")

# User inputs (simplified for prototype)
col1, col2, col3 = st.columns(3)

with col1:
    user_symptom = st.text_input("What symptoms are you experiencing (e.g., 'pain', 'allergies')?")
    user_age_group = st.selectbox("Your Age Group", ["", "Child", "Adult", "Senior"])

with col2:
    user_condition = st.text_input("Do you have a specific health condition (e.g., 'diabetes', 'high blood pressure')?")
    product_category = st.selectbox("Preferred Product Category", ["", "All", "OTC Medication", "Medical Device", "Supplement", "General Health"])

with col3:
    st.write("*(No PHI collected here)*")
    # Placeholder for future "insurance info" input
    # insurance_type = st.selectbox("Your Insurance Type (e.g., 'PPO', 'HMO')", ["N/A", "PPO", "HMO"])

st.markdown("---")

# --- Product Recommendation Logic (Simplified) ---

st.subheader("Suggested Products")

# Filter products based on user input
filtered_products = df_products.copy()

if user_symptom:
    filtered_products = filtered_products[
        filtered_products["suitable_for_conditions"].str.contains(user_symptom, case=False, na=False) |
        filtered_products["description"].str.contains(user_symptom, case=False, na=False)
    ]

if user_condition:
    filtered_products = filtered_products[
        filtered_products["suitable_for_conditions"].str.contains(user_condition, case=False, na=False)
    ]

if product_category and product_category != "All":
    filtered_products = filtered_products[
        filtered_products["category"] == product_category
    ]

if user_age_group:
    # Very basic age group filtering, would be much more complex in reality
    if user_age_group == "Child":
        # For simplicity, assume certain products are not for children in this dummy data
        filtered_products = filtered_products[
            ~filtered_products["name"].str.contains("Blood Pressure Monitor|Glucose Meter Kit|Multivitamin (Adult)", case=False, na=False)
        ]
    elif user_age_group == "Adult":
        # No specific exclusions for adult in this simple case
        pass
    elif user_age_group == "Senior":
        # Might prioritize certain types of products for seniors
        pass


if not filtered_products.empty:
    st.write(f"Based on your inputs, here are some products that might be suitable:")
    for index, row in filtered_products.iterrows():
        with st.expander(f"**{row['name']}** ({row['category']})"):
            st.markdown(f"**Description:** {row['description']}")
            st.markdown(f"**Suitable for:** {row['suitable_for_conditions']}")
            st.markdown(f"**General Price Range:** {row['general_price_range']}")
            st.info("*(Note: Actual prices and insurance coverage vary greatly. Consult your insurance provider and pharmacy.)*")
            st.write("---")
else:
    st.warning("No products found matching your criteria. Try adjusting your inputs.")

st.markdown("---")
st.markdown("### Educational Resources")
st.write("""
- **Understanding your Insurance Plan:** Learn about deductibles, co-pays, and formularies.
- **Generic vs. Brand-Name Drugs:** What's the difference and why does it matter?
- **Safe Medication Disposal:** How to properly dispose of unused or expired medications.
""")

st.markdown("---")
st.caption("This application is for informational purposes only and does not constitute medical advice. Consult with a qualified healthcare professional for any health concerns or before making any decisions related to your health or treatment.")