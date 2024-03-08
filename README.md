# Capillary-Utils


## Build
```
docker build . --tag capillary-web:latest
```

## Run
```
docker run --rm -v $(pwd)/app:/app -p 8501:8501 capillary-web:latest
```
