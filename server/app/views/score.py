from app.core import controller

controllerClass = getattr(controller, "Controller")


# 评分
class Score(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./score/",
            # 选择的服务
            "service": "score",
            # 唯一判断
            "unique": ["source_table", "source_field", "source_id", "user_id"]
        }
        config_temp = config
        config_temp.update(config_init)
        super(Score, self).__init__(config_temp)
