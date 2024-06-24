# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#.............................................................................
'''
Modified from the original cited above.
Author: Anindita Nath
Job Title: Postdoctoral Research Fellow
Location: Bioinformatics and Systems Medicine Laboratory, MSBMI, UTHH
Date: August, 2023 - January 2024
'''
#..............................................................................

#Purpose: Front-end design and back-end fucntionality of the Home page

#...............................................................................

# Importing essential libraries and modules
import os  # Operating system interfaces
from pathlib import Path  # File path manipulation
from dotenv import load_dotenv  # Load environment variables from a .env file
import streamlit as st  # Import Streamlit for creating web apps
from streamlit.logger import get_logger  # Import get_logger from Streamlit to enable logging
from streamlit_chat import message  # Import message for chat functionality in Streamlit
import base64  # Import base64 library for encoding/decoding data
import time  # Import time library for time-related functions
from streamlit_modal import Modal  # Import Modal for creating modal dialogs in Streamlit
from streamlit_player import st_player  # Import st_player for embedding media players in Streamlit apps
import openai  # OpenAI's API for GPT models
#from transformers import pipeline  # Import pipeline from the transformers library for NLP tasks

LOGGER = get_logger(__name__)  # Initialize a logger for the module with the module's name



# Check if the application is running in a local environment or on Azure
if os.getenv('WEBSITE_SITE_NAME') is None:
    # If local, load environment variables from 'secrets.env' file
    env_path = Path('.') / 'secrets.env'
    load_dotenv(dotenv_path=env_path)

# Function to load settings from environment variables or set them to default values
def load_setting(setting_name, session_name, default_value=''):  
    # If the setting is not already in the Streamlit session state
    if session_name not in st.session_state:
        # If the environment variable exists, use its value; otherwise, use the default value
        st.session_state[session_name] = os.environ.get(setting_name, default_value)

