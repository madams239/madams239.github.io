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

# Sidebar
st.sidebar.title("ChefGPT")
st.sidebar.write("Your Michelin-starred AI Chef")

# Set up the LLM
llm = HuggingFaceHub(repo_id="google/flan-t5-small", 
                     model_kwargs={"temperature": 0.7}, 
                     huggingfacehub_api_token=huggingfacehub_api_token)

# Define prompt templates
detect_type_template = PromptTemplate(
    input_variables=["user_input"],
    template=(
        "Determine whether the following input is a list of ingredients or a named dish. "
        "If it's a list of ingredients, return 'ingredients'. "
        "If it's a dish name, return 'dish'.\n\n"
        "User input: {user_input}\n\n"
        "Response:"
    )
)

ingredient_recipe_template = PromptTemplate(
    input_variables=["ingredients"],
    template=(
        "You are a Michelin-starred chef. Based on the available ingredients: {ingredients}, "
        "suggest multiple gourmet meal ideas. First, list dishes that can be made immediately, "
        "excluding common household items (e.g., salt, oil, butter). Then, suggest dishes where only "
        "one or two additional ingredients are needed. Clearly separate these two sections."
    )
)

dish_to_ingredients_template = PromptTemplate(
    input_variables=["dish"],
    template=(
        "You are a Michelin-starred chef. Given the dish '{dish}', list the most likely ingredients used in it."
    )
)

# Create LLM chains
detect_type_chain = LLMChain(llm=llm, prompt=detect_type_template)
ingredient_recipe_chain = LLMChain(llm=llm, prompt=ingredient_recipe_template)
dish_to_ingredients_chain = LLMChain(llm=llm, prompt=dish_to_ingredients_template)

# Chat interface
st.title("🍽️ ChefGPT - Gourmet Meal Generator")
st.write("Enter your ingredients or a dish name, and I'll help you cook something delicious!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "detection_log" not in st.session_state:
    st.session_state.detection_log = []

# User input
with st.container():
    user_input = st.text_input("Enter ingredients (e.g., 'chicken, garlic, lemon') or a dish name (e.g., 'chicken alfredo')", key="user_input")
    submit_button = st.button("Get Recipe")

# Process input
if submit_button and user_input:
    with st.spinner("Analyzing your input..."):
        # Determine if input is ingredients or dish
        input_type = detect_type_chain.run({"user_input": user_input}).strip().lower()

        # Store the decision log for transparency
        st.session_state.detection_log.append((user_input, input_type))

        if input_type == "ingredients":
            response = ingredient_recipe_chain.run({"ingredients": user_input})
        elif input_type == "dish":
            ingredients_list = dish_to_ingredients_chain.run({"dish": user_input})
            response = ingredient_recipe_chain.run({"ingredients": ingredients_list})
        else:
            response = "I'm not sure if that's a dish or a set of ingredients. Could you clarify?"

        # Save to chat history
        st.session_state.chat_history.append((user_input, response))

# Display chat messages
for user_msg, chef_msg in st.session_state.chat_history:
    message(user_msg, is_user=True, key=f"user_{user_msg}")
    message(chef_msg, key=f"chef_{chef_msg}")

# Expandable section to show action logs
with st.expander("🔍 Detection Log (See how ChefGPT processed your input)"):
    for user_input, detected_type in st.session_state.detection_log:
        st.write(f"**Input:** {user_input} → **Detected as:** {detected_type}")

# Footer
st.markdown(
    "---\n#### Built with ❤️ using LangChain, HuggingFace, and Streamlit"
)
