from app.core import controller

controllerClass = getattr(controller, "Controller")


# 论坛
class Forum(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./forum/",
            # 选择的服务
            "service": "forum",
            # 互动
            "interact": ["praise", "comment", "hits", "collect"],
        }
        config_temp = config
        config_temp.update(config_init)
        super(Forum, self).__init__(config_temp)
