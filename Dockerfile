FROM python:3
RUN apt-get update
RUN mkdir /tmp/code
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt
COPY comment_ripper.py /comment_ripper.py
COPY comment_ripper_schema.json /comment_ripper_schema.json
COPY config.json /config.json
COPY comment_ripper_service.py /comment_ripper_service.py
WORKDIR ./
EXPOSE 5000
CMD ["python" , "/comment_ripper_service.py"]