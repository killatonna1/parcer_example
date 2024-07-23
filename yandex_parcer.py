
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.common.by import By
import json
import asyncio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CollectCompanies:

    def __init__(self) -> None:
        self.url = "https://yandex.ru/maps/-/CDehJS-Q"
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.element_find = None
        self.element_click = None
        self.company_name = None
        self.company_link = None
        self.companies_data_json = {}
        self.name_and_link = ""
        self.i = 1

    
        

    async def download_scroll_list(self):
        
        for i in range(1, 10000):
            try:
                
                self.element_find = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div[8]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/ul/li[{i}]/div/div/div")
                await asyncio.sleep(0.22)
                self.driver.execute_script("arguments[0].scrollIntoView();", self.element_find)
            except:
                await asyncio.sleep(3)   
                self.element_find = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div[8]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/ul/li[{i-1}]/div/div/div")
                await asyncio.sleep(0.5)
                self.driver.execute_script("arguments[0].scrollIntoView();", self.element_find)
                
               
    async def find_company_info(self):
        self.element_click = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div[8]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/ul/li[{self.i}]/div/div/div")
                
        self.element_click.click()
        self.company_name = self.driver.find_element(By.CLASS_NAME, "card-title-view__title-link")
        print(self.company_name.text)
        await asyncio.sleep(0.25)
        self.company_link = self.driver.find_elements(By.PARTIAL_LINK_TEXT, ".")
        
        print(self.company_link[-1].get_attribute('href'))
        self.i += 1

    async def collect_company_list(self):
        for i in range(10000):
            try:
                await self.find_company_info()
            except:
                await asyncio.sleep(5)
                await self.find_company_info()
            finally:
                try:
                    with open("companies_data.json", "r+") as file:
                        self.companies_data_json = json.load(file)
                    # print("read JSON")
                except Exception as e:
                    print(e)


                self.name_and_link = {self.company_name.text: [self.company_link[-1].get_attribute("href")]}
                self.companies_data_json.update(self.name_and_link)
                try:
                    with open("companies_data.json", "w") as file:
                        json.dump(self.companies_data_json, file, ensure_ascii=False, indent=4)
                except Exception as e:
                    # print("write JSON")
                    await asyncio.sleep(2)
                
    
    


            
    def select_random_user_agent(self):
        with open("list_of_user_agents.txt") as file:
            data_users = file.readlines()
        random_user = random.choice(data_users)
        print(random_user)
        return random_user
        
    def webdriver_run(self):
        self.driver.get(url=self.url)
        self.driver.set_window_size(1920,1080)

        

run_yandex = CollectCompanies()
run_yandex.webdriver_run()
sleep(5)

async def main_run():
    task_1 = asyncio.create_task(run_yandex.download_scroll_list())
    task_2 = asyncio.create_task(run_yandex.collect_company_list())
    
    await task_1
    await task_2
asyncio.run(main_run())    
# run_yandex.webdriver_run()
# run_yandex.collect_company_list()
