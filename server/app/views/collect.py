from app.core import controller

controllerClass = getattr(controller, "Controller")


# 收藏
class Collect(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./collect/",
            # 选择的服务
            "service": "collect",
            # 唯一判断
            "unique": ["source_table", "source_field", "source_id", "user_id"]
        }
        config_temp = config
        config_temp.update(config_init)
        super(Collect, self).__init__(config_temp)

    # 增
    def Add(self, ctx):
        """
        增
        @param {Object} ctx http请求上下文
        @return {Object} 返回json-rpc格式结果
        """
        check_obj = self.service.Get_obj(ctx.body, self.config)
        if not check_obj is None:
            return {"result": "已收藏"}
        result = self.service.Add(ctx.body, self.config)
        if self.service.error:
            return {"error": self.service.error}
        return {"result": result}