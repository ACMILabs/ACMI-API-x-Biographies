"""
Use the ACMI Public API to match internet biographies to ACMI collection Works.
"""

from collections import OrderedDict
import requests

from wikidata.client import Client as WikidataClient

# Search for ACMI works made by a creator with 'Simon' in their name
ACMI_SEARCH_QUERY = 'Simon'.lower()
works = []
works_with_biographies = []

if ACMI_SEARCH_QUERY:
    search_response = requests.get(
        'https://api.acmi.net.au/search/',
        params={
            'query': ACMI_SEARCH_QUERY,
            'field': 'creators_primary.name',
        },
    ).json()

    works.extend(search_response['results'])

    print(
        f'Found {len(works)} ACMI works made by a creator with '
        f'{ACMI_SEARCH_QUERY} in their name: {[w["title"] for w in works]}'
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

    works.extend(search_response['results'])

    print(f'Found {len(works)} ACMI works featuring a director: {[w["title"] for w in works]}')


def add_biography(creator_data):
    """
    Get the biography for this creator and add the data to
    the field 'wikidata'. Return the creator.
    """
    match = False
    wikidata_search_response = requests.get(
        'https://www.wikidata.org/w/api.php',
        params={
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': creator_data['name'],
        },
    ).json()

    for result in wikidata_search_response['search']:
        for role in creator_data['roles']:
            try:
                if not match and role in result['description']:
                    match = True
                    creator_data['wikidata'] = result
                    print(
                        f'\n🥳 Matched ACMI {creator_data["name"]} ({creator_data["creator_id"]}) '
                        f'to WikiData: {result["label"]} ({result["id"]}) '
                        f'- {result["description"]}'
                    )
                    print(f'Wikidata: https:{result["url"]}')
                    wikidata_client = WikidataClient()
                    entity = wikidata_client.get(result['id'], load=True)
                    try:
                        creator_data['wikipedia_url'] = entity.data['sitelinks']['enwiki']['url']
                        print(f'Wikipedia: {creator_data["wikipedia_url"]}')
                        # Let's get the Wikipedia extract
                        wikipedia_search_response = requests.get(
                            'https://en.wikipedia.org/w/api.php',
                            params={
                                'action': 'query',
                                'format': 'json',
                                'titles': entity.data['sitelinks']['enwiki']['title'],
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
                            creator_data['wikipedia_extract'] = wikipedia_page["extract"]
                            print(
                                f'Wikipedia extract: {creator_data["wikipedia_extract"]}'
                            )
                        except KeyError:
                            pass
                    except KeyError:
                        pass
                    try:
                        creator_data['imdb_id'] = \
                            entity.data['claims']['P345'][0]['mainsnak']['datavalue']['value']
                        print(f'IMDB person: https://www.imdb.com/name/{creator_data["imdb_id"]}/')
                    except KeyError:
                        pass
                    try:
                        creator_data['tmdb_id'] = \
                            entity.data['claims']['P4985'][0]['mainsnak']['datavalue']['value']
                        print(
                            f'TMDB person: https://www.themoviedb.org/person/'
                            f'{creator_data["tmdb_id"]}'
                        )
                    except KeyError:
                        pass
                    try:
                        creator_data['image_url'] = entity[wikidata_client.get('P18')].image_url
                        print(f'Image: {creator_data["image_url"]}')
                    except KeyError:
                        pass
                    try:
                        creator_data['twitter'] = \
                            entity.data['claims']['P2002'][0]['mainsnak']['datavalue']['value']
                        print(f'Twitter: https://twitter.com/{creator_data["twitter"]}')
                    except KeyError:
                        pass
                    try:
                        creator_data['instagram'] = \
                            entity.data['claims']['P2003'][0]['mainsnak']['datavalue']['value']
                        print(f'Instagram: https://instagram.com/{creator_data["instagram"]}')
                    except KeyError:
                        pass
                    try:
                        creator_data['facebook'] = \
                            entity.data['claims']['P2013'][0]['mainsnak']['datavalue']['value']
                        print(f'Facebook: https://facebook.com/{creator_data["facebook"]}')
                    except KeyError:
                        pass
                else:
                    pass
            except KeyError:
                pass

    if not match:
        print(f'\n😭 Sorry, no Wikidata matches for: {creator_data["name"]}')

    return creator_data, match


for work in works:
    print(f'\nMatching biographies for ACMI collection item: {work["title"]} ({work["id"]})')
    print(f'ACMI API: https://api.acmi.net.au/works/{work["id"]}/')
    print(f'ACMI Website: https://www.acmi.net.au/works/{work["id"]}--{work["slug"]}/')
    # Sort the creators by ID
    sorted_creators = sorted(work['creators_primary'], key=lambda c: c['id'], reverse=True)
    # Only get biography data for unique creator names
    unique_creators = list(OrderedDict((c['name'], c) for c in sorted_creators).values())
    for creator in unique_creators:
        # Add all of their roles to 'roles'
        creator['roles'] = [d['role'] for d in sorted_creators if d['name'] in creator['name']]
        # Add 'film' to help match people?
        # creator['roles'].append('film')
        if ACMI_SEARCH_QUERY:
            if ACMI_SEARCH_QUERY in creator['name'].lower():
                add_biography(creator)
        else:
            add_biography(creator)
