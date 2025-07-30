""" Model Base Class setup module"""

import requests
import json
from pydantic import BaseModel
from enum import Enum
from abc import ABC
from time import sleep, perf_counter
from typing import Optional, ClassVar, Union
from typing_extensions import Self

from ant_connect.config import RequestsConfig, ThrottleConfig, empty_default
from ant_connect.enums import HttpMethodType


class ModelBaseClass(BaseModel, ABC):
    """
    Abstract base class for all ANT V2 data model classes.

    Once logged in to the ANT API using the APIConnector, this class
    stores a copy of the access token such that all models can use
    these credentials to load data from the API.
    """

    _get_host: ClassVar[Optional[str]] = None
    _access_token: ClassVar[Optional[str]] = None
    _headers: ClassVar[dict] = RequestsConfig.headers.copy()
    _throttle_counter: ClassVar[int] = 0
    _time: ClassVar[float] = 0.0
    _is_timing: ClassVar[bool] = False
    _auto_throttle: ClassVar[bool] = False

    @classmethod
    def _from_json(cls, json: dict) -> Self:
        """Constructs and returns an instance of an ANT model from a json object.
        The json object is expected to be the response from an API call.

        Parameters
        ----------
        json : dict
            Dict object from json response

        Returns
        -------
        Self
            Instance of the model class
        """
        return cls(**json)

    @classmethod
    def _call_api(
        cls,
        method_type: HttpMethodType,
        endpoint: str,
        parameters: Optional[Union[dict, list, str]] = None,
        is_query: bool = False,
    ) -> requests.Response:
        """
        Model base class for http requests with build-in throttle.
        See the config for throttle constants.

        Args:
                method_type (HttpMethodType): http method type enum
                endpoint (str): url endpoint for http request
                parameters (dict, optional): parameters as request content. Defaults to None.

        Raises:
                ValueError: error is thrown when auto_throttle is False and requests in time-frame has exceeded
                ValueError: error is thrown when invalid http method is given.

        Returns:
                requests.Response: response object from request
        """
        # check if connection is active
        if cls._get_host is None:
            raise ValueError("Connection is not active. Please use the ApiConnector class to activate")
        # check requests count for throttle
        if ModelBaseClass._is_timing:
            if ModelBaseClass._throttle_counter < ThrottleConfig.amount:
                ModelBaseClass._throttle_counter += 1
            else:
                if ModelBaseClass._auto_throttle:
                    while perf_counter() - ModelBaseClass._time <= ThrottleConfig.time_frame:
                        sleep(0.001)
                else:
                    raise ValueError(
                        f"Too many requests received {ThrottleConfig.time_frame} seconds. \
						Change your process or turn auto_throttle on with the ApiConnector class."
                    )

                ModelBaseClass._time = perf_counter()
                ModelBaseClass._throttle_counter = 1
        else:
            ModelBaseClass._time = perf_counter()
            ModelBaseClass._throttle_counter = 1
            ModelBaseClass._is_timing = True

        # set url and parameters for http request
        url = "/".join((ModelBaseClass._get_host, endpoint))
        ModelBaseClass._headers["Authorization"] = RequestsConfig._placeholder_string.format(
            ModelBaseClass._access_token
        )

        if parameters is None:
            processed_parameters = {}
        elif parameters is empty_default:
            processed_parameters = {}
        elif isinstance(parameters, dict):
            for key, value in parameters.items():
                if isinstance(value, Enum):
                    parameters[key] = value.value
            # check if there is an empty default value <class 'inspect._empty'> and remove these properties from dict
            processed_parameters = ModelBaseClass.empty_defaults_input_check(parameters)
        elif isinstance(parameters, list):
            processed_parameters = [ModelBaseClass.empty_defaults_input_check(value) for value in parameters]
        elif isinstance(parameters, str):
            processed_parameters = parameters
        else:
            raise ValueError("Invalid parameters type. Please provide a dict, list or str.")

        if not isinstance(processed_parameters, str) and not is_query:
            # processed request data
            request_data = json.dumps(processed_parameters)
        else:
            request_data = processed_parameters

        if method_type is HttpMethodType.GET:
            return requests.get(
                url=url,
                params=request_data,
                headers=ModelBaseClass._headers,
                verify=RequestsConfig.verify,
            )
        elif method_type is HttpMethodType.PUT:
            return requests.put(
                url=url,
                headers=ModelBaseClass._headers,
                data=request_data,
                verify=RequestsConfig.verify,
            )
        elif method_type is HttpMethodType.DELETE:
            return requests.delete(
                url=url,
                headers=ModelBaseClass._headers,
                data=request_data,
                verify=RequestsConfig.verify,
            )
        elif method_type is HttpMethodType.POST:
            return requests.post(
                url=url,
                headers=ModelBaseClass._headers,
                data=request_data,
                verify=RequestsConfig.verify,
            )
        else:
            raise ValueError("No correct HTTP method was provided")

    @staticmethod
    def empty_defaults_input_check(parameters_dict: dict) -> dict:
        """Check if the input parameters have default values. If they do,
        remove them from the object.

        Args:
            parameters_dict (dict): input parameters

        Returns:
            dict: converted parameters with empty strings
        """
        return {key: value for key, value in parameters_dict.items() if value is not empty_default}
