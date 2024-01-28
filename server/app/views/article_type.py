from app.core import controller

controllerClass = getattr(controller, "Controller")


# 论坛类型
class Article_type(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./article_type/",
            # 选择的服务
            "service": "article_type"
        }
        config_temp = config
        config_temp.update(config_init)
        super(Article_type, self).__init__(config_temp)
