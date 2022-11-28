# use prebuilt images of python
FROM python:3.8-slim-buster



RUN apt-get update && apt-get install -y gnupg2 \
    && apt-get install -y wget \
    && wget -qO - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get -y update \
    && apt-get install -y google-chrome-stable \ 
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/'curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE'/chromedriver_linux64.zip \
    && apt-get install -yqq unzip 
    #&& unzip /temp/chromedriver.zip chromedriver -d /isr/local/bin/


COPY . . 

RUN pip install -r requirements.txt

CMD ["python3", "DataCollectionPipeline.py"]