## Djinni Scraper & AI Cover Letter Generator

This project is an automated web scraper that searches for job vacancies on Djinni.co, filters them based on a specified tech stack, and generates personalized cover letters using the OpenAI API. Designed as a personal tool for a job search, this project demonstrates skills in asynchronous programming, API integration, database management, and Docker.



Features

Web Scraping:** Automatically collects job links from Djinni.co.
Intelligent Filtering:** Selects relevant vacancies by parsing job descriptions and matching them with a predefined tech stack.
AI-Powered Content Generation:** Creates unique and tailored cover letters for each suitable vacancy by leveraging the OpenAI API and a user-provided resume.
Database Integration:** Persists job data in a local **MongoDB** database to prevent reprocessing of previously scraped vacancies.
Dockerization:** Uses Docker for easy setup and dependency management of the MongoDB database.



Getting Started

Prerequisites

Python 3.10+
Docker Engine (or Docker Desktop)

Installation and Setup

1.  **Clone the repository:**
    bash:  git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    		cd your-repo-name


2.  **Set up your environment:**
    * Create a `.env` file in the root directory and add your OpenAI API key and the number of pages to scrape.
        OPENAI_API_KEY=your_api_key_here
        NUM_PAGES_TO_SCRAPE=5

    * Place your resume file (e.g., `my_cv.pdf`) in the project's root directory. Ensure the filename is correctly specified in the `AIManager` class within `ai_manager.py`.

3.  **Start the MongoDB container:**
    * This command launches a new MongoDB container and binds a Docker volume to persist your data across sessions.
    bash:  docker run --name my-mongodb-container -p 27017:27017 -v my_mongodb_data:/data/db -d mongo

4.  **Install dependencies:**
    * Create and activate a virtual environment:
	bash:    python3 -m venv venv
        	source venv/bin/activate

    * Install the required libraries:
	bash: pip install -r requirements.txt
 

5.  **Run the script:**
    bash: python3 main.py

    The script will begin scraping and processing vacancies. All scraped data will be stored in your local MongoDB instance.



Disclaimer

* Please be aware that web scraping policies vary. Always check the `robots.txt` file and terms of service of any website before scraping. This project is intended for educational purposes and personal use.
