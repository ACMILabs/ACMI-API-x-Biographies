# ACMI API x internet biography metadata

ACMI Public API example matching internet biographies to Work creators.

## Wikipedia biography data

An example of matching Wikipedia biography data to ACMI collection creators.

### Jupyter Notebook

The Jupyter Notebook code to run this example on [Google Colab](https://colab.research.google.com) can be found in in the file `acmi_api_biographies.ipynb`.

Run it in Google Colab: [![Open In Colab][colab-badge]][colab-notebook]

[colab-notebook]: <https://colab.research.google.com/drive/1iwBeiIKNnM2jzoimmlrejPTMvnL28pXB>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

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
