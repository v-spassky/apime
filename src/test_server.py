from fastapi.testclient import TestClient
from .server import app

"""
This module defines tests for the API.
"""

ANIME_PICS_URLS = [
    'https://glowmagzine.com/wp-content/uploads/2022/04/Screenshot-2022-04-26-at-2.32.19-PM.png',
    'https://i.pinimg.com/736x/e1/6e/45/e16e4533befd9e59240ce9a62a43b617.jpg',
    'https://i.pinimg.com/736x/3f/2f/64/3f2f646ea0a36712ffd4db6f880088a5.jpg',
    'https://qph.cf2.quoracdn.net/main-qimg-603a70b456b433931e2fbd534710ca95-lq',
    'https://www.statuspik.com/wp-content/uploads/2020/12/Beautiful-anime-profile-pics.jpg',
    'https://thypix.com/wp-content/uploads/2021/10/anime-avatar-profile-picture-thypix-124-700x700.jpg',
    'https://thypix.com/wp-content/uploads/2021/10/grey-anime-profile-picture-thypix-40-700x700.jpg',
    'https://thypix.com/wp-content/uploads/2021/10/grey-anime-profile-picture-thypix-36-700x700.jpg',
    'https://i.pinimg.com/originals/22/69/47/226947af00dfe2a773f726d0ad0435e9.jpg',
    'https://exploringbits.com/wp-content/uploads/2021/11/anime-girl-pfp-2.jpg?ezimgfmt=rs:352x380/rscb3/ng:webp/ngcb3',
]

RANDOM_PICS_URLS = [
    'https://miro.medium.com/max/1200/1*IC7_pdLtDMqwoqLkTib4JQ.jpeg',
    'https://urbanmatter.com/chicago/wp-content/uploads/2015/04/Chicago-Architecture.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZLQ9aUPQx3hl9nxSnOgL14LXt6GQu30Tm4w&usqp=CAU',
    'https://e3.365dm.com/21/07/1600x900/skynews-boeing-737-plane_5435020.jpg?20210702173340',
    'https://cars.usnews.com/pics/size/390x290/images/Auto/izmo/i159614825/2022_honda_accord_sedan_angularfront.jpg',
    'https://cdn.psychologytoday.com/sites/default/files/styles/article-inline-half-caption/public/field_blog_entry_images/2018-09/shutterstock_648907024.jpg?itok=0hb44OrI',
    'https://api.time.com/wp-content/uploads/2019/12/time-person-of-the-year-joe-biden-portrait.jpg?w=700&w=700',
    'https://image.shutterstock.com/image-photo/portrait-beautiful-mature-blonde-bearded-260nw-721917490.jpg',
    'https://img.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg?w=2000',
    'https://www.westend61.de/images/0001534567pw/handsome-young-man-smiling-on-sunny-day-UUF23064.jpg',
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
