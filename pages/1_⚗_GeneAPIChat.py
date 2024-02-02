'''
Author: Anindita Nath
Job Title: Postdoctoral Research Fellow
Location: Bioinformatics and Systems Medicine Laboratory, MSBMI, UTHH
Date: August, 2023 - January 2024
#..............................................................................
References:
STRING API Documentation: https://string-db.org/help/api/
ENRICHR API Documentation:https://maayanlab.cloud/Enrichr/help#api
#..............................................................................
Purpose: Front-end design and back-end fucntionality of the GeneAPI Chat page
'''
#...............................................................................

import streamlit as st  # Web app framework for Python, used for creating web applications
import pandas as pd  # Data manipulation and analysis library
import numpy as np  # Library for numerical operations
import networkx as nx  # Library for creating and studying complex networks
import plotly.express as px  # Visualization library for creating interactive plots
import plotly.graph_objs as go  # Graph objects for detailed plot configurations in Plotly
from analyze import AnalyzeGPT, SQL_Query, ChatGPT_Handler  # Custom modules for GPT analysis, SQL queries, and ChatGPT handling
import openai  # OpenAI's API for GPT models
from pathlib import Path  # File path manipulation
from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Operating system interfaces
import datetime  # Date and time operations
import base64  # Base64 encoding/decoding
import streamlit.components.v1 as components  # Components for Streamlit, used for integrating web components
import json  # Library for JSON operations
import requests  # Library for making HTTP requests
import sys  # System-specific parameters and functions
import io  # I/O core tools
import matplotlib.pyplot as plt  # Visualization library for 2D plots
import gseapy  # Gene set enrichment analysis library
import seaborn as sns  # Visualization library based on matplotlib, provides a high-level interface for drawing attractive statistical graphics
#import mpld3  # Matplotlib to D3 converter. (Commented out, not in use)



# Function to read a local image and convert it to a base64-encoded string
def load_image(image_path):
    # Open the image file in binary read mode ('rb')
    with open(image_path, "rb") as img_file:
        # Read the file, encode it in base64, and decode the bytes to a string
        return base64.b64encode(img_file.read()).decode()

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


