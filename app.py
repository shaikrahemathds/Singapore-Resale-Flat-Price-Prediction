import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pickle

# Set up page configuration for Streamlit
st.set_page_config(page_title='HDB Flat Resale Price Predictor', page_icon='house', initial_sidebar_state='expanded',
                    layout='wide')

# Columns for logo and title
col1, col2 = st.columns([1, 5])

with col1:   
    st.image("hdb.png", width=100)

with col2:   
    st.markdown(
        "<h1 style='color: red; font-size: 45px; text-align: left;'>🏠 Singapore Resale Flat Price Prediction</h1>",
        unsafe_allow_html=True
    )

# Sidebar options for main menu
selected = option_menu(
    menu_title="Main Menu",  
    options=["Home", "Get Prediction"],  
    icons=['house', "lightbulb"],  
    default_index=0,  
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "border": "2px ridge ", "background-color": "#002b36"},
        "icon": {"color": 'yellow', "font-size": "25px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#586e75"},
        "nav-link-selected": {"background-color": "#247579"},
    })

# User input values for select box and encoding for respective features
class option:
    option_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    encoded_month = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9,
                    "October": 10, "November": 11, "December": 12}
    
    option_town = [
        'TAMPINES', 'YISHUN', 'JURONG WEST', 'BEDOK', 'WOODLANDS', 'ANG MO KIO', 'HOUGANG',
        'BUKIT BATOK', 'CHOA CHU KANG', 'BUKIT MERAH', 'SENGKANG', 'PASIR RIS', 'TOA PAYOH',
        'QUEENSTOWN', 'GEYLANG', 'CLEMENTI', 'BUKIT PANJANG', 'KALLANG/WHAMPOA', 'JURONG EAST',
        'SERANGOON', 'PUNGGOL', 'BISHAN', 'SEMBAWANG', 'MARINE PARADE', 'CENTRAL AREA',
        'BUKIT TIMAH', 'LIM CHU KANG'
    ]
    
    encoded_town = {
        'TAMPINES': 23, 'YISHUN': 26, 'JURONG WEST': 13, 'BEDOK': 1, 'WOODLANDS': 25, 'ANG MO KIO': 0, 'HOUGANG': 11,
        'BUKIT BATOK': 3, 'CHOA CHU KANG': 8, 'BUKIT MERAH': 4, 'SENGKANG': 21, 'PASIR RIS': 17, 'TOA PAYOH': 24,
        'QUEENSTOWN': 19, 'GEYLANG': 10, 'CLEMENTI': 9, 'BUKIT PANJANG': 5, 'KALLANG/WHAMPOA': 14, 'JURONG EAST': 12,
        'SERANGOON': 22, 'PUNGGOL': 18, 'BISHAN': 2, 'SEMBAWANG': 20, 'MARINE PARADE': 16, 'CENTRAL AREA': 7,
        'BUKIT TIMAH': 6, 'LIM CHU KANG': 15
    }
    
    option_flat_type = [
        '4 ROOM', '3 ROOM', '5 ROOM', 'EXECUTIVE', '2 ROOM', '1 ROOM', 'MULTI-GENERATION'
    ]
    
    encoded_flat_type = {
        '4 ROOM': 3, '3 ROOM': 2, '5 ROOM': 4, 'EXECUTIVE': 5, '2 ROOM': 1, '1 ROOM': 0, 'MULTI-GENERATION': 6
    }

    option_flat_model = [
        'MODEL A', 'IMPROVED', 'NEW GENERATION', 'SIMPLIFIED', 'PREMIUM APARTMENT', 
        'STANDARD', 'APARTMENT', 'MAISONETTE', 'MODEL A2', 'DBSS', 
        'MODEL A-MAISONETTE', 'ADJOINED FLAT', 'TERRACE', 'MULTI-GENERATION', 
        'TYPE S1', 'TYPE S2', '2-ROOM', 'IMPROVED-MAISONETTE', 'PREMIUM APARTMENT LOFT', 
        'PREMIUM MAISONETTE', '3GEN'
    ]
    
    encoded_flat_model = {
        'MODEL A': 8, 'IMPROVED': 5, 'NEW GENERATION': 12, 'SIMPLIFIED': 16, 'PREMIUM APARTMENT': 13, 
        'STANDARD': 17, 'APARTMENT': 3, 'MAISONETTE': 7, 'MODEL A2': 10, 'DBSS': 4, 
        'MODEL A-MAISONETTE': 9, 'ADJOINED FLAT': 2, 'TERRACE': 18, 'MULTI-GENERATION': 11, 
        'TYPE S1': 19, 'TYPE S2': 20, '2-ROOM': 0, 'IMPROVED-MAISONETTE': 6, 'PREMIUM APARTMENT LOFT': 14, 
        'PREMIUM MAISONETTE': 15, '3GEN': 1
    }

