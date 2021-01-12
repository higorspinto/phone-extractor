# phone-extractor

The application visits a given input website and outputs the website’s logo, and
any found phone numbers. 

## How to run

This software can be run in two different environments: a Python virtual environment or a docker container.

### Python

First, install the dependencies:

```
pip install -r requirements.txt
```

Then you can execute:

```
cat websites.txt | python -m scraper
```

### Docker Container

First, build the environment into the folder of the Dockerfile.

```
docker build -t phone-extractor .
```

Then you can start the container:

```
cat websites.txt | docker run -i phone-extractor
```
