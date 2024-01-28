from app.core import controller

controllerClass = getattr(controller, "Controller")


# 轮播图
class User_group(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./user_group/",
            # 选择的服务
            "service": "user_group",
        }
        config_temp = config
        config_temp.update(config_init)
        super(User_group, self).__init__(config_temp)
