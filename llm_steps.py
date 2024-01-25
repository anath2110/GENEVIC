'''
Author: Anindita Nath
Job Title: Postdoctoral Research Fellow
Location: Bioinformatics and Systems Medicine Laboratory, MSBMI, UTHH
Date: August, 2023 - January 2024
#..........................................................................................
Modified from original:
Author: Jeff Zhao
Job Title: Summer Intern, UTH BIG-TCR program
Location: Bioinformatics and Systems Medicine Laboratory, MSBMI, UTHH
Code repository: https://github.com/Jeffz999/Medbot.git
#..........................................................................................
References:
Q&A with RAG:https://python.langchain.com/docs/use_cases/question_answering/
Google Scholar (SERP) API documentation:https://serpapi.com/google-scholar-api
Langchain SERP API wrapper:https://python.langchain.com/docs/integrations/providers/serpapi
Langchain Arxiv API wrapper:https://python.langchain.com/docs/integrations/tools/arxiv
#..........................................................................................
Purpose: 
        -Support code for Literature Search page
        -Uses modified_pubmed.py and Langchain's ArxivAPIWrapper and SerpAPIWrapper
'''
#..........................................................................................


# Importing essential libraries and modules
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from typing import Optional, Type
from langchain.agents import Tool

from modified_pubmed import NewPubMedAPIWrapper
from langchain.utilities import ArxivAPIWrapper
from langchain.utilities import SerpAPIWrapper


from bs4 import BeautifulSoup
from modified_requests import TextRequestsWrapper
import re


#This code snippet defines tools for searching academic and scientific literature in PubMed, Google Scholar, and Arxiv.
def load_tools(serpapi_api_key):
    # Initialize the PubMed API wrapper to fetch top 3 results
    pubmed = NewPubMedAPIWrapper(top_k_results=3)

    # Initialize the Arxiv API wrapper
    arxiv = ArxivAPIWrapper()

    # Define a custom tool for Google Scholar searches
    class GoogleScholar(BaseTool):
        # Metadata about the tool
        name = "Google Scholar"
        description = "Given a query for an article on Google Scholar, this returns a list of the resulting article's titles, authors, abstract links, and result ids"
        
        # Define parameters for SerpAPIWrapper
        params = {
            "engine": "google_scholar",
            "hl": "en",
            "num": 5,
        }

        # Initialize SerpAPIWrapper with the API key and defined parameters
        search = SerpAPIWrapper(params=params, serpapi_api_key=serpapi_api_key)
        
        def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
            """
            Search and return a specified number of articles' titles, links, ids, and authors.
            """
            # Fetch search results from Google Scholar
            search_result = self.search.results(query)['organic_results']
            # Process and refine the results
            refined_results = []
            for i in search_result:
                refined_results.append({
                    'title': i['title'],
                    'link': i['link'],
                    'result_id': i['result_id'],
                    'authors': i['publication_info']['summary']
                })

            # Convert the refined results into a string format
            search_results = ""
            for i in range(0, len(refined_results)):
                search_results = search_results + str(refined_results[i]) + "\n"
            return search_results
        
        async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
            """
            Asynchronous method for the tool, not implemented.
            """
            raise NotImplementedError("Not implemented")

    # Instantiate the GoogleScholar class
    google_scholar = GoogleScholar()



    #This code snippet defines a custom tool, AbstractSearcher, 
    #for retrieving abstracts from arbitrary links, such as those from Google Scholar, PubMed, or Arxiv, using HTTP GET requests and Beautiful Soup for parsing HTML content.
    #Use arbitrary links from google scholar to retrieve abstracts  
    class AbstractSearcher(BaseTool):
        # Metadata about the tool
        name = "Abstract searcher"
        description = "Uses an HTTP GET command + Beautiful Soup to get the abstract of an arbitrary link"
        
        # Initialize a wrapper for making HTTP requests
        http_caller = TextRequestsWrapper()

        
        def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
            """
            Redirects to a preexisting tool if the query matches a known pattern (Arxiv or PubMed),
            otherwise, it analyzes the HTML content to extract the abstract.
            """
            # Patterns to identify Arxiv and PubMed links
            arxiv_pattern = r'https://arxiv\.org/abs/(.*)'
            pubmed_pattern = r'https://pubmed\.ncbi\.nlm\.nih\.gov/(.*)/'
            
            # Check if the query matches the Arxiv pattern
            if re.match(arxiv_pattern, query):
                id = re.match(arxiv_pattern, query).group(1)
                return f"INSTRUCTIONS: use arxiv search with query {id}"
            
            # Check if the query matches the PubMed pattern
            elif re.match(pubmed_pattern, query):
                id = re.match(pubmed_pattern, query).group(1)
                return f"INSTRUCTIONS: use pubmed search with query {id}"
            
            # For other links, use Beautiful Soup to parse HTML content and extract abstract
            else:
                soup = BeautifulSoup(self.http_caller.get(query), 'lxml')
                returned_result = ""
                # Iterate through all paragraph tags and concatenate their text content
                for data in soup.find_all("p"): 
                    returned_result += (data.get_text() + "\n")
                return returned_result
            
        async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        ) -> str:
            """Use the tool asynchronously."""
            raise NotImplementedError("Not implemented")

    # Instantiate the AbstractSearcher class
    abs_search = AbstractSearcher()

    
# Initialize a list of tools
    tools = [
        # Arxiv Search Tool
        Tool(
            name="arxiv search",
            func=arxiv.run,
            description="Use this to use a query to get articles on arxiv. Input could be an arxiv ID, an article title, or a search term. IF THE USER SPECIFIES A TITLE OF AN ARTICLE OR PAPER AND THIS TOOL IS BEING USED, PREFIX THE QUERY WITH 'ti'. IF THE USER SPECIFIES AN AUTHOR, PREFIX THE QUERY WITH 'au'. The output will return a list of articles as dictionaries, which include their title, author, abstract, link, and publish date. Use the most relevant dictionary as text."
        ),
        # PubMed Search Tool
        Tool(
            name="pubmed search",
            func=pubmed.load_docs,
            description="Use this to use a query to get articles on Pubmed. Pubmed specializes in articles relating to bioinformatics. The input can be a pubmed id or a search term. The output will return a list of dictionaries that are the relevant articles and their ids, titles, publish dates, and links. From that list use the most relevant (based on the title and abstract) dictionary as text."
        ),
        # Google Scholar Search Tool
        Tool(
            name="google scholar search",
            func=google_scholar.run,
            description="Use this to use a query to get articles on Google Scholar. The input can be a google scholar id or a search term. The output will return a list of dictionaries that are the relevant article's titles, authors, abstract links, and result ids. THIS WILL NOT OUTPUT THE ABSTRACT. From that list use the most relevant (based on the title) dictionary as text."
        ),
        # Article Link Handler Tool
        Tool(
            name="article link handler",
            func=abs_search.run,
            description="Given a link to an abstract when no abstract is present, use this tool and extract the abstract. Always use this for google scholar results. Input will be a link to an article. Output could be 2 possibilities: instructions to use a tool with a specified query or the website's paragraph text which will contain the abstract."
        )
    ]
    # Return the list of initialized tools   
    return tools