def classify_choosecorrectAPI(user_input, max_response_tokens, temperature, model_engine):
    # Define the conversation context and examples for the OpenAI model
    messages = [
        # System message describing the assistant's role
        {"role": "system", "content": "You are a helpful assistant classifying user commands into either 'show_gene_network' or 'show_enrichment_uploader'."},

        # Predefined conversation examples guiding the model for classification
        {"role": "user", "content": "Show gene-gene interaction."},
        {"role": "assistant", "content": "Classification: show_gene_network."},
        {"role": "user", "content": "I want to see the interaction network."},
        {"role": "assistant", "content": "Classification: show_gene_network."},
        {"role": "user", "content": "Use STRING API to visualize interaction network"},
        {"role": "assistant", "content": "Classification: show_gene_network."},
        {"role": "user", "content": "Can you display the protein-protein interaction?"},
        {"role": "assistant", "content": "Classification: show_gene_network."},
        {"role": "user", "content": "Show pathway analysis results."},
        {"role": "assistant", "content": "Classification:show_enrichment_uploader."},
        {"role": "user", "content": "I need to see Kegg analysis."},
        {"role": "assistant", "content": "Classification:show_enrichment_uploader."},
        {"role": "user", "content": "Can we use Enrichr API for our data?"},
        {"role": "assistant", "content": "Classification:show_enrichment_uploader."},
        {"role": "user", "content": "I want to perform enrichment analysis."},
        {"role": "assistant", "content": "Classification:show_enrichment_uploader."},  
        
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
        st.write(classification)
        
        return classification  # Return the classification result
    except Exception as e:
        # If an error occurs (e.g., API request issue), display the error in the Streamlit app and return None
        st.error(e)
        return None


#This function reads an HTML file (interactivenetwork.html) which likely contains an interactive network visualization
#(e.g., a gene interaction network). 
#It then displays this visualization within the Streamlit app using Streamlit's components.html function. 
#The height, width, and scrolling parameters are configured to ensure the visualization is displayed effectively.

def show_gene_network():
    # Open the HTML file containing the interactive network visualization
    HtmlFile = open("interactivenetwork.html", 'r', encoding='utf-8')
    # Read the content of the file
    source_code = HtmlFile.read()
    # Display the HTML content within the Streamlit app
    components.html(source_code, height=1000, width=1000, scrolling=True)

#Following functions collectively provide tools for network graph construction, 
#node coloring, and distribution analysis, 
#which can be integral parts of a data analysis pipeline in genomics or related fields.
#...............................................................................................

#This function performs enrichment analysis on a list of genes using the gseapy.enrichr function.
#It accepts a pandas DataFrame or Series (genelist) with gene names, a selected library or collection of gene sets (selected_library), 
#and a path to save the results (folder_path). The function then saves the results of the enrichment analysis in a CSV file
#at the specified folder path and displays a message in the Streamlit app indicating where the results are saved.

def enrichr_function(genelist, selected_library, folder_path):
    # Extract gene list from the input data
    genes = genelist["gene"]
    
    # Perform enrichment analysis using the gseapy library
    enr_res = gseapy.enrichr(
        gene_list=genes,
        organism='human',
        gene_sets=selected_library,  # Use the selected gene set library
        cutoff=0.5  # Set the cutoff for the analysis
    )
    
    # Ensure the output folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Define the output file name based on the selected library
    if len(selected_library) == 0:
        output_file = os.path.join(folder_path, "enrichment_results_" + selected_library + ".csv")
    else:
        output_file = os.path.join(folder_path, "enrichment_results_multiplegenesets.csv")
    
    # Save the enrichment analysis results to a CSV file
    enr_res.results.to_csv(output_file, index=False)
    
    # Display a message in the app with the path to the results file
    st.write(f"Enrichment analysis results saved to {output_file}")
   
#This function constructs a network graph from the given data based on a specified p-value cutoff.
def create_network_graph(data, p_value_cutoff):
    # Initialize a new graph
    G = nx.Graph()
    
    # Iterate through each row in the data
    for _, row in data.iterrows():
        # Check if the row meets the p-value cutoff condition
        if row['Adjusted P-value'] <= p_value_cutoff:
            # Get the term and create a node for it
            term = row['Term']
            G.add_node(term, type='term')
            
            # Split the genes string and create nodes and edges for each gene
            genes = row['Genes'].split(';')
            for gene in genes:
                G.add_node(gene, type='gene')  # Add gene node
                G.add_edge(term, gene)  # Add edge between term and gene
    return G
    
#This function provides a simple way to get the color for a node in the network graph based on its type.
def get_node_color(node_type):
    # Return color based on node type
    if node_type == 'term':
        return 'blue'  # Color for term nodes
    else:
        return 'green'  # Color for gene nodes
        
#This function analyzes the categorical distribution of gene sets based on a p-value cutoff.
def create_categorical_distribution(data, p_value_cutoff):
    # Filter data based on the p-value cutoff
    filtered_data = data[data['Adjusted P-value'] <= p_value_cutoff]
    
    # Group data by gene set and count the occurrences
    distribution = filtered_data['Gene_set'].value_counts().reset_index()
    distribution.columns = ['Gene_set', 'Count']
    
    return distribution
#This function constructs a network graph using the create_network_graph function and visualizes it interactively using Plotly. 
#Nodes represent terms and genes, and edges represent associations between them. 
#The nodes are colored based on their type ('term' or 'gene').

#In the categorical distribution visualization, the function displays the distribution of gene sets as a bar plot. 
#It shows how many times each gene set appears in the data that meets the p-value cutoff,
#providing insights into the prevalence of different gene sets.
def enrichrvisualization_function(enrichment_data, selected_visualization, p_value_cutoff):
    # Check if the selected visualization is "Network Graph"
    if selected_visualization == "Network Graph":
        # Create a network graph from the enrichment data with a p-value cutoff
        G = create_network_graph(enrichment_data, p_value_cutoff)

        # Use NetworkX's spring layout algorithm for node positioning
        pos = nx.spring_layout(G)
        edge_x = []
        edge_y = []
        # Iterate through each edge in the graph to prepare for edge plotting
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])  # Add edge x-coordinates
            edge_y.extend([y0, y1, None])  # Add edge y-coordinates

        # Prepare the edge trace for Plotly
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),  # Line style for edges
            hoverinfo='none',  # No hover info
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        # Iterate through each node in the graph to prepare for node plotting
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)  # Node x-coordinate
            node_y.append(y)  # Node y-coordinate
            node_text.append(node)  # Node text

        # Prepare the node trace for Plotly
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',  # Node style
            hoverinfo='text',
            text=node_text,  # Text displayed on hover
            marker=dict(
                showscale=False,  # No color scale
                size=10,  # Node size
                color=[get_node_color(G.nodes[node]['type']) for node in G.nodes()],  # Node color based on type
                line_width=2))  # Line width around nodes

        # Create a Plotly figure with the edge and node traces
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,  # No legend
                            hovermode='closest',  # Hover mode
                            margin=dict(b=20, l=5, r=5, t=40),  # Margin
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # X-axis style
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))  # Y-axis style
                        )
        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    # Check if the selected visualization is "Distribution By Gene Sets"
    elif selected_visualization == "Distribution By Gene Sets":
        # Create a categorical distribution of gene sets with a p-value cutoff
        distribution = create_categorical_distribution(enrichment_data, p_value_cutoff)
        # Set up the plot
        plt.figure(figsize=(10, 6))
        # Create a bar plot with Seaborn
        sns.barplot(x='Count', y='Gene_set', data=distribution)
        # Set the plot title
        plt.title('Categorical Distribution of Gene Set Libraries')
        # Display the plot in Streamlit
        st.pyplot(plt)

        
