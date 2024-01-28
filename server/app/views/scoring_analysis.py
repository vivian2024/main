from app.core import controller

controllerClass = getattr(controller, "Controller")

# 评分分析
class Scoring_analysis(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./scoring_analysis/",
            # 选择的服务
            "service": "scoring_analysis",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Scoring_analysis , self).__init__(config_temp)


