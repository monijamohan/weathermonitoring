FROM python:3.8-slim-bullseye
RUN mkdir -p /code/app

# Copying the deps
COPY app /code/app
COPY tests /code/tests
COPY logs /code/logs
COPY requirements.txt /code/requirements.txt
COPY VERSION.txt /code/VERSION.txt

# Installing the requirements
RUN python3 -m pip install --no-cache-dir -r /code/requirements.txt
WORKDIR /code/

# Run unit tests
RUN python3 -m unittest discover -s /code/tests

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
