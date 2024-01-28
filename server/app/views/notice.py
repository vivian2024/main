from app.core import controller

controllerClass = getattr(controller, "Controller")


# 公告
class Notice(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./notice/",
            # 选择的服务
            "service": "notice",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Notice, self).__init__(config_temp)
