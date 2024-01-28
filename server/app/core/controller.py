from app.service import service_select
from app.core.mysql import MysqlPool
import json
import csv
import ast
import os

mysqlPool = MysqlPool()


# 帮助方法,合并对象
def obj_update(*config):
	config_temp = {}
	for o in config:
		config_temp.update(o)
	return config_temp


# 权限集合
dict_auth = {}


# 控制器父类
class Controller:
	def __init__(self, config):
		"""
		构造函数
		@param {Dictionary} config 配置参数
		"""
		# 配置参数
		self.config = config or {}
		# 添加服务
		self.service = service_select(self.config["service"])
		cg = {
			# 选择的模板那路径模板
			"tpl":
			"./index/",
			# 选择的服务
			"service":
			"user",
			# 注册get请求路由
			"get": ["list", "view", "table"],
			# 注册post请求路由
			"post": [],
			# 注册get api路由
			"get_api": [
				"del",
				"get_list",
				"get_obj",
				"count",
				"count_group",
				"sum",
				"sum_group",
				"avg",
				"avg_group",
				"list_group",
				"bar_group",
				"get_hits_list",
				"get_business_order_list"
			],
			# 注册post api路由
			"post_api": ["add", "del", "set", "import_db", "export_db", "upload"],
			"interact": [],
			"unique": []
		}
		if config:
			if "interact" in config:
				config["interact"].extend(cg["interact"])
			else:
				config["interact"] = cg["interact"]
			if "get" in config:
				config["get"].extend(cg["get"])
			else:
				config["get"] = cg["get"]
			if "post" in config:
				config["post"].extend(cg["post"])
			else:
				config["post"] = cg["post"]
			if "get_api" in config:
				config["get_api"].extend(cg["get_api"])
			else:
				config["get_api"] = cg["get_api"]
			if "post_api" in config:
				config["post_api"].extend(cg["post_api"])
			else:
				config["post_api"] = cg["post_api"]
			if "unique" in config:
				config["unique"].extend(cg["unique"])
			else:
				config["unique"] = cg["unique"]

	# 公共模型,用于在render（）为传递模板数据补充
	def model(self, ctx, model):
		m = {}
		m.update(model)
		#
		# model_temp.user = ctx.session.user

		# 获取导航
		service = service_select("nav")
		m["nav_top"] = service.Get_list({"location": "top"})
		m["nav_side"] = service.Get_list({"location": "side"})
		m["nav_foot"] = service.Get_list({"location": "foot"})

		# 获取轮播图
		service = service_select("slides")
		m["list_slides"] = service.Get_list({})

		# 获取公告
		service = service_select("notice")
		m["list_notice"] = service.Get_list({},
											{"orderby": "`update_time` desc"})

		# 交互模型接口
		if ("interact" in self.config) and self.config["interact"]:
			m = self.model_interact(ctx, m)

		m["query"] = ctx.query
		m["body"] = ctx.body
		m["auth"] = ctx.auth

		return m

	# 交互对象
	def interact_obj(self, ctx, o):
		interact = self.config["interact"]
		if interact:
			source_table = service_select(
				self.config["service"]).config["table"]
			source_field = source_table + "_id"
			# 评论
			if "comment" in interact:
				service = service_select("comment")
				source_id = o[source_field]
				o["comment_list"] = service.Get_list(
					{
						"source_table": source_table,
						"source_field": source_field,
						"source_id": source_id
					}, {
						"page": 1,
						"size": 10,
					})
				o["comment_len"] = service.Count({
					"source_table": source_table,
					"source_field": source_field,
					"source_id": source_id,
				})
			# 评分
			if "score" in interact:
				service = service_select("score")
				source_id = o[source_field]
				o["score_list"] = service.Get_list(
					{
						"source_table": source_table,
						"source_field": source_field,
						"source_id": source_id
					}, {
						"page": 1,
						"size": 10,
					})
				o["score_len"] = service.Avg(
					{
						"source_table": source_table,
						"source_field": source_field,
						"source_id": source_id,
					},
					{"field": "score_num"},
				)
			# 收藏
			if "collect" in interact:
				service = service_select("collect")
				source_id = o[source_field]
				o["collect_list"] = service.Get_list(
					{
						"source_table": source_table,
						"source_field": source_field,
						"source_id": source_id
					}, {
						"page": 1,
						"size": 10,
					})
				o["collect_len"] = service.Count({
					"source_table": source_table,
					"source_field": source_field,
					"source_id": source_id,
				})
			# 点赞
			if "praise" in interact:
				service = service_select("praise")
				source_id = o[source_field]
				o["praise_list"] = service.Get_list(
					{
						"source_table": source_table,
						"source_field": source_field,
						"source_id": source_id,
					}, {
						"page": 1,
						"size": 10,
					})
				o["praise_len"] = service.Count({
					"source_table": source_table,
					"source_field": source_field,
					"source_id": source_id,
				})
			return o

	# 交互列表
	def interact_list(self, ctx, list_1):
		interact = self.config["interact"]
		if interact:
			source_table = service_select(
				self.config["service"]).config["table"]
			source_field = source_table + "_id"

			# 评论数
			if "comment" in interact:
				service = service_select("comment")
				for o in list_1:
					source_id = o[source_field]
					o["comment_len"] = service.Count({
						"source_table": source_table,
						"source_field": source_field,
						"source_id": source_id,
					})
			# 平均分
			if "score" in interact:
				service = service_select("score")
				for o in list_1:
					source_id = o[source_field]
					o["score_len"] = service.Avg(
						{
							"source_table": source_table,
							"source_field": source_field,
							"source_id": source_id,
						},
						{"field": "score_num"},
					)

			# 收藏人数
			if "collect" in interact:
				service = service_select("collect")
				for o in list_1:
					source_id = o[source_field]
					o["collect_len"] = service.Count({
						"source_table": source_table,
						"source_field": source_field,
						"source_id": source_id,
					})

			# 点赞人数
			if "praise" in interact:
				service = service_select("praise")
				for o in list_1:
					source_id = o[source_field]
					o["praise_len"] = service.Count({
						"source_table": source_table,
						"source_field": source_field,
						"source_id": source_id,
					})

	# 交互模型
	def model_interact(self, ctx, m):
		if ("list" in m) and m["list"]:
			self.interact_list(ctx, m["list"])
		elif ("obj" in m) and m["obj"]:
			self.interact_obj(ctx, m["obj"])
		return m

	"""
	公共参数校验
	"""

	def Check_param(self, ctx):
		return True

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

		result_list = self.service.Get_list(
			query, obj_update(self.config, config_plus))
		result_dict = {"list": result_list}
		model = self.model(ctx, result_dict)
		return ctx.render(self.config["tpl"] + "index" + ".html", model)

	def Api(self, ctx):
		return {"demo": "hello world!"}

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

		result_list = self.service.Get_list(
			query, obj_update(self.config, config_plus))
		result_dict = {"list": result_list}
		model = self.model(ctx, result_dict)
		return ctx.render(self.config["tpl"] + "list" + ".html", model)

	# 表格页面
	def Table(self, ctx):
		"""
		表格页面
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

		result_list = self.service.Get_list(
			query, obj_update(self.config, config_plus))
		result_dict = {"list": result_list}
		model = self.model(ctx, result_dict)
		return ctx.render(self.config["tpl"] + "table" + ".html", model)

	# 详情页面
	def View(self, ctx):
		"""
		详情页面
		@param {Object} ctx http请求上下文
		@return {Object} 返回html页面
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field

		obj_result = self.service.Get_obj(query,
										  obj_update(self.config, config_plus))
		obj_dict = {"obj": obj_result}
		model = self.model(ctx, obj_dict)
		return ctx.render(self.config["tpl"] + "view" + ".html", model)

	# 编辑页面
	def Edit(self, ctx):
		"""
		编辑页面
		@param {Object} ctx http请求上下文
		@return {Object} 返回html页面
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field

		obj_result = self.service.Get_obj(query,
										  obj_update(self.config, config_plus))
		obj_dict = {"obj": obj_result}
		model = self.model(ctx, obj_dict)
		return ctx.render(self.config["tpl"] + "edit" + ".html", model)

	# 增
	def Add(self, ctx):
		"""
		增
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		body = ctx.body
		unique = self.config.get("unique")
		obj = None
		if unique:
			qy = {}
			for i in range(len(unique)):
				key = unique[i]
				qy[key] = body.get(key)
			obj = self.service.Get_obj(qy)

		if not obj:
			# 添加数据前
			error = self.Add_before(ctx)
			if error["code"]:
				return {"error": error}
			error = self.Events("add_before", ctx, None)
			if error["code"]:
				return {"error": error}

			# 添加数据
			result = self.service.Add(body, self.config)
			# 添加数据发生错误
			if self.service.error:
				return {"error": self.service.error}
			
			# 添加数据成功后
			res = self.Add_after(ctx, result)
			if res:
				result = res
			res = self.Events("add_after", ctx, result)
			if res:
				result = res
			return {"result": result}
		else:
			return {"error": {"code": 10000, "message": "已存在"}}

	# 删
	def Del(self, ctx):
		"""
		删
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		if len(ctx.query) == 0:
			errorMsg = {"code": 30000, "message": "删除条件不能为空！"}
			return errorMsg
		result = self.service.Del(ctx.query, self.config)
		if self.service.error:
			return {"error": self.service.error}
		return {"result": result}

	# 改
	def Set(self, ctx):
		"""
		改
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		# 修改数据前
		error = self.Set_before(ctx)
		if error["code"]:
			return {"error": error}
		error = self.Events("set_before", ctx, None)
		if error["code"]:
			return {"error": error}
		query = ctx.query
		if 'page' in query.keys():
			del ctx.query['page']
		if 'size' in query.keys():
			del ctx.query['size']
		if 'orderby' in query.keys():
			del ctx.query['orderby']
		# 修改数据
		result = self.service.Set(ctx.query, ctx.body, self.config)
		
		# 修改数据发生错误
		if self.service.error:
			return {"error": self.service.error}
		
		# 修改数据成功后
		res = self.Set_after(ctx, result)
		if res:
			result = res
		res = self.Events("set_after", ctx, result)
		if res:
			result = res
		return {"result": result}

	# 查多条
	def Get_list(self, ctx):
		"""
		查多条
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field
		if "page" in query:
			config_plus["page"] = query.pop("page")
		if "size" in query:
			config_plus["size"] = query.pop("size")
		if "orderby" in query:
			config_plus["orderby"] = query.pop("orderby")
		if "like" in query:
			config_plus["like"] = query.pop("like")
		if "groupby" in query:
			config_plus["groupby"] = query.pop("groupby")
		count = self.service.Count(query)
		lst = []
		if self.service.error:
			return {"error": self.service.error}
		elif count:
			lst = self.service.Get_list(query,
										obj_update(self.config, config_plus))
			if self.service.error:
				return {"error": self.service.error}
			self.interact_list(ctx, lst)
		return {"result": {"list": lst, "count": count}}

	# 查一条
	def Get_obj(self, ctx):
		"""
		查一条
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field

		obj = self.service.Get_obj(query, obj_update(self.config, config_plus))
		if self.service.error:
			return {"error": self.service.error}
		if obj:
			self.interact_obj(ctx, obj)
		return {"result": {"obj": obj}}

	# 饼图统计
	def List_group(self, ctx):
		"""
		饼图统计
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}
		
		if "groupby" in query:
			groupby_t = query.pop("groupby")
			config_plus["groupby"] = groupby_t
		else:
			err = {"error": 30000, "message": "groupby的值不能为空！"}
			return err
		
		lt = self.service.Count_group(query,obj_update(self.config, config_plus))
		for o in lt:
			o[1] = o[groupby_t]
			o[0] = o["count"]
		if self.service.error:
			return {"error": self.service.error}
		return {"result": { "list": lt }}

	# 柱状图统计
	def Bar_group(self, ctx):
		"""
		柱状图统计
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field
		else:
			err = {"error": 30000, "message": "field的值不能为空！"}
			return err
		if "groupby" in query:
			groupby_t = query.pop("groupby")
			config_plus["groupby"] = groupby_t
		else:
			err = {"error": 30000, "message": "groupby的值不能为空！"}
			return err
		
		lt = self.service.Bar_group(query,obj_update(self.config, config_plus))
		for k,v in enumerate(lt):
			new = list(v.values())
			lt[k] = new
			
		if self.service.error:
			return {"error": self.service.error}
		return {"result": { "list": lt }}
		
	# 总数
	def Count(self, ctx):
		"""
		总数
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		result = self.service.Count(ctx.query, self.config)
		if self.service.error:
			return {"error": self.service.error}

		return {"result": result}

	# 分组总计条数
	def Count_group(self, ctx):
		"""
		分组总计条数
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}

		if "groupby" in query:
			groupby_t = query.pop("groupby")
			config_plus["groupby"] = groupby_t
		else:
			err = {"error": 30000, "message": "groupby的值不能为空！"}
			return err

		lt = self.service.Count_group(query,
										  obj_update(self.config, config_plus))
		if self.service.error:
			return {"error": self.service.error}
		return {"result": { "list": lt }}

	# 合计
	def Sum(self, ctx):
		"""
		合计
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field
		else:
			err = {"error": 30000, "message": "field的值不能为空！"}
			return err

		result = self.service.Sum(query, obj_update(self.config, config_plus))
		if self.service.error:
			return {"error": self.service.error}
		return {"result": result}

	# 分组求和
	def Sum_group(self, ctx):
		"""
		分组求和
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field
		else:
			err = {"error": 30000, "message": "field的值不能为空！"}
			return err
		if "groupby" in query:
			groupby_t = query.pop("groupby")
			config_plus["groupby"] = groupby_t
		else:
			err = {"error": 30000, "message": "groupby的值不能为空！"}
			return err

		lt = self.service.Sum_group(query,
										obj_update(self.config, config_plus))
		if self.service.error:
			return {"error": self.service.error}
		return {"result": { "list": lt }}

	# 求平均数
	def Avg(self, ctx):
		"""
		求平均数
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field
		else:
			err = {"error": 30000, "message": "field的值不能为空！"}
			return err

		result = self.service.Avg(query, obj_update(self.config, config_plus))
		if self.service.error:
			return {"error": self.service.error}
		return {"result": result}

	# 分组平均数
	def Avg_group(self, ctx):
		"""
		分组平均数
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		query = dict(ctx.query)
		config_plus = {}
		if "field" in query:
			field = query.pop("field")
			config_plus["field"] = field
		else:
			err = {"error": 30000, "message": "field的值不能为空！"}
			return err
		if "groupby" in query:
			groupby_t = query.pop("groupby")
			config_plus["groupby"] = groupby_t
		else:
			err = {"error": 30000, "message": "groupby的值不能为空！"}
			return err

		lt = self.service.Avg_group(query,
										obj_update(self.config, config_plus))
		if self.service.error:
			return {"error": self.service.error}
		return {"result": { "list": lt }}

	# 导入数据
	def Import_db(self, ctx):
		"""
		导入数据
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		body = {"error": {"code": 10000, "message": "未定义表名！"}}
		return body

	# 导出数据
	def Export_db(self, ctx):
		"""
		导出数据
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		message = {
			"id": 1,
			"jsonrpc": "2.0",
		}
		query = ctx.query
		# 获取表名
		table = self.config["service"]
		path = ""
		if "path" in query:
			path = query.pop("path")
		if "name" in query:
			name = query.pop("name")
		# 通过服务获得数据
		service = service_select(table)
		lst = service.Export_db(query)
		# 1.创建文件对象
		f = open(str(path) + str(name) + ".csv",
				 "w",
				 newline="",
				 encoding="utf-8")
		# 2.基于文件对象构建 csv写入对象
		csv_writer = csv.writer(f)
		for row in lst:
			csv_writer.writerow(row)
		return message

	# 上传
	def Upload(self, ctx):
		"""
		上传
		@param {Object} ctx http请求上下文
		@return {Object} 返回json-rpc格式结果
		"""
		file_obj = ctx.request.FILES.get("file", None)
		if file_obj is None:
			error = {"code": 10000, "message": "上传的文件(file)不能为空"}
			return error
		try:
			file_obj = ctx.request.FILES.get("file", None)
			u = "/static/upload/" + file_obj.name
			fe = os.getcwd() + u
			with open(fe, "wb") as f:
				for line in file_obj.chunks():
					f.write(line)
			f.close()
		except (Exception):
			print("上传失败：", Exception)
		else:
			return {"result": {"url": u}}

	# 鉴权
	def Auth(self, ctx):
		if len(dict_auth.keys()) == 0:
			service = service_select("auth")
			lst = service.Get_list({}, {"page": 0})
			for o in lst:
				if "option" in o:
					o["option"] = ast.literal_eval(o["option"])
				else:
					o["option"] = {}
				path = o["path"]
				if not dict_auth[path]:
					dict_auth[path] = {}
				dict_auth[path][o["user_group"]] = o
		return dict_auth

	# 添加前
	def Add_before(self, ctx):
		# print("添加", ctx)
		return { "code": 0 }
	
	# 添加后
	def Add_after(self, ctx, result):
		# print("结果", ctx)
		return result

	# 修改前
	def Set_before(self, ctx):
		# print("修改前", ctx)
		return { "code": 0 }
	#分类推荐
	def Get_hits_list(self, ctx):
		return { "code": 0 }
	# 商家查询
	def Get_business_order_list(self, ctx):
		return {"code": 0}
	# 修改前
	def Set_after(self, ctx, result):
		return result

	# 事件
	def Events(self, event_name, param, paramB):
		if event_name == "add_before":
			return { "code": 0 }
		elif event_name == "del_before":
			return { "code": 0 }
		elif event_name == "set_before":
			return { "code": 0 }
		elif event_name == "get_obj_before":
			return { "code": 0 }
		elif event_name == "get_list_before":
			return { "code": 0 }
		elif event_name == "add_after":
			return paramB
		elif event_name == "del_after":
			return paramB
		elif event_name == "set_after":
			return paramB
		elif event_name == "get_obj_after":
			return paramB
		elif event_name == "get_list_after":
			return paramB
		else:
			return paramB
