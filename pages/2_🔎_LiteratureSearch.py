'''
Author: Anindita Nath
Job Title: Postdoctoral Research Fellow
Location: Bioinformatics and Systems Medicine Laboratory, MSBMI, UTHH
Date: August, 2023 - January 2024
#......................................................................................
Purpose: Front-end design and back-end fucntionality of the Literature Search Chat page
'''

#.......................................................................................

# Importing essential libraries and modules
#General libraries
import os  # Provides a way of using operating system dependent functionality.
import datetime  # Supplies classes for manipulating dates and times.
import base64  # Provides data encoding and decoding as per RFC 3548.
from pathlib import Path  # Offers classes representing filesystem paths with semantics appropriate for different operating systems.
from dotenv import load_dotenv  # Reads key-value pairs from a .env file and sets them as environment variables.
#Langchain libraries
import openai
from langchain.chat_models import AzureChatOpenAI  # Interface for Azure's Chat OpenAI.
from langchain.chains import RetrievalQA, MultiRetrievalQAChain, LLMChain  # Chains for question-answering and large language model operations.
from langchain.document_loaders import TextLoader, PyPDFLoader  # Loaders for text and PDF documents.
from langchain.embeddings.openai import OpenAIEmbeddings  # Embeddings module for OpenAI.
from langchain.llms import OpenAI  # Interface for OpenAI's language models.
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter  # Utilities for splitting text based on character count.
from langchain.vectorstores import Chroma  # Vector storage module.
from langchain.agents import initialize_agent, AgentExecutor, ConversationalChatAgent  # Utilities for initializing and executing conversational agents.
from langchain.prompts import MessagesPlaceholder  # Utility for handling message placeholders.
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory  # Memory modules for conversation buffering.
from langchain.chat_models import ChatOpenAI  # Chat model for OpenAI.

#Streamlit libraries
import streamlit as st
from streamlit_chat import message  # Streamlit component for chat messages.
from streamlit_extras.colored_header import colored_header  # Streamlit extra for colored headers.
from streamlit_extras.add_vertical_space import add_vertical_space  # Streamlit extra for adding vertical space.
from llm_steps import load_tools  # Custom module for loading tools.




# Function to read local image and convert to base64
def load_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()



#load_dotenv() #open AIAPI
#os.environ['OPENAI_API_KEY'] = st.session_state.apikey


# Check if the environment is local or Azure, then load environment variables
if os.getenv('WEBSITE_SITE_NAME') is None:
    env_path = Path('.') / 'secrets.env'
    load_dotenv(dotenv_path=env_path)

# Function to load settings from environment or set to default
def load_setting(setting_name, session_name, default_value=''):  
    if session_name not in st.session_state:  
        if os.environ.get(setting_name) is not None:
            st.session_state[session_name] = os.environ.get(setting_name)
        else:
            st.session_state[session_name] = default_value