# Load various settings related to Azure OpenAI into Streamlit's session state
load_setting("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "chatgpt", "gpt-35-turbo")
load_setting("AZURE_OPENAI_GPT4_DEPLOYMENT", "gpt4", "gpt-35-turbo")
load_setting("AZURE_OPENAI_ENDPOINT", "endpoint", "https://resourcenamehere.openai.azure.com/")
load_setting("AZURE_OPENAI_API_KEY", "apikey")

# Initialize 'show_settings' in session state if not already present
if 'show_settings' not in st.session_state:
    # This variable likely controls the visibility of some settings UI in the app
    st.session_state['show_settings'] = False

# Initialize 'chat_history' in session state if not already present (commented out)
# if 'chat_history' not in st.session_state:
    # This variable would store the history of chats/conversations
    # st.session_state['chat_history'] = []



# Function to save OpenAI and SQL settings into session state
def saveOpenAI():
    # Copy the settings from temporary text box state to session state
    st.session_state.chatgpt = st.session_state.txtChatGPT
    st.session_state.gpt4 = st.session_state.txtGPT4
    st.session_state.endpoint = st.session_state.txtEndpoint
    st.session_state.apikey = st.session_state.txtAPIKey
    

    # Close the settings panel
    st.session_state['show_settings'] = False

# Function to toggle the visibility of the settings panel
def toggleSettings():
    st.session_state['show_settings'] = not st.session_state['show_settings']

# Set OpenAI API configurations
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview" 
openai.api_key = st.session_state.get('apikey', '')
openai.api_base = st.session_state.get('endpoint', '')

# Set some constants for OpenAI API
max_response_tokens = 1250
token_limit= 4096
temperature=0

# Function to read local image and convert to base64
def load_image(image_path):
    with open(image_path, "rb") as img_file:  # Open the image file in binary read mode
        return base64.b64encode(img_file.read()).decode()  # Encode the binary data to base64 and return it as a string

# Function to read local video and convert to base64
def load_video(video_path):
    with open(video_path, "rb") as video_file:  # Open the video file in binary read mode
        video_base64 = base64.b64encode(video_file.read()).decode()  # Encode the binary data to base64 and return it as a string
    return video_base64  # Return the base64-encoded video data

#not in use
# def load_classifier():
    # # Load the zero-shot classification model
    # classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")  # Initialize the zero-shot classifier pipeline with the specified model
    # return classifier  # Return the initialized classifier

def category():
    # Define the categories and their corresponding Streamlit page URLs
    category_urls = {
        "PGSChat": "PGSChat",  # Define URL for the PGSChat page
        "GeneAPIChat": "GeneAPIChat",  # Define URL for the GeneAPIChat page
        "LiteratureSearch": "LiteratureSearch"  # Define URL for the LiteratureSearch page
    }
    return category_urls  # Return the dictionary of category URLs
 
#not in use 
# def classify_query(user_query, classifier, categories):
    # # Predict the category of the user's query
    # result = classifier(user_query, categories, multi_label=False)

    # # Find the label with the highest score
    # highest_score_index = result["scores"].index(max(result["scores"]))
    # predicted_category = result["labels"][highest_score_index]
    # confidence = result["scores"][highest_score_index]

    # # You can set a threshold for confidence here (e.g., 0.5)
    # confidence_threshold = 0.5
    # if confidence < confidence_threshold:
        # return None, None  # or handle low confidence scenarios differently
    # return predicted_category, confidence
def classify_query_correctTaskpasge(user_input, max_response_tokens, temperature, model_engine):
    # Define the conversation context and examples for the OpenAI model
    messages = [
        # System message describing the assistant's role
        {"role": "system", "content": "You are a helpful assistant classifying user commands into either 'PGSChat' or 'GeneAPIChat' or 'LiteratureSearch'"},

        # Predefined conversation examples guiding the model for classification
        {"role": "user", "content": "Show PGS Chat Page"},
        {"role": "assistant", "content": "PGSChat"},
        {"role": "user", "content": "What are the top ranked SNPids?"},
        {"role": "assistant", "content": "PGSChat"},
        {"role": "user", "content": "Show me the publication ids for the highest rank genes in Alzheimer."},
        {"role": "assistant", "content": "PGSChat"},
        {"role": "user", "content": "Plot the top ranked genes and PGS scores for Schizophrenia."},
        {"role": "assistant", "content": "PGSChat"},
        {"role": "user", "content": "Show pathway analysis results."},
        {"role": "assistant", "content": "GeneAPIChat"},
        {"role": "user", "content": "I need to see Kegg analysis."},
        {"role": "assistant", "content": "GeneAPIChat"},
        {"role": "user", "content": "Can we use Enrichr API for our data?"},
        {"role": "assistant", "content": "GeneAPIChat"},
        {"role": "user", "content": "I want to perform enrichment analysis."},
        {"role": "assistant", "content": "GeneAPIChat"},  
        {"role": "user", "content": "Show gene-gene interaction."},
        {"role": "assistant", "content": "GeneAPIChat"}, 
        {"role": "user", "content": "interaction."},
        {"role": "assistant", "content": "GeneAPIChat"}, 
        {"role": "user", "content": "network"},
        {"role": "assistant", "content": "GeneAPIChat"}, 
        {"role": "user", "content": "Use STRING API to visualize interaction network"},
        {"role": "assistant", "content": "GeneAPIChat"}, 
        {"role": "user", "content": "Can you display the protein-protein interaction?"},
        {"role": "assistant", "content": "GeneAPIChat"},     
        {"role": "user", "content": "Search for articles on APOE"},
        {"role": "assistant", "content": "LiteratureSearch"}, 
        {"role": "user", "content": "Search for papers on Alzheimer"},
        {"role": "assistant", "content": "LiteratureSearch"}, 
        {"role": "user", "content": "Search for literature on Cognitive traits"},
        {"role": "assistant", "content": "LiteratureSearch"}, 
        {"role": "user", "content": "Search pubmed on APOE"},
        {"role": "assistant", "content": "LiteratureSearch"}, 
        {"role": "user", "content": "Search Google Scholar on APOE"},
        {"role": "assistant", "content": "LiteratureSearch."}, 
        {"role": "user", "content": "Search for articles on APOE in Arxiv"},
        {"role": "assistant", "content": "LiteratureSearch"}, 
        
        # User's current input
        {"role": "user", "content": user_input}
    ]
    # Try to get a response from the OpenAI model
    try:
        response = openai.ChatCompletion.create(
            engine=model_engine,  # Specify the model engine (e.g., ChatGPT or GPT-4)
            messages=messages,  # Provide the context and user input
            temperature=temperature,  # Set the temperature for response variability
            max_tokens=max_response_tokens  # Set the maximum number of tokens for the model's response
        )
        
        # Extract the classification from the model's response
        classification = response['choices'][0]['message']['content'].strip()
        # Uncomment the line below to display the classification in the Streamlit app
        #st.write(classification)
        
        return classification  # Return the classification result
    except Exception as e:
        # If an error occurs (e.g., API request issue), display the error in the Streamlit app and return None
        st.error(e)
        return None
def run():
    # Set Streamlit page configuration
    st.set_page_config(
        page_title="Home",  # Set the page title displayed in the browser tab
        page_icon="🏡",  # Set the page icon (favicon) as a house emoji
        layout="wide"  # Set the page layout to wide
    )

    # Create a faded background image for the entire page   
    bkgroundimage = load_image("images/appvideobkglogo.png")
    
    st.markdown(
    f"""
    <style>
        <!--! Set the background image using base64 string -->
        body {{
            background-image: url("data:image/png;base64,{bkgroundimage}");
            <!--! Ensure the background image covers the entire page -->
            background-size: cover;
            <!--! Background image does not repeat -->
            background-repeat: no-repeat;
            <!--! Background image is fixed during scrolling -->
            background-attachment: fixed;
            <!--! Set the opacity of the background image -->
            opacity: 0.95;
        }}
    </style>
    """,
    unsafe_allow_html=True,  # Allow HTML in the markdown for custom styling
    )
   
    # Adding CSS to make the sidebar auto-extend
    st.markdown(
        """
        <style>
            <!--! Allow vertical scrolling in the sidebar -->
            .sidebar .sidebar-content {
                overflow-y: auto !important;
                <!--! Auto-adjust the height of the sidebar -->
                height: auto !important;
            }
        </style>
        """,
        unsafe_allow_html=True,  # Allow HTML in the markdown for custom styling
    )
    
    # Load local images, convert to base64 and store them in variables for later use
    sbmilogo_base64 = load_image("images/sbmilogo.png")  # Load and encode the SBMI logo image
    litsearchlogo_base64 = load_image("images/litsearchlogo.png")  # Load and encode the literature search logo image
    geneapilogo_base64 = load_image("images/geneapilogo.png")  # Load and encode the Gene API logo image
    pgslogo_base64 = load_image("images/pgslogo.png")  # Load and encode the PGS logo image
    appvideobkglogo_base64 = load_image("images/appvideobkglogo.png")  # Load and encode the app video background logo image
    applogo_base64 = load_image("images/applogo.png")  # Load and encode the app logo image
    #videotutorial_base64 = load_video("videos/video_tutorial.mp4")  # Load and encode the video tutorial

    #HTML/CSS code for various style environments used as and when required to design the Home page
    st.markdown(
        """
        <style>
            /*Remove padding and margin from the main block*/
            .block-container {
                padding-top: 3rem;  
                padding-bottom: 2rem;  
            }
            /*Adjust top margin of the report*/
            .reportview-container .main .block-container {
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
            /*Define animation for a waving hand gesture*/
            .waving-hand {
                animation: wave-animation 1.5s infinite;
                transform-origin: 70% 70%;
                display: inline-block;
            }
            /*Define keyframes for wave animation*/
            @keyframes wave-animation {
                0% { transform: rotate( 0.0deg) }
                10% { transform: rotate(14.0deg) }  
                20% { transform: rotate(-8.0deg) }
                30% { transform: rotate(14.0deg) }
                40% { transform: rotate(-8.0deg) }
                50% { transform: rotate( 0.0deg) }  
                100% { transform: rotate( 0.0deg) }
            }
            /*Define animated heading style*/
            .animated-heading {
                animation: growShrink 3s ease-in-out infinite;
                font-size: 1.5em; 
            }
            /*Define keyframes for grow and shrink animation*/
            @keyframes growShrink {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            /*Style for generic content blocks*/
            .block {
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                text-align: left;
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);          
                margin-top: 5px;  
                background-color: #ADD8E6;
                color: #333;               
                margin-bottom: 5px;  
            }
            /*Define zoom animation keyframes*/
            @keyframes zoom {
              0%, 100% {
                transform: scale(1); /*Original size*/
              }
              50% {
                transform: scale(2); /*Zoom in 150%*/
              }
            }
            /*Style for zooming animation*/
            .zooming {
              margin-top: 50px;
              animation: zoom 20s ease-in-out infinite;
            }
            /*Define keyframes for spin animation*/
            @keyframes spin {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
            /*Style for rotating animation*/
            .rotating {
                animation: spin 4s linear infinite;
            }
            /*Add hover effect to blocks*/
            .block:hover {
                box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
            }
            /*Add background image and color to each block type*/
            .block1 {
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                text-align: left;
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                background-color: #CCCCFF;
                color: #333;
                          
            }
            .block2 {
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                text-align: left;          
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                background-color: #FFCCCC;
                color: #333;
                
            }
            /*Style for header-flex*/
            .header-flex {
                display: flex;
                align-items: center;
            }
            .block3 {
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                text-align: left;           
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                background-color: #DFFAD5;
                color: #333;
                
            }
            /*Add hover effect for growth and shrink*/
            .hover-grow-shrink {
                transition: transform 0.3s ease;
            }
            .hover-grow-shrink:hover {
                transform: scale(1.1);
            }
            /*Style for block4*/
            .block4 {
                border: none;  /*No border*/
                border-radius: 0px;
                padding: 0px;
                text-align: center;
                box-shadow: none;  /*No shadow*/
                margin-bottom: 10px;  /*Add vertical margin to create gap*/
            }
            /*Style for header with icon*/
            .header-with-icon {
                display: flex;
                align-items: center;
                font-size: 1.2em; /*Adjust as needed*/
            }
            /*Style for pointer icon*/
            .pointer-icon {
                margin-right: 1px; /*Space between icon and text*/
                font-size:2.0em
            }
            /*Style for click message*/
            .click-message {
                margin-left: 5px; /*Space between heading and message*/
                font-size: 1em; /*Smaller font size for message*/
                font-style: italic; /*Optional styling*/
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"""
                    <!--Create a header with flex alignment-->
                    <div class="header-flex">                 
                       <img src="data:image/png;base64,{applogo_base64}" width="100" height="100" style="opacity:0.7;">  
                       <h1 style="font-size: 28px;"> GENEVIC: GENetic data Exploration and Visualization Intelligent interactive Console</h1>                       
                    </div>
    """, unsafe_allow_html=True)


    # Sidebar style code HTML/CSS
    with st.sidebar:
    
        # Animated heading in the sidebar
        st.markdown(f"""<div class="animated-heading">Select a task from above ☝""", unsafe_allow_html=True)
        # Add margin at the bottom
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)  
        # Settings heading
        st.markdown(f"""Click Settings 👇 for Azure's Open AI credentials""", unsafe_allow_html=True)       
        # Button to toggle the visibility of settings
        st.button("Settings", on_click=toggleSettings)    
        # If the settings are to be shown, display the settings form
        if st.session_state['show_settings']:
            with st.form("AzureOpenAI"):
                st.title("Azure OpenAI Credentials")
                # Text input fields for Azure OpenAI settings
                st.text_input("ChatGPT deployment name:", value=st.session_state.chatgpt, key="txtChatGPT")
                st.text_input("GPT-4 deployment name (if not specified, default to ChatGPT's):", value=st.session_state.gpt4, key="txtGPT4")
                st.text_input("Azure OpenAI Endpoint:", value=st.session_state.endpoint, key="txtEndpoint")
                st.text_input("Azure OpenAI Key:", value=st.session_state.apikey, type="password", key="txtAPIKey")
                # Submit button for the form
                st.form_submit_button("Submit", on_click=saveOpenAI)
                
        # Section heading with hover effect for "Resources"
        # Section with links to tutorials, websites, databases, and code repositories 
        st.markdown(
            f"""
            <div class="header-with-icon">                   
              <h3 class="hover-grow-shrink"> Resources</h3>
              </div>              
              """,
         unsafe_allow_html=True,
         )
        
        # List of resources with links
        st.markdown(
            f"""
            <div>
                <ul style="list-style-type: none;">
                    <li> <a href='https://github.com/anath2110/GENEVIC_Supplementary/blob/main/Architecture_Workflow_Schema.png' target=_blank>GENEVIC Architecture</a> </li> 
                    <li> <a href='https://github.com/anath2110/GENEVIC_Supplementary/blob/main/Test%20Runs/Documenation_TestCasesExlained.pdf' target=_blank>Documentation</a> </li>
                    <li> <a href='https://github.com/anath2110/GENEVIC_Supplementary/tree/main/Tutorial' target=_blank>Tutorial</a> </li>
                    <li> <a href='https://github.com/anath2110/GENEVIC_Supplementary/blob/main/Tutorial/InstallationGuide.md' target=_blank>Install and Run GENEVIC</a> </li>
                    <li> <a href='https://github.com/anath2110/GENEVIC_Supplementary/blob/main/Tutorial/Azure%20Open%20AI%20Documentation.pdf' target=_blank>Azure OpenAI Instructions</a> </li>
                    <li> <a href='https://www.pgscatalog.org/' target=_blank>PGS Catalog Website</a> </li>
                    <li> <a href='https://github.com/anath2110/GENEVIC_Supplementary/tree/main/Database' target=_blank>PGS Rank Database</a> </li>                                    
                    <li> <a href='https://github.com/anath2110/GENEVIC_Supplementary/tree/main/Test%20Runs' target=_blank>Test Cases</a> </li>                  
                   <li> <a href='https://github.com/anath2110/GENEVIC.git' target=_blank> Code Repository</a> </li>                    
                </ul>
            </div>
            
            """,
         unsafe_allow_html=True,
        )        
        
        # Add margin at the bottom
        st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)

        # Using HTML and CSS to set image opacity for the SBMI logo
        st.markdown(
            f"""
           <img src="data:image/png;base64,{sbmilogo_base64}" width="250" height="100" style="opacity:0.3;">           
            """,
            unsafe_allow_html=True,
        )

        # Add margin at the bottom
        st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
        
        # Section heading with hover effect for "Meet the Team"
        # Section with links and information about the team and organization 
        st.markdown(
            f"""
            <div class="header-with-icon">                   
              <h3 class="hover-grow-shrink">Meet the Team</h3>
              </div>
            <div>
                <ul style="list-style-type: none;"> 
                    <li> <a href='https://www.uth.edu/bioinfo/' target=_blank>Bioinfo & Systems Medicine Lab </li>                   
                    <li> <a href='https://sbmi.uth.edu/' target=_blank>Organization: MSBMI, UTHH</a> </li>                    
                </ul>
            </div>
           
            """,
         unsafe_allow_html=True,
        )

        # Add empty space before the copyright text
        st.markdown("")
        for _ in range(1):
            st.sidebar.write("")

        # Add copyright symbol and "Anindita Nath 2024" to the sidebar
        # Copyright notice for the application 
        st.markdown(
        """
        <div style="position: relative; bottom: 1px; left: 10px;">
            &copy; Anindita Nath 2024
          
        </div>
        """,
        unsafe_allow_html=True,
        )
    # Gap between two placeholders
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # HTML content for each block
    block0_html = f"""
                <div class="block block">
                    <div class="header-flex">
                        <img src="data:image/png;base64,{appvideobkglogo_base64}" width="100" height="100" style="opacity:0.3;margin-right:30px;margin-bottom:20px;">                          
                        <h3 class="hover-grow-shrink">About GENEVIC</h3>                           
                    </div>                  
                    <ul style="list-style-type: none;">                        
                        <li> <strong>An intelligent chat assistant</strong></li> 
                        <li> GENEVIC is augmented by <strong>generative AI</strong> models implemented via Azure OpenAI platform</li>
                        <li> It supports Python's built-in SQLITE as well as your own Microsoft SQL Server </li>
                        <li> It can be run from your local host or Streamlit cloud </li>                         
                        <li> It is designed specifically to support research in <strong>Biomedicalinformatics</strong></li>                        
                        <li> Tasks that can be performed with GENEVIC:
                            <ul style="list-style-type: none;">  
                                <li> <strong> PGS Chat: Retrieve information from and visualize any custom database </strong></li>
                                <li> <strong> GeneAPI Chat: Explore Bioinformatics websites via automated API calls  </strong></li>
                                <li> <strong> Literature Search: Search for relevant literature evidence in well known portals</strong></li>
                            </ul>
                        </li>
                    </ul>
                   
                 </div>
                """
    block1_html =   f"""               
                
                <div class="block block1">                  
                    <div class="animated-heading">Click on heading below 👇 to go the respective <strong>task</strong> page!</div>   
                    <div class="header-flex">                         
                        <img src="data:image/png;base64,{pgslogo_base64}" width="100" height="100" style="opacity:0.3; margin-right:30px;margin-bottom:20px;">              
                        <div class="header-with-icon">                   
                            <h3 class="hover-grow-shrink"><a href='PGSChat' target=_blank>PGS Chat</a></h3>                           
                        </div> 
                        
                   </div>        
               
                <ul style="list-style-type: none;">
                    <li> <strong> Retrieve information from and visualize custom database</strong>
                    <li> Demo database: <strong>Polygenic Score(PGS) Rank Database</strong></li>
                    <ul style="list-style-type: none;">                      
                        <li> <strong>Code Writer</strong>: Auto-translate prompts/questions in natural language (e.g., English (US)) to SQL queries or Python code
                            <ul style="list-style-type: none;">
                                <li><strong>Steps to use this section:</strong>                      
                                    <ul style="list-style-type: none;">
                                        <li> Use a question from the Prompts or enter your own question</li>
                                        <li> You can select show code and/or show prompt to show SQL & Python code and the prompt behind the scene</li>
                                        <li> Click on submit to execute and see result</li>
                                        <li> For advanced questions such as forecasting, you can use GPT-4 (if available) as the engine</li>                                    
                                    </ul>
                                </li>
                            </ul>                                         
                            <ul style="list-style-type: none;">
                                <li><strong>Example prompts/questions</strong>:                           
                                    <ul style="list-style-type: none;">
                                        <li> Show the top 10 ranked genes for Alzheimer</li>
                                        <li> Plot distribution of ranks for the top 100 SNPs for Schizophrenia</li>                                                 
                                    </ul>
                                </li>
                            </ul>
                        </li>                                             
                        <li> Download the query results as CSV for retrospective analysis and interpretation</li>
                    </ul>
                    <li><strong> Query ChatGPT directly</strong> to generate more information or novel research hypothesis</li>
                </ul>                           
                </div>
     """
    block2_html =  f"""
        <div class="block block2">            
            <div class="animated-heading">Click on heading below 👇 to go the respective <strong>task</strong> page!</div>
            <div class="header-flex">                
                <img src="data:image/png;base64,{geneapilogo_base64}" width="100" height="100" style="opacity:0.3; margin-right:30px;margin-bottom:20px;">
                <div>
               <div class="header-with-icon">                   
                    <h3 class="hover-grow-shrink"><a href='GeneAPIChat' target=_blank>GeneAPI Chat</a></h3>                  
               </div> 
            </div>                  
            </div>            
            <ul style="list-style-type: none;">
                <li><strong>Explore external Bioinformatics websites via automated web API calls</strong>
                     <ul style="list-style-type: none;">
                        <li> Demo APIs explored: <strong> STRING </strong> and <strong> ENRICHR </strong>
                        <li> Generate <strong>gene-gene interaction network</strong>, one or more gene names as input
                                <ul style="list-style-type: none;">
                                   <li> Entire functionality of STRING API replicated as is</li>
                                   <li> Interactive in-app display of the netowrk </li>
                                </ul>
                        </li>
                        <li> Perform <strong>gene enrichment analysis</strong> with reference gene set libraries, given gene list as input
                                <ul style="list-style-type: none;">
                                   <li> Visualize the <strong>network graph</strong> </li> 
                                   <li> Download the enrichment results as CSV and/or the visualizations in known image formats
                                </ul>                       
                        </li>                        
                    </ul>
                </li>
             </ul>             
        </div>
        """
    block3_html =   f"""
        <div class="block block3">
            <div class="animated-heading">Click on heading below 👇 to go the respective <strong>task</strong> page!</div>
            <div class="header-flex">               
                <img src="data:image/png;base64,{litsearchlogo_base64}" width="100" height="100" style="opacity:0.3; margin-right:30px;margin-bottom:20px;">                
                <div class="header-with-icon">                   
                    <h3 class="hover-grow-shrink"><a href='LiteratureSearch' target=_self>Literature Search</a></h3>                         
                </div> 
            </div>            
            <ul style="list-style-type: none;">
                <li>Search for <strong>literature evidence in PubMed, Google Scholar, or Arxiv</strong>
                    <ul style="list-style-type: none;">
                        <li> Search in 1 or 2 or all of websites at the same time
                            <ul style="list-style-type: none;">
                                <li> <strong> Example search queries</strong>:
                                    <ul style="list-style-type: none;">
                                        <li> Search for articles with gene APOE and Alzheimer in Pubmed </li>
                                        <li> Search for articles with Schizophrenia in Google Scholar </li>
                                        <li> articles with gene TREM2 and Schizophrenia in Arxiv</li>
                                        <li> Search for articles with APOE gene name and trait Alzheimer</li>	 	 
                                    </ul>
                                </li>
                            </ul>
                        </li>
                        <li> Display the <strong>name</strong>and <strong>links</strong> of the articles for any given search query</li>
                        <li> Displays the <strong>abstract</strong> of the article, given its link as search query </li>
                    </ul>
                </li>
            </ul>
        </div>
        """
    
    # Divide the page into 4 columns:
    # 1st for the query search box
    # 2nd for the submit button and where the search results will be displayed
    # 3rd for the auto-scroll blocks describing each task page 
    # 4th for the video tutorial

    # Create two columns for the first row
    col1, col2 = st.columns([1,1])    
    # Create two columns for the second row
    col3, col4 = st.columns([1.5,1])  

    # Column 1: User input for query
    with col1:
        # User input text box for queries
        user_query = st.text_input("Ask where you want to go:")
        # Add margin at the bottom
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
        
    # Column 2: Submit button and display results
    with col2:
        # Add margin at the top
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        # Check if the required Azure OpenAI Deployment settings are provided
        
        # When the user clicks the submit button
        if st.button("Submit"):
            if st.session_state.get('apikey', '') == '' or st.session_state.get('endpoint', '') == '' or st.session_state.get('chatgpt', '') == '':
            # If any of the settings are missing, display an error message
                st.error("👈 Alert! You need to specify Azure's Open AI Credentials, click Settings on the left sidebar! ")
            else:
                # Load the classifier and categories
                #classifier = load_classifier()
                category_urls = category()
                # Predict the category of the user's query
                #result = classifier(user_query, list(category_urls.keys()))
                # Find the label with the highest score
                #highest_score_index = result["scores"].index(max(result["scores"]))
                #predicted_category, confidence = classify_query(user_query, classifier, list(category_urls.keys()))
                # Classify the user input using the OpenAI model
                predicted_category = classify_query_correctTaskpasge(user_query, max_response_tokens, temperature, st.session_state.chatgpt)
                #st.write(predicted_category)
                # Generate an HTML link to navigate to the corresponding Streamlit page
                if predicted_category in category_urls:
                    page_url = category_urls[predicted_category]
                    link_text = f"Go to {predicted_category} Page"
                    link_html = f'<a href="{page_url}" target=_blank>{link_text}</a>'
                    st.markdown(link_html, unsafe_allow_html=True)
        # Add margin at the bottom
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)       

    
    
    # Creating a footer
    
    # footer="""
    # <style>
        # a:link , a:visited{
        # color: blue;
        # background-color: transparent;
        # text-decoration: underline;
        # }

        # a:hover,  a:active {
        # color: red;
        # background-color: transparent;
        # text-decoration: underline;
        # }

        # .footer {
        # position: fixed;
        # left: 0;
        # bottom: 0;
        # width: 100%;
        # background-color: white;
        # color: black;
        # text-align: center;
        # }
    # </style>
    # <div class="footer">
        # <p>Developed with ❤️ by [Your Name]</p>
        # <p><a style='display: block; text-align: center;' href="https://www.yourwebsite.com" target="_blank">www.yourwebsite.com</a></p>
    # </div>
    # """
   
    #st.markdown(footer,unsafe_allow_html=True)       
   

    # Column 4: Video tutorial block
    with col4:
        # Text and icon indicating the video tutorial
        st.markdown(
            f"""
            <div style="text-align:left;margin-left:100px;margin-bottom:10px">
                <span class="pointer-icon" style="font-size: 32px;"> Take our Guided Tour 👇</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Placeholder for loading message or video
        video_placeholder = st.empty()            

        # Display loading message
        video_placeholder.markdown(
        f""" 
        <div style="text-align:left;margin-left:100px;margin-top:100px">
           <span style="font-size: 24px; color: #006400;">Please wait, the video tutorial is loading...Be patient for 15 secs!</span>
        </div>""",unsafe_allow_html=True
        )
        
        # Optional: Delay for a short period (e.g., 1 second)
        # This is to simulate the loading, but it's not a real check to see if the video has loaded
        time.sleep(0.1)
        
        # Display the video after the short delay
        # video_placeholder.markdown(
            # f"""<video width="600" height="450" poster="data:image/png;base64,{bkgroundimage}" controls>
                    # <source src="data:video/mp4;base64,{videotutorial_base64}" type="video/mp4">
                # </video>           
            # """,
            # unsafe_allow_html=True
        # )
        video_placeholder.markdown(
            f"""
            <style>
                .video-iframe {{
                    width: 400px;
                    height: 400px;
                    border: 2px solid;
                    scrolling: no;
                    margin-left: 70px; /* Adjust this value to move the video to the left */
                    transform: scale(1); /* Initial scale */
                    transition: transform 0.3s ease, opacity 0.3s ease; /* Smooth transition for transformation and opacity */
                }}
                .video-iframe:hover {{
                    transform: scale(1.1); /* Slightly enlarge the iframe on hover */
                    opacity: 0.9; /* Slightly reduce opacity on hover */
                }}
            </style>
            <iframe class="video-iframe" src="https://www.youtube.com/embed/3d6GhuoiVHU" allowfullscreen="true" frameborder="0"></iframe>
            """, unsafe_allow_html=True)
     # Column 3: Auto-scroll blocks describing each task page
    with col3:
       
        #Create an empty placeholder for blocks
        placeholder = st.empty()

        # List of block contents (HTML content)
        block_contents = [block0_html, block1_html, block2_html, block3_html]

        # Time delay in seconds between each block's content
        delay = 3
        # Infinite loop to auto-scroll blocks
        while True:
            # Loop to update the placeholder with each block's content
            for content in block_contents:
                placeholder.markdown(content, unsafe_allow_html=True)
                time.sleep(delay)
        # List of block contents (HTML content)
        # block_contents = [block0_html, block1_html, block2_html, block3_html]

        # # Initialize session state for current block index if not already initialized
        # if 'current_block_index' not in st.session_state:
            # st.session_state.current_block_index = 0
        # # Center the button using columns
        # col1, col2= st.columns([1,0.5])
        # with col1:
            # # Create an empty placeholder for blocks
            # placeholder = st.empty()

            # # Display the current block in the placeholder
            # placeholder.markdown(block_contents[st.session_state.current_block_index], unsafe_allow_html=True)

       
        # # Place the button in the center column
        # with col2:
            # # Add margin at the bottom
            # st.markdown("<div style='margin-bottom: 150px;'></div>", unsafe_allow_html=True)       

            # # When the button is clicked, increment the index and update the placeholder
            # if st.button('Click for Next task ', key='next_button'):
                # # Increment the current block index
                # st.session_state.current_block_index = (st.session_state.current_block_index + 1) % len(block_contents)
                # # Update the placeholder with the new block content
                # placeholder.markdown(block_contents[st.session_state.current_block_index], unsafe_allow_html=True)

if __name__ == "__main__":
    run()

