<template>
	<div class="page_root" id="root_index">
		<div class="warp">
			<div class="container-fluid">
				<el-row>
					<el-col :span="4">
						<mm_label bg_color="bg_purple" icon="el-icon-user-solid" :url="url_user_count" unit="人"
								  title="用户数量"></mm_label>
					</el-col>
<!--					<el-col :span="4">-->
<!--						<mm_label bg_color="bg_green" icon="el-icon-view" :url="url_article_hits" unit="次"-->
<!--								  title="文章浏览量"></mm_label>-->
<!--					</el-col>-->
				</el-row>

				<el-row>
						<el-col v-if="user_group == '管理员' || $check_figure('/system_user/table')" :span="8">
						<div class="card chart">
																							<pieChart v-if="list_system_user.length" id="list_system_user" :list="list_system_user" :title="'系统用户统计'"></pieChart>
							<div v-if="!list_system_user.length">系统用户没有符合条件的数据</div>
															</div>
					</el-col>
							<el-col v-if="user_group == '管理员' || $check_figure('/film_information/table')" :span="8">
						<div class="card chart">
																							<pieChart v-if="list_film_information.length" id="list_film_information" :list="list_film_information" :title="'电影信息统计'"></pieChart>
							<div v-if="!list_film_information.length">电影信息没有符合条件的数据</div>
																																																																</div>
					</el-col>
							<el-col v-if="user_group == '管理员' || $check_figure('/scoring_analysis/table')" :span="8">
						<div class="card chart">
									<newBarChart v-if="bar_obj_scoring_analysis.values.length > 0" id="bar_obj_scoring_analysis" :vm="bar_obj_scoring_analysis" :title="'评分分析统计'">
							</newBarChart>
							<div v-if="!bar_obj_scoring_analysis.values.length">评分分析没有符合条件的数据</div>
								</div>
					</el-col>
							<el-col v-if="user_group == '管理员' || $check_figure('/regional_analysis/table')" :span="8">
						<div class="card chart">
																																					<pieChart v-if="list_regional_analysis.length" id="list_regional_analysis" :list="list_regional_analysis" :title="'地区分析统计'"></pieChart>
							<div v-if="!list_regional_analysis.length">地区分析没有符合条件的数据</div>
																						</div>
					</el-col>
					</el-row>


			</div>
		</div>
	</div>
