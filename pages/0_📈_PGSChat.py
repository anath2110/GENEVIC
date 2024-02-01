'''
Author: Anindita Nath
Job Title: Postdoctoral Research Fellow
Location: Bioinformatics and Systems Medicine Laboratory, MSBMI, UTHH
Date: August, 2023 - January 2024
#.........................................................................................
Modified from original found at:https://github.com/Microsoft-USEduAzure/OpenAIWorkshop.git
#.........................................................................................
Purpose: Front-end design and back-end fucntionality of the PGS Chat page
'''
#..........................................................................................

# Importing essential libraries and modules
import streamlit as st  # Web app framework
import pandas as pd  # Data manipulation
import numpy as np  # Numerical operations
import plotly.express as px  # Visualization library
import plotly.graph_objs as go  # Visualization library
from analyze import AnalyzeGPT, SQL_Query, ChatGPT_Handler  # Custom modules for GPT analysis, SQL queries, and ChatGPT handling
import openai  # OpenAI's API for GPT models
from pathlib import Path  # File path manipulation
from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Operating system interfaces
import datetime  # Date and time operations
import base64  # Base64 encoding/decoding

# Function to read local image and convert to base64
def load_image(image_path):
    # Open the image file in binary read mode, encode it to base64, and return the encoded string
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
      

# Check if the environment is local or Azure, then load environment variables
if os.getenv('WEBSITE_SITE_NAME') is None:
    # If running locally, load environment variables from the 'secrets.env' file
    env_path = Path('.') / 'secrets.env'
    load_dotenv(dotenv_path=env_path)
    

# Function to load settings from environment or set to default
def load_setting(setting_name, session_name, default_value=''): 
    # Load the setting into Streamlit's session state or use the default value if not present in the environment
    if session_name not in st.session_state:  
        if os.environ.get(setting_name) is not None:
            st.session_state[session_name] = os.environ.get(setting_name)
        else:
            st.session_state[session_name] = default_value
        

# Load API, SQL, and other settings from the environment into the session state for global access within the app
load_setting("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "chatgpt", "gpt-35-turbo")  
load_setting("AZURE_OPENAI_GPT4_DEPLOYMENT", "gpt4", "gpt-35-turbo")  
load_setting("AZURE_OPENAI_ENDPOINT", "endpoint", "https://resourcenamehere.openai.azure.com/")  
load_setting("AZURE_OPENAI_API_KEY", "apikey")  
load_setting("SQL_ENGINE", "sqlengine", "sqlite")
load_setting("SQL_SERVER", "sqlserver")
load_setting("SQL_DATABASE", "sqldatabase")
load_setting("SQL_USER", "sqluser")
load_setting("SQL_PASSWORD", "sqlpassword")
load_setting("SQLITE_DB_PATH", "sqlitedbpath", "data/PGSrankDB.db")


# Initialize show_settings in session state if not already present
if 'show_settings' not in st.session_state:
    # A flag in session state to control the visibility of settings in the app (e.g., for admin or debug use)  
    st.session_state['show_settings'] = False      


# Function to save OpenAI and SQL settings into session state
def saveOpenAI():
    # Copy the settings from temporary text box state to session state
    st.session_state.chatgpt = st.session_state.txtChatGPT
    st.session_state.gpt4 = st.session_state.txtGPT4
    st.session_state.endpoint = st.session_state.txtEndpoint
    st.session_state.apikey = st.session_state.txtAPIKey
    st.session_state.sqlengine = st.session_state.txtSQLEngine
    st.session_state.sqlitedbpath = st.session_state.txtSQLiteDBPath  # Save the SQLite DB path
    
    st.session_state.sqlserver = st.session_state.txtSQLServer
    st.session_state.sqldatabase = st.session_state.txtSQLDatabase
    st.session_state.sqluser = st.session_state.txtSQLUser
    st.session_state.sqlpassword = st.session_state.txtSQLPassword

    # Close the settings panel after saving
    st.session_state['show_settings'] = False

# Function to toggle the visibility of the settings panel
def toggleSettings():
    # Invert the show_settings flag to show/hide the settings panel
    st.session_state['show_settings'] = not st.session_state['show_settings']

# Function to make queries to Chat GPT directly
def chat_with_gpt(questions,max_response_tokens,temperature,sessionchatgptmodel):
    combined_responses = []
    
    try:
        # Structure the user message for OpenAI Chat API
        user_message = {
            "role": "user",
            "content": questions
        }
        assistant_messages = [user_message]

        # Make a request to OpenAI Chat API with the user message
        response = openai.ChatCompletion.create(
            engine=sessionchatgptmodel,
            temperature=temperature,
            max_tokens=max_response_tokens,
            messages=assistant_messages
        )

        # Parse the response from OpenAI Chat API
        if 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0] and 'content' in response['choices'][0]['message']:
            combined_responses.append(response['choices'][0]['message']['content'].strip())
        else:
            combined_responses.append("Unexpected API response format.")
    except Exception as e:
        # Append error message in case of an exception
        combined_responses.append(f"An error occurred: {e}")
    return combined_responses

