FROM python:3.10-slim

RUN apt update && \
    apt install -y --no-install-recommends \
    openssh-client  \
    iputils-ping

RUN pip install --upgrade pip &&\
    pip install     \
    fire            \
    python-dotenv   \
    PyYAML          \
    rich

CMD ["/bin/bash"]