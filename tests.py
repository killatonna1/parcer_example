from bs4 import BeautifulSoup
import json
import re
# import requests
# from urllib.parse import urlparse

# list_of_keywords = ["Вакансии", "Карьера", "career", "Career", "vacancies", "Vacancies", "контакты", "Контакты", "contacts", "Contacts"]
# headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def find_contact_page():
    with open ("example_page.html") as file:
        file_data = file.read()
    soup = str(BeautifulSoup(file_data, 'lxml'))
    
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+',soup)
    print(set(emails))
find_contact_page()

# def find_contact_page():
#     with open ("companies_data.json") as file:
#         file_data = json.load(file)

#     for company in file_data:
#         url = file_data[company]
#         parsed_url = urlparse(url)
#         main_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
#         response = requests.get(url=url, headers=headers)
#         response_text = response.text
#         soup = BeautifulSoup(response_text, "lxml")
#         file_data[company] = [file_data[company]]
#         for key in list_of_keywords:
#             elemet_contacts = soup.find('a', text=key)
#             if elemet_contacts:
#                 contact_link = elemet_contacts.get("href")
#                 if '.' not in contact_link and contact_link[0] == '/':
#                     result_contact_link = main_url + contact_link
#                     if result_contact_link not in file_data[company]:
#                     # print(result_contact_link)
#                         file_data[company].append(result_contact_link)
#                     print(file_data[company])
#                 elif '.' not in contact_link and contact_link[0] != '/':
#                     result_contact_link = f'{main_url}/{contact_link}'
#                     if result_contact_link not in file_data[company]:
#                     # print(result_contact_link)
#                         file_data[company].append(result_contact_link)
#                     print(file_data[company])
#                     break
#                 else:
#                     if contact_link not in file_data[company]:
#                         file_data[company].append(contact_link)
#                     print(file_data[company])
#                     # print(contact_link)
            
               

#         if not elemet_contacts:    
#             print('Не найдено')
    
#     print(file_data)

# def write_new_data_json():
#     with open("new_companies_data.json", 'w') as file:
#         json.dump(file_data, file, ensure_ascii=False, indent=4)



# find_contact_page()
# class A():
#     def __init__(self) -> None:
#         self.companies_json = {}

#     def get_page_data(self, url, page):
#         print(self.companies_json[page])



#     def read_json(self):
#         print('read_json')
#         with open("companies_data.json") as file:
#             self.companies_json = json.load(file)
#         #print(companies_json)
        
                
#     def gather_data(self):
#         # print('gather_data')
#         self.read_json()
        
#         for page in self.companies_json:
#             # print('page')
#             url = self.companies_json[page]
#             self.get_page_data(url, page)
# new = A()
# new.gather_data()
      