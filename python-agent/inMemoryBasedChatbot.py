from dotenv import load_dotenv
import streamlit as st
from utils import create_chain, read_pdf_and_split_docs, store_embeddings_in_memory

load_dotenv()

def main():
    st.title("Chat with pdf")
    uploaded_file = st.file_uploader("Choose a file")

    # initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "Assistant", "content": "Hello, I am your assistant. How can I help you today?"}
        ]

    if "chain" not in st.session_state: 
        if uploaded_file is not None:
            st.success("Saved File")
            docs = read_pdf_and_split_docs(uploaded_file)
            vector_store = store_embeddings_in_memory(docs)
            chain = create_chain(vector_store)
            st.session_state.chain = chain


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