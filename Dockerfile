FROM python:3.8-slim-bullseye
RUN mkdir -p /code/app
COPY start.sh /
COPY app /code/app
COPY tests /code/tests
COPY requirements.txt /code/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /code/requirements.txt
WORKDIR /code/
# Run unit tests
RUN python3 -m unittest discover -s /code/tests
#EXPOSE 8000
