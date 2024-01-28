<template>
	<el-main class="bg table_wrap">
		<el-form label-position="right" :model="query" class="form p_4" label-width="120">
			<el-row>


							<el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
					<el-form-item label="电影名称">
									<el-input v-model="query.film_title"></el-input>
								</el-form-item>
				</el-col>
																		<el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
					<el-form-item label="电影类型">
									<el-input v-model="query.film_type"></el-input>
								</el-form-item>
				</el-col>
																			<el-col :xs="24" :sm="10" :lg="8" class="search_btn_wrap_1">
					<el-form-item>
						<el-button type="primary" @click="search()" class="search_btn_find">查询</el-button>
						<el-button @click="reset()" style="margin-right: 74px;" class="search_btn_reset">重置</el-button>
						<router-link v-if="user_group == '管理员' || $check_action('/film_information/table','add') || $check_action('/film_information/view','add')" class="el-button el-button--default el-button--primary search_btn_add" to="./view?">添加
						</router-link>
            			<el-button v-if="user_group == '管理员' || $check_action('/film_information/table','del') || $check_action('/film_information/view','del')" class="search_btn_del" type="danger" @click="delInfo()">删除</el-button>
						<download-excel v-if="$check_option('/film_information/table','import_db')" class="export-excel-wrapper" :data="DetailsForm" :fields="json_fields" name="数据导入表格.xls" >
							<el-button type="success">下载导入文档</el-button>
						</download-excel>
						<el-upload v-if="$check_option('/film_information/table','import_db')" action accept = ".xlsx, .xls" :auto-upload="false" :show-file-list="false" :on-change="handle_import">
							<el-button type="primary">导入</el-button>
						</el-upload>
					</el-form-item>
				</el-col>

			</el-row>
		</el-form>
		<el-table :data="list" @selection-change="selectionChange" @sort-change="$sortChange" style="width: 100%" id="dataTable">
			<el-table-column fixed type="selection" tooltip-effect="dark" width="55">
			</el-table-column>
				<el-table-column prop="film_title" @sort-change="$sortChange" label="电影名称"
				v-if="user_group == '管理员' || $check_field('get','film_title')" min-width="200">
					</el-table-column>
					<el-table-column prop="film_year" @sort-change="$sortChange" label="电影年份"
				v-if="user_group == '管理员' || $check_field('get','film_year')" min-width="200">
					</el-table-column>
					<el-table-column prop="film_rating" @sort-change="$sortChange" label="电影评分"
				v-if="user_group == '管理员' || $check_field('get','film_rating')" min-width="200">
					</el-table-column>
					<el-table-column prop="country" @sort-change="$sortChange" label="所属国家"
				v-if="user_group == '管理员' || $check_field('get','country')" min-width="200">
					</el-table-column>
					<el-table-column prop="film_type" @sort-change="$sortChange" label="电影类型"
				v-if="user_group == '管理员' || $check_field('get','film_type')" min-width="200">
					</el-table-column>
					<el-table-column prop="film_director" @sort-change="$sortChange" label="电影导演"
				v-if="user_group == '管理员' || $check_field('get','film_director')" min-width="200">
					</el-table-column>
					<el-table-column prop="film_stars" @sort-change="$sortChange" label="电影主演"
				v-if="user_group == '管理员' || $check_field('get','film_stars')" min-width="200">
					</el-table-column>
					<el-table-column prop="movie_pictures" @sort-change="$sortChange" label="电影图片"
				v-if="user_group == '管理员' || $check_field('get','movie_pictures')" min-width="200">
						<template slot-scope="scope">
					<el-image style="width: 100px; height: 100px" :src="$fullUrl(scope.row['movie_pictures'])"
						:preview-src-list="[$fullUrl(scope.row['movie_pictures'])]">
						<div slot="error" class="image-slot">
							<img src="../../../public/img/error.png" style="width: 90px; height: 90px" />
						</div>
					</el-image>
				</template>
					</el-table-column>
					<el-table-column prop="film_introduction" @sort-change="$sortChange" label="电影简介"
				v-if="user_group == '管理员' || $check_field('get','film_introduction')" min-width="200">
					</el-table-column>
	



            <el-table-column sortable prop="create_time" label="创建时间" min-width="200">
                <template slot-scope="scope">
                	{{ $toTime(scope.row["create_time"],"yyyy-MM-dd hh:mm:ss") }}
                </template>
            </el-table-column>

			<el-table-column sortable prop="update_time" label="更新时间" min-width="200">
                <template slot-scope="scope">
                	{{ $toTime(scope.row["update_time"],"yyyy-MM-dd hh:mm:ss") }}
                </template>
			</el-table-column>







			<el-table-column fixed="right" label="操作" min-width="120" v-if="user_group == '管理员' || $check_action('/film_information/table','set') || $check_action('/film_information/view','set') || $check_action('/film_information/view','get') || $check_action('/评分分析|地区分析/table','add') || $check_action('/评分分析|地区分析/view','add')" >


				<template slot-scope="scope">
					<router-link class="el-button el-button--small is-plain el-button--success" style="margin: 5px !important;"
					v-if="user_group == '管理员' || $check_action('/film_information/table','set') || $check_action('/film_information/view','set') || $check_action('/film_information/view','get')"
						:to="'./view?' + field + '=' + scope.row[field]"
						 size="small">
						<span>详情</span>
					</router-link>
						<!--跨表按钮-->
							<el-button class="el-button el-button--small is-plain el-button--default" style="margin: 5px !important;" size="small" @click="to_table(scope.row,'/scoring_analysis/view')" v-if="user_group == '管理员' || $check_action('/scoring_analysis/table','add') || $check_action('/scoring_analysis/view','add')">
						<span>评分分析</span>
					</el-button>
							<el-button class="el-button el-button--small is-plain el-button--default" style="margin: 5px !important;" size="small" @click="to_table(scope.row,'/regional_analysis/view')" v-if="user_group == '管理员' || $check_action('/regional_analysis/table','add') || $check_action('/regional_analysis/view','add')">
						<span>地区分析</span>
					</el-button>
									<router-link v-if="user_group == '管理员' || $check_comment('/film_information/table')" class="el-button el-button--small is-plain el-button--primary"
								  :to="'../comment/table?size=10&page=1&source_table=film_information&source_field=' + field + '&source_id=' + scope.row[field]" size="small">
					查看评论
					</router-link>
					</template>
			</el-table-column>

		</el-table>

		<!-- 分页器 -->
		<div class="mt text_center">
			<el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
				:current-page="query.page" :page-sizes="[7, 10, 30, 100]" :page-size="query.size"
				layout="total, sizes, prev, pager, next, jumper" :total="count">
			</el-pagination>
		</div>
		<!-- /分页器 -->

									
		<div class="modal_wrap" v-if="showModal">
			<div class="modal_box">
				<!-- <div class="modal_box_close" @click="closeModal">X</div> -->
				<p class="modal_box_title">重要提醒</p>
				<p class="modal_box_text">当前有数据达到预警值！</p>
				<div class="btn_box">
					<span @click="closeModal">取消</span>
					<span @click="closeModal">确定</span>
				</div>
			</div>
		</div>


	</el-main>
