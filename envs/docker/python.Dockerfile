# One image per Python module: NAME picks requirements-<NAME>.txt.
# Python 3.12.6 as in ../clustbench.yml. fastcluster 1.2.6 has no cp312 wheel,
# so wheels are built in a full image and only installed in the slim one.
FROM python:3.12.6-bookworm AS build
ARG NAME=clustbench
COPY requirements-${NAME}.txt /tmp/requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r /tmp/requirements.txt

FROM python:3.12.6-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN --mount=type=bind,from=build,source=/wheels,target=/wheels \
    pip install --no-cache-dir --no-index /wheels/*.whl
