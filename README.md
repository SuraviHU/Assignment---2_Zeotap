# CDP Chatbot

This project implements a chatbot that answers "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot retrieves relevant information from the official documentation of these CDPs to guide users.

## Features

* **Answer "How-to" Questions:** Understands and responds to user questions about performing specific tasks or using features within each CDP.
* **Extract Information from Documentation:** Retrieves relevant information from the provided documentation to answer user questions.
* **Handle Variations in Questions:** Robustly handles variations in question phrasing and terminology.
* **Cross-CDP Comparisons:** Answers questions about the differences in approaches or functionalities between the four CDPs.
* **Handles out of scope questions:** Returns a message if a question is outside of the scope of the CDP documents.
* **Uses Selenium to handle Segment's anti-scraping measures.**

## Data Sources

* Segment Documentation: [https://segment.com/docs/](https://segment.com/docs/)
* mParticle Documentation: [https://docs.mparticle.com/](https://docs.mparticle.com/)
* Lytics Documentation: [https://docs.lytics.com/](https://docs.lytics.com/)
* Zeotap Documentation: [https://docs.zeotap.com/home/en-us/](https://docs.zeotap.com/home/en-us/)

## Installation

1.  **Install Python:** Ensure you have Python 3.x installed.
2.  **Install Required Libraries:**

    ```bash
    pip install requests beautifulsoup4 selenium webdriver-manager
    ```

3.  **Install Chrome and ChromeDriver:** Google Chrome is required. The `webdriver-manager` library will handle the correct chromedriver download.

## Usage

1.  **Save the Code:** Save the provided Python code as `cdp_chatbot.py`.
2.  **Run the Program:**

    ```bash
    python cdp_chatbot.py
    ```

3.  **Observe the Output:** The chatbot's responses will be printed to the console.

## Example Questions

* "How do I set up a new source in Segment?"
* "How can I create a user profile in mParticle?"
* "How do I build an audience segment in Lytics?"
* "How can I integrate my data with Zeotap?"
* "How does Segment's audience creation process compare to Lytics'?"
* "Which movie is getting released this week?"

## Code Structure

* `CDPChatbot` class: Contains the main logic for crawling, indexing, and answering questions.
* `build_index()`: Crawls and indexes the CDP documentation.
* `crawl_and_index()`: Crawls and indexes the documentation for mParticle, Lytics, and Zeotap.
* `crawl_and_index_selenium()`: Crawls and indexes the Segment documentation using Selenium.
* `find_relevant_docs()`: Finds relevant documents based on the user's question.
* `answer_question()`: Answers the user's question.
* `compare_cdps()`: Compares the functionalities of the CDPs.

## Potential Improvements

* Integrate more advanced NLP techniques for better question understanding.
* Optimize the document index for faster retrieval.
* Implement more sophisticated information extraction.
* Use the Segment API instead of scraping.
* Develop a user-friendly interface (e.g., a web application).
* Add more robust error handling.

## Author

Suravi H U