</template>
<script>
	import mixin from "@/mixins/page.js";
	import * as XLSX from 'xlsx/xlsx.mjs'

	export default {
		mixins: [mixin],
		data() {
			return {
				// 弹框
				showModal: false,
				// 获取数据地址
				url_get_list: "~/api/film_information/get_list?like=0",
				url_del: "~/api/film_information/del?",

				// 字段ID
				field: "film_information_id",

				// 查询
				query: {
					"size": 7,
					"page": 1,
								"film_title": "",
														"film_type": "",
												"login_time": "",
					"create_time": "",
					"orderby": `create_time desc`
				},

				// 数据
				list: [],
				json_fields: {
							"电影名称":'film_title',
						"电影年份":'film_year',
						"电影评分":'film_rating',
						"所属国家":'country',
						"电影类型":'film_type',
						"电影导演":'film_director',
						"电影主演":'film_stars',
						"电影图片":'movie_pictures',
						"电影简介":'film_introduction',
					},
				DetailsForm: [
					{
								film_title:"文本类型",
							film_year:"文本类型",
							film_rating:"文本类型",
							country:"文本类型",
							film_type:"文本类型",
							film_director:"文本类型",
							film_stars:"文本类型",
							movie_pictures:"图片类型",
							film_introduction:"多文本类型",
						},
				],
																														}
		},
		methods: {
			// 关闭弹框
			closeModal(){
				this.showModal = false;
				},


																		
			open_tip() {
				const h = this.$createElement;

				var message = "";
				var list = this.list;

				var ifs = [
													];
				for (var n = 0; n < ifs.length; n++) {
					var o = ifs[n];
					for (var i = 0; i < list.length; i++) {
						var lt = list[i];
						if (o.type == "数内") {
							if ((o.start || o.start === 0) && (o.end || o.end === 0)) {
								if (lt[o.factor] > o.start && lt[o.factor] < o.end) {
									o["idx"] = o["idx"] + 1;
								}
							} else if (o.start || o.start === 0) {
								if (lt[o.factor] > o.start) {
									o["idx"] = o["idx"] + 1;
								}
							} else if (o.end || o.end === 0) {
								if (lt[o.factor] < o.end) {
									o["idx"] = o["idx"] + 1;
								}
							}
						} else if (o.type == "数外") {
							if ((o.start || o.start === 0) && (o.end || o.end === 0)) {
								if (lt[o.factor] < o.start || lt[o.factor] > o.end) {
									o["idx"] = o["idx"] + 1;
								}
							} else if (o.start || o.start === 0) {
								if (lt[o.factor] < o.start) {
									o["idx"] = o["idx"] + 1;
								}
							} else if (o.end || o.end === 0) {
								if (lt[o.factor] > o.end) {
									o["idx"] = o["idx"] + 1;
								}
							}
						} else if (o.type == "日内") {
							if ((o.start) && (o.end)) {
								if (lt[o.factor] > o.start && lt[o.factor] < o.end) {
									o["idx"] = o["idx"] + 1;
								}
							} else if (o.start) {
								if (lt[o.factor] < o.start) {
									o["idx"] = o["idx"] + 1;
								}
							} else if (o.end) {
								if (lt[o.factor] > o.end) {
									o["idx"] = o["idx"] + 1;
								}
							}
						} else if (o.type == "日外") {
							if (o.start && o.end) {
								if (lt[o.factor] < o.start || lt[o.factor] > o.end) {
									o["idx"] = o["idx"] + 1;
								}
							} else if (o.start) {
								if (lt[o.factor] < o.start) {
									o["idx"] = o["idx"] + 1;
								}
							} else if (o.end) {
								if (lt[o.factor] > o.end) {
									o["idx"] = o["idx"] + 1;
								}
							}
						}
					}

					if (o["idx"]) {
						message += o.title;
						if (o["type"] == "数内") {
							if (o.start || o.start === 0) {
								message += "大于" + o.start;
							}
							if ((o.start || o.start === 0) && (o.end || o.end === 0)) {
								message += "并且";
							}
							if (o.end || o.end === 0) {
								message += "小于" + o.end;
							}
						} else if (o["type"] == "数外") {
							if (o.start || o.start === 0) {
								message += "小于" + o.start;
							}
							if ((o.start || o.start === 0) || (o.end || o.end === 0)) {
								message += "或者";
							}
							if (o.end || o.end === 0) {
								message += "大于" + o.end;
							}
						} else if (o["type"] == "日内") {
							if (o.start) {
								message += "在" + o.start + "之后";
							}
							if (o.start && o.end) {
								message += "并且";
							}
							if (o.end) {
								message += "在" + o.end + "之前";
							}
						} else if (o["type"] == "日外") {
							if (o.start) {
								message += "在" + o.start + "之前";
							}
							if (o.start || o.end) {
								message += "或者";
							}
							if (o.end) {
								message += "在" + o.end + "之后";
							}
						}
						message += "的有" + o["idx"] + "条";
					}
				}

				if (message) {
					message += "，需要处理、请尽快处理。";
					this.showModal = true;
					// this.$notify({
					// 	title: '提醒',
					// 	dangerouslyUseHTMLString: true,
					// 	message: h('i', {
					// 		style: 'color: teal'
					// 	}, message)
					// });
				}
			},



	/**
	 * 导入
	 */
	readFile(file){//文件读取
		return new Promise(resolve => {
			let reader = new FileReader();
			reader.readAsBinaryString(file);//以二进制的方式读取
			reader.onload = ev =>{
				resolve(ev.target.result);
			}
		})
	},
	async handle_import(ev){
		let file = ev.raw;
		console.log(file)
		if(!file){
			console.log("文件打开失败")
			return ;
		}else{
			let data = await this.readFile(file);
			let workbook = XLSX.read(data,{ type: "binary"});//解析二进制格式数据
			let worksheet = workbook.Sheets[workbook.SheetNames[0]];//获取第一个Sheet
			let result = XLSX.utils.sheet_to_json(worksheet);//json数据格式
			result.forEach((item) => {
				// 将中文的键名替换成英文的
				for (let k in this.json_fields) {
					let newKey = this.json_fields[k];
					if (newKey) {
						item[newKey] = item[k];
						delete item[k];
					}
				}
			});
			let _this = this;
				for (let i=0;i<result.length;i++){
				let url = "~/api/film_information/add?";
				await this.$post(url, result[i], function (json, status) {
					console.log("提交结果：", json);
					if (json.result) {
						_this.$toast("操作成功", 'success');
					} else if (json.error) {
						_this.$toast(json.error.message, 'danger');
					}
				});
			}
			}
	},

																					deleteRow(index, rows) {
				rows.splice(index, 1);
			}

		},
		created() {
																					setTimeout(() => {
				this.open_tip();
			}, 1000)
		}
	}
