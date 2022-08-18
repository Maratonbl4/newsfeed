# Solution of test task for project DATAPK

## start server via docker:

in shell type `make up`, container started in background and attached to logs

for stop and delete container type `make down`, image will not be removed

## start server in console:
install all requirements

in dir `web` type `python server.py`

in both cases server start on 8080 port 

## test
install `aiohttp` and `aiounittest`

in project root dir `python -m unittest`

## additions
to generate new news and comments run `web/utils/content_maker`
