from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Initialize the WebDriver
driver = webdriver.Chrome("C:/selenium_driver/chromedriver-win64_120/chromedriver.exe")

url = 'https://www.google.com/maps/@19.1987712,72.876032,12z?entry=ttu'

driver.get(url)

# Load the webpage
def data_load(targets):
    patterns = ['Address:', 'Phone:', 'Website:']

    final_rows = []
    for target in targets:
        try:
            time.sleep(2)
            # Wait for the button to be clickable
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'button.e2moi[aria-label={target}]'))
            )
            # Click the button
            button.click()
            time.sleep(5)

            # Find the scrollable div
            scroll_div = driver.find_element(By.XPATH, f'.//div[@aria-label="Results for {target}"]')

            # Scroll down the div multiple times to load more content
            for _ in range(40):  # Adjust the number of times to scroll as needed
                scroll_div.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.5)

            # Find all links with class name "hfpxzc"
            all_links = driver.find_elements(By.CLASS_NAME, "hfpxzc")

            # Iterate through each link
            for link in all_links:
                
                # Get aria-label of the link
                aria_label = link.get_attribute("aria-label")
                #print("Link aria-label:", aria_label)
                label = [aria_label]
                # Get href of the link
                href = link.get_attribute("href")
                #print("Link href:", href)
                ref = [href]
                link.click()
                time.sleep(1)
            # Find all buttons with the specified class name
                buttons = driver.find_elements(By.CSS_SELECTOR, 'button.CsEnBe')

                # Iterate through each button
                for button in buttons:
                    # Get the href attribute of the button
                    href = button.get_attribute("href")

                    # Get the aria-label attribute of the button
                    aria_label = button.get_attribute("aria-label")

                    # Print the href and aria-label attributes
                    #print("Button href:", href)
                    #print("Button aria-label:", aria_label)
                    label.append(aria_label)
                    ref.append(href)
                # Find all anchor tags with the specified class name
                anchor_tags = driver.find_elements(By.CSS_SELECTOR, 'a.CsEnBe')

                # Iterate through each anchor tag
                for num , anchor_tag in enumerate(anchor_tags):
                    # Get the aria-label attribute of the anchor tag
                    aria_label = anchor_tag.get_attribute("aria-label")
                    # Get the href attribute of the anchor tag
                    href = anchor_tag.get_attribute("href")

                    # Get the aria-label attribute of the anchor tag
                    aria_label = anchor_tag.get_attribute("aria-label")

                    # Print the href and aria-label attributes
                    #print("Anchor href:", href)
                    #print("Anchor aria-label:", aria_label)
                    label.append(aria_label)
                    ref.append(href)
                #print(label,ref)
                temp = []
                temp.append(label[0]) # name of buisness
                temp.append(ref[0]) # link for buisness
                for pat in patterns:  # code for address,phone no, website url
                    var = False 
                    for x in label :
                        if pat in x:
                            temp.append(x.replace(pat, "").strip())
                            var = True
                            break
                    if not var :
                        temp.append(None)
                temp.append(target)  # type of buisness eg. restaurant , hotel,etc
                references = ''
                for l in range(1,len(ref)):
                    if ref[l] is not None :
                        references =references+ str(ref[l]) + ','
                temp.append(references)
                final_rows.append(temp)
                    

            #print(final_rows)

            print("Links processed successfully!")

        except Exception as e:
            print("An error occurred:", e)
        time.sleep(3)
        driver.get(url)
    
    # Close the WebDriver
    driver.quit()
    return final_rows


def main():
    
    header = ['Restaurants','Hotels','Things to do','Museums','Transit','Pharmacies','ATMs']
    
    
    rows = data_load(header)
    columns = ['Buisness_name', 'link', 'Address','phone number','Website','type','other_links']

    df = pd.DataFrame(rows, columns = columns) 
    print(df)
    df.to_csv('file1.csv')


if __name__ == '__main__':
    main()
