#FROM python:3.9
#
#ENV PYTHONUNBUFFERED 1
#WORKDIR /app
#
#ADD . /app
#
#COPY cosmos .
#
#COPY transfer/requirements.txt ./
#RUN pip install -r requirements.txt
#
#
#COPY . /app
#
#WORKDIR /app
#RUN python manage.py makemigrations
#RUN python manage.py migrate
##EXPOSE 8000
##CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .
