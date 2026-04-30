import streamlit as st
import pickle
import numpy as np

# Load the saved model
model = pickle.load(open('model.pkl', 'rb'))

st.title('Customer Churn Predictor')
st.write('Fill in the customer details below to predict if they will leave or stay.')

tenure = st.slider('How many months has the customer stayed?', 0, 72, 12)
monthly_charges = st.number_input('Monthly Charges ($)', 0.0, 150.0, 50.0)
total_charges = st.number_input('Total Charges ($)', 0.0, 10000.0, 500.0)
senior_citizen = st.selectbox('Is the customer a Senior Citizen?', [0, 1])
contract = st.selectbox('Contract Type', [0, 1, 2],
                        format_func=lambda x: ['Month-to-Month', 'One Year', 'Two Year'][x])

if st.button('Predict'):
    input_data = np.array([[senior_citizen, tenure, monthly_charges,
                            total_charges, contract, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0]])
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error('⚠️ This customer is likely to CHURN')
    else:
        st.success('✅ This customer will likely STAY')