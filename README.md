# Ombi-alexa

This is a work in progress and is not currently functioning. There are a few issues that need resolved.

Installation:
You need a free Amazon developer account for this. You can import the json for the Alexa part. The python files go in the lambda backend. I'll probably add more detailed instructions later but you can just google how to import an alexa skil for now.

Notes:

-Make sure and put the API key for themoviedb in the movie_search.py file. Notice it is themoviedb API, not Ombi. I'll fix this at some point.

-Because Alexa is voice based, I had to make changes to the way Ombi does searches since the idea is to find the best match with minimal response from the user to find the right match. It does this based on Levenshtein distance.

Issues:

-I don't have a way yet to have individual users use Ombi.
-I don't know how to handle multiple results with Alexa. If there is more than one movie with the exact same name, like a remake, I don't know how to get ALexa to ask for more information. This is my biggest issue right now. I'm kind of stuck on it so if anyone has any ideas let me know.
-For some reason, I can only test the code in the Alexa simulator once. After that it doesn't respond until I reload the page.
