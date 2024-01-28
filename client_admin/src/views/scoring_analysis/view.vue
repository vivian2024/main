<template>
	<el-main class="bg edit_wrap">
		<el-form ref="form" :model="form" status-icon label-width="120px" v-if="is_view()">

							<el-col v-if="user_group === '管理员' || $check_field('get','film_title') || $check_field('add','film_title') || $check_field('set','film_title')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影名称" prop="film_title">
												<el-input id="film_title" v-model="form['film_title']" placeholder="请输入电影名称"
							  v-if="user_group === '管理员' || (form['scoring_analysis_id'] && $check_field('set','film_title')) || (!form['scoring_analysis_id'] && $check_field('add','film_title'))" :disabled="disabledObj['film_title_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_title')">{{form['film_title']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_year') || $check_field('add','film_year') || $check_field('set','film_year')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影年份" prop="film_year">
												<el-input id="film_year" v-model="form['film_year']" placeholder="请输入电影年份"
							  v-if="user_group === '管理员' || (form['scoring_analysis_id'] && $check_field('set','film_year')) || (!form['scoring_analysis_id'] && $check_field('add','film_year'))" :disabled="disabledObj['film_year_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_year')">{{form['film_year']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_rating') || $check_field('add','film_rating') || $check_field('set','film_rating')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影评分" prop="film_rating">
												<el-input id="film_rating" v-model="form['film_rating']" placeholder="请输入电影评分"
							  v-if="user_group === '管理员' || (form['scoring_analysis_id'] && $check_field('set','film_rating')) || (!form['scoring_analysis_id'] && $check_field('add','film_rating'))" :disabled="disabledObj['film_rating_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_rating')">{{form['film_rating']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','country') || $check_field('add','country') || $check_field('set','country')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="所属国家" prop="country">
												<el-input id="country" v-model="form['country']" placeholder="请输入所属国家"
							  v-if="user_group === '管理员' || (form['scoring_analysis_id'] && $check_field('set','country')) || (!form['scoring_analysis_id'] && $check_field('add','country'))" :disabled="disabledObj['country_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','country')">{{form['country']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_type') || $check_field('add','film_type') || $check_field('set','film_type')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影类型" prop="film_type">
												<el-input id="film_type" v-model="form['film_type']" placeholder="请输入电影类型"
							  v-if="user_group === '管理员' || (form['scoring_analysis_id'] && $check_field('set','film_type')) || (!form['scoring_analysis_id'] && $check_field('add','film_type'))" :disabled="disabledObj['film_type_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_type')">{{form['film_type']}}</div>
											</el-form-item>
			</el-col>
					
	
	
	
	
	
	
			<el-col :xs="24" :sm="12" :lg="8" class="el_form_btn_warp">
				<el-form-item>
					<el-button type="primary" @click="submit()">提交</el-button>
					<el-button @click="cancel()">取消</el-button>
				</el-form-item>
			</el-col>

		</el-form>
	</el-main>
</template>

<script>
	import mixin from "@/mixins/page.js";

	export default {
		mixins: [mixin],
		data() {
			return {
				field: "scoring_analysis_id",
				url_add: "~/api/scoring_analysis/add?",
				url_set: "~/api/scoring_analysis/set?",
				url_get_obj: "~/api/scoring_analysis/get_obj?",
				url_upload: "~/api/scoring_analysis/upload?",

				query: {
					"scoring_analysis_id": 0,
				},

				form: {
								"film_title":  '', // 电影名称
										"film_year":  '', // 电影年份
										"film_rating":  '', // 电影评分
										"country":  '', // 所属国家
										"film_type":  '', // 电影类型
											"scoring_analysis_id": 0, // ID
						
				},
				disabledObj:{
								"film_title_isDisabled": false,
										"film_year_isDisabled": false,
										"film_rating_isDisabled": false,
										"country_isDisabled": false,
										"film_type_isDisabled": false,
										},

	
		
		
		
		
	
			}
		},
		methods: {


	
	
			
	
			
	
			
	
			
	
		
			/**
			 * 获取对象之前
			 * @param {Object} param
			 */
			get_obj_before(param) {
				var form = "";
								// 获取缓存数据附加
				form = $.db.get("form");
							$.push(this.form ,form);
											
				if(this.form && form){
					Object.keys(this.form).forEach(key => {
						Object.keys(form).forEach(dbKey => {
							// if(dbKey === "charging_standard"){
							// 	this.form['charging_rules'] = form[dbKey];
							// 	this.disabledObj['charging_rules_isDisabled'] = true;
							// };
							if(key === dbKey){
								this.disabledObj[key+'_isDisabled'] = true;
							}
						})
					})
				}
														$.db.del("form");
				return param;
			},

			/**
			 * 获取对象之后
			 * @param {Object} json
			 * @param {Object} func
			 */
			get_obj_after(json, func){


															

			},

			/**
			 * 提交前验证事件
			 * @param {Object} 请求参数
			 * @return {String} 验证成功返回null, 失败返回错误提示
			 */
			submit_check(param) {
				let msg = null
																					return msg;
			},

			is_view(){
				var bl = this.user_group == "管理员";

				if(!bl){
					bl = this.$check_action('/scoring_analysis/table','add');
					console.log(bl ? "你有表格添加权限视作有添加权限" : "你没有表格添加权限");
				}
				if(!bl){
					bl = this.$check_action('/scoring_analysis/table','set');
					console.log(bl ? "你有表格添加权限视作有修改权限" : "你没有表格修改权限");
				}
				if(!bl){
					bl = this.$check_action('/scoring_analysis/view','add');
					console.log(bl ? "你有视图添加权限视作有添加权限" : "你没有视图添加权限");
				}
				if(!bl){
					bl = this.$check_action('/scoring_analysis/view','set');
					console.log(bl ? "你有视图修改权限视作有修改权限" : "你没有视图修改权限");
				}
				if(!bl){
					bl = this.$check_action('/scoring_analysis/view','get');
					console.log(bl ? "你有视图查询权限视作有查询权限" : "你没有视图查询权限");
				}

				console.log(bl ? "具有当前页面的查看权，请注意这不代表你有字段的查看权" : "无权查看当前页，请注意即便有字段查询权限没有页面查询权限也不行");

				return bl;
			},
			/**
			 * 上传文件
			 * @param {Object} param
			 */
			uploadimg(param) {
				this.uploadFile(param.file, "avatar");
			},

		},
		created() {
												},
	}
</script>

<style>
	.avatar-uploader .el-upload {
		border: 1px dashed #d9d9d9;
		border-radius: 6px;
		cursor: pointer;
		position: relative;
		overflow: hidden;
	}

	.avatar-uploader .el-upload:hover {
		border-color: #409EFF;
	}

	.avatar-uploader-icon {
		font-size: 28px;
		color: #8c939d;
		width: 178px;
		height: 178px;
		line-height: 178px;
		text-align: center;
	}

	.avatar {
		width: 178px;
		height: 178px;
		display: block;
	}




</style>
