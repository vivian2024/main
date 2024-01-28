# 这个类需要继承django的中间件方法，因此需要导入如下
from django.utils.deprecation import MiddlewareMixin
from app.service import service_select
from django.http import HttpResponse
import json


# 授权中间件类
class CorsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if(request.method == "Origin" or request.method == "OPTIONS"):
            return HttpResponse(status=204)
        else:
            pass

    def process_response(self, request, response):
        # 添加响应头

        # 允许你的域名来获取我的数据
        response['Access-Control-Allow-Origin'] = "*"

        # 允许你携带Content-Type请求头
        # 允许自定义前端可以添加请求头 token 字段
        response['Access-Control-Allow-Headers'] = "Content-Type,Accept,Authorization,x-auth-token"

        # 资格证书
        response["Access-Control-Allow-Credentials"] = "true"

        # 允许你发送DELETE,PUT
        response['Access-Control-Allow-Methods'] = "*"

        # 最大有效周期
        response["Access-Control-Max-Age"] = "86400"

        return response
