class SplashProxyMiddleware:
    @staticmethod
    def process_request(request, spider):
        if not request.meta.get("_splash_processed"):
            if not request.meta.get('splash')\
                    or request.method not in {'GET', 'POST'}\
                    or not request.meta.get('proxy'):
                return

            splash_args = request.meta['splash'].setdefault('args', {})
            splash_args['proxy'] = request.meta["proxy"]
        request.meta.pop('proxy', None)
