## Motivation

Once stumbled upon [this tweet](https://twitter.com/litavrinm/status/1527020571141320705) I decided to create a simple API that tells whether given image is anime or not.

<img src="files_for_readme/the_tweet.jpg" width="600" style="max-width: 100%;">

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

<img src="files_for_readme/demo_1.gif" style="max-width: 100%;">

... and with an image from ['This person does not exist'](https://this-person-does-not-exist.com/en):

<img src="files_for_readme/demo_2.gif" style="max-width: 100%;">

## Project file structure

Since pretty big part of the project files is gitingored here is a full presentation of it for context.

```
apime
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
│ │  └── random
│ │     ├── ...
│ │     ├── ...
│ │     └── ...
│ └── validation
│ │  ├── anime
│ │  │  ├── ...
│ │  │  ├── ...
│ │  │  └── ...
│ │  └── random
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

`.../apime$ uvicorn src.server:app --port 5000 --reload --reload-exclude bin/* --reload-exclude lib/* -reload-exclude *.html`

- Generate Keras model: 

`.../apime$ python src/utils.py generate-model <output_file_name>`

- Download random inages: 

`.../apime$ python src/utils.py download-random-images <how_much> <target_folder>`

- Feed the test images into the model and see results:

`python src/utils.py get-model-statistics`

- Run tests:

`.../apime$ pytest --ignore=bin --ignore=lib`

- Send request from commnad line:

```
curl -XPOST -H \
'pfp-url: <url>' \
'http://localhost:5000/is_it_anime'
```

## Deployment notes

SSH into an EC2 instance:

`ssh -i "<key_file>" <public_dns_name>`

Install Python, pip and python-venv:

`sudo apt update`

`sudo apt install software-properties-common`

`sudo add-apt-repository ppa:deadsnakes/ppa`

`sudo apt install python3.8`

`apt-get install python3.8-venv`

Clone git repo:

`git clone https://github.com/v-spassky/apime.git`

Cd into the project folder:

`cd apime/`

Create and enter virtual environment:

`python 3.8 -m venv .`

`source bin/activate`

Install dependencies:

`pip install -r requirements.txt`

Install Nginx:

`sudo apt install nginx`

Configure Nginx:

`sudo nano /etc/nginx/sites-enabled/apimeconf`

```
server {

    listen 443 ssl;

    ssl_certificate <path_to_cert_file>;

    ssl_certificate_key <path_to_private_key>;

    server_name <ec2_instance_public_dns_name> <ec2_instance_public_ip> apime.app;

    location / {

        proxy_pass_request_headers on;

        proxy_headers_hash_bucket_size 1024;

        proxy_headers_hash_max_size 4048;

        proxy_pass http://127.0.0.1:5000;

    }

}
```

Increase DNS name length:

`sudo nano /etc/nginx/nginx.conf`

Uncomment:

`server_names_hash_bucket_size 64;`

Restart Nginx:

`sudo service nginx restart`

Run server:

`nohup uvicorn src.server:app --host 127.0.0.1 --port 5000 &`

Find uvicorn process:

`ps -aux | grep uvicorn`

Kill a process:

`sudo kill -9 <pid>`
