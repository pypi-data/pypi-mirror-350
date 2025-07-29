# Authentication

We provide an `AuthenticatedAlgorithmServer` which is a drop-in replacement for `AlgorithmServer`. It extends the functionality of the base class by implementing a simple user model and token-based authentication for a server, based on [fastapi-users](https://github.com/fastapi-users/fastapi-users). Only authenticated users can access the `/process` route.

```python
from imaging_server_kit import AuthenticatedAlgorithmServer
```

```{note}
This feature is still experimental.
```