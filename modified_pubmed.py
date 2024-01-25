'''
Author: Anindita Nath
Job Title: Postdoctoral Research Fellow
Location: Bioinformatics and Systems Medicine Laboratory, MSBMI, UTHH
Date: August, 2023 - January 2024
#.....................................................................................................................
Adapted from the modified code:
Author: Jeff Zhao
Job Title: Summer Intern, UTH BIG-TCR program
Location: Bioinformatics and Systems Medicine Laboratory, MSBMI, UTHH
Code repository: https://github.com/Jeffz999/Medbot.git
#.....................................................................................................................
Modified from the original code:
Langchain's PubMed API wrapper:
https://api.python.langchain.com/en/latest/_modules/langchain_community/utilities/pubmed.html#
#..........................................................................................
References:
Langchain's PubMed API wrapper documentation:
https://api.python.langchain.com/en/latest/utilities/langchain_community.utilities.pubmed.PubMedAPIWrapper.html#langchain_community.utilities.pubmed.PubMedAPIWrapper
#.....................................................................................................................
Purpose: 
           -Support code for llm_steps.py
           -Modified Pubmed API wrapper
'''
#.....................................................................................................................


# Importing essential libraries and modules
import json
import logging
import time
import urllib.error
import urllib.request
from typing import List
from typing import ClassVar

from pydantic import BaseModel, Extra

from langchain.schema import Document

import ssl


logger = logging.getLogger(__name__)



class NewPubMedAPIWrapper(BaseModel):
    """
    Wrapper around PubMed API.

    This wrapper will use the PubMed API to conduct searches and fetch
    document summaries. By default, it will return the document summaries
    of the top-k results of an input search.

    Parameters:
        top_k_results: number of the top-scored document used for the PubMed tool
        load_max_docs: a limit to the number of loaded documents
        load_all_available_meta:
          if True: the `metadata` of the loaded Documents gets all available meta info
            (see https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch)
          if False: the `metadata` gets only the most informative fields.
    """

    base_url_esearch: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
    base_url_efetch: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    max_retry: int = 5
    sleep_time: float = 0.2

    # Default values for the parameters
    top_k_results: int = 3
    load_max_docs: int = 25
    ARXIV_MAX_QUERY_LENGTH: int= 300
    doc_content_chars_max: int = 2000
    load_all_available_meta: bool = False
    email: str = "your_email@example.com"

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True
    def run(self, query: str) -> str:
        """
        Run PubMed search and get the article meta information.
        See https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
        It uses only the most informative fields of article meta information.
        """

        try:
            # Retrieve the top-k results for the query
            docs = [
                f"Published: {result['pub_date']}\nTitle: {result['title']}\n"
                f"Summary: {result['summary']}"
                for result in self.load(query[: self.ARXIV_MAX_QUERY_LENGTH])
            ]

            # Join the results and limit the character count
            return (
                "\n\n".join(docs)[: self.doc_content_chars_max]
                if docs
                else "No good PubMed Result was found"
            )
        except Exception as ex:
            return f"PubMed exception: {ex}"

    def load(self, query: str) -> List[dict]:
        """
        Search PubMed for documents matching the query.
        Return a list of dictionaries containing the document metadata.
        """
        #changes from original: relevance filter and title/abstract fields (line 89). 
        url = (
            self.base_url_esearch
            + "db=pubmed&term="
            + str({urllib.parse.quote(query)})
            + f"&field=title/abstract&retmode=json&retmax={self.top_k_results}&usehistory=y&sort=relevance"
        )
        context = ssl._create_unverified_context()
        result = urllib.request.urlopen(url,context=context)
        text = result.read().decode("utf-8")
        json_text = json.loads(text)

        articles = []
        # Convert the list of articles to a JSON string
        webenv = json_text["esearchresult"]["webenv"]
        for uid in json_text["esearchresult"]["idlist"]:
            article = self.retrieve_article(uid, webenv)
            articles.append(article)       
        return articles

    def _transform_doc(self, doc: dict) -> Document:
        summary = doc.pop("summary")
        return Document(page_content=summary, metadata=doc)

    def load_docs(self, query: str) -> List[Document]:
        document_dicts = self.load(query=query)
        return [self._transform_doc(d) for d in document_dicts]

    def retrieve_article(self, uid: str, webenv: str) -> dict:
        url = (
            self.base_url_efetch
            + "db=pubmed&retmode=xml&id="
            + uid
            + "&webenv="
            + webenv
        )
        #print(url)
        retry = 0
        while True:
            try:
                context = ssl._create_unverified_context()
                result = urllib.request.urlopen(url,context=context)
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and retry < self.max_retry:
                    # Too Many Requests error
                    # wait for an exponentially increasing amount of time
                    print(
                        f"Too Many Requests, "
                        f"waiting for {self.sleep_time:.2f} seconds..."
                    )
                    time.sleep(self.sleep_time)
                    self.sleep_time *= 2
                    retry += 1
                else:
                    raise e

        xml_text = result.read().decode("utf-8")

        # Get title
        title = ""
        if "<ArticleTitle>" in xml_text and "</ArticleTitle>" in xml_text:
            start_tag = "<ArticleTitle>"
            end_tag = "</ArticleTitle>"
            title = xml_text[
                xml_text.index(start_tag) + len(start_tag) : xml_text.index(end_tag)
            ]

        # Get abstract
        abstract = ""
        if "<Abstract>" in xml_text and "</Abstract>" in xml_text:
            start_tag = "<Abstract>"
            end_tag = "</Abstract>"
            abstract = xml_text[
                xml_text.index(start_tag) + len(start_tag) : xml_text.index(end_tag)
            ]

        # Get publication date
        pub_date = ""
        if "<PubDate>" in xml_text and "</PubDate>" in xml_text:
            start_tag = "<PubDate>"
            end_tag = "</PubDate>"
            pub_date = xml_text[
                xml_text.index(start_tag) + len(start_tag) : xml_text.index(end_tag)
            ]

        # Return article as dictionary
        article = {
            "uid": uid,
            "title": title,
            "summary": abstract,
            "pub_date": pub_date,
            "link": f"https://pubmed\.ncbi\.nlm\.nih\.gov/{uid}/" #changes from original: added link field to article 
        }
        return article
