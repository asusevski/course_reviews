# syntax=docker/dockerfile:1
FROM huggingface/transformers-tensorflow-gpu as base

RUN python3 -m pip install notebook
RUN python3 -m pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu113
RUN python3 -m pip install tensorflow-addons

WORKDIR /course_reviews/

CMD ["bash"]
