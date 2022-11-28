# use prebuilt images of python
FROM python:3.8-slim-buster

    # Add trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    # Add chrome
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    # Updates chrome
    && apt-get -y update \
    # Install chrome
    && apt-get install -y google-chrome-stable \
    # Get chromedriver
    && wget -O /tmp/chromedriver.zip http://chromedriver.storgae.googleapis.com/'curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE' /-chromedriver_linux64.zip \
    # Unzip the chromedriver folder
    && apt-get install -yqq unzip \
    # Move it to the path
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Copy everything from the directory
COPY . . 

RUN pip install -r requirements.txt

CMD ["python", "DataCollectionPipeline.py"]