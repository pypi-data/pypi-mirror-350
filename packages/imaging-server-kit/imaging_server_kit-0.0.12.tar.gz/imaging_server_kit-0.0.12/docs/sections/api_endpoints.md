# API Endpoints

When the server is running, an OpenAPI documentation of the endpoints is automatically generated on the `/docs` route (e.g. http://localhost:8000/docs).

The algorithm servers implement a REST API with a common set of endpoints for processing and retreiving data. The main endpoints are listed in the table below.

| Type | Endpoint                     | Description                                 |
| ---- | ---------------------------- | ------------------------------------------- |
| GET  | `/`                          | Algorithm index or info page                |
| GET  | `/services`                  | List available algorithms                   |
| GET  | `/<algorithm>/info`          | Algorithm info page                         |
| POST | `/<algorithm>/process`       | Run the algorithm                           |
| GET  | `/<algorithm>/parameters`    | Get algorithm parameters                    |
| GET  | `/<algorithm>/sample_images` | Get samples images                          |
