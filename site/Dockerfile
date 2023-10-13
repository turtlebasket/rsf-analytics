FROM "rockylinux:9"

# required for contourpy
RUN ["dnf", "install", "-y", "python3-pip"]
RUN ["pip3", "install", "--upgrade", "pip"]

WORKDIR /app/
COPY requirements.txt /app/
RUN ["pip3", "install", "-r", "requirements.txt"]

COPY . /app

CMD ["hypercorn", "main.py", "-b", "0.0.0.0:8000"]
