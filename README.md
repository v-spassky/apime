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

## Project file structure

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
│ │  └── anime
│ │     ├── ...
│ │     ├── ...
│ │     └── ...
│ └── validation
│    └── anime
│       ├── ...
│       ├── ...
│       └── ...
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
  ├── generate_model.py
  └── server.py
```

## Development notes

...