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
huggingfacehub_api_token="YOUR_TOKEN_HERE"
# Sidebar with logo
# st.sidebar.image("chef_logo.png", use_column_width=True)
st.sidebar.title("ChefGPT")
st.sidebar.write("Your Michelin-starred AI Chef")

# Set up the LLM
llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature": 0.7}, huggingfacehub_api_token=huggingfacehub_api_token)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["ingredients"],
    template=(
        "You are a Michelin-starred chef. Based on the ingredients: {ingredients}, "
        "suggest a gourmet meal idea with detailed preparation steps and explain "
        "why this combination works well."
    )
)

# Create an LLMChain
chef_chain = LLMChain(llm=llm, prompt=prompt_template)

# Chat interface
st.title("🍽️ ChefGPT - Gourmet Meal Generator")
st.write("Enter your ingredients below, and I'll create a Michelin-star-worthy recipe for you!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
with st.container():
    user_input = st.text_input("Your ingredients (e.g., chicken, garlic, lemon)", key="user_input")
    submit_button = st.button("Get Recipe")

# Process input and generate response
if submit_button and user_input:
    with st.spinner("Cooking up ideas..."):
        response = chef_chain.run({"ingredients": user_input})
        
        # Save to chat history
        st.session_state.chat_history.append((user_input, response))

# Display chat messages
for user_msg, chef_msg in st.session_state.chat_history:
    message(user_msg, is_user=True, key=f"user_{user_msg}")
    message(chef_msg, key=f"chef_{chef_msg}")

# Footer
st.markdown(
    "---\n#### Built with ❤️ using LangChain, HuggingFace, and Streamlit"
)
