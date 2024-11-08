# using ubuntu LTS version
FROM ubuntu:24.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-dev python3-venv python3-pip python3-wheel build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3 -m venv /home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir gunicorn

FROM ubuntu:24.04 AS runner-image
RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home myuser
USER myuser
COPY --from=builder-image --chown=myuser:myuser /home/myuser/venv /home/myuser/venv

RUN mkdir /home/myuser/code && mkdir /home/myuser/output && mkdir /home/myuser/code/cheatsheets
WORKDIR /home/myuser/code
COPY --chown=myuser:myuser . .
RUN chmod +x docker/cmd.sh

EXPOSE 5000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"
ENV CHEATSHEET_OUTPUT_DIR="/home/myuser/output"

# /dev/shm is mapped to shared memory and should be used for gunicorn heartbeat
# this will improve performance and avoid random freezes
# CMD ["gunicorn","-b", "0.0.0.0:5000", "-w", "4", "-k", "gevent", "--worker-tmp-dir", "/dev/shm", "app:app"]

# CMD [ "python3", "src/generate_cheatsheet.py" ]
CMD [ "docker/cmd.sh" ]
