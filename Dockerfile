############ Release ######################
FROM python:3.7-alpine3.10
ENV TZ UTC
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY autoscrape autoscrape
COPY boot.sh run.py ./
RUN chmod +x boot.sh

############ Run Application ##############
RUN addgroup -g 9001 appgroup && adduser -u 9001 -S appuser -G appgroup
USER appuser
ENTRYPOINT ["./boot.sh"]