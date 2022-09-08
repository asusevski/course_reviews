from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import json

import time 
from selenium.webdriver.common.action_chains import ActionChains


def webscrape_uwflow() -> dict:
    root = "https://uwflow.com/explore"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Navigate to uwflow explore page
    driver.get(root)

    # Get course code and link to course website
    time.sleep(2.0)

    SCROLL_PAUSE_TIME = 1.0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Arbitrary limit of number of times page scrolls down
    c = 1
    while c <= 1:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        c += 1

    course_elems = driver.find_elements(by=By.XPATH, value="//div[@role='cell']/a")
    course_codes = [course_code.get_attribute('innerText') for course_code in course_elems]
    course_links = [course_code.get_attribute('href') for course_code in course_elems]

    courses = {}
    # temporary for quick testing: doing every 10th course
    for course_code, course_link in list(zip(course_codes, course_links))[::10]:
        driver.get(course_link)

        # Read reviews:
        time.sleep(2.0)

        # Load all reviews
        # Scroll down to "see more" button and click
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='sc-qYhTA dLAucL']/button")))
            driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='sc-qYhTA dLAucL']/button"))))
            time.sleep(2.0)
            ActionChains(driver).move_to_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='sc-qYhTA dLAucL']/button")))).click().perform()
        except TimeoutException:
            pass

        # Get reviews:
        reviews = [review.get_attribute('innerText') for review in driver.find_elements(by=By.XPATH, value="//div[@class='sc-pcZJD cnFfnA']/div/div/div[@class='sc-pLwIe kqSAIH']")]
        courses[course_code] = [{"id": idx, "review": review} for idx, review in enumerate(reviews)]\
    
    # Save
    with open("./data/courses_sample.json", "w") as f:
        json.dump(courses, f)


def webscrape_uwflow2() -> dict:
    root = "https://uwflow.com/explore"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Navigate to uwflow explore page
    driver.get(root)

    # Set search to courses with at least 1 rating:
    slider = driver.find_element(by=By.CLASS_NAME, value="sc-fzpkJw eOZpjb")
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(container.size['width'], 0).release().perform()
    # Get course code and link to course website
    time.sleep(2.0)

    # TEST
    # ----------------------------
    SCROLL_PAUSE_TIME = 1.0

    # Get scroll height
    at_least_one_review = True
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        if new_height == last_height:
            break
        last_height = new_height
    # ----------------------------

    time.sleep(10.0)
    courses = driver.find_elements(by=By.XPATH, value="//div[@role='cell']/a")
    print([course.get_attribute('innerText') for course in courses])

webscrape_uwflow()