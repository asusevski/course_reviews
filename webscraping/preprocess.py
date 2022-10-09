import json
import pandas as pd


def preprocess_webscraped_data(path="./data/raw_data/course_data.json"):
    out_path = "./data/processed_data/course_data_clean.csv"
    with open(path, "r") as f:
        course_data = json.load(f)

    course_data_clean = []
    for course_code, course_info in course_data.items():
        course_title = course_info['course_title']
        num_ratings = course_info['num_ratings']
        useful_rating = course_info['useful']
        easy_rating = course_info['easy']
        liked_percent = course_info['liked']
        reviews = course_info['reviews']
        num_reviews = len(reviews)

        course = {
                'course_code': course_code,
                'course_title': course_title,
                'num_ratings': num_ratings,
                'useful': useful_rating,
                'easy': easy_rating,
                'liked': liked_percent,
                'num_reviews': num_reviews
        }
        
        # Also assigning a label of 1 if the reviewer gave a thumbs up and 0 if they gave a thumbs down
        for review in reviews:
            review_text = review['review_text']
            course_rating = review['course_rating']
            if not course_rating:
                course_rating_int = None
            else:
                if course_rating == "liked course":
                    course_rating_int = 1
                else:
                    course_rating_int = 0
            
            course_clean = course.copy()
            course_clean['reviews'] = review_text
            course_clean['course_rating'] = course_rating
            course_clean['course_rating_int'] = course_rating_int
            # Each row is a review
            course_data_clean.append(course_clean)

    df = pd.DataFrame(course_data_clean)
    df.to_csv(out_path, index=False)


if __name__ == "__main__":
    preprocess_webscraped_data()
