from selenium import webdriver
import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class CollectPages:
    def __init__(self) -> None:
        self.companies_json = {}
        self.url = ""
        # self.options = webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(options=self.options)
        self.headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        self.file_data = {}
        self.list_of_keywords = ["Вакансии", "Карьера", "career", "Career", "vacancies", "Vacancies", "контакты", "Контакты", "contacts", "Contacts"]
        self.number_of_iteration = 1

    async def get_page_data(self, session, url, page):
        with open ("companies_data.json") as file:
            self.file_data = json.load(file)
        try:
            async with session.get(url=url, headers=self.headers) as response:
                response_text = await response.text()
                soup = BeautifulSoup(response_text, "lxml")
                parsed_url = urlparse(url)
                main_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                # response = requests.get(url=url, headers=self.headers)
                
                # self.file_data[page] = [self.file_data[page]]
                for key in self.list_of_keywords:
                    elemet_contacts = soup.find('a', text=key)
                    if elemet_contacts: 
                        contact_link = elemet_contacts.get("href")
                        if '.' not in contact_link and contact_link[0] == '/':
                            result_contact_link = main_url + contact_link
                            if result_contact_link not in self.file_data[page]:
                            # print(result_contact_link)
                                self.file_data[page].append(result_contact_link)
                            print(self.file_data[page])
                        elif '.' not in contact_link and contact_link[0] != '/':
                            result_contact_link = f'{main_url}/{contact_link}'
                            if result_contact_link not in self.file_data[page]:
                            # print(result_contact_link)
                                self.file_data[page].append(result_contact_link)
                            print(self.file_data[page])
                            break
                        else:
                            if contact_link not in self.file_data[page]:
                                self.file_data[page].append(contact_link)
                            print(self.file_data[page])
                            # print(contact_link)
                    
                    

                    else:    
                        print('Не найдены страницы контактов и вакансий!')

            print(f'Iteration #{self.number_of_iteration}')
            self.number_of_iteration += 1
        except Exception as e:
            print(e)
    def read_json(self):
        with open("companies_data.json") as file:
            self.companies_json = json.load(file)
            
    async def gather_data(self):
        async with aiohttp.ClientSession() as session:
            # response = await session.get(url=self.url, headers=self.headers)
            self.read_json()
            tasks = []
            for page in self.companies_json:
                url = self.companies_json[page][0]
                task = asyncio.create_task(self.get_page_data(session, url, page))
                tasks.append(task)
            await asyncio.gather(*tasks)
    def write_contact_pages_json(self):
        with open("contact_pages_data.json", 'w') as file:
            json.dump(self.file_data, file, indent=4, ensure_ascii=False)
            print("Data written to contact_pages_data.json")

def main():
    run_gather_data = CollectPages()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run_gather_data.gather_data())
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C interruption if needed

    run_gather_data.write_contact_pages_json()
    loop.close()

if __name__ == "__main__":
    main()
