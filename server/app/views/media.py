from app.core import controller

controllerClass = getattr(controller, "Controller")


# 媒体
class Media(controllerClass):
    def __init__(self, config={}):
        """
        构造函数
        @param {Object} config 配置参数
        """
        config_init = {
            # 选择的模板那路径模板
            "tpl": "./media/",
            # 选择的服务
            "service": "upload",
            "get": ["video", "image", "audio"],
        }
        config_temp = config
        config_temp.update(config_init)
        super(Media, self).__init__(config_temp)

    def Video(self, ctx):
        """
        视频预览
        @param {Object} ctx http上下文
        """
        model = self.model(ctx, {})
        return ctx.render(self.config["tpl"] + "video.html", model)

    def Image(self, ctx):
        """
        图片预览
        @param {Object} ctx http上下文
        """
        model = self.model(ctx, {})
        return ctx.render(self.config["tpl"] + "image.html", model)

    def Audio(self, ctx):
        """
        音频预览
        @param {Object} ctx http上下文
        """
        model = self.model(ctx, {})
        return ctx.render(self.config["tpl"] + "audio.html", model)
