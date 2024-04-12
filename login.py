import streamlit as st
from mail import*

def main():
    st.title("Chat PDF🤖")

    # Get email address from user
    email_address = st.text_input("Enter your email address")

    # Button to send the email
    if st.button("Send Email"):
        if email_address:
            if sendEmail(email_address,"http://192.168.254.197:8502"):
                st.success("Email sent successfully")
            else:
                st.error("Somthing went wrong pease try again..")
        else:
            st.warning("Please enter an email address")

if __name__ == "__main__":
    main()
