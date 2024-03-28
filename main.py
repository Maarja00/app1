import streamlit as st
from langchain import PromptTemplate
#from langchain.llms import OpenAI #so vananenud rida ning asendatud allolevaga
from langchain_community.llms import OpenAI
import os

template = """
 You are a marketing copywriter with 20 years of experience. You are analyzing customer's background to write personalized product description that only this customer will receive; 
    PRODUCT input text: {content};
    CUSTOMER work profession (y): {workprofession};
    CUSTOMER brand preference: {brandpreference};
    TASK: Write a product description that is tailored into this customer's Work profession and brand preference. Use work profession specific slang.;
    FORMAT: Present the result in the following order: (PRODUCT DESCRIPTION), (BENEFITS), (USE CASE);
    PRODUCT DESCRIPTION: describe the product in 5 sentences;
    BENEFITS: describe in 3 sentences why this product is perfect considering customers work profession and brand preference;
    USE CASE: write a story in 5 sentences, of an example weekend activity taking into account brand preference {brandpreference} and work profession {workprofession}, write a story in first person, example "I started my Saturday morning with ...";
"""

prompt = PromptTemplate(
    input_variables=["brandpreference", "workprofession", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personaliseeritud turundusteksti konverter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Otstarve: tootetutvustustekstide personaliseerimine igale kliendile või kliendigruppidele; väljundtekst on kohandatud kliendi a) brändieelistuse ja b) ametipositsiooniga; sisendtekstiks on neutraalses vormis tootekirjeldus. \
    \n\n Kasutusjuhend: 1) valmista ette tootekirjeldus (sisendtekst). 2) määra tarbijasegemendid lähtuvalt vanuserühma ja brändieelistuse kombinatsioonidest. 3) sisesta ükshaaval tarbijasegmentide lõikes eeltoodud info äpi kasutajaliideses, saada ära. \
    4) kopeeri ükshaaval tarbijasegmentide lõikes äpi väljundteksti kõnealuse toote tutvustuslehele.")

with col2:
    st.image(image='MaarjaCompanyLogo.jpg', caption='Maarja SmartPhones for everybody')

st.markdown("## Enter Your Content To Convert")

def get_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return openai_api_key
    # If OPENAI_API_KEY environment variable is not set, prompt user for input
    input_text = streamlit.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_brandpreference = st.selectbox(
        'Which brand would you prefer?',
        ('Apple', 'Samsung', 'Huawei', 'Xiaomi', 'Motorola', 'Nokia', 'Poco')
    
def get_hobby():
    input_text = st.text_input(label="Customers work profession", key="workprofession_input")
    return input_text

workprofession_input = get_workprofession()

def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "t shirts, all clolors, cotton, responsible manufacturing"

st.button("*GENERATE TEXT*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)

st.markdown("### Your customer tailored content:")

if content_input:
#    if not openai_api_key:
#        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
#        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(brandpreference=option_brandpreference, workposition=workposition_input, content=content_input)

    formatted_content = llm(prompt_with_content)

    st.write(formatted_content)