# Load various settings into Streamlit's session state
load_setting("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "chatgpt", "gpt-35-turbo") 
load_setting("OPENAI_CHATGPT_MODEL_NAME", "chatgptmodel", "gpt-35-turbo-16k")  
load_setting("AZURE_OPENAI_ENDPOINT", "endpoint", "https://resourcenamehere.openai.azure.com/")  
load_setting("AZURE_OPENAI_API_KEY", "apikey")  
load_setting("SERP API KEY (for Google Scholar Search)", "serpapikey")

# Initialize show_settings in session state if not already present
if 'show_settings' not in st.session_state:  
    st.session_state['show_settings'] = False  

# Function to save OpenAI and SQL settings into session state
def saveOpenAI():
    # Copy the settings from temporary text box state to session state
    st.session_state.chatgpt = st.session_state.txtChatGPT
    st.session_state.chatgptmodel = st.session_state.txtChatGPTmodel   
    st.session_state.endpoint = st.session_state.txtEndpoint
    st.session_state.apikey = st.session_state.txtAPIKey
    st.session_state.serpapikey = st.session_state.txtSERPAPIKey
   
   

    # Close the settings panel
    st.session_state['show_settings'] = False

# Function to toggle the visibility of the settings panel
def toggleSettings():
    st.session_state['show_settings'] = not st.session_state['show_settings']

# Configure Azure OpenAI Service API
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = st.session_state.endpoint
openai.api_key = st.session_state.apikey


# Set some constants for OpenAI API
max_response_tokens = 1250
token_limit= 4096
temperature=0

############### STREAMLIT INITIALIZATION #################

st.set_page_config(
    page_title="LiteratureSearch",
    page_icon="random",
    layout="wide",
    #layout="wide",
    initial_sidebar_state="auto",   
)
# Create a faded background image for the entire page

bkgroundimage = load_image("images/appvideobkglogo.png")
st.markdown(
    f"""
    <style>
        body {{
            background-image: url("data:image/png;base64,{bkgroundimage}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            opacity: 0.95;
        }}
    </style>
    """,
    unsafe_allow_html=True,
    )

# Main app logic starts here
#Heading
st.markdown(f"""<h1 style="font-size: 32px;">Find literature evidence in PubMed, Google Scholar or Arxiv</h1>""", unsafe_allow_html=True)
st.markdown(f"""<h1 style="margin-top: -20px; font-size: 22px;">Mention the portal you want to search in along with your search query</h1>""", unsafe_allow_html=True)

# Create columns for the Streamlit app layout
col1, col2 = st.columns((3,1)) 

with st.sidebar:
    
    #Settings for Azure Open AI
    st.button("Settings",on_click=toggleSettings)
    if st.session_state['show_settings']:  
        
        with st.form("AzureOpenAI"):
            st.title("Azure OpenAI")
            st.text_input("ChatGPT deployment name:", value=st.session_state.chatgpt,key="txtChatGPT") 
            st.text_input("GPT-4 deployment name:", value=st.session_state.chatgptmodel,key="txtChatGPTmodel")
             
     
            st.text_input("Azure OpenAI Endpoint:", value=st.session_state.endpoint,key="txtEndpoint")  
            st.text_input("Azure OpenAI Key:", value=st.session_state.apikey, type="password",key="txtAPIKey")      
            
            
            st.title("Google Scholar API")
            st.text_input("SERP API Key:", value=st.session_state.serpapikey, type="password",key="txtSERPAPIKey")      
            
            st.form_submit_button("Submit",on_click=saveOpenAI)




#################AGENT SETUP####################
# Check if the necessary API settings are provided
if st.session_state.apikey == '' or st.session_state.endpoint == '' or st.session_state.chatgpt == '' or st.session_state.serpapikey == '':
    # Display an error message if any of the API settings are missing or incorrect
    st.error("Some or all of the API settings are missing or incorrect. Click on Settings on the right to update!")

else:
    # Initialize the AzureChatOpenAI model
    llm = AzureChatOpenAI(openai_api_base=st.session_state.endpoint, openai_api_version="2023-05-15", deployment_name=st.session_state.chatgpt, openai_api_key=st.session_state.apikey, openai_api_type="azure", temperature=0)
    
    # Initialize OpenAIEmbeddings
    OpenAIEmbeddings(deployment=st.session_state.chatgpt, model=st.session_state.chatgptmodel, openai_api_key=st.session_state.apikey, openai_api_base=st.session_state.endpoint, openai_api_type="azure")
    
    # Load tools for the agent
    tools = load_tools(st.session_state.serpapikey)

    # Initialize a text splitter for handling large texts
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

            
    #Agent initalization
    # Define the agent's prefix or system message

    prefix = """You are a Literature Mining Assistant. 

    You will cite sources for literature evidence for a given search phrase or phrases by providing links to the sources, pubmed ids, arxiv ids, or naming them.
    Assistant is able to look back at previous messages and intelligently read them to get information for new input.

    If Assistant is unable to answer a question, it will answer 'I don't know' but also give helpful details to help the user. 
    If Assistant is unable to use a link, it will state it has difficulty parsing the link.

    """

       # Create a prompt for the ConversationalChatAgent
    prompt = ConversationalChatAgent.create_prompt(tools, system_message=prefix)

    # Initialize a ConversationBufferWindowMemory to store the agent's memory
    if "agent_memory" not in st.session_state:
        st.session_state["agent_memory"] = ConversationBufferWindowMemory(k=4, memory_key="chat_history", return_messages=True)

    # Initialize the LLMChain with the AzureChatOpenAI model and the created prompt
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Initialize the ConversationalChatAgent with the LLMChain and tools
    agent = ConversationalChatAgent(llm_chain=llm_chain, tools=tools, verbose=True)

    # Initialize the AgentExecutor with the agent, tools, and memory
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=st.session_state["agent_memory"])



    
#################Conatiner SETUP####################   
#This section of the code sets up containers for user input and responses in the Streamlit application, 
#providing a structured and visually appealing interface for user interaction.

# Initialize containers for the input and response sections of the app
input_container = st.container()  # Container for user input
colored_header(label='', description='', color_name='orange-50')  # Colored header (seems to have empty label and description)
response_container = st.container()  # Container for responses



# User input
# Function to get text input from the user
def get_text():
    # Create a text input box and return the inputted text
    input_text = st.text_input("You: ", "", key="input")
    return input_text

# Applying the user input box within the input container
with input_container:
    # Get the user input using the get_text function
    user_input = get_text()


         





############### STREAMLIT CHATBOT #################
#This section of the code sets up the core functionality for a Streamlit-based chatbot, 
#specifically designed for literature review assistance. 
#It manages the conversation state, generates responses using an agent,
#and displays the conversation in the Streamlit app.

# Initialize 'generated' in the session state if not present
if 'generated' not in st.session_state:
    st.session_state['generated'] = [""" Welcome to your Literature Review Assistant. 
    Enter your query above, e.g. 'Search for articles with gene APOE and Alzheimer in Pubmed.'"""]

# Initialize 'past' in the session state if not present
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']


# Function to generate a response from the agent based on the user's prompt
def generate_response(prompt): 
    # Execute the agent chain with the provided input
    response = agent_chain.run(input=prompt)
    # Debugging: Print the current conversation buffer
    print(st.session_state["agent_memory"].buffer)
    return response



# Container for displaying the conversation
with response_container:
    # Check if there is user input
    if user_input:
        # Generate a response for the user input
        response = generate_response(user_input)
        # Append the user input and the generated response to their respective lists in the session state
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    # If there are generated responses, display the conversation
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            # Display the user's input and the chatbot's response
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['generated'][i], key=str(i))

            






