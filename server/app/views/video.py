from app.core import controller

controllerClass = getattr(controller, "Controller")


# 视频类
class Video(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./video/",
            # 选择的服务
            "service": "video",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Video, self).__init__(config_temp)

    def Index(self, ctx):
        """首页
        @param {Object} ctx http请求上下文
        @return {Object} 返回html页面
        """
        query = dict(ctx.query)
        query["type"] = "video"
        config_plus = {}
        if "field" in query:
            field = query.pop("field")
            config_plus["field"] = field
        if "page" in query:
            page = query.pop("page")
            config_plus["page"] = page
        if "size" in query:
            size = query.pop("size")
            config_plus["size"] = size

        config_temp = self.config
        config_temp.update(config_plus)
        obj = self.service.Get_obj(query, config_temp)
        name_arr = obj["name"].split(".")
        obj["extension"] = name_arr[len(name_arr) - 1]
        result_dict = {"obj": obj}
        model = self.model(ctx, result_dict)
        return ctx.render(self.config["tpl"] + "index" + ".html", model)
