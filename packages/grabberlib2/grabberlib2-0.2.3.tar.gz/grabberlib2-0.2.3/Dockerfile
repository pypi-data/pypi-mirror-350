# Backend setup
FROM python:3.11 AS development

WORKDIR /usr/src/app

ARG UV_SYSTEM_PYTHON=true
ARG UV_CONCURRENT_DOWNLOADS=10
ARG UV_CONCURRENT_BUILDS=5
ARG UV_CONCURRENT_INSTALLS=10
ARG FORCE_COLOR=1



ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.11 \
    UV_PROJECT_ENVIRONMENT=/usr \
    UV_SYSTEM_PYTHON=$UV_SYSTEM_PYTHON \
    UV_CONCURRENT_DOWNLOADS=$UV_CONCURRENT_DOWNLOADS \
    UV_CONCURRENT_BUILDS=$UV_CONCURRENT_BUILDS \
    UV_CONCURRENT_INSTALLS=$UV_CONCURRENT_INSTALLS \
    FORCE_COLOR=$FORCE_COLOR

# Installing uv
RUN pip install -U pip uv --no-cache-dir

# Installing requirements
COPY README.md pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv,id=uv uv sync

# Copying actuall application
COPY . .
