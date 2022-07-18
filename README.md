## Motivation

Once stumbled upon [this tweet](https://twitter.com/litavrinm/status/1527020571141320705) I decided to create a simple API that tells whether given image is anime or not.

<img src="files_for_readme/the_tweet.jpg" width="600">

## Tech stack

- Keras with all the underlying dependencies (Tensorflow, Scipy, PIL);
- FastAPI with Uvicorn web server.

## Usage guide

Send a POST request to `/is_it_anime` with the `pfp-url` header containing link to the image of interest. 

Possible responses:

- `200 { "conclusion": "Yes" }`
- `200 { "conclusion": "No" }`
- `400 { "details": "Error message..." }`
- `500 { "details": "Error message..." }`

## Demonstration

Trying out the API with [this image](https://pbs.twimg.com/media/D_jHn2fW4AAQlsz.jpg):

<img src="files_for_readme/demo_1.gif">

... and with an image from ['This person does not exist'](https://this-person-does-not-exist.com/en):

<img src="files_for_readme/demo_2.gif">

## Project file structure

Since pretty big part of the project files is gitingored here is a full presentation of it for context.

```
isanime
│
├─ __init__.py
├─ .gitignore
├─ config.ini
├─ LICENSE
├─ pyvenv.cfg
├─ README.md
├─ requirements.txt
├─ __pycache__
│ ├── ...
│ ├── ...
│ └── ...
├─ .pytest_cache
│ ├── ...
│ ├── ...
│ └── ...
├─ bin                # Python interpreter stuff
│ ├── ...
│ ├── ...
│ └── ...
├─ data               # Images for training and validation the model  
│ ├── train
│ │  ├── anime
│ │  │  ├── ...
│ │  │  ├── ...
│ │  │  └── ...
│ │  └── not_anime
│ │     ├── ...
│ │     ├── ...
│ │     └── ...
│ └── validation
│ │  ├── anime
│ │  │  ├── ...
│ │  │  ├── ...
│ │  │  └── ...
│ │  └── not_anime
│ │     ├── ...
│ │     ├── ...
│ │     └── ...
├─ files_for_readme
│ └── the_tweet.jpg
├─ lib                # Python interpreter stuff
│ ├── ...
│ ├── ...
│ └── ...
├─ models             # Stores generated .h5 models
│ ├── ...
│ ├── ...
│ └── ...
└─ src
  ├── __pycache__
  │     ├── ...
  │     ├── ...
  │     └── ...
  ├── .pytest_cache
  │     ├── ...
  │     ├── ...
  │     └── ...
  ├── __init__.py
  ├── server.py
  ├── test_server.py
  └── utils.py
```

## Development notes

 - Run server: 

`.../isanime$ uvicorn src.server:app`

- Generate Keras model: 

`.../isanime$ python src/utils.py generate-model <output_file_name>`

- Download random inages: 

`.../isanime$ python src/utils.py download-random-images <how_much> <target_folder>`

- Run tests:

`.../isanime$ pytest --ignore=bin --ignore=lib`

- Send request from commnad line:

```
curl -XPOST -H \
'pfp-url: <url>' \
'http://localhost:8000/is_it_anime'
```
