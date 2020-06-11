import tmdbsimple as tmdb

def construct(search_result):
    print('constructor: ', search_result)
    dialogue = f'There are {len(search_result)} results named {search_result[0]["title"]}.'
    print(dialogue)
    for i, match in enumerate(search_result):
        dialogue += f' {i+1}. Released in {match["year"]} and starring {get_cast(match)}.'
    #dialogue += ' Which one?'
    return dialogue

def get_cast(match):
    search = tmdb.Movies(match['id']).credits()
    if search['cast']:
        return search['cast'][0]['name']
    else:
        return "an unknown actor"