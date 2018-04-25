FROM       python:3.6-slim-stretch
RUN        pip install kubernetes
COPY       sidecar/sidecar.py /app/
WORKDIR    /app/
CMD [ "python", "/app/sidecar.py" ]