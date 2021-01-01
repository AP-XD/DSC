FROM python:3.9

RUN apt -qq update
RUN apt -qq install -y --no-install-recommends \
    curl \
    git \
    gnupg2 \
    wget

RUN git clone https://github.com/APXD-git/DSC /root/dsc
WORKDIR /root/dsc/
RUN chmod +x /usr/local/bin/*
RUN pip install -r requirements.txt
CMD [ "python3", "-m", "dsc" ]
