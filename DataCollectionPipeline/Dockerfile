# use prebuilt images of python
FROM python:3.8-slim-buster

COPY . . 

# RUN pip install -r requirements.txt
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - | 
    && sh -c ''

CMD ["python", "DataCollectionPipeline.py"]