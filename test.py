import streamlit as st
import streamlit_authenticator as stauth
from mail import *

# Define your users and hashed passwords
users = {
    "jsmith": {
        "email": "jsmith@gmail.com",
        "name": "John Smith",
        "password": "hashed_password"
    },
    # Add more users as needed
}

# Create an authenticator object
authenticator = stauth.Authenticate(users)

# Render the login widget
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write('Welcome ', name)
    # Your main app goes here
else:
    st.write('Please enter your email to receive a login link.')
    email = st.text_input('Email')
    if email:
        sendEmail(email,"http://localhost:5000/send_login_link")
        st.write('Login link has been sent to your email.')
