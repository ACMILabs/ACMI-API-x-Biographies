"""
Use the ACMI Public API to match internet biographies to ACMI collection Works.
"""

from collections import OrderedDict
import requests

from wikidata.client import Client as WikidataClient

# Get the creators for the ACMI Work ID 113980 (Mad Max)
ACMI_WORK_ID = '113980'
creators = []

api_response = requests.get(
    f'https://api.acmi.net.au/works/{ACMI_WORK_ID}',
).json()

if api_response['creators_primary']:
    creators.extend(api_response['creators_primary'])
if api_response['creators_other']:
    creators.extend(api_response['creators_other'])

unique_creators = list(OrderedDict((c['name'], c) for c in creators).values())
for creator in unique_creators:
    # Add all of their roles to 'roles'
    creator['roles'] = [d['role'] for d in creators if d['name'] in creator['name']]
    # TODO: Use TMDB person ID to match Wikidata results after we add it to the Work API
    # Add work type to aid Wikidata matches for now
    creator['roles'].append(api_response['type'])
    if 'cast' in creator['roles']:
        creator['roles'].append('actor')

print(f'\nACMI collection item: {api_response["title"]} ({api_response["id"]})')
print(f'API: https://api.acmi.net.au/works/{api_response["id"]}/')
print(f'Website: https://www.acmi.net.au/works/{api_response["id"]}--{api_response["slug"]}/')

if unique_creators:
    print(f'\nCreators: {", ".join([c["name"] for c in unique_creators])}')
else:
    print(f'\nNo creators found for {api_response["title"]}, sorry!')


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
                if not match and role.lower() in result['description'].lower():
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


for creator in unique_creators:
    add_biography(creator)
