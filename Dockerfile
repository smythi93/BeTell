FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN git config --global user.email "betell@example.org" && git config --global user.name "betell" \
    && git config --global --add safe.directory '*'
WORKDIR /opt/betell
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
WORKDIR /repo
ENTRYPOINT ["betell"]
CMD ["demo"]
