FROM python:3.11
COPY app /app
WORKDIR /app
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
CMD ["python", "crawler.py"]
