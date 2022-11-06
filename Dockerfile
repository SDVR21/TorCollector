#Dockerfile
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt install -y git python3.9 tor python3-pip
RUN update-alternatives --install /usr/bin/python3 python /usr/bin/python3.9 3
RUN git clone https://github.com/SDVR21/TorCollector.git /home/dwc
WORKDIR /home/dwc
RUN pip3 install -r requirements.txt
COPY ./onion.txt .
ENTRYPOINT ["sh", "command.sh"]