from app.core import controller

controllerClass = getattr(controller, "Controller")


# 导航
class Nav(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./nav/",
            # 选择的服务
            "service": "nav",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Nav, self).__init__(config_temp)
