from app.core import controller

controllerClass = getattr(controller, "Controller")

# 系统用户
class System_user(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./system_user/",
            # 选择的服务
            "service": "system_user",
        }
        config_temp = config
        config_temp.update(config_init)
        super(System_user , self).__init__(config_temp)


