![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# Scikit-image LoG detector API in docker

Implementation of a web API server for [Scikit Image's LoG detector](https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.blob_log).

## Installing the algorithm server with `pip`

Install dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
python main.py
```

The server will be running on http://localhost:8000.

## Using `docker-compose`

To build the docker image and run a container for the algorithm server in a single command, use:

```
docker compose up
```

The server will be running on http://localhost:8000.