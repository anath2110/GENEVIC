
# GENEVIIC

## GENetic data Exploration and Visualization Intelligent Interactive Console

Short description of your app and what it does.

---

## Table of Contents

- [Features](#features)
	- [PGS Chat](#pgs-chat)
	- [GeneAPI Chat](#geneapi-chat)
	- [Literature Search](#literature-search)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction

- **A smart chat assistant.**
- **Augmented by ChatGPT/GPT-4 implemented via Azure OpenAI platform.**
- Run from your local browser or Streamlit cloud.
- Designed to support novice to intermediate research in Biomedical Informatics.
- Tasks that can be performed with GENEVIIC:
    - **PGS Chat:** Retrieve information from and visualize any custom database.
    - **GeneAPI Chat:** Explore Bioinformatics websites via automated API calls.
    - **Literature Search:** Search for relevant literature evidence in well-known portals for a given search query.

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

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

---

## Cite Us

If you use this software in your research or wish to refer to its results, please cite the following paper:

Authors. (Year). Title. Journal, Volume(Issue), Page numbers. DOI

### BibTeX Entry for LaTeX Users

If you are using LaTeX, you can use the following BibTeX entry:

\```latex
>	@article{YourLastNameYear,
>	  title={Title of the Paper},
>	  author={First Author and Second Author and Others},
>	  journal={Journal Name},
>	  volume={xx},
>	  number={yy},
>	  pages={zz--aa},
>	  year={20xx},
>	  publisher={Publisher},
>	  doi={xx.xxxx/yyyyy}
>	}
\```



---

## Contact

Your Name – [@YourTwitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/yourusername/your-repo-name](https://github.com/yourusername/your-repo-name)

---
