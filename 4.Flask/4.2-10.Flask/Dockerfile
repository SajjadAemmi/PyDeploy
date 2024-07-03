FROM python

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /myapp

COPY requirements.txt /myapp

RUN pip install -r requirements.txt

# COPY . /myapp

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