# Set up the information for the 'Get Prediction' menu
if selected == "Get Prediction":
    st.write('')
    st.markdown("<h5 style=color:orange>To Predict the Resale Price of a Flat, Please Provide the Following Information:", unsafe_allow_html=True)
    st.write('')

    # Form to get the user input 
    with st.form('prediction'):
        col1, col2 = st.columns(2)
        with col1:
            user_month = st.selectbox(label='Month', options=option.option_months, index=None)
            user_town = st.selectbox(label='Town', options=option.option_town, index=None)
            user_flat_type = st.selectbox(label='Flat Type', options=option.option_flat_type, index=None)
            user_flat_model = st.selectbox(label='Flat Model', options=option.option_flat_model, index=None)
            floor_area_sqm = st.number_input(label='Floor area sqm', min_value=10.0)
            price_per_sqm = st.number_input(label='Price Per sqm', min_value=100.00)

        with col2:
            year = st.text_input(label='Year', max_chars=4)
            block = st.text_input(label='Block', max_chars=3)
            lease_commence_year = st.text_input(label='Year of lease commence', max_chars=4)
            remaining_lease = st.number_input(label='Remaining lease year', min_value=0, max_value=99)
            storey_start = st.number_input(label='Storey Start', min_value=1, max_value=50)
            
            st.markdown('<br>', unsafe_allow_html=True)
            button = st.form_submit_button('PREDICT', use_container_width=True)

    if button:
        with st.spinner("Predicting..."):

            # Check whether user has filled all required fields
            if not all([user_month, user_town, user_flat_type, user_flat_model, floor_area_sqm, price_per_sqm, year, block,
                        lease_commence_year, remaining_lease, storey_start]):
                st.error("Please fill in all required fields.")
            else:
                # Create features from user input 
                month = option.encoded_month[user_month]
                town = option.encoded_town[user_town]
                flat_type = option.encoded_flat_type[user_flat_type]
                flat_model = option.encoded_flat_model[user_flat_model]
                
                storey_start = np.log1p(storey_start)
                price_per_sqm = np.log1p(price_per_sqm)

                # Open pickle model and predict resale price with user data
                with open('Decisiontree.pkl', 'rb') as files:
                    model = pickle.load(files)
                
                user_data = np.array([[month, town, flat_type, block, floor_area_sqm, flat_model, lease_commence_year,
                                        remaining_lease, year, storey_start, price_per_sqm]])

                predict = model.predict(user_data)
                resale_price = np.exp(predict[0])

                # Display the predicted resale price 
                st.subheader(f"Predicted Resale price is: :green[{resale_price:.2f}]")

# Set up the information for the 'Home' menu
if selected == "Home":
    
    st.markdown(
    """
    <style>
    body {
        font-size: 32px; /* Change this value to adjust font size */
    }
    h1 {
        font-size: 32px;
    }
    p {
        font-size: 42px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    st.markdown("""
    <p style='text-align:center; color:#FF6347; font-size:18px;font-weight:bold;'>Welcome to the Singapore Resale Flat Price Prediction App! 🎉</p>
    <p style='text-align:center; color:white; font-size:16px;'>This web application utilizes machine learning to predict the resale prices of flats in Singapore based on various features like town, flat type, and storey range. 
    Whether you are a potential buyer or seller, this app provides you with valuable insights into the potential resale price of a flat, helping you make informed decisions in a highly competitive real estate market. 🏘️</p>
    <p style='text-align:center; color:white; font-size:16px;'>The app uses historical data to give accurate predictions, making it a useful tool for anyone in the real estate domain.</p>
    """, unsafe_allow_html=True)

    # Two Columns: Technologies & Process Overview
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h5 style='color:#FF6347;'>📌 Domain & Technologies</h5>", unsafe_allow_html=True)
        st.markdown("""
        - **Domain**: Real Estate 🏠
        - **Technologies Used**:
            - Python scripting 🐍
            - Data Preprocessing 📊
            - Exploratory Data Analysis (EDA) 🔍
            - Machine Learning Models 🤖
            - Streamlit for Web Deployment 🌐
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h5 style='color:#FF6347;'>🔨 Steps in the Process</h5>", unsafe_allow_html=True)
        st.markdown("""
        - **Step 1**: Data Collection and Preprocessing
        - **Step 2**: Data Exploration and Handling
        - **Step 3**: Model Selection and Training
        - **Step 4**: Model Deployment & Application
        """, unsafe_allow_html=True)

    # Final Note
    st.markdown("<br><p style='text-align:center; font-size:16px; color:white;'>Start by entering flat details to get resale price predictions based on our trained machine learning model. 🚀</p>", unsafe_allow_html=True)
