# THIS IS A TEST TO MAKE SURE IT UPLOADS TO AN EC2 INSTANCE

# python image
FROM python:3.8-slim-buster

# Copy everything from this directory into the container
COPY . .

# Install everything needed
RUN pip install -r requirements.txt

# Hey python, run file
#CMD ["python", "scraper/celebrities_scraper.py"]
CMD ["python", "test.py"]