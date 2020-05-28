from num2words import num2words
import itertools
import tmdbsimple as tmdb
from fuzzywuzzy import fuzz
import roman

upperLimitRatio = 90
tmdb.API_KEY = ''

def expandTitle(input_title):
    input_title = input_title.split()
    expanded_title = input_title.copy()
    for i, word in enumerate(expanded_title):
        expanded_title[i] = expanded_title[i].split()  # makes every word in title a list
        if word[0].isdigit() and word[-2:].isalpha():  # makes numeric ordinal to text ordinal
            ordinal = num2words(word[:-2], ordinal=True)
            expanded_title[i].append(ordinal)
        if word.isdigit():  # makes numeric number to text number
            cardinal = num2words(word)
            expanded_title[i].append(cardinal)
    if input_title[-1].isdigit():
        # If last word is number, also make it a roman numeral (titles usually only have them at the end)
        # Higher ratio threshold if it ends in a number because sequels match too closely.
        # Ex. Iron Man 2 returns a higher ratio
        global upperLimitRatio
        upperLimitRatio = 95
        print(upperLimitRatio)
        romannum = roman.toRoman(int(input_title[-1]))
        expanded_title[-1].append(romannum)
    titles = (list(itertools.product(*expanded_title)))  # makes list of every possible title
    for i, title in enumerate(titles):
        titles[i] = ' '.join(titles[i])
    return titles


def searchTitles(list_of_titles):
    search = tmdb.Search()
    searchResults = []
    for title in list_of_titles:
        results = search.movie(query=title)
        rateTitles(title, results, searchResults)
    return searchResults


def rateTitles(title, results, searchResults):
    # Gives each result a ratio for how well it matches search.
    # Removes duplicates, keeping only highest ratio (really only happens with numbers in title).
    for result in results['results']:
        if not any(i['id'] == result['id'] for i in searchResults):  # if it is a new result
            ratio = fuzz.ratio(result['title'].lower(), title.lower())
            result.update({'ratio': ratio})
            if result['ratio'] >= 25:
                searchResults.append(result)
        else:  # if it is a duplicate, keep highest ratio
            ratio = fuzz.ratio(result['title'].lower(), title.lower())
            for r in searchResults:
                if result['id'] == r['id']:
                    if ratio > r['ratio']:
                        r['ratio'] = ratio
    return searchResults

def searchAlternates(expandedTitles, searchResults):
    # Searches every result, searches alternate titles and then compares alternate titles to input.
    # If an alternate title has a higher ratio, that ratio becomes the new ratio for that result.
    for result in searchResults:
        alternates = tmdb.Movies(result['id']).alternative_titles(country="US")['titles']
        for alternate in alternates:
            for title in expandedTitles:
                ratio = fuzz.ratio(alternate['title'].lower(), title.lower())
                if ratio > result['ratio']:
                    result['ratio'] = ratio


def removeDuds(results):
    [results.remove(match) for match in results if 'release_date' not in match.keys() or match['release_date']=='']
    return results

def phaseOne(searchResults, expandedTitles):
    # Searches for every variation of the title (ex. Frozen 2 vs Frozen Two vs Frozen II)
    # Duplicates and duds are removed and sorted by ratio.

    if not searchResults:
        print('No results found!')
        return searchResults
    removeDuds(searchResults)
    sortedResults = (sorted(searchResults, key=lambda i: i['ratio']))
    print(expandedTitles)
    print('Phase 1 search results:')
    for result in sortedResults:
        print(f'    {result["ratio"]}% match {result["title"]}, id:{result["id"]}')
    return sortedResults

def phaseTwo(searchResults, expandedTitles):
    # Search for alternate titles, sorts them by ratio.
    searchAlternates(expandedTitles, searchResults)
    sortedResults = (sorted(searchResults, key=lambda i: i['ratio']))
    print('Phase 2 search results:')
    for result in sortedResults:
        print(f'    {result["ratio"]}% match {result["title"]}, id:{result["id"]}')
    return sortedResults

def search(input_title):
    expandedTitles = expandTitle(input_title)
    searchResults = searchTitles(expandedTitles)
    sortedResults = phaseOne(searchResults, expandedTitles)
    if sortedResults[-1]['ratio'] <= upperLimitRatio:
        sortedResults = phaseTwo(searchResults,expandedTitles)
    bestMatches = list(filter(lambda person: person['ratio'] == sortedResults[-1]['ratio'], sortedResults))

    return bestMatches
