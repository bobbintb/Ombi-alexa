# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import tmdbsimple as tmdb
import pyombi
import re
import ask_sdk_core.utils as ask_utils
import searches.movie_search
import searches.dialogue_constructor

from datetime import datetime
from ask_sdk_model import (
    Response, IntentRequest, DialogState, SlotConfirmationStatus, Slot)
from ask_sdk_model.dialog import DelegateDirective
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui import StandardCard
from ask_sdk_model.ui import Image


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ombi = pyombi.Ombi(
        ssl=True,
        host="",
        port="443",
        username=None,
        api_key=""
        )


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can say Hello or Help. Which would you like to try?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class SearchMovieIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("SearchMovieIntent")(handler_input) and handler_input.request_envelope.request.dialog_state != DialogState.COMPLETED)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print(DialogState)
        currentIntent = handler_input.request_envelope.request.intent
        slots = currentIntent.slots
        movie = slots["Movie"].value
        search_result = searches.movie_search.search(movie)
        if not search_result:
            speak_output = f"Sorry, there were no matches for {movie}."
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .response
            )
        for i, date in enumerate(search_result):
            year = datetime.strptime(search_result[i]['release_date'], '%Y-%M-%d')
            search_result[i]['year']=(year.year)
        if len(search_result) == 1:
            text = f"{search_result[0]['title']} ({search_result[0]['year']}) \n\n{search_result[0]['overview']}"
            #speak_output = search_result[0]['title']
            img = Image(small_image_url="https://image.tmdb.org/t/p/w440_and_h660_face" + search_result[0]['poster_path'])
            if movieDownload(search_result[0]) == True:
                speak_output = f'{search_result[0]["title"]} has succesfully been added to the request list.'
            else:
                speak_output = 'Sorry, there was a problem requesting the movie.'
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    #.set_card(StandardCard(title="Results", text=text, image=img))
                    #.add_directive(DelegateDirective(currentIntent))
                    #.addDelegateDirective(currentIntent)
                    .response
            )
        else:
            sorted_x = (sorted(search_result, key = lambda i: i['year'], reverse=True))
            session_attr = handler_input.attributes_manager.session_attributes
            session_attr["sorted_x"] = sorted_x
            #searches.dialogue_constructor.get_cast(sorted_x)
            for i, x in enumerate(sorted_x):
                actor = searches.dialogue_constructor.get_cast(sorted_x[i])
                sorted_x[i]['actor']=actor
            
            test = searches.dialogue_constructor.construct(sorted_x)
            handler_input.response_builder.speak(test)#.ask(speak_output)
            #handler_input.request_envelope.session.sorted_x.value = sorted_x
            #print("sorted :", handler_input.request_envelope.session.sorted_x.value)
            print(DialogState)
            return (
                handler_input.response_builder
                #handler_input.response_builder
                    .speak(test)
                    .add_directive(DelegateDirective(currentIntent))
                    #.ask(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    #.set_card(StandardCard(title=len(search_result), text=title))
                   .response
            )

class CompletedSearchMovieIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("SearchMovieIntent")(handler_input) and DialogState.COMPLETED)
    
    def handle(self, handler_input):
        currentIntent = handler_input.request_envelope.request.intent
        slots = currentIntent.slots
        user_response = slots["response"].value
        print(user_response)
        session_attr = handler_input.attributes_manager.session_attributes
        item=narrowDownResults(user_response,session_attr["sorted_x"])
        print(session_attr["sorted_x"])
        if movieDownload(item) ==True:
            speak_output = f"{item['title']} has succesfully been added to the request list."
        else:
            speak_output = 'Sorry, there was a problem requesting the movie.'
        return (
            handler_input.response_builder
                .speak(Alexa.escapeXmlCharacters(speak_output))
                .set_should_end_session(True)
                .response
            )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

def narrowDownResults(user_response,sorted_x):
    result = re.sub('[^0-9]','', user_response)
    if result.isnumeric() and len(result) <= 2 and len(user_response) <= 4:
        for i, item in enumerate(sorted_x):
            if i+1 == int(result):
                return sorted_x[i]
    elif result.isnumeric() and len(result) == 4 and len(user_response) == 4:
        for item in sorted_x:
            if item['year'] == int(result):
                return item
    elif user_response == 'last':
        return sorted_x[-1]
    else:
        for item in sorted_x:
            if user_response.lower() in item['actor'].lower():
                return item

def movieDownload(item):
    ombi.authenticate()
    try:
        ombi.test_connection()
        print("Connection success")
    except pyombi.OmbiError as e:
        print(e)
        return False
    
    errorMessage=ombi.request_movie(item['id'])
    print(errorMessage)
    return True

def addResponseBuilder(item):
    pass
    # speak_output = f"{item['title']} has succesfully been added to the request list."
    # speak_output = f"{item['title']} has already been requested."
    #"errorMessage": "\"Hotel Transylvania\" has already been requested"

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SearchMovieIntentHandler())
sb.add_request_handler(CompletedSearchMovieIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()