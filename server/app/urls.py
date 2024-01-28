from django.urls import path
from app.router import router

import importlib
import os


urlpatterns = []

# 获得视图控制器路径
controller_dir = os.getcwd() + "\\app\\views"
# 模块绝对路径的数组
arr = []


# 遍历模块文件(绝对路径)加到arr数组
def foreach_file(path_name):
    for root, dirs, files in os.walk(path_name):
        for f in files:
            arr.append(os.path.join(root, f))


# 读取模块
# f:文件路径
def loadModule(f):
    # 将f变成相对路径
    route_path = (
        f.replace(controller_dir + "\\", "").replace(".py", "").replace("\\", "/")
    )
    mod = importlib.import_module("app.views." + route_path)
    cs_controller = getattr(mod, route_path.capitalize())
    # controller是view文件夹下的内容
    controller = cs_controller()
    # 遍历出所有的controller的方法名（即action名）
    if route_path == "index":
        loadRoute(controller, "")
    else:
        loadRoute(controller, route_path)


# render(request, 'index.html', context)

# 注册路由
# @param {Object} controller 控制器模块
# @param {String} route_path 路由路径
def loadRoute(controller, route_path):
    get = controller.config["get"]
    post = controller.config["post"]
    get_api = controller.config["get_api"]
    post_api = controller.config["post_api"]
    
    # 帮助函数 ，负责添加路由urlpatterns列表,其中controller是外部变量
    def append_urlpatterns(req_method, route_path_plus, action):
        router_method = router(req_method, getattr(controller, action))
        urlpatterns.append(path(route_path_plus, router_method))

    if hasattr(controller, "Index"):
        append_urlpatterns("all", route_path, "Index")
    if hasattr(controller, "Api"):
        append_urlpatterns("all", "api" + "/" + route_path, "Api")
    for action in get:
        if action == "index":
            append_urlpatterns("get", action, action.capitalize())
        elif not route_path == "":
            append_urlpatterns("get", route_path + "/" + action, action.capitalize())
    for action in post:
        if action == "index":
            append_urlpatterns("post", action, action.capitalize())
        else:
            append_urlpatterns("post", route_path + "/" + action, action.capitalize())
    for action in get_api:
        if action == "index":
            append_urlpatterns("get", "api" + "/" + route_path, action.capitalize())
        else:
            append_urlpatterns("get", "api" + "/" + route_path + "/" + action, action.capitalize())
        
    for action in post_api:
        if action == "index":
            append_urlpatterns("post", "api" + "/" + route_path, action.capitalize())
        else:
            append_urlpatterns("post", "api" + "/" + route_path + "/" + action, action.capitalize())


# 添加绝对路径到arr
foreach_file(controller_dir)

# 遍历模块数组，加载每个模块（内有加载路由）
for f in arr:
    if f.find(".pyc") == -1 and f.find("__init__") == -1:
        loadModule(f)
