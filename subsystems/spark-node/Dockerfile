FROM renien/spark-stand-alone

LABEL maintainer="Manfredi G. Pistone & Walter D. Vergara for Engineering Ingegneria Informatica"

USER root

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y nano
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# python libraries
RUN pip3 install tensorflow==2.9.1
RUN pip3 install Pillow
RUN pip3 install numpy
RUN pip3 install requests
RUN pip3 install scikit-learn
