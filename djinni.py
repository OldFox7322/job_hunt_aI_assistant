import re
import asyncio
import logging
import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from database import DescriptionVacancies, CoverLetterVacancies
from typing import List, Dict, Tuple, AsyncGenerator
from dotenv import load_dotenv



load_dotenv()


logger = logging.getLogger(__name__)

skills = ['Python', 'FastAPI', 'SQLAlchemy', 'asyncio', 'Pydantic', 'PostgreSQL', 'CI/CD', 'SQL', 'Playwright', 'Docker-Compose', 'API', 'REST API', 'Linux', 'Alembic', 'AI']


class BaseScraper:
	def __init__(self, page):
		self.page = page
	#Generator that obtains HTML from the transmitted link
	async def get_page_html_generator(self, urls: List[str])-> AsyncGenerator[Tuple[str, str], None]:
		for url in urls:
			try:
				logging.info(f'Navigation to {url} . . .')
				await self.page.goto(url, timeout=60000)
				await self.page.mouse.wheel(0, 500) # Scroll down a bit
				await asyncio.sleep(1) # Wait for a second
				await self.page.mouse.wheel(0, 500)

				html_content = await self.page.content()

				yield (url, html_content)
			except Exception as e:
				logging.error(f'Error navigating to {url}: {e}')
				continue 

    #Obtaining all links to vacancies from pages with a list of vacancies
class JobListScraper(BaseScraper):
	def __init__(self, page, cover_letter_db: CoverLetterVacancies):
		super().__init__(page)
		self.cover_letter_db = cover_letter_db


	def get_urls(self)->List[str]:
		url: str = 'https://djinni.co/jobs/?primary_keyword=Python&exp_level=no_exp&exp_level=1y&region=eu&page='
		urls: List[str] = []
		page_num_str = os.getenv('NUM_PAGES_TO_SCRAPE')
		page_num = int(page_num_str)
		for num in range(1, page_num+1):
			urls.append(f'{url}{num}')
		return urls 


	async def get_job_links(self) -> List:
		urls = self.get_urls()
		links: List = []
		page_content = super().get_page_html_generator(urls)
		async for _, html_content in page_content:
			soup = BeautifulSoup(html_content, 'html.parser')
			li_tags = soup.find_all('h2', class_='fs-3 mb-2')
			for li_tag in li_tags:
				a_tag = li_tag.find('a')
				if a_tag:
					link_href = a_tag.get('href')
					if link_href:
						link = 'https://djinni.co' + link_href
						existing_document = self.cover_letter_db.collection.find_one({'url': link})
						if existing_document is None:
							links.append(link)
		return links


		#Get a job description from the job page
class VacancyContentScraper(BaseScraper):
	def __init__(self, page, db_vacancies: DescriptionVacancies):
		super().__init__(page)
		self.db_vacancies = db_vacancies


	async def selection_current_vacancies(self, job_links: List[str]) -> Dict[str, str]:
		result: Dict = {}
		page_content = super().get_page_html_generator(job_links)
		async for url, html_content in page_content:
			coincidence = []
			soup = BeautifulSoup(html_content, 'html.parser')
			div_tag = soup.find('div', class_='mb-4 job-post__description')
			if div_tag:
				text_content = div_tag.get_text().strip()
				for skil in skills:
					if skil in text_content and skil not in coincidence:
						coincidence.append(skil)
				if len(coincidence) >= 4:
					result[url] = text_content
		self.db_vacancies.save_data(result)
		return result



