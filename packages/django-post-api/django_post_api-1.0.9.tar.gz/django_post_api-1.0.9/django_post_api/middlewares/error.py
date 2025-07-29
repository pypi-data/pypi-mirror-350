from logging import getLogger

from django.utils.deprecation import MiddlewareMixin

from django_post_api.errors import MyError
from django_post_api.views import BaseAPIView

debug_logger = getLogger("debug")
default_logger = getLogger("default")


class ErrorMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response
        self.base_api_view = BaseAPIView()  # 在初始化时创建实例

    def process_exception(self, request, exception):
        debug_logger.exception(f"Exception occurred in request {request.path}: {exception}")
        if isinstance(exception, MyError):
            err_msg = getattr(exception, "err_msg", "")
            status_code = getattr(exception, "status_code", 500)
        else:
            default_logger.exception(f"Exception occurred in request {request.path}: {exception}")
            status_code = 500
            err_type = exception.__class__.__name__
            err_msg = f"{err_type}: {';'.join([str(i) for i in exception.args])}"

        return self.base_api_view.error_return(err_msg, status_code)
