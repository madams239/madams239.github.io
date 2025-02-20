import streamlit as st
from streamlit_chat import message
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFaceHub

# Page Configurations
st.set_page_config(
    page_title="ChefGPT - Gourmet Ideas",
    page_icon="🍳",
    layout="wide"
)

huggingfacehub_api_token = "YOUR_TOKEN_HERE"

# Sidebar with logo
st.sidebar.title("ChefGPT")
st.sidebar.write("Your Michelin-starred AI Chef")

# Set up the LLM
llm = HuggingFaceHub(repo_id="google/flan-t5-small", 
                     model_kwargs={"temperature": 0.7}, 
                     huggingfacehub_api_token=huggingfacehub_api_token)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["chat_history", "user_input"],
    template=(
        "You are a Michelin-starred chef. Maintain a conversation based on the previous dialogue.\n"
        "Chat history:\n{chat_history}\n"
        "User: {user_input}\n"
        "ChefGPT:"
    )
)

# Create an LLMChain
chef_chain = LLMChain(llm=llm, prompt=prompt_template)

# Chat interface
st.title("🍽️ ChefGPT - Gourmet Meal Generator")
st.write("Enter your ingredients or continue the conversation!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
with st.container():
    user_input = st.text_input("Your message (e.g., suggest a recipe, ask for tips, modify ingredients)", key="user_input")
    submit_button = st.button("Send")

# Process input and generate response
if submit_button and user_input:
    with st.spinner("Cooking up ideas..."):
        # Convert chat history to a formatted string
        chat_history_str = "\n".join([f"User: {msg[0]}\nChefGPT: {msg[1]}" for msg in st.session_state.chat_history])

        # Get response from LLM
        response = chef_chain.run({"chat_history": chat_history_str, "user_input": user_input})

        # Save to chat history
        st.session_state.chat_history.append((user_input, response))

# Display chat messages
for user_msg, chef_msg in st.session_state.chat_history:
    message(user_msg, is_user=True, key=f"user_{user_msg}")
    message(chef_msg, key=f"chef_{chef_msg}")

# Footer
st.markdown(
    "---\n#### Built using LangChain, HuggingFace, and Streamlit"
)
