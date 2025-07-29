# fileshiftlib

* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [License](#license)

## Package Description

SFTP client Python package that uses [paramiko](https://pypi.org/project/paramiko/) library.

## Usage

* [fileshiftlib](#fileshiftlib)

from a script:

```python
import fileshiftlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

host = "localhost"
username = "123..."
password = "xxxx"
port = 22

# Initialize SFTP client
sftp = fileshiftlib.SFTP(host=host,
                         username=username,
                         password=password,
                         port=port)
```

## Installation

* [fileshiftlib](#fileshiftlib)

Install python and pip if you have not already.

Then run:

```bash
pip install pip --upgrade
```

For production:

```bash
pip install fileshiftlib
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:

```bash
git clone https://github.com/aghuttun/fileshiftlib.git
cd fileshiftlib
pip install -e ".[dev]"
```

To test the development package: [Testing](#testing)

## License

* [fileshiftlib](#fileshiftlib)

BSD License (see license file)
