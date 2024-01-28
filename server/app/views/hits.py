from app.core import controller

controllerClass = getattr(controller, "Controller")


# 导航
class Hits(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./hits/",
            # 选择的服务
            "service": "hits",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Hits, self).__init__(config_temp)
