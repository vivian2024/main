from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")


# 管理后台
class Admin(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./admin/",
            # 选择的服务
            "service": "admin",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Admin, self).__init__(config_temp)

    # 用户数，访问次数，营业额，消费人数统计，销售量，订单数
    def Index(self, ctx):
        # 分类文章数
        article_type_num = service_select("article").Count_group(
            {}, {"groupby": "type"}
        )
        # 最近7日注册用户
        register_7day = service_select("user").date_comput(
            {}, {"date_key": "create_time", "size": 7}
        )
        # 最近7日订单量
        order_7day = service_select("user").date_comput(
            {}, {"date_key": "create_time", "size": 7}
        )
        # 最近7日营业额
        revenue_7day = service_select("user").date_comput(
            {},
            {
                "date_key": "create_time",
                "method": "sum",
                "field": "price_count",
                "size": 7,
            },
        )
        # 最近7日总销量
        sales_7day = service_select("user").date_comput(
            {},
            {
                "date_key": "create_time",
                "method": "sum",
                "field": "price_count",
                "size": 7,
            },
        )
        # 商品分类销量
        goods_type_sales = service_select("goods").Sum_group(
            {}, {"groupby": "type", "field": "sales"}
        )

        model = {
            "result": {
                "article_type_num": article_type_num,
                "register_7day": register_7day,
                "order_7day": order_7day,
                "revenue_7day": revenue_7day,
                "sales_7day": sales_7day,
                "goods_type_sales": goods_type_sales,
            }
        }
        return ctx.render(self.config["tpl"] + "index" + ".html", model)
