import json


def good_course(course, col_name='liked', threshold=50):
    percent = course[col_name]
    percent = percent.replace('%', '')
    if not percent.isnumeric():
        # If no rating, return 0 (not a good course)
        return 0
    percent = int(percent)
    if percent >  threshold:
        return 1
    return 0


def preprocess_webscraped_data(path="./data/raw_data/course_data.json"):
    out_path = "./data/processed_data/course_data_clean.json"
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
        # We may also be interested in knowing how many reviews a course has where the reviewer ALSO left a rating
        num_reviews_with_rating = 0

        # Also assigning a label of 1 if the reviewer gave a thumbs up and 0 if they gave a thumbs down
        reviews_clean = []
        for review in reviews:
            course_rating = review['course_rating']
            review_clean = review.copy()
            if not course_rating:
                review_clean['course_rating_int'] = None
                reviews_clean.append(review_clean)
                continue

            num_reviews_with_rating += 1
            if course_rating == "liked course":
                course_rating_int = 1
            else:
                course_rating_int = 0
            
            review_clean['course_rating_int'] = course_rating_int
            reviews_clean.append(review_clean)

        course = {
                'course_code': course_code,
                'course_title': course_title,
                'num_ratings': num_ratings,
                'useful': useful_rating,
                'easy': easy_rating,
                'liked': liked_percent,
                'reviews': reviews_clean,
                'num_reviews': num_reviews,
                'num_reviews_with_rating': num_reviews_with_rating
        }
        
        course['good_course'] = good_course(course)
        course_data_clean.append(course)
    
    with open(out_path, "w") as f:
        json.dump(course_data_clean, f)


if __name__ == "__main__":
    preprocess_webscraped_data()
