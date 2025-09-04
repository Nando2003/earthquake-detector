FROM ghcr.io/astral-sh/uv:python3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./django_app /django_app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

WORKDIR /django_app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "earthquake_detector.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