</template>
<script>
	import mixin from "@/mixins/page.js";
	import pieChart from "@/components/charts/pie_chart";
	import barChart from "@/components/charts/bar_chart";
	import newBarChart from "@/components/charts/new_bar_chart";
	import lineChart from "@/components/charts/line_chart";
	import newLineChart from "@/components/charts/new_line_chart";
	import mm_label from "@/components/mm_label.vue";
	export default {
		mixins: [mixin],
		name: "Home",
		components: {
			pieChart,
			barChart,
			newBarChart,
			lineChart,
			newLineChart,
			mm_label
		},
		data() {
			return {
				activeName: "third",
					list_system_user: [],
						list_film_information: [],
						bar_obj_scoring_analysis: {
					names:[],
					xAxis: [],
					values:[]
				},
						list_regional_analysis: [],
					url_user_count: "~/api/user/count?",
				url_article_hits: "~/api/article/sum?field=hits",
			};
		},
		created() {
				// 执行系统用户数据获取
			this.get_list_system_user();
					// 执行电影信息数据获取
			this.get_list_film_information();
					// 执行评分分析数据获取
			this.get_list_scoring_analysis();
					// 执行地区分析数据获取
			this.get_list_regional_analysis();
			},
		mounted() {},
		methods: {
			async get_nickname(list,flag){
				if (flag) {
					for (let i=0;i<list.length;i++){
						await this.$get(
								"~/api/user/get_obj?user_id="+list[i],
								null,
								(json) => {
									if (json.result) {
										list[i] = json.result.obj.nickname;
									}
								});
					}
				}else {
					for (let i=0;i<list.length;i++){
						await this.$get(
								"~/api/user/get_obj?user_id="+list[i].name,
								null,
								(json) => {
									if (json.result) {
										list[i].name = json.result.obj.nickname;
									}
								});
					}
				}
			},
														// 获取系统用户统计图数据
			get_list_system_user() {
				let data = {};
								let flag = false;
												this.$get("~/api/system_user/list_group?groupby=user_gender", data, (json) => {
					if (json.result) {
						var list = json.result.list;
						this.list_system_user = list.map((o) => {
							return {
												name: o[1],
												value: o[0]
							};
						});
						if (flag){
							this.get_nickname(this.list_system_user,false);
						}
					}
				});
			},
																				// 获取电影信息统计图数据
			get_list_film_information() {
				let data = {};
								let flag = false;
												this.$get("~/api/film_information/list_group?groupby=film_year", data, (json) => {
					if (json.result) {
						var list = json.result.list;
						this.list_film_information = list.map((o) => {
							return {
												name: o[1],
												value: o[0]
							};
						});
						if (flag){
							this.get_nickname(this.list_film_information,false);
						}
					}
				});
			},
																																													// 获取评分分析统计柱状图
			async get_list_scoring_analysis() {
				let name_list = [];
				let query_str = "";
									let group_by_value = "film_title";
								let flag = false;
												let date_flag = "其他"
																														name_list.push("电影评分");
				query_str = query_str+"film_rating"+","
																									this.bar_obj_scoring_analysis.names = name_list
				query_str = query_str.substr(0,query_str.length-1);
				let data = {};
						await this.$get(
						"~/api/scoring_analysis/bar_group?field="+query_str+"&groupby="+group_by_value,
						data,
						(json) => {
							if (json.result) {
								let xAxis = [];
								let values = [];
								json.result.list.map((o) => {
									if (date_flag === "日期") {
										xAxis.push(this.$toTime(o[0] ,"yyyy-MM-dd"));
									}else if (date_flag === "时间") {
										xAxis.push(this.$toTime(o[0] ,"hh:mm:ss"));
									}else if (date_flag === "日长") {
										xAxis.push(this.$toTime(o[0] ,"yyyy-MM-dd hh:mm:ss"));
									}else {
										xAxis.push(o[0]);
									}
									values.push(o.splice(1))
								});
								this.bar_obj_scoring_analysis.xAxis = xAxis;
								this.bar_obj_scoring_analysis.values = values;
							}
							if (flag){
								this.get_nickname(this.bar_obj_scoring_analysis.xAxis,true);
							}
						});
			},
																									// 获取地区分析统计图数据
			get_list_regional_analysis() {
				let data = {};
								let flag = false;
												this.$get("~/api/regional_analysis/list_group?groupby=country", data, (json) => {
					if (json.result) {
						var list = json.result.list;
						this.list_regional_analysis = list.map((o) => {
							return {
												name: o[1],
												value: o[0]
							};
						});
						if (flag){
							this.get_nickname(this.list_regional_analysis,false);
						}
					}
				});
			},
											
		},
		computed:{
			recognitionHeight(){
				return "830px"
			},
			recognitionUrl(){
				return "https://www.faceplusplus.com.cn/${model.filter.recognitionType}/"
			}
		}
	};
</script>

<style scoped="scoped">
	.chart {
		display: block;
		width: 100%;
		height: 400px;
		padding: 1rem;
		position: relative;
	}

	.el-col {
		padding: 0.5rem;
	}

	.card {
		overflow: hidden;
	}

	.iframe_box ,.iframe_box_change{
		width: 100%;
		height: 1180px;
		position: relative;
		margin-top: 25px;
	}
	.iframe_box_change{
		height: 580px;
		padding-top: 50px;
	}
	.iframe_box	.iframe_box_content, .iframe_box_change .iframe_box_content{
		width: 100%;
		height: 100%;
	}
	.iframe_box_top{
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100px;
		font-size: 25px;
		line-height: 100px;
		background: #fff;
		z-index: 99999999;
		padding-left: 50px;
	}
	#iframe_box_face div::before {
		content: '';
		width: 100px;
		position: absolute;
		top: 154px;
		right: 129px;
		z-index: 999;
		height: 20px;
		background-color: #FFFFFF;
	}

	#iframe_box_face>h1 {
		margin-top: 100px;
		margin-bottom: 20px;
	}
</style>
