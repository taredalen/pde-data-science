FROM rasa/rasa:3.3.3

WORKDIR '/app'
COPY . /app
USER root

COPY ./data /app/data
COPY ./models /app/models

RUN pip install --verbose spacy
RUN python -m spacy download en_core_web_md

VOLUME /app
VOLUME /app/data
VOLUME /app/models
CMD ["run", "-m", "/app/models", "--enable-api", "--cors","*","--debug" , "--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]

