![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# serverkit-orientationpy

Implementation of a web server for [Orientationpy](https://gitlab.com/epfl-center-for-imaging/orientationpy).

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

## Sample images provenance

- `image1_from_OrientationJ.tif`: Example image from [OrientationJ](https://bigwww.epfl.ch/demo/orientationj/).
