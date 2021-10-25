"""
Use the ACMI Public API to match internet biographies to ACMI collection Works.
"""

import random
import requests

# Search for ACMI creators with 'Simon' in their name
ACMI_SEARCH_QUERY = 'Simon'.lower()
creators = set()

if ACMI_SEARCH_QUERY:
    search_response = requests.get(
        'https://api.acmi.net.au/search/',
        params={
            'query': ACMI_SEARCH_QUERY,
            'field': 'creators_primary.name',
        },
    ).json()

    for result in search_response['results']:
        for creator in result.get('creators_primary'):
            if ACMI_SEARCH_QUERY in creator.get('name').lower():
                creators.add(creator.get('name'))

    print(
        f'Found {len(creators)} ACMI creators with {ACMI_SEARCH_QUERY} '
        f'in their name: {creators}'
    )
else:
    # Let's search for all directors instead
    search_response = requests.get(
        'https://api.acmi.net.au/search/',
        params={
            'query': 'director',
            'field': 'creators_primary.role',
        },
    ).json()

    for result in search_response['results']:
        for creator in result.get('creators_primary'):
            if 'director' in creator.get('role').lower():
                creators.add(creator.get('name'))

    print(f'Found {len(creators)} ACMI creators who are directors: {creators}')

if len(creators) > 10:
    # Let's be nice and limit our search to 10 ACMI creators
    creators = random.sample(creators, 10)

# Search Wikipedia for information on each person
for creator in creators:
    wikipedia_search_response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': creator,
            'prop': 'info|extracts',
            'exintro': True,
            'explaintext': True,
            'inprop': 'url',
        },
    ).json()
    try:
        wikipedia_page = next(
            iter(wikipedia_search_response['query']['pages'].values()),
        )
        print(
            f'Wikipedia data for {creator}: {wikipedia_page["fullurl"]}\n'
            f'Title: {wikipedia_page["title"]}\n'
            f'Extract: {wikipedia_page["extract"]}'
        )
    except KeyError:
        print(f'Sorry, no data from Wikipedia for: {creator}')
    print('')