# Set OpenAI API configurations
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview" 
openai.api_key = st.session_state.apikey
openai.api_base = st.session_state.endpoint

# Set some constants for OpenAI API
max_response_tokens = 1250
token_limit= 4096
temperature=0

# Initialize the Streamlit app with page configurations
st.set_page_config(page_title="PGSChat", page_icon="📈", layout="wide")

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

# Create columns for the Streamlit app layout
col1, col2 = st.columns((3,1)) # Divide the page into two columns with ratios 3:1

# Initialize a variable to hold any potential error messages
error_message = None

# Sidebar layout and options
with st.sidebar:   
    # Define the options for the sidebar radio button
    options = ("Retrieve from DB", "Visualize DB","Query ChatGPT directly")
    # Create a radio button for user to choose an option    
    index = st.radio("Choose what to do:", range(len(options)), format_func=lambda x: options[x])
    # Option 0: Retrieve from Database
    if index == 0:
        # Display heading in the main column
        with col1:  
            # Display heading in the main column
            st.markdown(f"""<h1 style="font-size: 32px;">Retrieve information from custom database 📈</h1>""", unsafe_allow_html=True)
        # Define a system message for interaction with SQL database
        system_message="""
        You are an agent designed to interact with a SQL database with schema detail in <<data_sources>>.
        Given an input question, create a syntactically correct {sql_engine} query to run, then look at the results of the query and return the answer.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        Remember to format SQL query as in ```sql\n SQL QUERY HERE ``` in your response.
        """
        # Initialize few_shot_examples variable (content not shown for brevity)        
        few_shot_examples=""
        # Define patterns for extracting SQL queries from ChatGPT responses
        extract_patterns = [('sql', r"```sql\n(.*?)```")]
        
        # Initialize a ChatGPT handler with the extract patterns
        extractor = ChatGPT_Handler(extract_patterns=extract_patterns)

        # Define prompts for ChatGPT and GPT-4 (content not shown for brevity)
        prompts_dict = { 
           "ChatGPT": [  
                        "Show all information corresponding to top ranked genes, ranked from top to bottom in Alzheimer.",
                        "Show the gene and rank, ranked from top to bottom.",
                        "Show the gene and rank, ranked from top to bottom. If duplicate, show only once.",
                        "Display the genes with top ranks first and their ranks corresponding to each PGS score.",
                        "How often does APOE gene occur in Alzheimer?",
                        "Show all information corresponding to the SNP ids that are top-ranked for Alzheimer.",
                        "What are the top 5 most frequently occurring gene in Alzheimer?",
                        "How often does gene APOE occur for Alzheimer?",
                        "Show genes and their frequency for ALzheimer that occur less frequently than APOE?",
                        "Show all information for SNPs with top ranks. If duplicate, show only once.",
                        "Show gene, variants and ranks for SNPs with top ranks. If duplicate, show only once.",
                        "List the variants with top ranks and corresponding all info associated with European Ancestry.",
                        "Plot the PGS score IDs and other info for the top 5 genes with top ranks displayed first in Alzheimer.",
                        "Plot a bar plot  top 5 most frequently occurring gene in Alzheimer.",
                        "Plot the PGS score IDs and their count in European Ancestory for Alzheimer." ,
            ],  
            "GPT-4": [  
                        "Show all information corresponding to top ranked genes, ranked from top to bottom in Alzheimer.",
                        "Show the gene and rank, ranked from top to bottom.",
                        "Show the gene and rank, ranked from top to bottom. If duplicate, show only once.",
                        "Display the genes with top ranks first and their ranks corresponding to each PGS score.",
                        "How often does APOE gene occur in Alzheimer?",
                        "Show all information corresponding to the SNP ids that are top-ranked for Alzheimer.",
                        "What are the top 5 most frequently occurring gene in Alzheimer?",
                        "How often does gene APOE occur for Alzheimer?",
                        "Show genes and their frequency for ALzheimer that occur less frequently than APOE?",
                        "Show all information for SNPs with top ranks. If duplicate, show only once.",
                        "Show gene, variants and ranks for SNPs with top ranks. If duplicate, show only once.",
                        "List the variants with top ranks and corresponding all info associated with European Ancestry.",
                        "Plot the PGS score IDs and other info for the top 5 genes with top ranks displayed first in Alzheimer.",
                        "Plot a bar plot  top 5 most frequently occurring gene in Alzheimer.",
                        "Plot the PGS score IDs and their count in European Ancestory for Alzheimer." ,
            ]  
        }  
    # Option 1: Visualize Database
    elif index == 1:
        with col1:
            # Display heading in the main column
            st.markdown(f"""<h1 style="font-size: 32px;">Visualize custom database 📈</h1>""", unsafe_allow_html=True)
        #Define a system message for visualizing and analyzing data       
        system_message="""
        You are a smart AI assistant to help answer business questions based on analyzing data. 
        You can plan solving the question with one more multiple thought step. At each thought step, you can write python code to analyze data to assist you. Observe what you get at each step to plan for the next step.
        You are given following utilities to help you retrieve data and commmunicate your result to end user.
        1. execute_sql(sql_query: str): A Python function can query data from the <<data_sources>> given a query which you need to create. The query has to be syntactically correct for {sql_engine} and only use tables and columns under <<data_sources>>. The execute_sql function returns a Python pandas dataframe contain the results of the query.
        2. Use plotly library for data visualization. 
        3. Use observe(label: str, data: any) utility function to observe data under the label for your evaluation. Use observe() function instead of print() as this is executed in streamlit environment. Due to system limitation, you will only see the first 10 rows of the dataset.
        4. To communicate with user, use show() function on data, text and plotly figure. show() is a utility function that can render different types of data to end user. Remember, you don't see data with show(), only user does. You see data with observe()
            - If you want to show  user a plotly visualization, then use ```show(fig)`` 
            - If you want to show user data which is a text or a pandas dataframe or a list, use ```show(data)```
            - Never use print(). User don't see anything with print()
        5. Lastly, don't forget to deal with data quality problem. You should apply data imputation technique to deal with missing data or NAN data.
        6. Always follow the flow of Thought: , Observation:, Action: and Answer: as in template below strictly. 

        """
        # Initialize few_shot_examples variable (content not shown for brevity)
       
        few_shot_examples="""
        <<Template>>
        Question: User Question
        Thought 1: Your thought here.
        Action: 
        ```python
        #Import neccessary libraries here
        import numpy as np
        #Query some data 
        sql_query = "SOME SQL QUERY"
        step1_df = execute_sql(sql_query)
        # Replace NAN with 0. Always have this step
        step1_df['Some_Column'] = step1_df['Some_Column'].replace(np.nan,0)
        #observe query result
        observe("some_label", step1_df) #Always use observe() instead of print
        ```
        Observation: 
        step1_df is displayed here
        Thought 2: Your thought here
        Action:  
        ```python
        import plotly.express as px 
        #from step1_df, perform some data analysis action to produce step2_df
        #To see the data for yourself the only way is to use observe()
        observe("some_label", step2_df) #Always use observe() 
        #Decide to show it to user.
        fig=px.line(step2_df)
        #visualize fig object to user.  
        show(fig)
        #you can also directly display tabular or text data to end user.
        show(step2_df)
        ```
        Observation: 
        step2_df is displayed here
        Answer: Your final answer and comment for the question. Also use Python for computation, never compute result youself.
        <</Template>>

        """
        # Define patterns for extracting thoughts, actions, and answers from ChatGPT responses        
        extract_patterns=[("Thought:",r'(Thought \d+):\s*(.*?)(?:\n|$)'), ('Action:',r"```python\n(.*?)```"),("Answer:",r'([Aa]nswer:) (.*)')]
         # Initialize a ChatGPT handler with the extract patterns        
        extractor = ChatGPT_Handler(extract_patterns=extract_patterns)
        # Define prompts for ChatGPT or GPT-4        
        prompts_dict = {  
            "ChatGPT": [  
                         "Show all information corresponding to top ranked genes, ranked from top to bottom in Alzheimer.",
                        "Show the gene and rank, ranked from top to bottom.",
                        "Show the gene and rank, ranked from top to bottom. If duplicate, show only once.",
                        "Display the genes with top ranks first and their ranks corresponding to each PGS score.",
                        "How often does APOE gene occur in Alzheimer?",
                        "Show all information corresponding to the SNP ids that are top-ranked for Alzheimer.",
                        "What are the top 5 most frequently occurring gene in Alzheimer?",
                        "How often does gene APOE occur for Alzheimer?",
                        "Show genes and their frequency for ALzheimer that occur less frequently than APOE?",
                        "Show all information for SNPs with top ranks. If duplicate, show only once.",
                        "Show gene, variants and ranks for SNPs with top ranks. If duplicate, show only once.",
                        "List the variants with top ranks and corresponding all info associated with European Ancestry.",
                        "Plot the PGS score IDs and other info for the top 5 genes with top ranks displayed first in Alzheimer.",
                        "Plot a bar plot  top 5 most frequently occurring gene in Alzheimer.",
                        "Plot the PGS score IDs and their count in European Ancestory for Alzheimer." ,

            ],  
            "GPT-4": [  
                        "Show all information corresponding to top ranked genes, ranked from top to bottom in Alzheimer.",
                        "Show the gene and rank, ranked from top to bottom.",
                        "Show the gene and rank, ranked from top to bottom. If duplicate, show only once.",
                        "Display the genes with top ranks first and their ranks corresponding to each PGS score.",
                        "How often does APOE gene occur in Alzheimer?",
                        "Show all information corresponding to the SNP ids that are top-ranked for Alzheimer.",
                        "What are the top 5 most frequently occurring gene in Alzheimer?",
                        "How often does gene APOE occur for Alzheimer?",
                        "Show genes and their frequency for ALzheimer that occur less frequently than APOE?",
                        "Show all information for SNPs with top ranks. If duplicate, show only once.",
                        "Show gene, variants and ranks for SNPs with top ranks. If duplicate, show only once.",
                        "List the variants with top ranks and corresponding all info associated with European Ancestry.",
                        "Plot the PGS score IDs and other info for the top 5 genes with top ranks displayed first in Alzheimer.",
                        "Plot a bar plot  top 5 most frequently occurring gene in Alzheimer.",
                        "Plot the PGS score IDs and their count in European Ancestory for Alzheimer." ,
            ]  
        } 
    # Option 2: Query ChatGPT directly
    elif index == 2:
        with col1:
           # Display heading in the main column
          st.markdown(f"""<h1 style="font-size: 32px;">Query ChatGPT directly</h1>""", unsafe_allow_html=True)
         # Define a system message for querying ChatGPT directly
        system_message="""
            You are a smart AI assistant to help answer biomedical research question based on the prompt.            

            """
        # Define prompts for ChatGPT and GPT-4 (content not shown for brevity)
        prompts_dict = {  
            "ChatGPT": [  
                "Functional annotation of the genes: [Paste the gene names separated by comma as a list here]"
         

            ],  
            "GPT-4": [  
               "Functional annotation of the genes: [Paste the gene names separated by comma as a list here]"
            ]  
        } 
    # Add margin at the bottom
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)  
    # Settings heading
    st.markdown(f"""Click Settings 👇 for Open AI and DataBase Credentials""", unsafe_allow_html=True)    
    # Implement settings button with a toggle functionality
    st.button("Settings",on_click=toggleSettings)
    # If the settings are to be shown, display the settings panel
    if st.session_state['show_settings']:  
         # Form for Azure OpenAI settings
        with st.form("AzureOpenAI"):
            
            st.title("Azure OpenAI Credentials")
            # Text input fields for OpenAI settings
            st.text_input("ChatGPT deployment name:", value=st.session_state.chatgpt,key="txtChatGPT")  
            st.text_input("GPT-4 deployment name (if not specified, default to ChatGPT's):", value=st.session_state.gpt4,key="txtGPT4") 
            st.text_input("Azure OpenAI Endpoint:", value=st.session_state.endpoint,key="txtEndpoint")  
            st.text_input("Azure OpenAI Key:", value=st.session_state.apikey, type="password",key="txtAPIKey")
            
            st.write("Select Database")
             # Radio button and text input fields for SQL settings
            st.radio("Choose SQL Engine:",["sqlite","sqlserver"],index=0,key="txtSQLEngine")
            st.text_input("SQLite Database Path:", value=st.session_state.sqlitedbpath, key="txtSQLiteDBPath")  # Textbox for SQLite DB Path
    
            st.write("SQL Server Settings (Optional)")
            st.text_input("SQL Server:", value=st.session_state.sqlserver,key="txtSQLServer")  
            st.text_input("Database:", value=st.session_state.sqldatabase,key="txtSQLDatabase")
            st.text_input("User:", value=st.session_state.sqluser,key="txtSQLUser")  
            st.text_input("Password:", type="password",value=st.session_state.sqlpassword,key="txtSQLPassword")
            
            # Submit button for the form
            st.form_submit_button("Submit",on_click=saveOpenAI)
    # Prepare list of chat models based on user settings
    chat_list=[]
    if st.session_state.chatgpt != '':
        chat_list.append("ChatGPT")
    if st.session_state.gpt4 != '':
        chat_list.append("GPT-4")
    # Dropdown to select the GPT model
    gpt_engine = st.selectbox('GPT Model', chat_list)  
    
    # Update the GPT model and prompts based on user selection
    if gpt_engine == "ChatGPT":  
        gpt_engine = st.session_state.chatgpt  
        prompts = prompts_dict["ChatGPT"]  
    else:  
        gpt_engine = st.session_state.gpt4
        prompts = prompts_dict["GPT-4"]  
    
    # Dropdown to select the prompt
    option = st.selectbox('Prompts',prompts)  

    # Show code and prompt checkboxes for Retrieve from DB and Visualize DB options
    if index!=2:
        show_code = st.checkbox("Show code", value=False)  
        show_prompt = st.checkbox("Show prompt", value=False)
   
    # Text area for user to ask a question
    question = st.text_area("Ask me a question", option)
    if index==2:     
        # File uploader for Query ChatGPT directly option
        uploaded_file = st.file_uploader("You may also upload a CSV file with your gene list", type="csv")
        
     # Submit button for the form
    if st.button("Submit"): 
        if index!=2:
            # Validate settings and perform operations based on the selected index
            if st.session_state.apikey == '' or st.session_state.endpoint == '' or st.session_state.chatgpt == '' or st.session_state.sqlengine == '':
                error_message=("You need to specify OpenAI credentials, click Settings on the left sidebar!")
            elif st.session_state.sqlengine =="sqlserver" and (st.session_state.sqlserver == '' or st.session_state.sqldatabase == '' or st.session_state.sqluser == '' or st.session_state.sqlpassword == ''):
                error_message=("You need to specify SQL Server connection details, click Settings on the left sidebar!")
            else:
                if st.session_state.sqlengine =="sqlserver":
                    sql_query_tool = SQL_Query(driver='ODBC Driver 17 for SQL Server',dbserver=st.session_state.sqlserver, database=st.session_state.sqldatabase, db_user=st.session_state.sqluser ,db_password=st.session_state.sqlpassword)
                elif st.session_state.sqlengine == "sqlite":
                    if st.session_state.sqlitedbpath is not None and st.session_state.sqlitedbpath.strip() != '' and os.path.exists(st.session_state.sqlitedbpath):
                        # Proceed with database operations
                        sql_query_tool = SQL_Query(db_path=st.session_state.sqlitedbpath)
                    else:
                        error_message=("SQLITE database Path is empty, click Settings on the left sidebar!!")
                # Code for validation and operation based on the selected index
                analyzer = AnalyzeGPT(sql_engine=st.session_state.sqlengine,content_extractor= extractor, sql_query_tool=sql_query_tool,  system_message=system_message, few_shot_examples=few_shot_examples,st=st,  
                                    gpt_deployment=gpt_engine,max_response_tokens=max_response_tokens,token_limit=token_limit,  
                                    temperature=temperature)  
                if index==0:
                    # Code for validation and operation based on the selected index
                    analyzer.query_run(question,show_code,show_prompt, col1)  
                elif index==1:
                    # Code for validation and operation based on the selected index
                    analyzer.run(question,show_code,show_prompt, col1)
                  
                        
                else:
                    error_message=("Not implemented yet!")
        elif index==2:           

            # Make sure all the required settings are provided
            if st.session_state.apikey == '' or st.session_state.endpoint == '':
                error_message=("You need to specify OpenAI credentials, see left sidebar!")
                
            else:
                error_message=None
                # Call OpenAI API here
                openai.api_key = st.session_state.apikey
                openai.api_base = st.session_state.endpoint
                model_engine =  st.session_state.chatgpt  # Replace with the model you are using
                if st.session_state.chatgpt!="":
                    
                    csv_genelist = []
                    with col1:
                        # Read and display CSV contents
                        if uploaded_file is not None:
                            df = pd.read_csv(uploaded_file)
                            st.write(df)
                            csv_genelist = df['gene'].tolist()

                            # Text input for direct question
                            additional_question = question

                            # Combine questions from CSV and text input
                            questions_to_ask = additional_question + ','.join(csv_genelist)
                        elif uploaded_file is None:
                            questions_to_ask = question
                        
                        if questions_to_ask:
                            st.write("Questions to be asked:")
                            
                            st.write(questions_to_ask)
                            if(error_message):
                                st.error(error_message)
                            else:
                                # Make API calls for the combined questions
                                responses = chat_with_gpt(questions_to_ask,max_response_tokens,temperature,st.session_state.chatgpt)                            
                                st.write(responses[0].strip())
               
                elif st.session_state.gpt4!="":
                    csv_genelist = []
                    with col1:
                        # Read and display CSV contents
                        if uploaded_file is not None:
                            df = pd.read_csv(uploaded_file)
                            st.write(df)
                            
                            csv_genelist = df['gene'].tolist()

                            # Text input for direct question
                            additional_question = question

                            # Combine questions from CSV and text input
                            questions_to_ask = additional_question + ','.join(csv_genelist)
                        elif uploaded_file is None:
                            questions_to_ask = question
                        
                        if questions_to_ask:
                            st.write("Questions to be asked:")
                            
                            st.write(questions_to_ask)
                            if(error_message):
                                st.error(error_message)
                            else:
                                # Make API calls for the combined questions
                                responses = chat_with_gpt(questions_to_ask,max_response_tokens,temperature,st.session_state.gpt4)                            
                                st.write(responses[0].strip())
                    




if(error_message):
    st.error(error_message)
else:
    st.write("")