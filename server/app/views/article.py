from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")


# 帮助方法,合并对象
def obj_update(*config):
    config_temp = {}
    for o in config:
        config_temp.update(o)
    return config_temp


# 文章
class Article(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./article/",
            # 选择的服务
            "service": "article",
            # 互动
            "interact": ["praise", "comment", "hits", "score", "collect"],
        }
        config_temp = config
        config_temp.update(config_init)
        super(Article, self).__init__(config_temp)

    #  列表页面
    def List(self, ctx):
        """
        列表页面
        @param {Object} ctx http请求上下文
        @return {Object} 返回html页面
        """
        query = dict(ctx.query)
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
        if "orderby" in query:
            orderby = query.pop("orderby")
            config_plus["orderby"] = orderby

        # 文章列表
        art_list = self.service.Get_list(
            query,
            obj_update(self.config, config_plus),
        )

        # 获取点击量列表
        hot_list = self.service.Get_list(
            {},
            obj_update(
                self.config,
                {
                    "field": "article_id,description,hits,create_time,author,title,img,url",
                    "page": 1,
                    "size": 10,
                    "orderby": "hits desc",
                },
            ),
        )
        
        # 获取分类
        article_type = service_select("article_type").Get_list(
            {},
            obj_update(
                self.config,
                {
                    "page": 1,
                    "size": 5,
                },
            ),
        )
        # 放入模型中
        model = self.model(
            ctx, {"list": art_list, "hot_list": hot_list, "article_type": article_type}
        )
        return ctx.render(self.config["tpl"] + "list.html", model)

    #  展示页面
    def View(self, ctx):
        """
        列表页面
        @param {Object} ctx http请求上下文
        @return {Object} 返回html页面
        """
        query = dict(ctx.query)
        config_plus = {}
        if "field" in query:
            field = query.pop("field")
            config_plus["field"] = field

        # 文章列表
        obj = self.service.Get_obj(
            query,
            obj_update(self.config, config_plus),
        )

        # 获取点击量列表
        hot_list = self.service.Get_list(
            {},
            obj_update(
                self.config,
                {
                    "field": "article_id,description,hits,create_time,author,title,img,url",
                    "page": 1,
                    "size": 10,
                    "orderby": "hits desc",
                },
            ),
        )

        # 获取分类
        article_type = self.service.Get_list(
            {},
            obj_update(
                self.config,
                {
                    "page": 1,
                    "size": 5,
                },
            ),
        )

        # 获取上一条集合
        prev_list = self.service.Prev("article_id", obj["article_id"])
        prev = {}
        if len(prev_list):
            prev = prev_list[0]

        # 获取下一条集合
        next_list = self.service.Next("article_id", obj["article_id"])
        next_t = {}
        if len(next_list):
            next_t = next_list[0]

        # 放入模型中
        model = self.model(
            ctx,
            {
                "obj": obj,
                "hot_list": hot_list,
                "article_type": article_type,
                "prev": prev,
                "next": next_t,
            },
        )
        return ctx.render(self.config["tpl"] + "view.html", model)
