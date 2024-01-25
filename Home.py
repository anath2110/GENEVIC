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
import streamlit as st  # Import Streamlit for creating web apps
from streamlit.logger import get_logger  # Import get_logger from Streamlit to enable logging
from streamlit_chat import message  # Import message for chat functionality in Streamlit
import base64  # Import base64 library for encoding/decoding data
import time  # Import time library for time-related functions
from streamlit_modal import Modal  # Import Modal for creating modal dialogs in Streamlit
from streamlit_player import st_player  # Import st_player for embedding media players in Streamlit apps
from transformers import pipeline  # Import pipeline from the transformers library for NLP tasks

LOGGER = get_logger(__name__)  # Initialize a logger for the module with the module's name


# Function to read local image and convert to base64
def load_image(image_path):
    with open(image_path, "rb") as img_file:  # Open the image file in binary read mode
        return base64.b64encode(img_file.read()).decode()  # Encode the binary data to base64 and return it as a string

# Function to read local video and convert to base64
def load_video(video_path):
    with open(video_path, "rb") as video_file:  # Open the video file in binary read mode
        video_base64 = base64.b64encode(video_file.read()).decode()  # Encode the binary data to base64 and return it as a string
    return video_base64  # Return the base64-encoded video data


def load_classifier():
    # Load the zero-shot classification model
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")  # Initialize the zero-shot classifier pipeline with the specified model
    return classifier  # Return the initialized classifier

def category():
    # Define the categories and their corresponding Streamlit page URLs
    category_urls = {
        "PGSChat": "PGSChat",  # Define URL for the PGSChat page
        "GeneAPIChat": "GeneAPIChat",  # Define URL for the GeneAPIChat page
        "LiteratureSearch": "LiteratureSearch"  # Define URL for the LiteratureSearch page
    }
    return category_urls  # Return the dictionary of category URLs


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
    videotutorial_base64 = load_video("videos/video_tutorial.mp4")  # Load and encode the video tutorial

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
                height: 500px;
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
                height: 500px;          
            }
            .block2 {
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                text-align: left;          
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                background-color: #FFCCCC;
                color: #333;
                height: 500px;
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
                height: 500px;
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
                       <h1 style="font-size: 36px;">GENEVIIC:GENetic data Exploration and Visualization Intelligent Interactive Console</h1>                       
                    </div>
    """, unsafe_allow_html=True)


    # Sidebar style code HTML/CSS
    with st.sidebar:
    
        # Animated heading in the sidebar
        st.markdown(f"""<div class="animated-heading">Select from above ☝</div>""", unsafe_allow_html=True)
        # Add margin at the bottom
        st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
        
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
                    <li> <a href='https://www.pgscatalog.org/' target=_blank>Tutorial</a> </li>
                    <li> <a href='https://www.pgscatalog.org/' target=_blank>PGS Catalog Website</a> </li>
                    <li> <a href='http://tinyurl.com/PGSrankDB' target=_blank>PGS Rank Database</a> </li>                     
                    <!-- <li> <a href='Link' target=_blank>Publication</a></li> -->
                    <li> <a href='https://www.pgscatalog.org/' target=_blank> Code Repository</a> </li>                    
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
                    <li><a href='http://tinyurl.com/GenVICcontact' target=_blank>Contact Us</a> </li>
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
                        <h3 class="hover-grow-shrink">About GENEVIIC</h3>                           
                    </div>                  
                    <ul style="list-style-type: none;">                        
                        <li> An automated web-based smart chat application </li> 
                        <li> Run from your local browser or Streamlit cloud </li>                         
                        <li> Designed specifically to support certain important research aspects in the field of Biomedicalinformatics </li>
                        <li> <strong>Back-end powered by ChatGPT implemented via Azure OpenAI platform</strong></li> 
                        <li> Tasks that you can perform with GENEVIIC:
                            <ul style="list-style-type: none;">  
                                <li> <strong> PGS Chat: Retrieve information from and visualize any custom database </strong></li>
                                <li> <strong> GeneAPI Chat: Explore Bioinformatics websites via automated API calls  </strong></li>
                                <li> <strong> Literature Search: Search for relevant literature evidence in well known portals for a given search query </strong></li>
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
                        <li> Query in natural language (e.g. Enlish(US)), for example:
                            <ul style="list-style-type: none;">
                                <li> Show the top 10 ranked genes for Alzheimer</li>
                                <li> Plot distribution of ranks for the top 100 SNPs for Schizophrenia</li>
                            </ul>
                        </li> 
                    </ul>
                    </li>
                    
                </ul>
                <ul style="list-style-type: none;">
                    <li> Auto-transform natural language to SQL queries 
                    <li> Download the query results as CSV</li>
                    <li> <strong> Query ChatGPT directly to generate more information or novel research hypothesis </strong></li>
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
                        <li> Generate gene-gene interaction network, one or more gene names as input
                                <ul style="list-style-type: none;">
                                   <li> Entire functionality of STRING API replicated as is</li>
                                   <li> Interactive in-app display of the netowrk </li>
                                </ul>
                        </li>
                        <li> Perform Gene Enrichment Analysis with reference gene sets, given gene list as input
                        <li> Visualize the Network Graph </li> 
                        </li>
                        <li> Download the enrichment results as CSV and/or the visualizations in known image formats
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
                <li><strong>Search for literature evidence in PubMed, Google Scholar, or Arxiv</strong>
                    <ul style="list-style-type: none;">
                        <li> Either search in 1 or 2 or all of websites at the same time</li>
                        <li> Display the name and links to the articles corresponding to the given search query</li>
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
    col3, col4 = st.columns([1,1])  

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
        # When the user clicks the submit button
        if st.button("Submit"):
            # Load the classifier and categories
            classifier = load_classifier()
            category_urls = category()
            # Predict the category of the user's query
            result = classifier(user_query, list(category_urls.keys()))
            # Find the label with the highest score
            highest_score_index = result["scores"].index(max(result["scores"]))
            predicted_category = result["labels"][highest_score_index]

            # Generate an HTML link to navigate to the corresponding Streamlit page
            if predicted_category in category_urls:
                page_url = category_urls[predicted_category]
                link_text = f"Go to {predicted_category} Page"
                link_html = f'<a href="{page_url}" target=_blank>{link_text}</a>'
                st.markdown(link_html, unsafe_allow_html=True)
        # Add margin at the bottom
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)       

    # Column 4: Video tutorial block
    with col4:
        # Text and icon indicating the video tutorial
        st.markdown(
            f"""
            <div style="text-align:left;margin-left:180px;margin-bottom:0px">
                <span class="pointer-icon" style="font-size: 32px;"> Take our Guided Tour 👇</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Embed the video tutorial
        st.markdown(
            f"""<video width="600" height="450" poster="data:image/png;base64,{bkgroundimage}" controls>
                    <source src="data:video/mp4;base64,{videotutorial_base64}" type="video/mp4">
                </video>           
            """,
            unsafe_allow_html=True
        )
            
    # Column 3: Auto-scroll blocks describing each task page
    with col3:
        # Create an empty placeholder for blocks
        placeholder = st.empty()

        # List of block contents (HTML content)
        block_contents = [block0_html, block1_html, block2_html, block3_html]

        # Time delay in seconds between each block's content
        delay = 10
        # Infinite loop to auto-scroll blocks
        while True:
            # Loop to update the placeholder with each block's content
            for content in block_contents:
                placeholder.markdown(content, unsafe_allow_html=True)
                time.sleep(delay)



if __name__ == "__main__":
    run()

