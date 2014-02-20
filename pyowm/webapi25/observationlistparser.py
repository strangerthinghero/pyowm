#!/usr/bin/env python

"""
Module containing a concrete implementation for JSONParser abstract class,
returning lists of Observation objects
"""

from json import loads, dumps
from pyowm.abstractions.jsonparser import JSONParser
from pyowm.webapi25.observationparser import ObservationParser
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_response_error import APIResponseError


class ObservationListParser(JSONParser):
    """
    Concrete *JSONParser* implementation building a list of *Observation* 
    instances out of raw JSON data coming from OWM web API responses.

    :param observation_parser: a servant ObservationParser object
    :type observation_parser: ObservationParser
    :returns: a *Location* instance

    """

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses a list of *Observation* instances out of raw JSON data. Only
        certain properties of the data are used: if these properties are not
        found or cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a list of *Observation* instances or ``None`` if no data is
            available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the OWM API
            returns a HTTP status error (this is an OWM web API 2.5 bug)

        """
        d = loads(JSON_string)
        observation_parser = ObservationParser()
        if 'cod' not in d:
                raise ParseResponseError(''.join([__name__,
                                        ': impossible to read JSON data']))
        # Check if server returned errors: this check overcomes the lack of use
        # of HTTP error status codes by the OWM API 2.5. This mechanism is
        # supposed to be deprecated as soon as the API fully adopts HTTP for
        # conveying errors to the clients
        if d['cod'] == "404":
            print "OWM API: data not found - response payload: " + dumps(d)
            return None
        if d['cod'] == "200":
            # Handle the case when no results are found
            if 'count' in d and d['count'] is "0":
                return []
            else:
                if 'list' in d:
                    return [observation_parser.parse_JSON(dumps(item)) \
                             for item in d['list']]
                else:
                    raise ParseResponseError(''.join([__name__,
                                            ': impossible to read ' \
                                            'observation list from JSON data']))
        raise APIResponseError("OWM API: error - response payload: " + dumps(d))

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
