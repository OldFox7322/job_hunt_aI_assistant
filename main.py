import asyncio
import logging
from typing import NoReturn
from playwright.async_api import async_playwright
from djinni import JobListScraper, VacancyContentScraper
from database import DescriptionVacancies, CoverLetterVacancies
from ai_manager import AIManager


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')






async def main() -> NoReturn:
	logging.info('Lauching browser . . .')
	async with async_playwright() as p:
		browser = await p.chromium.launch(headless=False)
		context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", viewport={"width": 1280, "height": 720})
		page = await context.new_page()
		ai_manager = AIManager()
		db_vacancies = DescriptionVacancies()
		cover_letter_db = CoverLetterVacancies()
		#Step 1, get vacancies links
		job_list_scraper = JobListScraper(page, cover_letter_db)
		job_links = await job_list_scraper.get_job_links()

		if job_links:
			# Step 2, selection suitable vacancies
			vacancy_content_scraper = VacancyContentScraper(page, db_vacancies)
			vacancy_content = await vacancy_content_scraper.selection_current_vacancies(job_links)
			if vacancy_content:
			# Step 3, creating a cover letter
				description = db_vacancies.get_data()
				cover_letters = await ai_manager.cover_letter_creater(description)
				if cover_letters:
					print(cover_letters)
					cover_letter_db.save_data(cover_letters)


if __name__ == '__main__':
	asyncio.run(main())

