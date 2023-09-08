FROM "python:3.9.18-alpine3.18"

COPY . /app
WORKDIR /app

# required for contourpy
RUN ["apk", "add", "make", "g++", "meson"]
RUN ["pip3", "install", "--upgrade", "pip"]
RUN ["pip3", "install", "-r", "requirements.txt"]
CMD ["hypercorn", "main.py", "-b", "0.0.0.0:8000"]
