from selenium import webdriver
from browsermobproxy import Server
import json
from haralyzer import HarParser

# Start the BrowserMob Proxy server
server = Server("C:\Python311\Lib\site-packages\browsermobproxy\server.py")
server.start()
proxy = server.create_proxy()

# Configure the Selenium driver to use the proxy
chrome_options = webdriver.FirefoxOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))

# Open the webpage using the Selenium driver
driver = webdriver.Chrome("C:\Selenium", chrome_options=chrome_options)
driver.get("https://exactspace.co/")

# Generate the .har file
proxy.new_har("exactspace")

# Parse the generated .har file
har = json.loads(proxy.har)['log']
har_parser = HarParser(har)
entries = har_parser.har_data['entries']

# Count the status codes
total_count = len(entries)
status_2xx_count = 0
status_4xx_count = 0
status_5xx_count = 0

for entry in entries:
    status_code = entry['response']['status']
    if status_code >= 200 and status_code < 300:
        status_2xx_count += 1
    elif status_code >= 400 and status_code < 500:
        status_4xx_count += 1
    elif status_code >= 500 and status_code < 600:
        status_5xx_count += 1

# Display the status code counts
print("Total status code count:", total_count)
print("Total count for 2XX status codes:", status_2xx_count)
print("Total count for 4XX status codes:", status_4xx_count)
print("Total count for 5XX status codes:", status_5xx_count)
print(proxy.har)

# Stop the BrowserMob Proxy server and close the Selenium driver
server.stop()
driver.quit()
