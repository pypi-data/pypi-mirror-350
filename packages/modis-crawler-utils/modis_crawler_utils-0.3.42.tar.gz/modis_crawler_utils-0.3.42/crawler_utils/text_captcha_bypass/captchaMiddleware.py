import scrapy.crawler
import scrapy.exceptions

from .captchaRule import CaptchaRule


__all__ = ['CaptchaMiddleware']


class CaptchaMiddleware:
    """
            The middleware for text captcha solving.
        It automatically solves text captcha on the pages using
        rules defined by user.
        If there is no captcha on the page nothing will happen with the response.
        If the middleware finds captcha it solves it with user defined rules and
        checks again for captcha on the page. For more info about rules look at
        CaptchaRule class.

            If you want to turn text captcha solving off on the exact request provide
        meta-key 'dont_captcha' with True value. The middleware will skip the request
        through itself
        .

            The middleware uses additionally these meta-keys, do not use them, because their changing
        could possibly (almost probably) break determined behaviour:
        '_captcha_response', '_captcha_action'

            Settings:

        CAPTCHA_RULES: CaptchaRule | list[CaptchaRule] - instance(-s) of CaptchaRule
        defined by user in order to solve text captcha on the pages.
    """

    CAPTCHA_RULES = "CAPTCHA_RULES"

    def __init__(self, rules):
        self.captcha_rules = rules

    @classmethod
    def from_crawler(cls, crawler: scrapy.crawler.Crawler):
        rules = crawler.settings.get(cls.CAPTCHA_RULES)
        if rules is None:
            raise ValueError("No rules for CaptchaMiddleware")
        if isinstance(rules, CaptchaRule):
            rules = [rules]
        elif isinstance(rules, list):
            for rule in rules:
                if not isinstance(rule, CaptchaRule):
                    raise ValueError(f"Not valid rule for CaptchaMiddleware: {rule}")
        else:
            raise TypeError("Not valid type of rule for ")
        return cls(rules)

    @staticmethod
    def process_request(request, spider):
        return None

    def process_response(self, request, response, spider):
        if request.meta.get('dont_captcha', False):
            # No captcha solving due to key
            return response

        original_response = request.meta.pop('_captcha_response', None)
        if original_response is not None:
            # The last response in captcha solving process
            for rule in self.captcha_rules:
                if rule.domain in original_response.url:
                    if rule.is_captcha(request, response):
                        procedure_function = rule.action_sequence(request, response, original_response)
                        return procedure_function(request, response)
                    return rule.change_response(original_response, response)
            raise scrapy.exceptions.IgnoreRequest(f"No valid rule for response: {original_response}")

        if request.meta.get('_captcha_action', False):
            # Next request in captcha solving sequence
            return request.callback(response, **request.cb_kwargs)

        # Ordinary response, checking for text captcha
        for rule in self.captcha_rules:
            if rule.domain in response.url and rule.is_captcha(request, response):
                procedure_function = rule.action_sequence(request, response, response)
                return procedure_function(request, response)
        return response
