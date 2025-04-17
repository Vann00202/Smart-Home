#!/usr/bin/env python3

import sys

# Local Modules
from asyncserver import asyncserver
from webserver import webserver


if __name__ == "__main__":

    # asyncserver.start_server()
    webserver.app.run(host='0.0.0.0', port=3000)

    sys.exit(0)
