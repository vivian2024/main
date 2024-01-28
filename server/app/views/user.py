from hashlib import md5
from app.core import controller
from app.service import service_select
from django.utils import timezone
import json
import time

controllerClass = getattr(controller, "Controller")


# 帮助方法，取得md5后的hash值
def md5hash(key):
    input_name = md5()
    input_name.update(key.encode("utf-8"))
    return input_name.hexdigest()


# 帮助方法,合并对象
def obj_update(*config):
    config_temp = {}
    for o in config:
        config_temp.update(o)
    return config_temp


def tokenGetUserId(token, request):
    # 缓存获取用户ID
    user_id = request.session.get(token, None) or 0
    # 数据库获取用户ID
    if user_id == 0:
        tokenService = service_select("access_token")
        obj = tokenService.Get_obj({"token": token})
        if obj:
            user_id = obj["user_id"]
    return user_id


# 用户类
class User(controllerClass):
    def __init__(self, config={}):
        """
		构造函数
		@param {Object} config 配置参数
		"""
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./user/",
            # 选择的服务
            "service": "user",
            # 注册API
            "get_api": ["state", "quit"],
            "post_api": ["login", "register", "change_password", "forget_password"],
            # 唯一判断
            "unique": ["username"]
        }
        config_temp = config
        config_temp.update(config_init)
        super(User, self).__init__(config_temp)

    def Register(self, ctx):
        """
		注册API
		@param {Object} config 配置参数
		"""
        print("===================注册=====================")
        userService = service_select("user")
        body = ctx.body

        # 判断必须信息
        if "username" not in body and body["username"] == '':
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "用户名不能为空",
                }
            }, ensure_ascii=False))
        if "user_group" not in body and body["user_group"] == '':
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "用户组不能为空",
                }
            }, ensure_ascii=False))
        if "password" not in body and body["password"] == '':
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "密码不能为空",
                }
            }, ensure_ascii=False))

        # 取出表单
        post_param = body
        post_param['nickname'] = body["nickname"] or ""
        post_param['password'] = md5hash(body["password"])

        # 校验是否存在用户
        obj = userService.Get_obj({"username": post_param['username']}, {"like": False})
        if obj:
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "用户名已存在",
                }
            }, ensure_ascii=False))

        ret = {
            "error": {
                "code": 70000,
                "message": "注册失败",
            }
        }
        # 添加
        bl = userService.Add(post_param)
        if bl:
            ret = {
                "result": {
                    "bl": True,
                    "message": "注册成功"
                }
            }
        return ctx.response(json.dumps(ret, ensure_ascii=False))

    def Forget_password(self, ctx):
        """
		找回密码API
		@param {Object} config 配置参数
		"""
        print("===================修改密码=====================")
        ret = {
            "error": {
                "code": 70000,
                "message": "用户信息不能没有"
            }
        }
        body = ctx.body
        if not body["code"]:
            return {
                "error": {
                    "code": 70000,
                    "message": "验证码不存在或者错误"
                }
            }

        # 获取用户
        obj = service_select("user").Get_obj(
            {"username": body["username"]}, {"like": False}
        )

        if not obj:
            return {
                "error": {
                    "code": 70000,
                    "message": "用户名不存在或者错误"
                }
            }

        password = md5hash(body["password"])
        if not password:
            return {
                "error": {
                    "code": 70000,
                    "message": "密码不存在或者错误"
                }
            }

        # 修改密码
        bl = service_select("user").Set({"user_id": obj["user_id"]}, {"password": password})
        if bl:
            ret = {"result": {"bl": True, "message": "修改成功"}}
        else:
            ret = {
                "error": {
                    "code": 70000,
                    "message": "修改失败",
                }
            }
        return ctx.response(json.dumps(ret, ensure_ascii=False))

    def Login(self, ctx):
        """
		登录API
		@param {Object} ctx http请求上下文
		"""
        print("===================登录=====================")
        ret = {
            "error": {
                "code": 70000,
                "message": "账户不存在",
            }
        }
        body = ctx.body
        # 获取用户
        password = md5hash(body["password"]) or ""
        obj = service_select("user").Get_obj(
            {"username": body["username"]}, {"like": False}
        )
        if obj:
            # 检查用户所属用户组
            user_group = service_select("user_group").Get_obj({'name': obj['user_group']}, {"like": False})
            if user_group and user_group['source_table'] != '':
                user_obj = service_select(user_group['source_table']).Get_obj({"user_id": obj['user_id']},
                                                                              {"like": False})
                if user_obj['examine_state'] == '未通过':
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "账户未通过审核",
                        }
                    }
                    return ret
                if user_obj['examine_state'] == '未审核':
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "账户未审核",
                        }
                    }
                    return ret
            # 校验用户状态
            if obj["state"] == 1:
                # 校验密码
                if obj["password"] == password:
                    # 生成Token
                    timeout = timezone.now()
                    timestamp = int(time.mktime(timeout.timetuple())) * 1000
                    token = md5hash(str(obj["user_id"]) + "_" + str(timestamp))
                    # 存储Token
                    ctx.request.session[token] = obj["user_id"]
                    service_select("access_token").Add(
                        {"token": token, "user_id": obj["user_id"]}
                    )
                    # 回传用户
                    obj["token"] = token
                    ret = {
                        "result": {"obj": obj}
                    }
                else:
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "密码错误",
                        }
                    }
            else:
                ret = {
                    "error": {
                        "code": 70000,
                        "message": "用户账户不可用，请联系管理员",
                    }
                }
        return ctx.response(json.dumps(ret, ensure_ascii=False))

    def Change_password(self, ctx):
        """
		修改密码API
		@param {Object} config 配置参数
		"""
        print("===================修改密码=====================")
        ret = {
            "error": {
                "code": 70000,
                "message": "账号未登录",
            }
        }
        request = ctx.request
        headers = request.headers
        # 判断Token
        if ("x-auth-token" in headers) and headers["x-auth-token"]:
            token = headers["x-auth-token"]
            user_id = tokenGetUserId(token, request)
            userService = service_select("user")
            # 获取密码和新密码
            body = ctx.body
            password = md5hash(body["o_password"])
            # 判断用户密码是否正确
            obj = userService.Get_obj({"user_id": user_id, "password": password}, {"like": False})
            if obj:
                # 修改密码并返回结果
                password = md5hash(body["password"])
                bl = userService.Set({"user_id": user_id}, {"password": password})
                if bl:
                    ret = {"result": {"bl": True, "message": "修改成功"}}
                else:
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "修改失败",
                        }
                    }
            else:
                ret = {
                    "error": {
                        "code": 70000,
                        "message": "密码错误",
                    }
                }
        else:
            ret = {
                "error": {
                    "code": 70000,
                    "message": "账户未登录",
                }
            }
        return ctx.response(json.dumps(ret, ensure_ascii=False))

    def State(self, ctx):
        """
		状态函数API
		@param {Object} self
		@param {Object} ctx
		"""
        print("===================获取登录态=====================")
        ret = {
            "error": {
                "code": 50000,
                "message": "账户未登录！"
            }
        }
        request = ctx.request
        headers = request.headers
        # 判断Token
        if ("x-auth-token" in headers) and headers["x-auth-token"]:
            token = headers.get("x-auth-token", None)
            user_id = tokenGetUserId(token, request)
            # 判断用户ID是否存在
            if user_id > 0:
                userService = service_select("user")
                user = userService.Get_obj({"user_id": user_id})
                user["token"] = token
                ret = {
                    "result": {
                        "obj": user
                    }
                }
        return json.dumps(ret, ensure_ascii=False)

    def Quit(self, ctx):
        """
		退出函数API
		@param {Object} self
		@param {Object} ctx
		"""
        print("===================退出=====================")
        ret = {
            "error": {
                "code": 50000,
                "message": "账户未登录！"
            }
        }
        request = ctx.request
        headers = request.headers
        # 判断Token是否存在
        if ("x-auth-token" in request.headers) and request.headers["x-auth-token"]:
            # 根据Token获取用户ID
            token = request.headers["x-auth-token"]
            service = service_select("access_token")
            user_id = request.session.get(token, None)
            del request.session[token]
            service.Del({
                token: token
            })
            # 判断用户状态
            ret = {
                "result": {
                    "bl": True,
                    "tip": "已退出！"
                }
            }
        return json.dumps(ret, ensure_ascii=False)

    # 增
    def Add(self, ctx):
        """
		增
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
        ctx.body['password'] = md5hash(ctx.body["password"])
        result = self.service.Add(ctx.body, self.config)
        if self.service.error:
            return {"error": self.service.error}
        return {"result": result}
