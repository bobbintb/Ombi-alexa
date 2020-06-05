# Ombi-alexa

This is a work in progress and is not currently functioning. Right now I have movie searches working.

Installation:
You need a free Amazon developer account for this. You can import the json for the Alexa part. The python files go in the lambda backend. I'll probably add more detailed instructions later but you can just google how to import an alexa skil for now.

Notes:

-Make sure and put the API key for Ombi in the lambda_function.py file.

-Because Alexa is voice based, I had to make changes to the way Ombi does searches since the idea is to find the best match with minimal response from the user to find the right match. It does this based on Levenshtein distance. It also uses themoviedb to do searches instead of Ombi's built in search, which actually searches themoviedb. This is because the Ombi search doesn't have enough information to be able to narrow down the results.

Issues:

-I don't have a way yet to have individual users use Ombi. 

-Only movies working for now.
