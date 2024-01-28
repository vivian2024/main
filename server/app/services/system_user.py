from app.core.mysql import Service


# 系统用户服务
class System_user(Service):
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
                "table": "system_user",
                # 分页大小
                "size": 30,
                "page": 1,
            }
        super(System_user , self).__init__(config_temp)
