# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By

# path = "D:\Tools\crawl\chromedriver-win64\chromedriver.exe" # path_to_chromedriver.exe

# service = Service(executable_path=path)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=service, options=options)

# # Open the URL of the website
# url = 'https://example.com'
# driver.get(url)

# # Wait for the page to fully load (you might need to adjust the timeout)
# driver.implicitly_wait(10)

# # Create a list to store all the links
# all_links = []

# try:
#     # Extract links from various HTML elements
#     tags_to_extract = ['a', 'img', 'script', 'link', 'area', 'form', 'frame', 'iframe', 'object', 'embed']

#     for tag_name in tags_to_extract:
#         elements = driver.find_elements_by_tag_name(tag_name)
        
#         for element in elements:
#             if tag_name in ['a', 'link', 'area']:
#                 link = element.get_attribute('href')
#             elif tag_name in ['img', 'script']:
#                 link = element.get_attribute('src')
#             elif tag_name == 'form':
#                 link = element.get_attribute('action')
#             elif tag_name == 'object':
#                 link = element.get_attribute('data')
#             elif tag_name == 'embed':
#                 link = element.get_attribute('src')
#             elif tag_name in ['frame', 'iframe']:
#                 link = element.get_attribute('src')
            
#             if link:
#                 all_links.append(link)

#     # Print the extracted links
#     print("All Links:")
#     for link in all_links:
#         print(link)

# except Exception as e:
#     print("Error:", e)

# # Close the browser
# driver.quit()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://example.com/")

# elem = driver.find_element(By.TAG_NAME , "a")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source

print(driver.page_source)

element = driver.find_element(By.TAG_NAME , "a")
print(element.get_attribute("href"))

driver.close()

# from selenium import webdriver
# from selenium.webdriver.common.by import By

# # Set up the Selenium WebDriver (ensure you have the appropriate driver installed)
# driver = webdriver.Firefox()

# # Open the URL of the website
# url = 'https://example.com'
# driver.get(url)

# # Wait for the page to fully load (you might need to adjust the timeout)
# driver.implicitly_wait(10)

# # Create a list to store all the links
# all_links = []

# try:
#     # Define the HTML tags to extract links from
#     tags_to_extract = ['a', 'img', 'script', 'link', 'area', 'form', 'frame', 'iframe', 'object', 'embed']

#     for tag_name in tags_to_extract:
#         elements = driver.find_elements(By.TAG_NAME, tag_name)

#         for element in elements:
#             if tag_name in ['a', 'link', 'area']:
#                 link = element.get_attribute('href')
#             elif tag_name in ['img', 'script']:
#                 link = element.get_attribute('src')
#             elif tag_name == 'form':
#                 link = element.get_attribute('action')
#             elif tag_name == 'object':
#                 link = element.get_attribute('data')
#             elif tag_name == 'embed':
#                 link = element.get_attribute('src')
#             elif tag_name in ['frame', 'iframe']:
#                 link = element.get_attribute('src')

#             if link:
#                 all_links.append(link)

#     # Print the extracted links
#     print("All Links:")
#     for link in all_links:
#         print(link)

# except Exception as e:
#     print("Error:", e)

# # Close the browser
# driver.quit()
