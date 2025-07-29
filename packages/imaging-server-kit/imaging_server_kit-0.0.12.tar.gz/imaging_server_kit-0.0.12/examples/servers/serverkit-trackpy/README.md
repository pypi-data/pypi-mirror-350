![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# serverkit-trackpy

Implementation of a web server for [Trackpy](https://soft-matter.github.io/trackpy/) (linking only).

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
## Sample images provenance -->

- `tracks.tif`: Example image from the [Trackmate](https://imagej.net/plugins/trackmate/tutorials/getting-started) getting started guide.
