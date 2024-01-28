from app.core.mysql import Service


# 首页
class Index(Service):
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
                "table": "user_account",
                # 分页大小
                "size": 1,
            }
        super(Index, self).__init__(config_temp)
