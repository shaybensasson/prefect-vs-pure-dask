FROM python:3.8.2

# set labels to this final image
LABEL author="Shay Ben-Sasson"
LABEL owner="shaybensasson@gmail.com"

# we set environment variables that set the locale correctly,
# stop Python from generating .pyc files, and enable Python tracebacks on segfaults:
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

###########################################################
# Create the user that will run the app, copy app files
#  and amend security stuff
###########################################################
RUN adduser --home /usr/app --disabled-password --gecos '' appuser
RUN usermod -aG sudo appuser
WORKDIR /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install --no-cache-dir --no-deps -e .

# FUTURE: each run creates a new layer, can we join them?
# essential permissions (e.g. create dask-worker-space)
RUN chown -R appuser:appuser /usr/app
RUN chmod 755 /usr/app

###########################################################
# Final environment settings
###########################################################
USER appuser

# only local testing runs, orchestrators discard it
#dask-scheduler
EXPOSE 8786
EXPOSE 8787

CMD ["python", "prefect_vs_pure_dask/lightgbm_train_and_inference_sanity.py"]