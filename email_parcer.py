from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp
import re

class CollectEmails():
    def __init__(self) -> None:
        self.pages_json = {}
        self.headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    async def find_email(self, session, url, company):
        try:
            async with session.get(url=url, headers=self.headers) as response:
                await asyncio.sleep(0.5)
                response_text = await response.text()
                
                soup = str(BeautifulSoup(response_text, "lxml"))
                
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup)
                print(self.pages_json[company])
                self.pages_json[company][-1].update(set(emails))
                    

        except Exception as e:
            print(e)
    
    async def gather_data(self):
        self.read_json()
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = []
            for company in self.pages_json:
            #    print(f'HERE IS THET PRINT STRING {self.pages_json[company]}')
                if not isinstance(self.pages_json[company][-1], set) and isinstance(self.pages_json[company], list):
                    self.pages_json[company].append(set())
            for company in self.pages_json:
                for page in self.pages_json[company]:
                    url = page
                    task = asyncio.create_task(self.find_email(session, url, company))
                    tasks.append(task)
            
            await asyncio.gather(*tasks)
            # print(self.pages_json)

    def read_json(self):
        with open("contact_pages_data.json") as file:
            self.pages_json = json.load(file)

    def convert_set_to_list(self):
        try:
            for company in self.pages_json:
                if isinstance(self.pages_json[company][-1], set):
                    self.pages_json[company][-1] = list(self.pages_json[company][-1])
                    print(self.pages_json[company][-1])
        except Exception as e:
            print(e)

    def write_emails_to_json(self):
        try:
            with open("emails_pages_data.json", 'w') as file:
                json.dump(self.pages_json, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"An error occurred: {e}")
    

    def temprorary_write_emails_to_json(self):
        try:
            with open("emails_pages_data.txt", 'w') as file:
                file.write(self.pages_json)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    email_collecor = CollectEmails()
    asyncio.run(email_collecor.gather_data())
    email_collecor.convert_set_to_list()
    # email_collecor.temprorary_write_emails_to_json()
    email_collecor.write_emails_to_json()
    
    
