from app.core import controller

controllerClass = getattr(controller, "Controller")


# 新闻
class News(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./news/",
            # 选择的服务
            "service": "news",
            "interact": ["comment", "praise", "score", "collect", "hits"],
        }
        config_temp = config
        config_temp.update(config_init)
        super(News, self).__init__(config_temp)
