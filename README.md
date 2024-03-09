# Capillary-Utils


## Build
```
docker build . --tag capillary-web:latest
```

## Run Server
```
docker run --rm -v $(pwd)/app:/app -p 8501:8501 capillary-web:latest ./start_server.sh
```

## Run cli
```
docker run --rm -v $(pwd)/app:/app -p 8501:8501 capillary-web:latest python capillary_cli.py -h
```
