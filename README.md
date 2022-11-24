# prefect-vs-pure-dask

Prefect (with dask runner) vs Dask

# Docker and docker-compose

## Build the docker

```bash
docker build . -t prefect-vs-dask:latest
```

## Sanity check for `docker run`

checks training (using lightgbm) and inference (using intel's d4p engine) on breast cancer:

```bash
docker run -it --rm prefect-vs-dask:latest
```

## `docker-compose`: using dask - a scheduler and worker/s orchestration

```bash
docker compose up
```

Finally, we have to run `orchestrator.py` to use that cluster. We have to feed it with the scheduler address.

```bash
python orchestrator.py --scheduler-uri=tcp://localhost:8786
```

- Lastly, we also have dashboard in [http://localhost:8787/status](http://localhost:8787/status).

# Installation for developers

```bash
pipenv install --dev
pip install -e . --no-deps
```