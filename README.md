# Phone Extractor

The application visits a given list of websites and outputs the website’s logo, and
any found phone numbers.

The Phone Extractor matches different phone formats and identifies phones that contains any separators, hyphen `-`, white space ` `, or dots `.` between the branch number and the phone number. It also identifies phones that contain the area code between parentheses `(AREA_CODE)`.

Examples:

```
(517) 788-0550 - Valid
517 788 0550 - Valid
5177880550 - Not valid
```

```
+1 (212) 465-9555 - Valid
+1 212 465 9555 - Valid
12124659555 - Not Valid
```

To scrape the website logos, the Phone Extractor looks for the string pattern `logo` (case insensitive) in all the images found on the page and returns a list containing all the matches found.

## How to run

This software can be run in two different environments: a Python virtual environment or a docker container.

### 1 - Python

First, install the package dependencies:

```
pip install -r requirements.txt
```

Then you can execute:

```
cat websites.txt | python -m scraper
```

This module was created with Python 3.8, and it wasn't tested with other Python versions.

### 2 - Docker Container

First, build the environment into the folder of the Dockerfile.

```
docker build -t phone-extractor .
```

Then you can start the container:

```
cat websites.txt | docker run -i phone-extractor
```

## Logs

The log level defined is `INFO`. The logs and the output are printed in the standard output. You can send the logs and the output to a file using:

```
cat websites.txt | python -m scraper 1> output.json 2>log.txt
```

or

```
cat websites.txt | docker run -i phone-extractor 1> output.json 2> log.txt
```

