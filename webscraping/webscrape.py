import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager


def webscrape_uwflow():
    root = "https://uwflow.com/explore"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Navigate to uwflow explore page
    driver.get(root)

    # Get course code and link to course website
    time.sleep(2.0)

    SCROLL_PAUSE_TIME = 1.0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    course_elems = driver.find_elements(by=By.XPATH, value="//div[@role='cell']/a")
    course_codes = [course_code.get_attribute('innerText') for course_code in course_elems]
    course_links = [course_code.get_attribute('href') for course_code in course_elems]

    # Contains the text on "num ratings", "liked", "useful", etc...
    course_elems = driver.find_elements(by=By.XPATH, value="//div[@class='sc-pIjat juxdEH']")
    course_elems_text = [course_code.get_attribute('innerText') for course_code in course_elems]

    rows = driver.find_elements(by=By.XPATH, value="//div[@role='rowgroup']/div[@role='row']")
    courses = {}
    for row in rows:
        # Get info from row
        course_info = row.find_elements(by=By.XPATH, value=".//div")
        
        # Course code
        course_code = course_info[0].text
       
        # Course title
        course_title = course_info[1].text
        
        # Course hyperlink
        course_link = course_info[0].find_element(by=By.XPATH, value=".//a")
        course_link = course_link.get_attribute('href')        
        
        # Course number of ratings
        course_num_ratings = course_info[2].text
        
        # Course usefulness rating
        course_useful_rating = course_info[3].text
        
        # Course easiness rating
        course_easy_rating = course_info[4].text
        
        # Course percent liked
        course_liked_rating = course_info[5].text

        courses[course_code] = {
            "course_title": course_title,
            "num_ratings": course_num_ratings,
            "useful": course_useful_rating,
            "easy": course_easy_rating,
            "liked": course_liked_rating
        }
    
    for course_code, course_link in list(zip(course_codes, course_links))[:5]:
        driver.get(course_link)

        # Read reviews:
        time.sleep(2.0)

        # Load all reviews
        # Scroll down to "see more" button and click
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='sc-qYhTA dLAucL']/button")))
            driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='sc-qYhTA dLAucL']/button"))))
            time.sleep(2.0)
            ActionChains(driver).move_to_element(WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='sc-qYhTA dLAucL']/button")))).click().perform()
        except TimeoutException:
            pass

        # Get reviews and get "liked" or "disliked" for each review:
        reviews = driver.find_elements(by=By.XPATH, value="//div[@class='sc-pcZJD cnFfnA']")
        reviews_clean = []
        for review in reviews:
            # Get review text
            review_text = review.find_element(by=By.XPATH, value=".//div/div/div[@class='sc-pLwIe kqSAIH']")
            review_text = review_text.text

            # Get "liked" or "disliked" from review:
            review_ratings = review.find_elements(by=By.XPATH, value=".//div[@class='sc-pRFHb kfZOQo']/div")
            review_ratings = [review_rating.get_attribute('class') for review_rating in review_ratings]
            good_course = 'sc-pZCuu gDCRrI'
            bad_course = 'sc-pZCuu blNAgC'

            try:
                if review_ratings[0] == good_course:
                    rating = "liked course"
                    #review_ratings_verbose.append("liked course")
                else:
                    rating = "disliked course"
                    #review_ratings_verbose.append("disliked course")
            except IndexError:
                # Happens if the review did not give a rating to the course
                rating = None
            
            reviews_clean.append({
                "review_text": review_text,
                "course_rating": rating
            })

        # Add reviews to course
        courses[course_code]["reviews"] = reviews_clean
                
    # Save
    with open("./data/course_data.json", "w") as f:
        json.dump(courses, f)


if __name__ == "__main__":
    webscrape_uwflow()
