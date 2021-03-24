# Love Geomertry

Application to parse Love Stories.

Love story is a set of sentences separated by a dot '.' 

Love story consists of love cases. Each love case 
represents relationship between two objects.
example: `A loves B`. Relationship also can be 
represented as a double-ended relationship with
`mutually` keywoard.

## Example

### input:

A loves B but B hates A.

A hates B, A loves D while B loves C and D hates A.

A mutually hates B.

### output:
```
[
  {
    'A': { 'loves': ['B'] },
    'B': { 'hates': ['A'] }
  },
  {
    'A': { 'hates': ['B'], 'loves': ['D'] },
    'B': { 'loves': ['C'] },
    'D': { 'hates': 'A' }
  },
  {
    'A': { 'hates': ['B'] },
    'B': { 'hates': ['A'] }
  }
]
```

## Data flow

After "love story" was received it's got processed with several components:
1. Parser:

during parsing some cases got validated:
- duplicated love case ("A loves B, A loves B.")
- more than one feeling to the same object ("A loves B, A hates B.")

2. Serializer:

during serialization some cases got validated:

- duplicated sentences ("A loves B. A loves B.")


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

- Navigate to the directory which contains package file:

`love-geometry-danil-buiko-v1-1.tar.gz`

- Create virtual environment to setup application:

`python -m venv env`

And activate it:

Windows:
  `env\Scripts\activate`

Linux:
  `source env/bin/activate`
  
- Unpack `.tar.gz` archive.

- Navigate to the package directory

- Run installation script: `python setup.py install`

- Run `tox` to execute tests

- Navigate to `love_geometry` directory and set environment variable

Windows:

 `set FLASK_APP=server`

Linux:

 `export FLASK_APP=server`

- Run application with `flask run` command.

- Application will start on port `5000`.

- To send requests to the application it's possible to use `httpie` utility:

`echo '{"love_story": "A loves B, A hates B and B loves A."}' | http POST http://127.0.0.1:5000/parse-love-story`

payload: 
`{"love_story": "A loves B, A loves C and B loves A."}`

- Check `love_geometry.ipynb` for simple playground.


