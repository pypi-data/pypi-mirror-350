

# Easy HTTP Server 

This is a simple HTTP server for Raspberry Pi or PC that can:

* display custom HTML files
* respond to custom POST requests
* has a `webserverautofile` switch for easy usage

## Usage

```python
from easy_http_server import EasyHTTPServer

server = EasyHTTPServer(port=8000, webserverautofile=True)
server.start()
```
