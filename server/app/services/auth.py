from app.core.mysql import Service


# 权限
class Auth(Service):
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
                "table": "auth",
                # 分页大小
                "size": 100
            }
        super(Auth, self).__init__(config_temp)
