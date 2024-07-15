from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
banks=['NICA','SBL','GBIME','NABIL','PRVU']
driver=webdriver.Chrome()
for bank in banks:
        file_name=f"data/{bank}_Dividend.csv"
        driver.get(f"https://eng.merolagani.com/CompanyDetail.aspx?symbol={bank}#0")
        # dividend_button=driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_CompanyDetail1_lnkDividendTab")
        time.sleep(3)
        # Wait for the dividend tab button to be clickable
        dividend_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_CompanyDetail1_lnkDividendTab"))
        )
        dividend_button.click()
        

        time.sleep(4)
        page_content=driver.page_source

        # with open("webpage.html", "w", encoding='utf-8') as file:
        #         file.write(page_content)

       
        soup = BeautifulSoup(page_content, "html.parser")

        # Find the table with the dividend data
        tables = soup.find_all('table', class_="table table-bordered table-striped table-hover")
        dividend_table = tables[6]


        # Initialize a list to hold the extracted data
        dividend_data = []

        # Iterate over the rows of the table
        for row in dividend_table.find_all('tr')[1:]:  # Skipping the header row
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                dividend_data.append(cols)


        # Print the extracted data
        # for data in dividend_data:
        # print(data)

        # Save the extracted data to a CSV file (optional)
        import csv
        with open(file_name, "w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["#", "Fiscal Year", "Cash Dividend", "Bonus Share", "Right Share"])
                writer.writerows(dividend_data)

        print(f"Dividend data has been saved to {file_name}")

driver.close()