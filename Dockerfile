FROM python:3.8.3-buster
ENV virtual=docker
RUN apt-get update && apt-get upgrade -y \
    python3 \
    python3-pip \
    nano \
    unixodbc-dev \
    curl 

WORKDIR /code

## now just copy all files here
COPY / .

RUN pip install -r requirements.txt
ENV PYTHONBUFFERED 1
# CMD python3 main.py --my-parameter $MY_PARAMETERS

CMD ["python", "main.py"]
# CMD ["bash"]