FROM qiime2/core:2019.1
MAINTAINER Mingxun Wang "mwang87@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install urllib3==1.23
RUN pip install peewee
RUN pip install flask
RUN pip install requests
RUN pip install requests-cache
RUN pip install gunicorn
RUN pip install xmltodict
RUN apt-get install -y unzip
RUN wget https://github.com/mwang87/q2_metabolomics/archive/2.zip && unzip 2.zip && cd q2_metabolomics-2 && pip install .
RUN pip install tensorflow
RUN pip install tqdm
RUN pip install git+https://github.com/biocore/rhapsody.git
RUN qiime dev refresh-cache

COPY . /app
WORKDIR /app
