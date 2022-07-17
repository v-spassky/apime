from fastapi.testclient import TestClient
from .server import app

"""
This module defines tests for the API.
"""

ANIME_PICS_URLS = [
    'https://i.pinimg.com/originals/10/9b/5e/109b5e84fd01c7dc621ce1011b2a96d9.jpg',
    'https://static.wikia.nocookie.net/evangelion/images/0/0d/OP_C016_rei.jpg/revision/latest/top-crop/width/360/height/360?cb=20171121184144&path-prefix=ru',
    'https://i.pinimg.com/originals/ae/e2/b4/aee2b41aa6c18317cfab9af184bc2d2e.jpg',
    'https://64.media.tumblr.com/24a099f06104b248ead01ae15e281375/tumblr_pn36dohkBZ1vm1a59o1_640.jpg',
    'https://i.pinimg.com/originals/9e/b9/4b/9eb94bf1b0aae8c5a6ddf32d092a64e1.jpg',
    'https://i.pinimg.com/236x/2c/67/80/2c678002e587299b3511cec86382daf1.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTH1Tho9kwiFmUsAzz5mUSE3EOdyx-n1UpbPDnNetLdCiAjteTchS-75nD7fcq4l2V3ciU&usqp=CAU',
    'https://i.pinimg.com/1200x/31/39/f8/3139f84211ab1498537fda031eb76d10.jpg',
    'https://b-static.besthdwallpaper.com/my-dress-up-darling-anime-marin-kitagawa-4k-sfondo-3554x1999-89573_53.jpg',
    'https://i.pinimg.com/474x/56/44/6d/56446d6df6331068c2c02d114f99b672.jpg',
]

RANDOM_PICS_URLS = [
    'https://i.pinimg.com/736x/6b/f0/7a/6bf07a463c434f56e8a1bb860924863d--christian-bale-celebrity-portraits.jpg',
    'https://play-lh.googleusercontent.com/q1A3iAYUJI6wxOWI7iLvmjAx9rb53QiKUqB1wIfiPzkihWbYgqs_uuDrls45ayKqsUg',
    'https://media.wired.com/photos/62b25f4c18e6fafaa97a6477/master/pass/Air-Serbia-Plane-Russian-Sanctions-Safety-Hazard-Business-1239498184.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Alexei_Navalny_marching_in_2017_%28cropped_2%29.jpg/250px-Alexei_Navalny_marching_in_2017_%28cropped_2%29.jpg',
    'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/golden-retriever-royalty-free-image-506756303-1560962726.jpg?crop=0.672xw:1.00xh;0.166xw,0&resize=640:*',
    'http://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_64/f_auto,q_auto,w_1100/v1565279671/shape/mentalfloss/578211-gettyimages-542930526.jpg',
    'https://efi.int/sites/default/files/2020-12/placeholder.jpeg',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/City_of_London_skyline_from_London_City_Hall_-_Sept_2015_-_Crop_Aligned.jpg/1200px-City_of_London_skyline_from_London_City_Hall_-_Sept_2015_-_Crop_Aligned.jpg',
    'https://img.freepik.com/free-photo/young-and-beautiful-woman-in-pink-warm-sweater-natural-look-smiling-portrait-on-isolated-long-hair_285396-896.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/President_Barack_Obama_%28cropped%29.jpg/1200px-President_Barack_Obama_%28cropped%29.jpg',
]

FAULTY_URLS = [
    'https://example.com/',
    'https://www.google.com/',
    'https://www.nature.com/',
    'https://singularityhub.com/',
    'https://www.wikipedia.org/',
    'https://www.mit.edu/',
    'https://www.python.org/',
    'https://htmx.org/',
    'https://www.chess.com/',
    'https://github.com/torvalds',
]


client = TestClient(app)


def test_is_it_anime():
    """
    Runs tests for the /is_it_anime route 
    accordingly to the supposed usage thereof.

    Supposed usage: .../isanime$ pytest --ignore=bin --ignore=lib
    """

    for url in ANIME_PICS_URLS:
        print(f'Checking {url}')
        response = client.post('/is_it_anime', headers={'pfp-url': f'{url}'})
        assert response.json() == {"conclusion": "Yes"}

    for url in RANDOM_PICS_URLS:
        print(f'Checking {url}')
        response = client.post('/is_it_anime', headers={'pfp-url': f'{url}'})
        assert response.json() == {"conclusion": "No"}

    for url in FAULTY_URLS:
        print(f'Checking {url}')
        response = client.post('/is_it_anime', headers={'pfp-url': f'{url}'})
        assert "detail" in response.json()
