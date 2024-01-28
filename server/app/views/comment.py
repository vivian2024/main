from app.core import controller

controllerClass = getattr(controller, "Controller")


# 评论
class Comment(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./comment/",
            # 选择的服务
            "service": "comment",
			"like": False
        }
        config_temp = config
        config_temp.update(config_init)
        super(Comment, self).__init__(config_temp)
