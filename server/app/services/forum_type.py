from app.core.mysql import Service


# 论坛类型
class Forum_type(Service):
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
                "table": "forum_type",
                # 分页大小
                "size": 0,
            }
        super(Forum_type, self).__init__(config_temp)
