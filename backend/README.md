# Tick Track

[DOCUMENTATION OUTDATED]

## Usage

### Runing the server

#### Apply database's migrations

```make
make migrate
```

#### Run produtction app
```make
make run-prod
```

#### Run development app
```make
make run-dev
```

#### Run tests
```make
make run-test
```

### API

- All endpoints return `duration` of activities in seconds.

#### All activities

```py
import requests


response = requests.get('http://0.0.0.0:8000/activities/all')
response.json()
```

**returns**
```py
[
    {
        'detailed_description': 'API Documentation — peewee 3.13.3 documentation ',
        'duration': 2.078565,
        'main_description': ' Google Chrome',
        'more_details': None,
        'name': 'API Documentation — peewee 3.13.3 documentation - Google Chrome'
    },
]
```

#### Today's activities

```py
import requests


response = requests.get('http://0.0.0.0:8000/activities/today')
response.json()
```

**returns**
```py
[
    {
        'detailed_description': 'API Documentation — peewee 3.13.3 documentation ',
        'duration': 2.078565,
        'main_description': ' Google Chrome',
        'more_details': None,
        'name': 'API Documentation — peewee 3.13.3 documentation - Google Chrome'
    },
]
```

#### Date range activities

```py
import requests


body = {'start_date': '2020-04-15', 'end_date': '2020-04-30'}
response_post = requests.post('http://0.0.0.0:8000/activities/date.range', body)
response.json()
```

**returns**
```py
[
    {
        'detailed_description': 'API Documentation — peewee 3.13.3 documentation ',
        'duration': 2.078565,
        'main_description': ' Google Chrome',
        'more_details': None,
        'name': 'API Documentation — peewee 3.13.3 documentation - Google Chrome'
    },
]
```

#### Activities in a date range

```py
import requests


body = {'start_date': '2020-04-15', 'end_date': '2020-04-30'}
response_post = requests.post('http://0.0.0.0:8000/activities/date.range', body)
response.json()
```

**returns**
```py
[
    {
        'detailed_description': 'API Documentation — peewee 3.13.3 documentation ',
        'duration': 2.078565,
        'main_description': ' Google Chrome',
        'more_details': None,
        'name': 'API Documentation — peewee 3.13.3 documentation - Google Chrome'
    },
]
```

#### Full text search

```py
import requests


body = {
    'text': 'Notebook', 'start_date': '2020-04-15', 'end_date': '2020-04-30'}
response_search = requests.post('http://0.0.0.0:8000/activities/search', body)
response_search.json()
```
*note: start_date and end_date params are optional*

**returns**
```py
[
    {
        'name': 'user@localhost: ~/Documentos/repos/notebooks',
        'duration': 20.454825,
        'main_description': 'user@localhost: ~/Documentos/repos/notebooks',
        'detailed_description': None,
        'more_details': None
    }
]
```
## Notes
- User idle implemented only for Linux users