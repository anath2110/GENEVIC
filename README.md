
# GENEVIIC

## Introduction

- **A smart chat assistant.**
- **Augmented by Generative AI models implemented via Azure OpenAI platform.**
- The application supports Python's built-in SQLITE as well as your own Microsoft SQL Server.
- Designed to support novice to intermediate research in Biomedical Informatics.
- Run from your local host or Streamlit cloud.
- Tasks that can be performed with GENEVIIC:
    - **PGS Chat:** Retrieve information from and visualize any custom database.
    - **GeneAPI Chat:** Explore Bioinformatics websites via automated API calls.
    - **Literature Search:** Search for relevant literature evidence in well-known portals for a given search query.

---


## Table of Contents

- [Features](#features)
	- [PGS Chat](#pgs-chat)
	- [GeneAPI Chat](#geneapi-chat)
	- [Literature Search](#literature-search)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

---


## Features
### PGS Chat

- Retrieve information from and visualize custom database.
- Demo database: **Polygenic Score (PGS) Rank Database**.
- **Code Writer**: Auto-convert queries in natural language (e.g., English (US)) to SQL queries or Python code.
  - Show the top 10 ranked genes for Alzheimer.
  - Plot distribution of ranks for the top 100 SNPs for Schizophrenia.
- Download the query results as CSV for retrospective analysis and interpretation.
- **Query ChatGPT directly to generate more information or novel research hypothesis.**
---

### GeneAPI Chat

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
  - Display the **name** and **links** of the articles for any given search query.
---

## Installation

Provide step-by-step instructions on how to get a development environment running.

\```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
\```

---

## Usage

Explain how to run the Streamlit app.

\```bash
streamlit run yourapp.py
\```

Include information about how to navigate the app and any important usage notes.

---


## Credits

This project was made possible by the dedicated efforts of our research team and the comprehensive support provided by [Bioinformatics and Systems Medicine Laboratory, McWilliams School of Bioinformatics, UTHealth Houston](https://www.uth.edu/bioinfo/).

### Team Members
- **Member 1 Name** (Department Name): Role/Contribution
- **Member 2 Name** (Department Name): Role/Contribution
- ...

### Supervision and Guidance
- **Supervisor Name** (Department Name): Their contribution or how they helped

### Organizational Support
- **[Organization Name](Organization URL)**: We extend our sincere gratitude to our organization for providing the infrastructure, resources, and environment conducive to innovative research.
  - **Department 1**: Special thanks to the Department 1 for [specific support or contribution].
  - **Department 2**: Special thanks to the Department 2 for [specific support or contribution].
  - ...

### Major Reference Websites
- **[Website Name 1](Website URL 1)**: Description of the information or data provided by the website.
- **[Website Name 2](Website URL 2)**: Description of the information or data provided by the website.
- ...

### GitHub Repositories and Resources
- **[Repository/Resource Name 1](GitHub URL 1)**: Description of how the repository/resource contributed to the project.
- **[Repository/Resource Name 2](GitHub URL 2)**: Description of how the repository/resource contributed to the project.

---
Our heartfelt thanks go to each team member, department, and external contributor for their indispensable roles in the fruition of this project.
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

Supplementary materials for this project : [https://github.com/anath2110/GENEVIIC_Supplimentary.git](https://github.com/anath2110/GENEVIIC_Supplimentary.git)

---
