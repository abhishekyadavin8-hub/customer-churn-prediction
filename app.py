import streamlit as st
import pickle
import numpy as np

# Load the saved model
model = pickle.load(open('model.pkl', 'rb'))

st.title('Customer Churn Predictor')
st.write('Fill in the customer details below to predict if they will leave or stay.')

# Input fields
gender = st.selectbox('Gender', ['Male', 'Female'])
senior_citizen = st.selectbox('Is the customer a Senior Citizen?', [0, 1])
partner = st.selectbox('Has Partner?', ['Yes', 'No'])
dependents = st.selectbox('Has Dependents?', ['Yes', 'No'])
tenure = st.slider('How many months has the customer stayed?', 0, 72, 12)
internet_service = st.selectbox('Internet Service', ['DSL', 'Fiber optic', 'No'])
contract = st.selectbox('Contract Type', ['Month-to-month', 'One year', 'Two year'])
paperless_billing = st.selectbox('Paperless Billing?', ['Yes', 'No'])
payment_method = st.selectbox('Payment Method', [
    'Bank transfer (automatic)', 'Credit card (automatic)',
    'Electronic check', 'Mailed check'
])
monthly_charges = st.number_input('Monthly Charges ($)', 0.0, 150.0, 50.0)
total_charges = st.number_input('Total Charges ($)', 0.0, 10000.0, 500.0)

# Encode inputs
gender_encoded = 1 if gender == 'Male' else 0
partner_encoded = 1 if partner == 'Yes' else 0
dependents_encoded = 1 if dependents == 'Yes' else 0
contract_encoded = ['Month-to-month', 'One year', 'Two year'].index(contract)
internet_encoded = ['DSL', 'Fiber optic', 'No'].index(internet_service)
paperless_encoded = 1 if paperless_billing == 'Yes' else 0
payment_encoded = ['Bank transfer (automatic)', 'Credit card (automatic)',
                   'Electronic check', 'Mailed check'].index(payment_method)

if st.button('Predict'):
    input_data = np.array([[
        gender_encoded,        # gender
        senior_citizen,        # SeniorCitizen
        partner_encoded,       # Partner
        dependents_encoded,    # Dependents
        tenure,                # tenure
        0,                     # PhoneService
        0,                     # MultipleLines
        internet_encoded,      # InternetService
        0,                     # OnlineSecurity
        0,                     # OnlineBackup
        0,                     # DeviceProtection
        0,                     # TechSupport
        0,                     # StreamingTV
        0,                     # StreamingMovies
        contract_encoded,      # Contract
        paperless_encoded,     # PaperlessBilling
        payment_encoded,       # PaymentMethod
        monthly_charges,       # MonthlyCharges
        total_charges          # TotalCharges
    ]])

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error('⚠️ This customer is likely to CHURN')
    else:
        st.success('✅ This customer will likely STAY')