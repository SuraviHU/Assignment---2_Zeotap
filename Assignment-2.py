import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class CDPChatbot:
    def __init__(self, cdp_docs):
        self.cdp_docs = cdp_docs
        self.index = {}
        self.build_index()

    def build_index(self):
        for cdp, base_url in self.cdp_docs.items():
            self.index[cdp] = {}
            if cdp == "Segment": #Segment requires selenium or API, this is the selenium case.
                self.crawl_and_index_selenium(base_url, cdp)
            else:
                self.crawl_and_index(base_url, cdp)

    def crawl_and_index(self, base_url, cdp):
        visited = set()
        queue = [base_url]
        headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/'
            },
            # Add more header variations
        ]

        while queue:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)

            try:
                headers = random.choice(headers_list)
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                self.index[cdp][url] = text

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('http'):
                        full_url = href
                    else:
                        full_url = urljoin(url, href)

                    if base_url in full_url and full_url not in visited:
                        queue.append(full_url)
                time.sleep(1) #respectful delay
            except requests.exceptions.RequestException as e:
                print(f"Error crawling {url}: {e}")

    def crawl_and_index_selenium(self, base_url, cdp):
        visited = set()
        queue = [base_url]
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        while queue:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)

            try:
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                self.index[cdp][url] = text

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('http'):
                        full_url = href
                    else:
                        full_url = urljoin(url, href)

                    if base_url in full_url and full_url not in visited:
                        queue.append(full_url)

                time.sleep(1) #respectful delay
            except Exception as e:
                print(f"Error crawling {url}: {e}")
        driver.quit()

    def find_relevant_docs(self, question, cdp=None):
        relevant_docs = {}
        question_lower = question.lower()

        if cdp:
            if cdp in self.index:
                relevant_docs[cdp] = {}
                for url, text in self.index[cdp].items():
                    if question_lower in text.lower():
                        relevant_docs[cdp][url] = text
        else:
            for cdp, docs in self.index.items():
                relevant_docs[cdp] = {}
                for url, text in docs.items():
                    if question_lower in text.lower():
                        relevant_docs[cdp][url] = text

        return relevant_docs

    def answer_question(self, question, cdp=None):
        if "movie" in question.lower() or "music" in question.lower():
            return "I can only answer questions related to Segment, mParticle, Lytics, and Zeotap."

        relevant_docs = self.find_relevant_docs(question, cdp)

        if not relevant_docs:
            return "I couldn't find any relevant information."

        answers = {}
        for cdp, docs in relevant_docs.items():
            answers[cdp] = {}
            for url, text in docs.items():
                match = re.search(re.escape(question.lower()), text.lower())
                if match:
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    answers[cdp][url] = text[start:end]
                else:
                    answers[cdp][url] = "Relevant information found, but unable to extract specific answer."

        return answers

    def compare_cdps(self, question):
        if "compare" not in question.lower():
            return "This function is for comparing CDPs. Please use a comparison question."

        relevant_docs = self.find_relevant_docs(question)

        if not relevant_docs:
            return "I couldn't find any relevant information for comparison."

        comparison = {}
        for cdp, docs in relevant_docs.items():
            comparison[cdp] = {}
            for url, text in docs.items():
                match = re.search(re.escape(question.lower()), text.lower())
                if match:
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    comparison[cdp][url] = text[start:end]
                else:
                    comparison[cdp][url] = "Relevant information found, but unable to extract specific answer."

        return comparison

cdp_docs = {
    "Segment": "https://segment.com/docs/",
    "mParticle": "https://docs.mparticle.com/",
    "Lytics": "https://docs.lytics.com/",
    "Zeotap": "https://docs.zeotap.com/home/en-us/"
}

chatbot = CDPChatbot(cdp_docs)

print(chatbot.answer_question("How do I set up a new source in Segment?"))
print(chatbot.answer_question("How can I create a user profile in mParticle?", cdp="mParticle"))
print(chatbot.answer_question("How do I build an audience segment in Lytics?"))
print(chatbot.answer_question("How can I integrate my data with Zeotap?"))
print(chatbot.answer_question("Which Movie is getting released this week?"))
print(chatbot.compare_cdps("How does Segment's audience creation process compare to Lytics'?"))