# Initialize the Streamlit page
st.set_page_config(page_title="GeneAPIChat", page_icon="⚗", layout="wide")

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

st.markdown(
    """
    <style>
        /* CSS for blinking animation */
        @keyframes blink {
            0% {
                opacity: 1;
            }
            30% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
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
        .custom-error {
            /* Custom styles for the error box */
            background-color: #ffcccc;
            padding: 10px;
            border: 2px solid #ff0000;
            animation: blink 2s infinite; /* Apply blinking animation */
            font-size: 40px; /* Increase font size */
        }
        
        .custom-steps {
            background-color: yellow;
            padding: 10px;
            margin-top: 24px; /* Add a gap between the two divs */
            font-size: 18px;
        }

    </style>
    """,
    unsafe_allow_html=True,
)
# Create two columns for the Streamlit app layout with ratios 3:1
col1, col2 = st.columns((3, 1))

# Use the first column to display a header
with col1:
    st.markdown(f"""<h1 style="font-size: 32px;">Explore external websites related to genetic data and information ⚗</h1>""", unsafe_allow_html=True)

#In the sidebar, there's a button to toggle the visibility of Azure OpenAI settings.
#When the settings are shown, the user can input various details such as the ChatGPT deployment name, 
#GPT-4 deployment name, Azure OpenAI Endpoint, and Azure OpenAI Key. The settings are submitted using a form.
# Sidebar layout and options
with st.sidebar:
    # Add margin at the bottom
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)  
    # Settings heading
    st.markdown(f"""Click Settings 👇 for Open AI credentials""", unsafe_allow_html=True)   
    #Settings for Azure Open AI
    st.button("Settings",on_click=toggleSettings)    
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


# Initialize 'uploaded_file' in session state if not already present
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

# Initialize 'show_uploader' in session state if not already present
if 'show_uploader' not in st.session_state:
    st.session_state['show_uploader'] = False

    
    
# Main panel
# Check if the required Azure OpenAI Deployment settings are provided
if st.session_state.get('apikey', '') == '' or st.session_state.get('endpoint', '') == '' or st.session_state.get('chatgpt', '') == '':
    # If any of the settings are missing, display an error message
    #st.error("You need to specify OpenAI credentials, click Settings on the left sidebar! ")
    error_message=f"""
                <div class="custom-error">
                    <ul style="list-style-type: none;">
                        <li>
                            <strong>Alert! Alert!</strong>
                            <i class="fas fa-exclamation-triangle"></i>
                            <ul style="list-style-type: none;">
                                <li>You need to specify Open AI (here, Azure's) credentials and SQL (SQLITE path or SQL Server connection) database settings to proceed.</li>                               
                            </ul>
                        </li>
                    </ul>
                </div>
                <div class="animated-heading">
                        <span style="font-size: 24px;">👈</span> Click on Settings on the left sidebar!
                </div>
                <!-- Additional div for steps -->
                <div class="custom-steps">
                    <ul style="list-style-type: none;">
                        <li>
                            <strong>Steps to navigate this section:</strong>
                            <ul>
                                <li><a href='https://github.com/anath2110/GENEVIIC_Supplementary/blob/main/Tutorial/Azure%20Open%20AI%20Documentation.pdf' target=_blank>Azure OpenAI Instructions</a> </li></li>
                                <li>Use prompts with keywords interaction or network to invoke "STRING API"</li>
                                <li>Use prompts with keywords enrichment or enrich or analysis or pathway to invoke "ENRICHR API"</li>
                                <li>Click on Submit or Enrichment or Visualize button, as the case may be , to see the result</li>
                                <li>For advanced questions such as forecasting, you can use GPT-4 (if available) as the engine</li>
                            </ul>
                        </li>
                    </ul>
                </div>"""
     # Display the error message
    st.markdown(error_message, unsafe_allow_html=True)
