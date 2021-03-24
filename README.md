# Love Geomertry

## Theory 

### Description
Application to parse Love Stories.

Love story is a set of sentences separated by a dot '.' 

Love story consists of love cases. Each love case 
represents relationship between two objects.
example: `A loves B`. Relationship also can be 
represented as a double-ended relationship with
`mutually` keywoard.

### Example

**Input:**

A loves B but B hates A.

A hates B, A loves D while B loves C and D hates A.

A mutually hates B.

**Output:**

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

1. Parser. During parsing some cases got validated:
	- duplicated love case ("A loves B, A loves B.")
	- more than one feeling to the same object ("A loves B, A hates B.")

1. Serializer. During serialization some cases got validated:
	- duplicated sentences ("A loves B. A loves B.")


## Requirements

**Python 3.9**

## Installation

Make sure you're running python3.9

1. Checkout from repository
1. Create virtual environment to setup application:
	`python -m venv env`

	And activate it.
   
   	Windows: `env\Scripts\activate`
   
	Linux: `source env/bin/activate`
1. Setup dependencies by running `pip install -r requirements.txt` 

## Initialization

1. Run application by executing `python -m love_geometry`

## Usage

To use package you may want to execute `POST` request against `/parse-love-story` 
endpoint with JSON payload:

```
{
   "love_story":"A loves B, A hates B and B loves A."
}
```

You may use `httpie` package to do this by executing:

**Good example:**

```
http POST http://localhost:5000/parse-love-story love_story="A loves B, A hates C. A loves M while M loves C."
```

Expected output is:

```
[
   {
      "data":{
         "A":{
            "hates":[
               "C"
            ],
            "loves":[
               "B"
            ]
         }
      },
      "errors":[]
   },
   {
      "data":{
         "A":{
            "loves":[
               "M"
            ]
         },
         "M":{
            "loves":[
               "C"
            ]
         }
      },
      "errors":[]
   }
]
```

**Bad example with DISABLED validation:**

```
http POST http://localhost:5000/parse-love-story love_story="A loves B, A loves B."
```

Expected output is:

```
[
   {
      "data":{
         "A":{
            "loves":[
               "B",
               "B"
            ]
         }
      },
      "errors":[]
   }
]
```

**Bad example with ENABLED validation:**

```
http POST http://localhost:5000/parse-love-story love_story="A loves B, A loves B."
```

Expected output is:

```
[
   {
      "data":{
         "A":{
            "loves":[
               "B",
               "B"
            ]
         }
      },
      "errors":[
         "Duplicated love case: `A loves B`"
      ]
   }
]
```

## Testing 

1. Run `tox` to execute tests


