FROM python:3.14-slim-bookworm

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen

COPY crawl.py main.py ./

ENTRYPOINT ["uv", "run", "main.py"]



