FROM cypress/included:9.5.3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  build-essential \
  musl-dev \
  libpq-dev \
  python3-dev \
  python3-pip \
  libssl-dev \
  rustc \
  git

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt