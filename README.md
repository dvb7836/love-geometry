# Love Geomertry

Application to parse Love Stories

## Requirements

- **Python** 3.9.
- Several Python packages:
	- **pyPEG2**.
	- **flask**.
	- **marshmallow**.
	- **networkx**.
	- **matplotlib**.

## Usage

Make sure you're running python3.9

1 . Navigate to the directory which contains package file:

`love-geometry-danil-buiko-v1-1.tar.gz`

2. Create virtual environment to setup application:

`python -m venv env`

And activate it:
* Windows:
  `env\Scripts\activate`
* Linux:
  `source env/bin/activate`
  
3. Unpack `.tar.gz` archive.

4. Navigate to the package directory

5. Run installation script: `python setup.py install`

5. Run `tox` to execute tests

6. Navigate to `love_geometry` directory and set environment variable

- Windows:
	- `set FLASK_APP=server`
- Linux:
	- `export FLASK_APP=server`

7. Run application with `flask run` command.

8. Check `love_geometry.ipynb` for simple playground.
