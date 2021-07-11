FROM ubuntu:latest
WORKDIR /usr/local/app
RUN apt-get  update 
RUN apt-get  install nano
RUN apt list --upgradable
RUN apt-get install iputils-ping -y 
RUN apt-get install net-tools -y
RUN apt-get install sysstat -y
Run apt-get install iproute2 -y
RUN adduser oba --shell /bin/bash 