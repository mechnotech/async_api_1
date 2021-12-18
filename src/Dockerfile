FROM python:3.9
RUN apt-get update && apt-get install -y iputils-ping
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY ./ /code
CMD ["python3", "/code/main.py"]