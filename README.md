# GENEVIC
## GENetic data Exploration and Visualization Intelligent interactive Console
This is a smart chat assistant that is crafted to facilitate research in Biomedical Informatics for both beginners and intermediate-level researchers.
---
## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
	- [PGS Chat](#pgs-chat)
	- [Gene API Chat](#gene-api-chat)
	- [Literature Search](#literature-search)
- [Local Installation](#local-installation)
- [Docker Installation](#docker-installation)
- [Web Usage](#web-usage)
- [Contact](#contact)
---
## Introduction
- GENEVIC is augmented by generative AI models implemented via Azure OpenAI platform.
- It supports Python's built-in SQLITE as well as your own Microsoft SQL Server.
- It can be run from your local host or Streamlit cloud.
- Tasks that can be performed with GENEVIC:
    - **PGS Chat:** Retrieve information from and visualize any custom database.
    - **GeneAPI Chat:** Explore Bioinformatics websites via automated API calls.
    - **Literature Search:** Search for relevant literature evidence in well-known portals for a given search query.
---
## Project Structure
GENEVIC/
│
├── Home.py ──────Main entry point──────(calls)──────
│ │── analyze.py                                     │
│ ├── llm_steps.py                                   │
│ ├── modified_pubmed.py                             │                         
│ ├── modified_requests.py                           │
▲                                                    │
│                                                    ▼
└─────(import)────── page/ ────── ────── ────── ──────                           
│ ├── PGSChat.py #Imports and uses functions from analyze.py
│ ├── GeneAPIChat.py 
│ └── LiteratureSearch.py #Imports and uses functions from llmsteps.py
---
## Features
### PGS Chat
- Retrieve information from and visualize custom database.
- Demo database: **Polygenic Score (PGS) Rank Database**. See [Supplimentary Materials](https://github.com/anath2110/GENEVIC_Supplimentary.git) for more information.
- **Code Writer**: Auto-translate prompts/questions in natural language (e.g., English (US)) to SQL queries or Python code.
    - Steps to use this section:
    	- Use a question from the FAQ or enter your own question.
    	- You can select ```show code``` and/or ```show prompt``` to show SQL & Python code and the prompt behind the scene.
    	- Click on submit to execute and see result.
    	- For advanced questions such as forecasting, you can use GPT-4 (if available) as the engine. 
    - Example prompts/questions:
      - Show the top 10 ranked genes for Alzheimer.
      - Plot distribution of ranks for the top 100 SNPs for Schizophrenia.
- Download the query results as CSV for retrospective analysis and interpretation.
- **Query ChatGPT directly** to generate more information or novel research hypothesis.

### Gene API Chat
- Explore external Bioinformatics websites via automated web API calls.
- Demo APIs explored: **STRING** and **ENRICHR**.
- Generate **gene-gene interaction network**, one or more gene names as input.
  - Entire functionality of STRING API replicated as is.
  - Interactive in-app display of the network.
- Perform **gene enrichment analysis** with reference gene set libraries, given gene list as input.
  - Visualize the **network graph**.
  - Download the enrichment results as CSV and/or the visualizations in known image formats.

### Literature Search
- Search for **literature evidence in PubMed, Google Scholar, or Arxiv**.
- Search in 1 or 2 or all of these websites at the same time.
	- Example search queries:
		 - Search for articles with gene APOE and Alzheimer in Pubmed
		 - Search for articles with Schizophrenia in Google Scholar
		 - articles with gene TREM2 and Schizophrenia in Arxiv
		 - Search for articles with APOE gene name and trait Alzheimer	 	 	 	 
- Displays the **name** and **links** of the articles for any given search query.
- Displays the **abstract** of the article, given its link as search query.
 	- Example:
    		- [Link to the article](https://link-to-your-article)
---

## Local Installation
### Pre-requisites
- [Python 3.10+](https://www.python.org/downloads/)\
  **Important**: Python and the pip package manager must be in the path in Windows for the setup scripts to work.\
          Ensure you can run `python --version` from console.\
          On Ubuntu, you might need to run `sudo apt install python-is-python3` to link `python` to `python3`.
  
### Step-wise Instructions 
## Step 1. Clone this repository

Clone this repository:git clone https://github.com/anath2110/GENEVIC.git \
From the terminal, navigate to ```cd [path-to-project-root-folder]```

## Step 2. Set up environmental variables

Provide settings for Open AI and Database. You can either create a file named `secrets.env` file in the root of this project folder in your PC as below or do it using the app's GUI later on.

    - Option 1: use built-in SQLITE. Then you don't need to install SQL Server.

        AZURE_OPENAI_API_KEY="9999999999999999999999999"
        AZURE_OPENAI_GPT4_DEPLOYMENT="NAME_OF_GPT_4_DEPLOYMENT"
        AZURE_OPENAI_CHATGPT_DEPLOYMENT="NAME_OF_CHATGPT_4_DEPLOYMENT"
        AZURE_OPENAI_ENDPOINT=https://openairesourcename.openai.azure.com/
        SQL_ENGINE = "sqlite"


    - Option 2: use your own SQL Server

        AZURE_OPENAI_API_KEY="9999999999999999999999999"
        AZURE_OPENAI_ENDPOINT="https://openairesourcename.openai.azure.com/"
        AZURE_OPENAI_GPT4_DEPLOYMENT="NAME_OF_GPT_4_DEPLOYMENT"
        AZURE_OPENAI_CHATGPT_DEPLOYMENT="NAME_OF_CHATGPT_4_DEPLOYMENT"
        SQL_USER="sqluserid"
        SQL_PASSWORD="sqlpassword"
        SQL_DATABASE="WideWorldImportersDW"
        SQL_SERVER="sqlservername.database.windows.net"



> **IMPORTANT** If you are a Mac user, please follow [this](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16) to install ODBC for PYODBC

## Step 3. Configure development environment

> **NOTE** all activities in this step will performed using the command line 

### Step 3.1 Navigate to the root directory of this project

Navigate to ```cd [path-to-project-root-folder]```

### Step 3.2 Create a python environment 

This step is required **ONLY if did not perform this earlier as part of the pre-requisites**

### Step 3.3  Import the requirements.txt

Run the command: `pip install -r requirements.txt`

### Step 3.4 Run the application locally

To run the application from the command line: `streamlit run Home.py` \
You will see the application load in your browser.

> **Note**: For troubleshoot, see [here](https://github.com/anath2110/GENEVIC_Supplimentary/blob/main/Tutorial/TSHOOT.md)
> **Note**: For Azure Open AI subscription and set up: see [here](https://github.com/anath2110/GENEVIC_Supplimentary/blob/main/Tutorial/Azure%20Open%20AI%20Documentation.docx)
---
## Docker Installation 
### **Prerequisites:**  
Install 'Docker' in local system or create an account in Docker Cloud.
Help Resources: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
### Download Docker Image for GENEVIC: 
*[Click here to download the zipped docker image file](https://1drv.ms/u/s!AseKDnkTg9K9wclLakIa4G1jRC39jg?e=zx1xmJ)*
### Commands:
>> Run the following commands from the directory where you loaded the above image (here, exmaple for Windows CMD prompt is shown):\
  *docker load -i genevic-v1.tar*\
  This command loads the Docker image from the tar file into your local Docker repository. \
  *docker run -p 8501:8501 genevic-v1*\
  This command runs the container, mapping port 8501 on your local machine to port 8501 in the container.
---
## Web Usage
Access the web application at: [https://geneviic-anathjan24.streamlit.app/](https://geneviic-anathjan24.streamlit.app/)

---
## Credits

This project was made possible by the dedicated efforts of our research team and the comprehensive support provided by [Bioinformatics and Systems Medicine Laboratory](https://www.uth.edu/bioinfo/) and [Department of Health Data Science and Artificial Intelligence](https://sbmi.uth.edu/prospective-students/dsai.htm) at [McWilliams School of Biomedicalinformatics at UTHealth Houston](https://sbmi.uth.edu/).

### Team Members
- **Anindita Nath**: First Author, AI Programmer, Web Application Developer and Maintener, Database Designer and Manager
- **Ushijima Mwesigwa, Goh Savannah**: Co-Author, PGS Rank database curator, application evaluator
- **[Yulin Dai, PhD](https://sbmi.uth.edu/faculty-and-staff/yulin-dai.htm)** : Co-Author, Guided the database development and evaluation of the application 


### Supervision and Guidance
- [**Xiaoqian Jiang, PhD**](https://sbmi.uth.edu/faculty-and-staff/xiaoqian-jiang.htm): Co-Author, Co-supervisor
- [**Zhongping Zhao, PhD, MS**](https://sbmi.uth.edu/faculty-and-staff/zhongming-zhao.htm): Co-Author, Principal Investigator 


### Major Reference Websites
- **[STRING API Documentation](https://string-db.org/help/api/)**: \
  Documentation for the web API of the STRING API website. This is the backbone web API used as one of the demos in the Gene API chat module. This web API is primarily used to generate and visualize the gene-gene interaction network graph.
- **[ENRICHR API Documentation](https://maayanlab.cloud/Enrichr/help#api)**: \
     Documentation for the web API for ENRICHR website. This is the backbone web API used as one of the demos in the Gene API chat module. This web API is primarily used to perform gene enrichment ananlysis for a set of genes using the reference gene set libraries.
- **[Langchain's PubMed API wrapper source code](https://api.python.langchain.com/en/latest/_modules/langchain_community/utilities/pubmed.html#)**:
   Source code for langchain_community.utilities.pubmed.
- **[Langchain's PubMed API wrapper documentation](https://api.python.langchain.com/en/latest/utilities/langchain_community.utilities.pubmed.PubMedAPIWrapper.html#langchain_community.utilities.pubmed.PubMedAPIWrapper)**:
  Documentation for langchain_community.utilities.pubmed. 
- **[Q&A with RAG](https://python.langchain.com/docs/use_cases/question_answering/)**: Question and Answering use case of Langchain.  
- **[Google Scholar (SERP) API documentation](https://serpapi.com/google-scholar-api)**: Google Scholar API which allows to scrape SERP results from a Google Scholar search query.  
- **[Langchain SERP API wrapper](https://python.langchain.com/docs/integrations/providers/serpapi)**: This page covers how to use the SerpAPI search APIs within LangChain.
- **[Langchain Arxiv API wrapper](https://python.langchain.com/docs/integrations/tools/arxiv)**: Entire documentation for Arxiv API wrapper and Arxiv tool of Langchain.

### GitHub Repositories and Resources
- **[Microsoft Azure Open AI workshop](https://github.com/Microsoft-USEduAzure/OpenAIWorkshop.git)**   
- **[Literature search project code](https://github.com/Jeffz999/Medbot.git)**
 
Our heartfelt thanks go to each team member, department, and external contributor for their indispensable roles in the fruition of this project.

---
## Cite Us
<!-- 
If you use this software in your research or wish to refer to its results, please cite the following paper:

Authors. (Year). Title. Journal, Volume(Issue), Page numbers. DOI

### BibTeX Entry for LaTeX Users

If you are using LaTeX, you can use the following BibTeX entry:

\```latex
	@article{YourLastNameYear,\
	title={Title of the Paper},\
	  author={First Author and Second Author and Others},\
	  journal={Journal Name\
	  volume={xx},\
	  number={yy},\
	  pages={zz--aa},\
	  year={20xx},\
	  publisher={Publisher},\
	  doi={xx.xxxx/yyyyy}\
	}\
\```
-->
Manuscript in review with Bioinformatics Journal.

You may find the pre-print at [arXIV](https://arxiv.org/abs/2404.04299)

## Contact

Anindita Nath– nath.anindita2110@gmail.com, Anindita.Nath@uth.tmc.edu

Project Link: [https://github.com/anath2110/GENEVIC.git](https://github.com/anath2110/GENEVIC.git)

Supplementary Materials: [https://github.com/anath2110/GENEVIC_Supplimentary.git](https://github.com/anath2110/GENEVIC_Supplimentary.git)
---
