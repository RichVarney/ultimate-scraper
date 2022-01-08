# ultimate-scraper
Scrape tabs from ultimate guitar

This script downloads tabs from https://www.ultimate-guitar.com/ and saves them as .txt files.

BeautifulSoup is used to search ultimate guitar for tabs. There is a command line interface to allow the user to perform the search and to choose which tabs to download.

During testing, tabs were being downloaded at around 4-5 tabs per second.

## How to use:
- Run the 'ultimate.scraper.py' script using python 3
- Follow the prompts that ask for user input
- The search functionality allows you to search by artist, or just using general
keywords
- If searching by artist, you will be presented with a few options to ensure the
correct artist is selected
- You can then choose to download individual, a selection, a range, or all tabs
from the search result
    - e.g.:  
        1, 2, 3, 4 (tabs 1, 2, 3 and 4 in the list)  
        1, 2, 6, 8 (tabs 1, 2, 6 and 8 in the list)  
        1-4 (tabs 1 to 4 in the list)  
        2-7 (tabs 2 to 7 in the list)  
        all (all tabs in the list)
- Tabs will be saved as .txt format
- Tabs will be saved in a folder '/tabs' where you ran this script from


#### Example usage downloading single tabs at a time, from a 'general' search:

```
python /Users/user_name/ultimate-scraper.py

> General search or specific artist/band?
> Options "general" or "artist": general

> Search for: laura marling daisy

[0] Laura Marling - Daisy (Chords) Version 1, rating: 4.8404, votes: 7
[1] Laura Marling - Daisy (Tabs) Version 1, rating: 4.91133, votes: 15

> Pick a tab by entering a number, range or "all": 1

> Download finished
> Location: /Users/user_name/tabs
```

#### Example usage downloading all tabs for a specific artist/ band:

> **Note:** 'album tabs' won't be displayed

```
python /Users/user_name/ultimate-scraper.py
> General search or specific artist/band?
> Options "general" or "artist": artist

> Search for: snarky
[0] Snarky Puppy
Select which band by choosing the relevant number:
0

[0] Snarky Puppy - Bent Nails (Tabs) Version 1, rating: 4.76024, votes: 12
[1] Snarky Puppy - Bent Nails (Tabs) Version 2, rating: 0, votes: 0
[2] Snarky Puppy - Brother Im Hungry (Tabs) Version 1, rating: 4.5505, votes: 5
[3] Snarky Puppy - Chonks (Tabs) Version 1, rating: 0, votes: 0
...
[12] Snarky Puppy - Tarova (Tabs) Version 1, rating: 4.734, votes: 3
[13] Snarky Puppy - The Clearing (Tabs) Version 1, rating: 4.85491, votes: 8
[14] Snarky Puppy - What About Me (Tabs) Version 1, rating: 4.59364, votes: 28
[15] Snarky Puppy - Whitecap (Tabs) Version 1, rating: 0, votes: 0

> Pick a tab by entering a number, range or "all": all

> Download finished

> Location: /Users/user_name/tabs

```

#### Example usage downloading multiple tabs at a time, from searching for a specific artist:

> **Note:** 'album tabs' won't be displayed

```
python /Users/user_name/ultimate-scraper.py

> General search or specific artist/band?
> Options "general" or "artist": artist

> Search for: pink floyd
[0] Pink Floyd
[1] Red Hot Chili Peppers
[2] Misc Television
[3] Lessons - Guitar
[4] Misc Originals
[5] Misc Mashups
Select which band by choosing the relevant number:
0
Skipping album tabs...
Skipping album tabs...
Skipping album tabs...
Skipping album tabs...
Skipping album tabs...
Skipping album tabs...

[0] Pink Floyd - A Great Day For Freedom (Chords) Version 1, rating: 4.70035, votes: 9
[1] Pink Floyd - A Great Day For Freedom (Tabs) Version 1, rating: 4.117, votes: 9
[2] Pink Floyd - A New Machine (Chords) Version 1, rating: 0, votes: 0
[3] Pink Floyd - A Pillow Of Winds (Chords) Version 1, rating: 4.25372, votes: 38
...
[413] Pink Floyd - Pigs On The Wing Parts 1 And 2 (Chords) Version 1, rating: 4.8703, votes: 71
[414] Pink Floyd - Pigs On The Wing Parts 1 And 2 (Tabs) Version 1, rating: 4.70035, votes: 9
[415] Pink Floyd - Pigs Three Different Ones (Chords) Version 1, rating: 4.6674, votes: 92
[416] Pink Floyd - Pigs Three Different Ones (Chords) Version 2, rating: 4.64041, votes: 7

> Pick a tab by entering a number, range or "all": 0, 2, 3, 413      

> Download finished
> Location: /Users/user_name/tabs
```


## Requirements:
- Python 3 (3.7.7 was using in testing this project)
- Beautiful Soup (3.2.2 was used in testing this project)
This is just something I wanted to do in my free time.

Inspiration for this was taken from [https://github.com/ccabrales/TabHero](https://github.com/ccabrales/TabHero)

## Contributing
Pull requests are welcome, however, I will not be looking at this frequently. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