</script>

<style type="text/css">
	.bg {
		background: white;
	}

	.form.p_4 {
		padding: 1rem;
	}

	.form .el-input {
		width: initial;
	}

	.mt {
		margin-top: 1rem;
	}

	.text_center {
		text-align: center;
	}

	.float-right {
		float: right;
	}


	.modal_wrap{
		width: 100vw;
		height: 100vh;
		position: fixed;
		top: 0;
		left: 0;
		background: rgba(0,0,0,0.5);
		z-index: 9999999999;
	}
	.modal_wrap .modal_box{
		width: 400px;
		height: 200px;
		background: url("../../assets/modal_bg.jpg") no-repeat center;
		background-size: cover;
		position: absolute;
		top: 50%;
		left: 50%;
		margin-left: -200px;
		margin-top: -100px;
		border-radius: 10px;
		}
	.modal_wrap .modal_box .modal_box_close{
		font-size: 20px;
		position: absolute;
		top: 10px;
		right: 10px;
		cursor: pointer;
		}
	.modal_wrap .modal_box .modal_box_title{
	  text-align: center;
    font-size: 18px;
    margin: 16px auto;
    color: #fff;
    border-bottom: 1px solid rgba(117, 116, 116,0.5);
    padding-bottom: 16px;
    width: 356px;
		}
	.modal_wrap .modal_box .modal_box_text{
			text-align: center;
		font-size: 15px;
		color: #fff;
		margin-top: 25px;
		}
	.modal_wrap .modal_box .btn_box{
		display: flex;
		flex-direction: row;
		justify-content: center;
		margin-top: 42px;
		}
			.modal_wrap .modal_box .btn_box span{
				display: inline-block;
				width: 80px;
				height: 30px;
				line-height: 30px;
				text-align: center;
				border: 1px solid #ccc;
				font-size: 14px;
				cursor: pointer;
				color: #fff;
			}
	.modal_wrap .modal_box .btn_box span:nth-child(2){
		background: #409EFF;
		color: #fff;
		border-color: #409EFF;
		margin-left: 15px;
	}
</style>
