from selenium import webdriver
import selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions 
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import os
import undetected_chromedriver as uc



## PATH & URL
DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
DOWNLOAD_PATH = "C:/Users/TolgaKurt/Desktop/odmd"
NAV_XPATH = "//*[@class='navigatelink_current' or @class='navigatelink']"
url = "https://www.odmd.org.tr/web_2837_1/sortial.aspx?linkpos=1&target=categorial1&type=36&primary_id=&detail=single&sp_table=&sp_primary=&sp_fields=&sp_language=&sp_table_extra=&extracriteria=&language_id=1&search_fields=&search_values="


## Driver setup
# download file path

def driver_setup(driver_path, download_path = None):

    if download_path == None:
        options = ChromeOptions()
        driver = uc.Chrome(options=options)
        return driver
    else:
        if os.path.exists(download_path):
            pass
        else:
            os.makedirs(download_path)

        options = ChromeOptions()
        #options.add_experimental_option("prefs",chrome_prefs)
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        driver = uc.Chrome()
        params = {
            "behavior": "allow",
            "downloadPath": download_path
        }
        driver.execute_cdp_cmd("Page.setDownloadBehavior", params)


    return driver




#######################





## get navigation link

def get_nav_link(driver, XPATH):
    
    navigate_links = driver.find_elements(By.XPATH,XPATH)
    
    navigate_lists = []

    navigate_text = []
    
    ## navigation bar elements
    [navigate_lists.append(x) for x in navigate_links if x not in navigate_lists and x.text != 'Sonraki >']

    ##navigation bar text (for unique values)
    [navigate_text.append(x.text) for x in navigate_links if x.text not in navigate_text and x.text != 'Sonraki >']
    
    unique_value = len(navigate_text)

    return navigate_lists, navigate_text,unique_value


## click event

def click_nav_item(item):

    retries = 3
    
    for _ in range(retries):
    
        try:
    
            item.click()
    
            return True
    
        except selenium.common.exceptions.StaleElementReferenceException:
    
            time.sleep(1)
    
    return False



## fetch current page elements by class name
def fetch_elements(driver, class_name):
    
    elements = driver.find_elements(By.CLASS_NAME,class_name)

    return elements




def main():
    driver = driver_setup(driver_path= DRIVER_PATH)

    driver.get(url)

    ## Wait until load navigation links
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, NAV_XPATH))
        )
    
    ##get navigate lists and number of navigation page
    navigate_lists, navigate_text, unique_value = get_nav_link(driver= driver, XPATH= NAV_XPATH)

    ##setup main window
    main_window = driver.current_window_handle


    for i in range(0,unique_value):
        time.sleep(5)
        ## fetch navigate links for every iterations
        navigate_lists, navigate_text, unique_value = get_nav_link(driver=driver, XPATH= NAV_XPATH)
        
        ## fetch page elements by class name
        elements = fetch_elements(driver= driver, class_name= "td_reports_name")

        ##check nav links
        if click_nav_item(navigate_lists[i]):
            # Wait for the page to load or some specific element on the new page
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, NAV_XPATH))
                )

            elements = fetch_elements(driver=driver, class_name= "td_reports_name")

            ## loop on files
            for item in elements:

                item.click()

            
                ### wait until open new page
                WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))

                new_window = [window for window in driver.window_handles if window != main_window][0]
                
                driver.switch_to.window(new_window)

                time.sleep(8)

                driver.close()
        
                # Ana pencereye geri dön
                driver.switch_to.window(main_window)

                print(item.text,"  Clicked!")


    ##Quit browser
    driver.quit()


if __name__ == "__main__":
    main()