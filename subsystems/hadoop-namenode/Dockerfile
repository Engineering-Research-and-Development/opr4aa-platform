FROM bde2020/hadoop-namenode:2.0.0-hadoop3.1.3-java8

LABEL maintainer="Manfredi G. Pistone & Walter D. Vergara for Engineering Ingegneria Informatica"

USER root

COPY ./custom-init.sh /custom-init.sh
RUN chmod a+x /custom-init.sh

COPY ./inject.sh /inject.sh
RUN chmod a+x /inject.sh

CMD ["/custom-init.sh"]
