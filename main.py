#import gradio as gr
import json
#import numpy as np
#from transformers import pipeline


def main():

    # Read data:
    file_path = "./data/processed_data/course_data_clean.json"
    with open(file_path, "r") as f:
        courses = json.load(f)

    # Set up dropdown options
    course_reviews_mapping = {}
    course_good_course_mapping = {}
    for course in courses:
        course_code = course['course_code']
        review = course['review_text']
        good_course = course['good_course']
        if course_code not in course_reviews_mapping:
            course_reviews_mapping[course_code] = [review]
            continue
        course_reviews_mapping[course_code].append(review)

        if course_code not in course_good_course_mapping:
            course_good_course_mapping[course_code] = good_course

    dropdown_options = list(course_reviews_mapping.keys())

    def zero_shot_classifier_fn(dropdown_choice):
        course_reviews = course_reviews_mapping.get(dropdown_choice)
        if not course_reviews:
            print("Error, course not found.")
            return
        
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        candidate_labels = ['good course', 'bad course']
        
        classifications = classifier(course_reviews, candidate_labels)
        counts = Counter()
        for clf in classifications:
            idx = np.where(np.array(clf['scores']) > 0.5)[0][0]
            label = clf['labels'][idx]
            counts.update({label: 1})
        return f"Course results for {dropdown_choice}: {counts}"

    gr.Interface(zero_shot_classifier_fn, [gr.inputs.Dropdown(dropdown_options)], "text").launch()


if __name__ == "__main__":
    main()
