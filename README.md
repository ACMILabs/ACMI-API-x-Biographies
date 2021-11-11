# ACMI API x internet biography metadata

ACMI Public API example matching internet biographies to Work creators.

## Wikidata and Wikipedia biography data

An example of matching Wikidata and Wikipedia biography data to ACMI collection creators.

### Jupyter Notebook

The Jupyter Notebook code to run this example on [Google Colab](https://colab.research.google.com) can be found in in the file `acmi_api_biographies.ipynb`.

Run it in Google Colab: [![Open In Colab][colab-badge]][colab-notebook]

[colab-notebook]: <https://colab.research.google.com/drive/1iwBeiIKNnM2jzoimmlrejPTMvnL28pXB>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

<img src="./_images/ACMI-Public-API-x-Wikipedia-biographies.png" width="100%"></img>

### Python

Run `python3 acmi_api_biographies.py` to first retrieve the creators of a Work from the ACMI Works API, and then search the Wikidata/Wikipedia API to get an extract of the biography of that person.

Example output:

```bash
$ python3 acmi_api_biographies.py

Matching biographies for ACMI collection item: Mad Max (113980)
ACMI API: https://api.acmi.net.au/works/113980/
ACMI Website: https://www.acmi.net.au/works/113980--mad-max/

🥳 Matched ACMI George Miller (66844) to WikiData: George Miller (Q446960) - Australian filmmaker and former physician
Wikidata: https://www.wikidata.org/wiki/Q446960
Wikipedia: https://en.wikipedia.org/wiki/George_Miller_(filmmaker)
Wikipedia extract: George Miller  (born 3 March 1945) is an Australian film director, producer, screenwriter, and physician. He is best known for his Mad Max franchise, whose second installment, Mad Max 2, and fourth, Fury Road, have been hailed as two of the greatest action films of all time, with Fury Road winning six Academy Awards. Miller is very diverse in genre and style as he also directed the biographical medical drama Lorenzo's Oil, the dark fantasy The Witches of Eastwick, the Academy-Award winning animated film Happy Feet, produced the family friendly fantasy adventure Babe and directed the sequel Babe: Pig in the City.
Miller is a co-founder of the production houses Kennedy Miller Mitchell, formerly known as Kennedy Miller, and Dr. D Studios. His younger brother Bill Miller and Doug Mitchell have been producers on almost all the films in Miller's later career, since the death of his original producing partner Byron Kennedy.
In 2006, Miller won the Academy Award for Best Animated Feature for Happy Feet (2006). He has been nominated for five other Academy Awards: Best Original Screenplay in 1992 for Lorenzo's Oil, Best Picture and Best Adapted Screenplay in 1995 for Babe, and Best Picture and Best Director for Fury Road in 2015.
IMDB person: https://www.imdb.com/name/nm0004306/
TMDB person: https://www.themoviedb.org/person/20629
Image: https://upload.wikimedia.org/wikipedia/commons/1/18/George_Miller_-_Happy_Feet_2.jpg
VIAF ID: 17273086
Library of Congress authority ID: no88004808
WorldCat Identities ID: lccn-no88004808
```
