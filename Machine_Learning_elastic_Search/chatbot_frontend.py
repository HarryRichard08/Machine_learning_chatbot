import streamlit as st
import requests

# Streamlit interface
st.title('University Service Chatbot')
st.write('Ask  questions about university')

# User input
user_input = st.text_input("Your question", "")

# Button to send the request
if st.button('Submit'):
    # Prepare the request data
    request_data = {'question': user_input, 'top_n': 3}
    
    # URL of your FastAPI endpoint
    url = 'http://localhost:8000/search/'
    
    # POST request to the FastAPI server
    response = requests.post(url, json=request_data)
    
    if response.status_code == 200:
        # Display each result
        results = response.json()['results']
        if results:
            for idx, result in enumerate(results, start=1):
                st.subheader(f"Result {idx}")
                st.write(f"Section: {result['section']}")
                st.write(f"Content: {result['content']}")
                st.write(f"Score: {result['score']:.2f}")
        else:
            st.write("No results found.")
    else:
        # Display error message
        st.error(f"An error occurred: {response.text}")



