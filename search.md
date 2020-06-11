This is an explanation of the search process this skill uses. Ombi search results don't really work very well for Alexa because of the visual component. You are meant to search and select the result. This is not ideal for Alexa as it would lead to a lot of back and forth conversation just to try and select the intended movie. I added some logic to the skill to help with this. Additionally, films with numbers cause issues. Alexa converts spoken numbers to digits so "the edge of 17" will return no results but "the edge of seventeen" will work correctly. There are also issues with sequels, roman numerals, etc. Here is a summary of the process:

1. Take the given title and look for numbers.
2. If there are numbers, create additional titles with different forms of numbers.
    ex. back to the future 2, back to the future two, back to the future II (roman numerals only if the number is on the end)
3. Search the database for a matching movie, score results based on Levenshtein distance. This measures how similar the titles are.
4. If there is a good enough match and the second closest match isn't too similar to the best match, we found our movie.
5. If the results aren't good enough to determine a match, we do a phase two search but first, we remove a bunch of the really bad matches as it's a waste of resources to include them in the second search.
6. Phase two search includes alternate titles. For example, the official name is "back to the future part II" and we are searching for "back to the future II". By searching alternate titles, we get a better match.
7. If we have a good enough match now, we download it. Otherwise, we return the best results and ask the user to pick. Most of the time, this is due to movies with the exact same title.
