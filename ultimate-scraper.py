"""
This script downloads tabs from https://www.ultimate-guitar.com/
Uses the search functionality to find the tabs, then can choose from a list
which ones to downloads
Works at around 4-5 tabs per second

How to use:
- Run this script using python 3
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

Requirements:
- Beautiful Soup

"""


import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


save_location = os.getcwd()+'/tabs'


def get_search_terms_from_user_input():
    search_type = input('\n> General search or specific artist/band?\n> Options "general" or "artist": ').lower()
    search_terms = input('\n> Search for: ').split(' ')
    return search_terms, search_type

def search(search_url):
    page = requests.get(search_url)
    tabs_soup = BeautifulSoup(page.text, "lxml")
    results = tabs_soup.find(class_="js-store")
    json_content = json.loads(results.get('data-content'))
    return json_content

def make_url(search_terms, page_number=1, filter='general', select_band=None, quiet=False):
    search_string = '+'.join(item for item in search_terms)
    search_url = 'https://www.ultimate-guitar.com/search.php?page={}&title={}'.format(page_number, search_string)
    if filter == 'artist':
        json_content = search(search_url)
        list_of_bands = json_content['store']['page']['data']['filters']['bands']
        if quiet:
            pass
        else:
            for i, j in enumerate(list_of_bands):
                print('[{}] {}'.format(i, list_of_bands[i]['name']))
            select_band = input('Select which band by choosing the relevant number:\n')
        search_url = 'https://www.ultimate-guitar.com{}?page={}'.format(list_of_bands[int(select_band)]['url'], page_number)
        return search_url, select_band
    return search_url, select_band

def filter_json(_json, filtered_json={}, filter=None):
    # remove irrelevant results from list e.g. ukulele chords or marketing_type
    if filter == 'artist':
        tabs_location_in_json = 'other_tabs'
    else:
        tabs_location_in_json = 'results'
    for i, j in enumerate(_json['store']['page']['data'][tabs_location_in_json]):
        if 'marketing_type' in j:
            pass
        elif j['type'] in ['Ukulele Chords', 'Bass Tabs', 'Pro', 'Power', 'Official', 'Drum Tabs', 'Video']:
            pass
        else:
            # add new values to a dictionary and auto increment the key
            filtered_json[len(filtered_json)] = j
    return filtered_json

def display_search_results(_json):
    print('')
    for i, j in enumerate(_json.items()):
        print(('[{}] {} - {} ({}) Version {}, rating: {}, votes: {}'.format(i, j[1]['artist_name'], j[1]['song_name'], j[1]['type'], j[1]['version'], j[1]['rating'], j[1]['votes'])))

def compile_list_of_urls(_json):
    selection = input('\n> Pick a tab by entering a number, range or "all": ')
    # selection = input('\n> Pick from the above:\n> (Can select individual tabs, a range, or "all")\n> Loading...\n')

    if ' ' in selection:  # replace spaces with commas
        selection = selection.replace(' ', ',')

    if ',' in selection:  # list of items
        # trim leading or trailing commas
        selection = selection.rstrip(',').lstrip(',')
        # Split by spaces or commas or both
        selection = selection.replace(',,', ',').split(',')
        url = [_json[int(i)]['tab_url'] for i in selection]

    elif '-' in selection:  # range of items
        range_selection = selection.split('-')
        url = [_json[i]['tab_url'] for i in range(int(range_selection[0]), int(range_selection[1])+1)]
    elif selection.isnumeric():  # single item
        url = [_json[int(selection)]['tab_url']]
    elif selection.isalpha():  # all items
        if selection.lower() == 'all':
            url = [i[1]['tab_url'] for i in _json.items()]
    else:
        raise ValueError('{} entered. You must enter either a number, a range of numbers or "all"\
        examples:\n1\n1, 2, 3, 4, 5\n1-5\n3-10\nall'.format(selection))

    url = list(set(url))  # remove duplicates
    return url

def get_page_count(_json, filter=None):
    if filter == 'artist':
        page_count = _json['store']['page']['data']['pagination']['pages']
        count = 0
        for i in page_count:
            count = i['page']
        page_count = count
    else:
        page_count = _json['store']['page']['data']['pagination']['total']
    return page_count

def get_tab_json_data(url):
    # Get tab
    # tab_url = 'https://tabs.ultimate-guitar.com/tab/laura-marling/held-down-chords-3028859'
    tab_page = requests.get(url)
    tab_page_soup = BeautifulSoup(tab_page.text, "lxml")
    tab_content = tab_page_soup.find(class_='js-store')
    tab_json_content = json.loads(tab_content.get('data-content'))
    return tab_json_content

def get_tab_metadata_from_json(tab_json_content):
    # Get metadata artist, song, tab ID, rating, vote counts
    tab_metadata = {'artist_name':'',
    'song_name':'',
    'type':'',
    'version':'',
    'rating':'',
    'votes':'',
    'date':'',
    'song_id':'',
    'artist_id':'',
    'tab_access_type':'',
    'tab_url':''
    }

    for key, value in tab_metadata.items():
        if key == 'date':
            tab_metadata[key] = datetime.fromtimestamp(int(tab_json_content['store']['page']['data']['tab'][key]))
            continue
        tab_metadata[key] = tab_json_content['store']['page']['data']['tab'][key]

    return tab_metadata

def save_tab(tab_json_content):
    tab_metadata = get_tab_metadata_from_json(tab_json_content)
    file_name_format = ['artist_name', 'song_name', 'rating', 'votes', 'type']
    filename = '-'.join(str(tab_metadata[item]) for item in file_name_format).replace(' ', '_')
    file_extension = '.txt'
    metadata = ['{}: {}'.format(key, value) for (key, value) in tab_metadata.items()]
    folder_name = str(tab_metadata['artist_name']).replace(' ', '_')
    directory = os.path.join(save_location, folder_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename+file_extension)
    if os.path.exists(filepath):
        pass
    else:
        with open(filepath, 'w') as f:
            f.write('\n'.join([i for i in metadata]))
            f.write('\n\n')
            try:
                f.write(tab_json_content['store']['page']['data']['tab_view']['wiki_tab']['content'].replace('[tab]','').replace('[/tab]','').replace('[ch]','').replace('[/ch]',''))
            except Exception as e:
                print('Exception {} for {}'.format(e, filename))
                if e == 'content':
                    print('No tab content available')
    return folder_name

def main():
    search_terms, search_type = get_search_terms_from_user_input()
    url, select_band = make_url(search_terms, filter=search_type)
    json_content = search(url)
    total_page_count = get_page_count(json_content, filter=search_type)
    for i in range(total_page_count):
        try:
            url = make_url(search_terms, page_number=i+1, filter=search_type, select_band=select_band, quiet=True)
            json_content = search(url[0])
            filtered_json_search_results = filter_json(json_content, filter=search_type)
        except AttributeError as ae:
            print('Skipping album tabs...')
        except Exception as e:
            print('Exception', e)

    display_search_results(filtered_json_search_results)
    compiled_list_of_urls = compile_list_of_urls(filtered_json_search_results)
    for url in compiled_list_of_urls:
        tab_json_data = get_tab_json_data(url)
        save_tab(tab_json_data)
    print('\n> Download finished')
    print('> Location: {}'.format(save_location))


if __name__ == '__main__':
    main()
