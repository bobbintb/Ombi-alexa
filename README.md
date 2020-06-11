# Ombi-alexa

This is a work in progress and is currently partially functioning. Right now I have movie requests working.

Installation:
You need a free Amazon developer account for this. Follow these instructions:
https://developer.amazon.com/en-US/docs/alexa/hosted-skills/alexa-hosted-skills-git-import.html

Notes:

-Make sure and put the API key for Ombi in the lambda_function.py file.

-Because Alexa is voice based, I had to make changes to the way Ombi does searches since the idea is to find the best match with minimal response from the user to find the right match. It does this based on Levenshtein distance. It also uses themoviedb to do searches instead of Ombi's built in search, which actually searches themoviedb. This is because the Ombi search doesn't have enough information to be able to narrow down the results.

Issues:

-I don't have a way yet to have individual users use Ombi. 

-Only movies working for now.
