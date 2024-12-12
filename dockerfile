
FROM python:3.11-slim-buster


WORKDIR /code


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

EXPOSE 8000

# Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]