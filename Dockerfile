FROM python:3.13-slim-bookworm@sha256:a5a7017efc5969e00ae2b91c8eb0631049a569652aa4ffc4501769049ae45c72 AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/src
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt \
    && groupadd --gid 10001 clinic && useradd --uid 10001 --gid clinic --no-create-home clinic
COPY src/ src/
USER 10001:10001
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "clinic_ai.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]

FROM runtime AS test
USER root
COPY requirements-test.txt .
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements-test.txt
COPY tests/functional/ tests/functional/
USER 10001:10001
ENTRYPOINT ["python", "-m", "pytest", "-p", "no:cacheprovider", "-v", "tests/functional"]
