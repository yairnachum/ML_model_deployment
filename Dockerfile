# use python 3.8 as base image
FROM python:3.8-slim-buster
# setting working directory
WORKDIR /
# Set environment variables used by the flask command
ENV FLASK_APP=app.py
# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# open port 3000
EXPOSE 3000
COPY . .
CMD ["python", "app.py"]