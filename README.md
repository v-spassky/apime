> **Note**
>
> This project is still in process...

## Motivation

Once stumbled upon [this tweet](https://twitter.com/litavrinm/status/1527020571141320705) I decided to create a simple API that evaluetes whether given image is anime.

<img src="files_for_readme/the_tweet.jpg" width="600">

## Tech stack

- Keras with all the underlying dependencies (Tensorflow, Scipy, PIL);
- FastAPI with Uvicorn web server inside a Docker container.

## Demonstration

...

## Usage guide

...

## Project file structure

Since pretty big part of the project files is gitingored here is a full presentation of it for context.

```
isanime
│
├─ .gitignore
├─ LICENSE
├─ pyvenv.cfg
├─ README.md
├─ requirements.txt
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
├─ models             # Stores generated models
│ ├── ...
│ ├── ...
│ └── ...
└─ src
├── server.py
└── utils.py
```

## Development notes

Run server:

    .../isanime$ uvicorn src.server:app

Generate Keras model:

    .../isanime$  python src/utils.py generate-model <output_file_name>

Download random inages:

    .../isanime$  python src/utils.py download-random-images <how_much> <target_folder>