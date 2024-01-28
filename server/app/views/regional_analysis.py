from app.core import controller

controllerClass = getattr(controller, "Controller")

# 地区分析
class Regional_analysis(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./regional_analysis/",
            # 选择的服务
            "service": "regional_analysis",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Regional_analysis , self).__init__(config_temp)


