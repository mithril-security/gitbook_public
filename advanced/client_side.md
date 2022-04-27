# Build the BlindAI Client SDK from source

## Build the client SDK from source&#x20;

In order to build the package from the source, the following requirements must be satisfied  on your **Linux** machine:

* CMake >= 3.12
* Make >= 4.0
* g++ >= 7.1
* python >= 3.6.8
* python3-dev package (or python-devel in CentOs based distros) - The version of python3-dev depends on the version of python you are using.

Once the requirements are satisfied, proceed as follows:

1. Clone the repository

```bash
$ git clone https://github.com/mithril-security/blindai
$ cd blindai/client
```

1. Install third party libraries

```bash
$ git submodule init
$ git submodule update
```

1. Create and activate a python virtual environment

```bash
$ python3 -m venv env
$ source env/bin/activate
```

* Check pip version (pip 21 is needed)

```bash
$ pip --version
```

* If the installed version is pip 9.x.x , upgrade pip

```bash
$ pip install -U pip
```

1. Install development dependencies

```bash
$ pip install -r requirements.txt
```

1. Trigger the build and installation

```bash
pip install . --use-feature=in-tree-build
```
