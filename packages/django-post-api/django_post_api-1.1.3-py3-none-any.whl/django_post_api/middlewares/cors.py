from django.utils.deprecation import MiddlewareMixin

DEFAULT_HEADERS = [
    "accept", "accept-encoding", "authorization", "content-type",
    "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with",
    "accept-language", "http-req-source"
]
# 在HTTP headers的规范中，当列出多个值时，它们通常是由一个逗号和一个空格（, ）分隔的。这种格式可以使头部值更易于阅读，尤其是在开发和调试时。
EXPOSED_HEADERS = ", ".join(DEFAULT_HEADERS + ["content-disposition", "content-filename"])
ALLOWED_HEADERS = ", ".join(DEFAULT_HEADERS)
ALLOWED_METHODS = ", ".join(["POST"])


class BaseCorsMiddleware(MiddlewareMixin):

    @staticmethod
    def set_headers(response, headers):
        for header, value in headers.items():
            response[header] = value
        return response


class CorsMiddleware(BaseCorsMiddleware):

    def process_response(self, request, response):
        # if getattr(request, "request_act", None) in [RequestActEnum.export.name, RequestActEnum.download.name]:
        #     self.set_headers(response, {"Access-Control-Expose-Headers": EXPOSED_HEADERS})

        # if not settings.NOW_ENV_IS_PROD:
        self.set_headers(response, {"Access-Control-Allow-Origin": "*"})

        if request.method == "OPTIONS":
            self.set_headers(response, {
                "Access-Control-Allow-Headers": ALLOWED_HEADERS,
                "Access-Control-Allow-Methods": ALLOWED_METHODS
            })

        return response
