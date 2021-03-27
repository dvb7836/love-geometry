# Love Geomertry

## Theory 

### Description
API to parse Love Stories.

Love story is a set of sentences separated by a dot '.' 

*example:
(A loves D while B loves C and D hates A. M hates N.)*

Love story consists of love cases. Each love case 
represents relationship between two objects.
example: `A loves B`. Relationship also can be 
represented as a double-ended relationship with
`mutually` keywoard.

API has two endpoints:

- `/parse-love-story` - used to parse love story into a list of sentences;

- `/find-circles-of-affection` - used to build a graph representing 
  relationships from a text story and find elementary cycles in it;
  
  - can find cheaters (if validation enabled):
		
	* Someone considered as a cheater in case if has more than one 
	feeling to the same person.
	
	* In case if cheater is found it's got removed from the circle of affection candidates and 
	circle search happens without a cheater.
	  
  - can show visual representation of built graph (if enabled in config)

### Example

**Input:**

A loves B but B hates A.

A hates B, A loves D while B loves C and D hates A.

A mutually hates B.

**Output from `/parse-love-story` endpoint:**

```buildoutcfg
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

**Output from `/find-circles-of-affection`**
```buildoutcfg
{
   "circles_of_affection":[
      {},
      {},
      {
         "hates":[
            [
               "A",
               "B"
            ],
            [
               "B",
               "A"
            ]
         ]
      }
   ],
   "cheaters":[]
}
```
## Data flow

After "love story" was received it's got processed with several components:

1. Parser. Parses provided love story sting and outputs parsed data.

1. Validator. Validates parsed love story by converting it to XML.

1. Serializer. Serializes parsed love story to JSON.


## Requirements

**Python >= 3.6**

## Installation

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


