# ACMI API x internet biography metadata

ACMI Public API example matching internet biographies to Work creators.

## Wikipedia biography data

An example of matching Wikipedia biography data to ACMI collection creators.

### Python

Run `python3 acmi_api_biographies.py` to first search the ACMI Works API for creators named `Simon`, and then search the Wikipedia API to get an extract of the biography of that person.

Example output:

```bash
$ python3 acmi_api_biographies.py

Found 14 ACMI creators with simon in their name: {'Jamil Simon', 'Phil Simon', 'Jamil Simon Productions', 'Simon Trevor', 'Simon Wincer', 'Simon Price', 'Simon Bruty', 'Simon Penny', 'Simon McIntyre', 'Simon Moore', 'Simon West', 'Simon Bejer', 'Simon Terrill', 'Simon Maidment'}

Sorry, no data from Wikipedia for: Jamil Simon

Wikipedia data for Phil Simon: https://en.wikipedia.org/wiki/Phil_Simon
Title: Phil Simon
Extract: Phil Simon (born ca. 1972) is an American speaker, professor, and author. He writes about management, technology, disruption, communication, and analytics.

...
```

### Jupyter Notebook

TODO...
