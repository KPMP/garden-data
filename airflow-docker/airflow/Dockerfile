FROM python:3.6.3

# supervisord setup                       
RUN apt-get update && apt-get install -y supervisor                       
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Airflow setup                       
ENV AIRFLOW_HOME=/app/airflow
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes
RUN pip install --upgrade pip
RUN pip install pymongo
RUN pip install apache-airflow                       

RUN airflow initdb
EXPOSE 8080
CMD ["/usr/bin/supervisord"]
