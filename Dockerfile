FROM python:3.7-alpine3.10
ENV TZ UTC
COPY . /
RUN pip install -r requirements.txt
RUN chmod +x run.py
CMD ["python", "run.py"]