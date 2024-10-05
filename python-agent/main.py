from dotenv import load_dotenv
import streamlit as st
from utils import load_and_split_docs, upsert_to_pinecone, create_chain ,random_string
import os

load_dotenv()

def main():
    st.title("Chat with your pdf")

    uploaded_file = st.file_uploader("Choose a file")

    # load the file and create the chain from the file 
    if uploaded_file is not None:
        file_details = {"FileName":uploaded_file.name,"FileType": uploaded_file.type}
        st.session_state.file_details = file_details
        st.write(file_details)
        with open(os.path.join("/home/kaif-siddiqui/2024/python-langchan/pinecone-chatbot/python-agent/tempDir",uploaded_file.name),"wb") as f: 
            f.write(uploaded_file.getbuffer())         
            st.success("Saved File")
            docs = load_and_split_docs("/home/kaif-siddiqui/2024/python-langchan/pinecone-chatbot/python-agent/tempDir/"+ uploaded_file.name)
            vector_store = upsert_to_pinecone(docs, random_string())
            chain = create_chain(vector_store)
            st.session_state.chain = chain

    # initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "Assistant", "content": "Hello, I am your assistant. How can I help you today?"}
        ]

    #  display chat messages in the screeen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

        # accept user input
    if input := st.chat_input("What is up"):
        # add user messages to chat history
        st.session_state.messages.append({"role": "User", "content": input})

        # display user message in chat message container
        with st.chat_message("User"):
            st.markdown(input)

        with st.chat_message("Assistant"):
            response = st.session_state.chain.invoke(input)
            st.markdown(response)

        st.session_state.messages.append({"role": "Assistant", "content": response})



if __name__ == "__main__":
    main()