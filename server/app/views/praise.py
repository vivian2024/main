from app.core import controller

controllerClass = getattr(controller, "Controller")


# 点赞
class Praise(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./praise/",
            # 选择的服务
            "service": "praise",
            # 唯一判断
            "unique": ["source_table", "source_field", "source_id", "user_id"]
        }
        config_temp = config
        config_temp.update(config_init)
        super(Praise, self).__init__(config_temp)
