FROM python:3.7.4-slim-stretch


COPY ./app /Food_Delivery/app
COPY ./static /Food_Delivery/static
COPY ./templates /Food_Delivery/templates
COPY ./requirements.txt /Food_Delivery
COPY ./main.py /Food_Delivery

WORKDIR /Food_Delivery

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]

