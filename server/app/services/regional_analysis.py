from app.core.mysql import Service


# 地区分析服务
class Regional_analysis(Service):
    def __init__(self, *config):
        """
        构造函数
        @param {Object} config 配置参数
        """
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "regional_analysis",
                # 分页大小
                "size": 30,
                "page": 1,
            }
        super(Regional_analysis , self).__init__(config_temp)
