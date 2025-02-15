# Install Poetry and create venv in the builder step,
# then copy the venv to the runtime image, so that the runtime image is as small as possible.
FROM --platform=linux/amd64 python:3.10.14-bookworm AS builder

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM --platform=linux/amd64 python:3.10.14-bookworm AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY pyproject.toml poetry.lock ./
COPY mech_tool_deployment mech_tool_deployment
COPY tests tests

ENV PYTHONPATH=/app
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

CMD ["bash", "-c", "python mech_tool_deployment/run_agent.py ${runnable_agent_name} ${market_type}"]
