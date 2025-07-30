<h1 align="center">Quick JWT</h1>
<p align="center">
    <em>Quick JWT library for authorization in FastAPI applications</em>
</p>

<p align="center">
<img alt="Run Tests" src="https://github.com/maxim-f1/quick_jwt/actions/workflows/tests.yml/badge.svg">

<img alt="Coverage" src="https://github.com/maxim-f1/quick_jwt/blob/master/coverage.svg?raw=true">

<a href="https://pypi.org/project/quick-jwt" target="_blank">
    <img src="https://img.shields.io/pypi/v/quick-jwt?color=%234c1&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/quick-jwt" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/quick-jwt.svg?color=%234c1" alt="Supported Python versions">
</a>
</p>

---

**Source Code**: <a href="https://github.com/maxim-f1/quick_jwt" target="_blank">https://github.com/maxim-f1/quick_jwt</a>

**Documentation** <a href="https://maxim-f1.github.io/quick_jwt/" target="_blank">https://maxim-f1.github.io/quick_jwt/</a>

---

Quick JWT is a lightweight and convenient solution for handling JWT token-based authorization.

The key features are:
* Full integration with FastAPI framework and Intuitive use of FastAPI style features.
* Easy customization of environment variables via Pydantic-Settings and Middleware.
* Convenient functions for wrapping Depends with data type persistence.
* Many Depends functions for a large number of tasks.
* Ability to customize standard PyJWT driver to custom solutions.
* Support for function arguments for PyJWT driver, as well as Pydantic validation functions.

## Requirements

Quick JWT stands on the shoulders of giants:

* <a href="https://fastapi.tiangolo.com/" class="external-link" target="_blank">FastAPI</a> - main web framework.
* <a href="https://pyjwt.readthedocs.io/" class="external-link" target="_blank">PyJWT</a> - default JWT driver.
* <a href="https://docs.pydantic.dev/latest/concepts/pydantic_settings/" class="external-link" target="_blank">Pydantic Settings</a> - extension for pydantic with .env variables.

## Installation

Create and activate a virtual environment and then install Quick JWT:

<div class="termy">

```console
$ pip install quick-jwt
```

</div>

## Example

### Create it

Create a file `main.py` with:

```Python
from fastapi import FastAPI
from pydantic import BaseModel
from quick_jwt import (
    QuickJWTConfig,
    QuickJWTMiddleware,
    create_jwt_depends,
)

key = "default_key"
quick_jwt_config = QuickJWTConfig(encode_key=key, decode_key=key)

app = FastAPI()
app.add_middleware(QuickJWTMiddleware, quick_jwt_config)


class UserScheme(BaseModel):
    sub: str


@app.get("/create-tokens")
async def create_tokens(
    sub: str, 
    jwt: create_jwt_depends(UserScheme, UserScheme)
):
    user = UserScheme(sub=sub)
    tokens = await jwt.create_jwt_tokens(user, user)
    return tokens

```


### Run it

Run the server with:

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

### Check it

Open your browser at <a href="http://127.0.0.1:8000/create-tokens?sub=some_id" class="external-link" target="_blank">http://127.0.0.1:8000/create-tokens?sub=some_id</a>.

You will see the JSON response as:

```JSON
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb21lX2lkIn0.EerZU4uZCRh7yXxOqsZKTwzls7BnL-6C8jidTTkit6k",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb21lX2lkIn0.EerZU4uZCRh7yXxOqsZKTwzls7BnL-6C8jidTTkit6k"
}
```

### Interactive API docs upgrade

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

## License

This project is licensed under the terms of the MIT license.
