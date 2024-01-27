
# GENEVIIC
This is an intelligent chat assistant which is crafted to facilitate research in Biomedical Informatics for both beginners and intermediate-level researchers.
---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
	- [PGS Chat](#pgs-chat)
	- [GeneAPI Chat](#geneapi-chat)
	- [Literature Search](#literature-search)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)
---
## Introduction
- GENEVIIC is augmented by generative AI models implemented via Azure OpenAI platform.
- It supports Python's built-in SQLITE as well as your own Microsoft SQL Server.
- Run from your local host or Streamlit cloud.
- Tasks that can be performed with GENEVIIC:
    - **PGS Chat:** Retrieve information from and visualize any custom database.
    - **GeneAPI Chat:** Explore Bioinformatics websites via automated API calls.
    - **Literature Search:** Search for relevant literature evidence in well-known portals for a given search query.

## Features
### PGS Chat
- Retrieve information from and visualize custom database.
- Demo database: **Polygenic Score (PGS) Rank Database**. See [Supplimentary Materials](https://github.com/anath2110/GENEVIIC_Supplimentary.git) for more information.
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
---

### Gene API Chat

- Explore external Bioinformatics websites via automated web API calls.
- Demo APIs explored: **STRING** and **ENRICHR**.
- Generate **gene-gene interaction network**, one or more gene names as input.
  - Entire functionality of STRING API replicated as is.
  - Interactive in-app display of the network.
- Perform **gene enrichment analysis** with reference gene set libraries, given gene list as input.
  - Visualize the **network graph**.
  - Download the enrichment results as CSV and/or the visualizations in known image formats.
---

### Literature Search

- Search for **literature evidence in PubMed, Google Scholar, or Arxiv**.
- Search in 1 or 2 or all of these websites at the same time.
	- Example search queries:
		 - Search for articles with gene APOE and Alzheimer in Pubmed
		 - Search for articles with Schizophrenia in Google Scholar
		 - articles with gene TREM2 and Schizophrenia in Arxiv
		 - Search for articles with APOE gene name and trait Alzheiemr	 	 	 	 
- Displays the **name** and **links** of the articles for any given search query.
- Displays the **abstract** of the article, given its link as search query.
 	- Example:
    		- [Link to the article](https://link-to-your-article)
---

## Local Installation
### Prerequisites

Provide step-by-step instructions on how to get a development environment running.

\```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
\```
\```

---

## Web Usage

Access the web application at: [https://geneviic-anathjan24.streamlit.app/](https://geneviic-anathjan24.streamlit.app/)

## Credits

This project was made possible by the dedicated efforts of our research team and the comprehensive support provided by [Bioinformatics and Systems Medicine Laboratory](https://www.uth.edu/bioinfo/) and [Department of Health Data Science and Artificial Intelligence](https://sbmi.uth.edu/prospective-students/dsai.htm) at [McWilliams School of Biomedicalinformatics at UTHealth Houston](https://sbmi.uth.edu/).

### Team Members
- **Member 1 Name** : Role/Contribution
- **Member 2 Name** : Role/Contribution
- ...

### Supervision and Guidance
- **Supervisor Name** (Department Name): Their contribution or how they helped


### Major Reference Websites
- **[STRING API Documentation](https://string-db.org/help/api/)**: \
  This is the API that is included for generating and visualizing gene-gene interation network in the module 
- **[ENRICHR API Documentation](https://maayanlab.cloud/Enrichr/help#api)**: \
     Documentation for the web API for ENRICHR website. This is the backbone web API used as one of the demos in the Gene API chat module.
- **[Langchain's PubMed API wrapper](https://api.python.langchain.com/en/latest/_modules/langchain_community/utilities/pubmed.html#)**:
- **[Langchain's PubMed API wrapper source code](https://api.python.langchain.com/en/latest/utilities/langchain_community.utilities.pubmed.PubMedAPIWrapper.html#langchain_community.utilities.pubmed.PubMedAPIWrapper)**:\
- **[Q&A with RAG](https://python.langchain.com/docs/use_cases/question_answering/)**:\
- **[Google Scholar (SERP) API documentation](https://serpapi.com/google-scholar-api)**:\
- **[Langchain SERP API wrapper](https://python.langchain.com/docs/integrations/providers/serpapi)**:\
- **[Langchain Arxiv API wrapper](https://python.langchain.com/docs/integrations/tools/arxiv)**:\

### GitHub Repositories and Resources
- **[Microsoft Open AI workshop](https://github.com/Microsoft-USEduAzure/OpenAIWorkshop.git)**:\
     Description of how the repository/resource contributed to the project.
- **[Literature search project code](https://github.com/Jeffz999/Medbot.git)**:\
   Description of how the repository/resource contributed to the project.

Our heartfelt thanks go to each team member, department, and external contributor for their indispensable roles in the fruition of this project.

---
## Cite Us

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

---
## Contact

Your Name – nath.anindita2110@gmail.com, Anindita.Nath@uth.tmc.edu

Project Link: [https://github.com/anath2110/GENEVIIC.git](https://github.com/anath2110/GENEVIIC.git)

Supplementary Materials: [https://github.com/anath2110/GENEVIIC_Supplimentary.git](https://github.com/anath2110/GENEVIIC_Supplimentary.git)

---
