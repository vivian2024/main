from app.core.mysql import Service


# 用户类
class User_group(Service):
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
                "table": "user_group",
                # 分页大小
                "size": 30,
            }
        super(User_group, self).__init__(config_temp)
