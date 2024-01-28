from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")

# 授权
class Auth(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./auth/",
            # 选择的服务
            "service": "auth",
			"like": False
        }
        config_temp = config
        config_temp.update(config_init)
        super(Auth, self).__init__(config_temp)
