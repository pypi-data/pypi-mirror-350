import abc
import typing

import scrapy


__all__ = ['CaptchaRule']


class CaptchaRule(abc.ABC):
    @property
    @abc.abstractmethod
    def domain(self) -> str:
        """
        Name of resolving rule and domain of
        :return: str - domain.
        """
        ...

    @abc.abstractmethod
    def is_captcha(self, request, response) -> bool:
        """
        Says if there is a captcha on the page

        :param request: request that caused the corresponding response
        :param response: response to be checked for text captcha
        :return: bool - True if there is a captcha on the page False otherwise.
        """
        ...

    @abc.abstractmethod
    def action_sequence(self,
                        request,
                        response,
                        original_response,
                        **kwargs) -> typing.Callable[[scrapy.Request, scrapy.http.Response], scrapy.Request]:
        """
        Function for defining captcha solving process

        :param request: request that caused the corresponding response
        :param response: page response with captcha on the page
        :param original_response: original page response that provoked the middleware
            to solve text captcha
        :return: function that implements sequence of actions that procedure request
            response and **kwargs. The sequence has to end up with the Request that includes
            meta-key '_captcha_response' with a link to the original response and
            each new request must have '_captcha_action' meta-key with True value.
        """
        ...

    @abc.abstractmethod
    def change_response(self, original_response, response) -> scrapy.http.Response:
        """
        Changed response in corresponding way for more convenient usage by user

        :param original_response: original response with captcha that is possibly
            needed to replace certain parameters
        :param response: response with no text captcha on the page
        :return: response with replaced parameters, so user works with this response.
        """
        ...