else:
    # If settings are provided, proceed with the application functionality

    with col1:
        # Text area for user input
        user_input = st.text_area("Your question or command:", value="")
        # Submit button
        if st.button("Submit"):
            # Classify the user input using the OpenAI model
            classification = classify_choosecorrectAPI(user_input, max_response_tokens, temperature, st.session_state.chatgpt)

            # Decide the action based on the classification
            if "show_gene_network" in classification:
                # If classified as 'show_gene_network', call the respective function
                show_gene_network()
            elif "show_enrichment_uploader" in classification:
                # If classified as 'show_enrichment_uploader', set the 'show_uploader' flag to True
                st.session_state['show_uploader'] = True
            else:
                # For any other classification, set the 'show_uploader' flag to False
                st.session_state['show_uploader'] = False


        if st.session_state['show_uploader']:
            # File uploader UI element
            uploaded_file = st.file_uploader("Upload your gene list", key="gene_uploader")
            # If a file is uploaded, store it in the session state
            if uploaded_file is not None:
                st.session_state['uploaded_file'] = uploaded_file


        # Check if an uploaded file is present in the session state
        if st.session_state['uploaded_file'] is not None:
            # Display options for enrichment analysis if a file is uploaded
            if st.session_state['uploaded_file'] is not None:
                # Multiselect dropdown for users to choose gene set libraries
                gene_set_libraries = ['GO_Biological_Process_2018', 'KEGG_2019_Human', 'WikiPathways_2019_Human']
                selected_library = st.multiselect("Choose gene set libraries", gene_set_libraries, key="library_select")

                # Button to trigger enrichment analysis
                if st.button("Enrich", key="enrich_button"):
                    # Read the uploaded gene list file as a pandas DataFrame
                    genelist = pd.read_csv(st.session_state['uploaded_file'])
                    # Call the enrichr_function to perform enrichment analysis on the gene list using the selected libraries
                    response = enrichr_function(genelist, selected_library, "test_results")
  
            # Initialize session state variables if not present
            if 'visualization_confirmed' not in st.session_state:
                st.session_state['visualization_confirmed'] = False
            if 'uploaded_enrichment_file' not in st.session_state:
                st.session_state['uploaded_enrichment_file'] = None

            # Checkbox for the user to confirm if they want to visualize the enrichment results
            visualization_confirm = st.checkbox("Do you want to visualize the enrichment results?")
            if visualization_confirm:
                # Set the 'visualization_confirmed' flag to True if the user confirms
                st.session_state['visualization_confirmed'] = True

            # Enrichment file upload for visualization
            if st.session_state['visualization_confirmed']:
                uploaded_enrichment_file = st.file_uploader("Upload your enrichment results file", type="csv", key="enrichment_file_uploader")
                if uploaded_enrichment_file is not None:
                    st.session_state['uploaded_enrichment_file'] = uploaded_enrichment_file
                    
                # Visualization section   
                # Check if an enrichment results file has been uploaded
                if st.session_state['uploaded_enrichment_file'] is not None:
                    # Dropdown for the user to choose the type of visualization
                    visualization_types = ['Network Graph', 'Distribution By Gene Sets']
                    selected_visualization = st.selectbox("Choose type of visualization", visualization_types, key="visualization_select")

                    # Input for the user to specify a p-value cutoff
                    p_value_cutoff = st.number_input("Enter p-value cutoff", min_value=0.0, max_value=1.0, value=0.05, step=0.01, key="pvalue_cutoff")

                    # Button to trigger the visualization
                    if st.button("Visualize Enrichment", key="enrichvisualize_button"):
                        # Read the uploaded enrichment results file as a pandas DataFrame
                        enrichment_data = pd.read_csv(st.session_state['uploaded_enrichment_file'])
                        # Call the enrichrvisualization_function to visualize the enrichment data
                        enrichrvisualization_function(enrichment_data, selected_visualization, p_value_cutoff)

                 
           

   