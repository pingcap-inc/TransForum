FROM python:3.11.9-slim

RUN apt-get update

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

ENV PYTHONPATH /app

EXPOSE 4000

CMD ["python", "manage.py", "runserver", "--host", "0.0.0.0", "--port", "4000"]
