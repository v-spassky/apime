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

Send a POST request to `/is_it_anime` with the `pfp-url` header containing link to the image of interest. 

Possible responses:

- `200 { 'Yes' }`
- `200 { 'No' }`
- `400 { details: 'Error message...' }`

## Project file structure

Since pretty big part of the project files is gitingored here is a full presentation of it for context.

```
isanime
│
├─ .gitignore
├─ config.ini
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
├─ models             # Stores generated .h5 models
│ ├── ...
│ ├── ...
│ └── ...
└─ src
  ├── __pycache__
  │     ├── ...
  │     ├── ...
  │     └── ...
  ├── __init__.py
  ├── server.py
  └── utils.py
```

## Development notes

Run server: 

`.../isanime$ uvicorn src.server:app`

Generate Keras model: 

`.../isanime$ python src/utils.py generate-model <output_file_name>`

Download random inages: 

`.../isanime$ python src/utils.py download-random-images <how_much> <target_folder>`

## Deployment backlog

SSH into the EC2 instance:

`ssh -i "<key_file>.pem" ubuntu@<dns_name>`

Update package information and install Pyton, pip and Nginx:

`ubuntu@<private-ip>:~$ sudo apt-get update && sudo apt install -y python3-pip nginx`

Configure Nginx like this:

`ubuntu@<private-ip>:~$ sudo nano /etc/nginx/sites-enabled/isanime_server`

```
server {
        listen 80;
        server_name <public-ip>;
        location / {
                proxy_pass http://127.0.0.1:8000;
        }
}
```

... and then resart Nginx:

`ubuntu@<private-ip>:~$ sudo service nginx restart`

Clone the repo from Github:

`ubuntu@<private-ip>:~$ git clone https://github.com/v-spassky/isanime.git`

Cd into the project folder:

`ubuntu@<private-ip>:~$ cd isanime/`

Install dependencies:

`ubuntu@<private-ip>:~/isanime$ pip install -r requirements.txt`

Run the application:

`ubuntu@<private-ip>:~/isanime$ uvicorn src.server:app`
