from collections import Counter
import gradio as gr
import json
import numpy as np
from transformers import pipeline


def main():

    # Read data:
    file_path = "./data/courses_sample.json"
    with open(file_path, "r") as f:
        course_examples = json.load(f)

    # Set up dropdown options
    options = list(course_examples.keys())
    def fn(dropdown_choice):
        retval = course_examples.get(dropdown_choice)
        if not retval:
            print("Error, course not found.")
            return
            
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        candidate_labels = ['good course', 'bad course']
        course_data = course_examples[dropdown_choice]
        course_reviews = [elem["review"] for elem in course_data]
        classifications = classifier(course_reviews, candidate_labels)
        counts = Counter()
        for clf in classifications:
            idx = np.where(np.array(clf['scores']) > 0.5)[0][0]
            label = clf['labels'][idx]
            counts.update({label: 1})
        return f"Course results for {dropdown_choice}: {counts}"


    gr.Interface(fn, [gr.inputs.Dropdown(options)], "text").launch()


if __name__ == "__main__":
    main()
