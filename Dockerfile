FROM python:3.11-slim-buster


RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev  \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libpython3-dev \
    wget \
    git \
    libxmlsec1 \
    libxmlsec1-dev \
    wkhtmltopdf \
    cmake 

WORKDIR /app

COPY mysite/ /app/mysite/
COPY mysite/requirements.txt /app/

COPY ./runtime.txt .
COPY entrypoint.sh /app/entrypoint.sh
RUN pip install -r requirements.txt
# Permisos
RUN chmod +x /app/entrypoint.sh
# Expose port 8000 for the Django development server
EXPOSE 8000

CMD ["/app/entrypoint.sh"]