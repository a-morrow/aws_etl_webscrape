# Package import
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# AWS Workshops URL
aws_url = "https://workshops.aws/"

# Connection -- Fetch web-page
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(aws_url)

# Allow web-page to render
sleep(3)

workshops_list = []

for k in range(1,366):
    print('Beginning Extract',k)
    filter_path = f"//aws-workshop-card[{k}]//mat-card[1]"
    title_path = f"//aws-home[1]/section[1]/aws-workshop-card[{k}]/mat-card[1]/mat-card-content[1]/div[1]/div[1]"
    level_path = f"//aws-home[1]/section[1]/aws-workshop-card[{k}]/mat-card[1]/mat-card-content[1]/div[1]/div[2]/span[1]"
    categories_path = f"//aws-home[1]/section[1]/aws-workshop-card[{k}]/mat-card[1]/mat-card-content[1]/div[1]/div[3]/span[1]"
    tags_path = f"//aws-home[1]/section[1]/aws-workshop-card[{k}]/mat-card[1]/mat-card-content[1]/div[1]/div[4]/span[1]"
    duration_path = f"//aws-workshop-card[{k}]/mat-card[1]/mat-card-content[1]/div[1]/div[5]/span[1]"
    descr_path = f"//aws-workshop-card[{k}]/mat-card[1]/mat-card-content[1]/div[1]/p[1]"
    links_path = f"//aws-workshop-card[{k}]//mat-card[1]//mat-card-actions[1]//a[1]"

    workshops = driver.find_elements('xpath',filter_path)

    for i in workshops:
        title = i.find_element('xpath',title_path).text
        level = i.find_element('xpath',level_path).text
        categories = i.find_element('xpath',categories_path).text
        tags = i.find_element('xpath',tags_path).text
        duration = i.find_element('xpath',duration_path).text
        description = i.find_element('xpath',descr_path).text
        link = [k.get_attribute("href") for k in i.find_elements('xpath',links_path)]
        workshop_item = {
            'title': title,
            'level': level,
            'categories': categories,
            'tags':tags,
            'duration':duration,
            'description':description,
            'link':link
        }
        workshops_list.append(workshop_item)
    print('Extract Complete')
    sleep(1)

# Create DateFrame
df = pd.DataFrame(workshops_list)

# Close Web-Driver
driver.close()

# Write data to csv-file
print('Extracting to CSV')
df.to_csv('C:\\Users\\amorrow\\Documents\\AWS_Workshops\\aws_workshops_v1.csv', encoding='utf-8',index=False)
print('Extract to CSV Complete')

# Read csv-file
print('Reading-in csv-file')
aws_workshops_df = pd.read_csv('C:\\Users\\amorrow\\Documents\\AWS_Workshops\\aws_workshops_v1.csv')
# Begin data-cleaning process
print('Begin data cleaning...')
aws_workshops_df['categories'] = aws_workshops_df['categories'].map(lambda x: x.lstrip('Categories:'))
aws_workshops_df['tags'] = aws_workshops_df['tags'].map(lambda x: x.lstrip('Tags:'))
aws_workshops_df['level'] = aws_workshops_df['level'].map(lambda x: x.lstrip('Level:'))
aws_workshops_df['link'] = aws_workshops_df['link'].map(lambda x: x.lstrip("['").rstrip("']"))
print('End data cleaning...\nExtracting to new CSV')
# Write data to new csv-file
aws_workshops_df.to_csv('C:\\Users\\amorrow\\Documents\\AWS_Workshops\\aws_workshops_v2.csv', index=False)