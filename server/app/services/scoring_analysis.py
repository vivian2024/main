from app.core.mysql import Service


# 评分分析服务
class Scoring_analysis(Service):
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
                "table": "scoring_analysis",
                # 分页大小
                "size": 30,
                "page": 1,
            }
        super(Scoring_analysis , self).__init__(config_temp)
