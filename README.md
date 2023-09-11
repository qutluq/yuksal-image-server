This media server was created to handle requests from nextjs13, which at the time being can not serve dynamically uploaded images.

## Getting Started

First, run the development server:

Python version I was using: 3.10.12

```bash
python3 -m pip install -r requirements.txt
```

Create folder `media` within root folder. All the media files will be served from `media` directory.

run the server:

```bash
python3 manage.py runserver
```

There are no pages to display on [http://localhost:8000](http://localhost:8000), only REST API endpoints can be served, for details refer to docstrings.
