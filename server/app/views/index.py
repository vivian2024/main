from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")


# 帮助方法,合并对象
def obj_update(*config):
    config_temp = {}
    for o in config:
        config_temp.update(o)
    return config_temp


# 首页
class Index(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./user/",
            # 选择的服务
            "service": "article",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Index, self).__init__(config_temp)

    # 首页
    def Index(self, ctx):
        """首页
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

        # 文章列表
        result_list = self.service.Get_list(query, obj_update(self.config, config_plus))

        # 获取点击量列表
        list_article_hot = self.service.Get_list(
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

        # 获取点击量列表
        list_article_new = self.service.Get_list(
            {},
            obj_update(
                self.config,
                {
                    "field": "article_id,description,hits,create_time,author,title,img,url",
                    "page": 1,
                    "size": 10,
                    "orderby": "create_time desc",
                },
            ),
        )

        # 热门畅销
        list_goods_sales = service_select("goods").Get_list(
            {}, {"orderby": "`sales` desc"}
        )
        # 新品
        list_goods_new = service_select("goods").Get_list(
            {}, {"orderby": "`create_time` desc"}
        )
        # 广告
        list_ad = service_select("ad").Get_list({}, {"orderby": "`display` desc"})
        # 链接
        list_link = service_select("link").Get_list({}, {"orderby": "`display` desc"})
        model = self.model(
            ctx,
            {
                "list": result_list,
                "list_goods_sales": list_goods_sales,
                "list_goods_new": list_goods_new,
                "list_article_hot": list_article_hot,
                "list_article_new": list_article_new,
                "list_ad": list_ad,
                "list_link": list_link,
            },
        )
        result_dict = {"list": result_list}
        model = self.model(ctx, result_dict)
        return ctx.render(self.config["tpl"] + "index.html", model)
