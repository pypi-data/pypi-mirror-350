![PegParser Logo](https://mauricelambert.github.io/info/python/code/PegParser_small.png "PegParser logo")

# PegParser

## Description

This package implements a PEG (Parsing Expression Grammar) to parse
syntax, i add rules to parse URL, HTTP request and response easily
with security and some format like hexadecimal, base32, base64,
base85, CSV, JSON (strict and permissive), system file path...

> This module implements standard functions for a PEG Parser, *standard match* (like digit, hexadecimal, letter, upper case letter, lower case letter, ...), *standard rules* (like integer, float, string, ...), *standard formats* (like hexadecimal data, base64 data, ...), *network* formats (like IPv4, IPv6, hostname, ...), a full URL parser, a full HTTP parser (request and response), a full CSV parser, a full JSON parser (strict and permissive) and system file path (Windows (DOS and NT path) and Linux path).

## Requirements

This package require:

 - python3
 - python3 Standard Library

## Installation

### Pip

```bash
python3 -m pip install PegParser
```

### Git

```bash
git clone "https://github.com/mauricelambert/PegParser.git"
cd "PegParser"
python3 -m pip install .
```

### Wget

```bash
wget https://github.com/mauricelambert/PegParser/archive/refs/heads/main.zip
unzip main.zip
cd PegParser-main
python3 -m pip install .
```

### cURL

```bash
curl -O https://github.com/mauricelambert/PegParser/archive/refs/heads/main.zip
unzip main.zip
cd PegParser-main
python3 -m pip install .
```

## Usages

```python
from PegParser import *

# Build bytes for a full HTTP response, useful to make a HTTP server response
http_response = bytes(HttpResponse(b'HTTP', 1.0, 200, 'OK', [], b'body content'))
http_response = bytes(HttpResponse(b'HTTP', 1.1, 201, 'Created', [('Content-Length', '12'), ('Content-Type', 'application/json'), ('Server', 'TestServer')], b'', 10, 'plain/text'))

# Parse the HTTP response, useful to parse the server response from a HTTP client
response = parse_http_response(http_response)
response.code
response.body

# Build bytes for a full HTTP request, useful to make a HTTP client request
http_request = bytes(HttpRequest('GET', '/', b'HTTP', 1.0, [], b'body content'))
http_request = bytes(HttpRequest('POST', '/upload', b'HTTP', 1.1, [('Content-Length', '12'), ('Content-Type', 'application/json'), ('User-Agent', 'TestClient')], b'', 10, 'plain/text'))

# Parse the HTTP request, useful to parse the client request from a HTTP server
request = parse_http_request(http_request)
response.verb
response.uri

# Parse a full URL
url_parsed = get_matchs(StandardRules.Url.full(b"https://my.full.url/with/path;and=parameters?query=too#fragment")[1])
url_parsed['host']
url_parsed['path']
url_parsed['scheme']

# Parse base64
base64_parsed = get_matchs(StandardRules.Format.base64(b"09AZaz+/"))

# Write your own rule
def digits(data, position):
    return PegParser.one_or_more(
        StandardMatch.is_digit,
        data,
        position,
    )

position, data = digits(b'01234', 0)          # match: 01234
position, data = digits(b'\x0001234toto', 0)  # no match
position, data = digits(b'\x0001234toto', 1)  # match: 01234

with open('data.csv', 'rb') as file:
    for line in csv_file_parse(file):
        field1 = line[0]
        field2 = line[1]
        ...

data = get_json(b'{"1": null, "2" : 1.5 , "3": {"test": true, "1": 2}, "4": [1, 2, false]}')
data = get_json(b'{"1" null, "2" : 1.5 , "3": {"test" true "1" 2},"4" :[1 2, false],}', permissive=True)

with open('data.mjson', 'rb') as file:
    for data in mjson_file_parse(file):
        print(data)

match(StandardRules.Path.path, b'\\\\?\\test\\1\\2\\test.txt**', 7) # b'\\\\?\\test\\1\\2\\test.txt'
```

## Links

 - [Pypi](https://pypi.org/project/PegParser)
 - [Github](https://github.com/mauricelambert/PegParser)
 - [Documentation](https://mauricelambert.github.io/info/python/code/PegParser.html)

## License

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
