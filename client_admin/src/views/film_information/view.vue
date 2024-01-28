<template>
	<el-main class="bg edit_wrap">
		<el-form ref="form" :model="form" status-icon label-width="120px" v-if="is_view()">

							<el-col v-if="user_group === '管理员' || $check_field('get','film_title') || $check_field('add','film_title') || $check_field('set','film_title')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影名称" prop="film_title">
												<el-input id="film_title" v-model="form['film_title']" placeholder="请输入电影名称"
							  v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','film_title')) || (!form['film_information_id'] && $check_field('add','film_title'))" :disabled="disabledObj['film_title_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_title')">{{form['film_title']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_year') || $check_field('add','film_year') || $check_field('set','film_year')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影年份" prop="film_year">
												<el-input id="film_year" v-model="form['film_year']" placeholder="请输入电影年份"
							  v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','film_year')) || (!form['film_information_id'] && $check_field('add','film_year'))" :disabled="disabledObj['film_year_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_year')">{{form['film_year']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_rating') || $check_field('add','film_rating') || $check_field('set','film_rating')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影评分" prop="film_rating">
												<el-input id="film_rating" v-model="form['film_rating']" placeholder="请输入电影评分"
							  v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','film_rating')) || (!form['film_information_id'] && $check_field('add','film_rating'))" :disabled="disabledObj['film_rating_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_rating')">{{form['film_rating']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','country') || $check_field('add','country') || $check_field('set','country')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="所属国家" prop="country">
												<el-input id="country" v-model="form['country']" placeholder="请输入所属国家"
							  v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','country')) || (!form['film_information_id'] && $check_field('add','country'))" :disabled="disabledObj['country_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','country')">{{form['country']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_type') || $check_field('add','film_type') || $check_field('set','film_type')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影类型" prop="film_type">
												<el-input id="film_type" v-model="form['film_type']" placeholder="请输入电影类型"
							  v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','film_type')) || (!form['film_information_id'] && $check_field('add','film_type'))" :disabled="disabledObj['film_type_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_type')">{{form['film_type']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_director') || $check_field('add','film_director') || $check_field('set','film_director')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影导演" prop="film_director">
												<el-input id="film_director" v-model="form['film_director']" placeholder="请输入电影导演"
							  v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','film_director')) || (!form['film_information_id'] && $check_field('add','film_director'))" :disabled="disabledObj['film_director_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_director')">{{form['film_director']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_stars') || $check_field('add','film_stars') || $check_field('set','film_stars')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影主演" prop="film_stars">
												<el-input id="film_stars" v-model="form['film_stars']" placeholder="请输入电影主演"
							  v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','film_stars')) || (!form['film_information_id'] && $check_field('add','film_stars'))" :disabled="disabledObj['film_stars_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_stars')">{{form['film_stars']}}</div>
											</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','movie_pictures') || $check_field('add','movie_pictures') || $check_field('set','movie_pictures')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影图片" prop="movie_pictures">
								<el-upload :disabled="disabledObj['movie_pictures_isDisabled']" id="movie_pictures" class="avatar-uploader" drag
						accept="image/gif, image/jpeg, image/png, image/jpg" action="" :http-request="upload_movie_pictures"
						:show-file-list="false" v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','movie_pictures')) || (!form['film_information_id'] && $check_field('add','movie_pictures'))">
						<img v-if="form['movie_pictures']" :src="$fullUrl(form['movie_pictures'])" class="avatar">
						<i v-else class="el-icon-plus avatar-uploader-icon"></i>
					</el-upload>
					<el-image v-else-if="$check_field('get','movie_pictures')" style="width: 100px; height: 100px"
						:src="$fullUrl(form['movie_pictures'])" :preview-src-list="[$fullUrl(form['movie_pictures'])]">
						<div slot="error" class="image-slot">
							<img src="../../../public/img/error.png" style="width: 90px; height: 90px" />
						</div>
					</el-image>
							</el-form-item>
			</el-col>
								<el-col v-if="user_group === '管理员' || $check_field('get','film_introduction') || $check_field('add','film_introduction') || $check_field('set','film_introduction')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="电影简介" prop="film_introduction">
								<el-input type="textarea" id="film_introduction" v-model="form['film_introduction']" placeholder="请输入电影简介"
						v-if="user_group === '管理员' || (form['film_information_id'] && $check_field('set','film_introduction')) || (!form['film_information_id'] && $check_field('add','film_introduction'))" :disabled="disabledObj['film_introduction_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','film_introduction')">{{form['film_introduction']}}</div>
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
				field: "film_information_id",
				url_add: "~/api/film_information/add?",
				url_set: "~/api/film_information/set?",
				url_get_obj: "~/api/film_information/get_obj?",
				url_upload: "~/api/film_information/upload?",

				query: {
					"film_information_id": 0,
				},

				form: {
								"film_title":  '', // 电影名称
										"film_year":  '', // 电影年份
										"film_rating":  '', // 电影评分
										"country":  '', // 所属国家
										"film_type":  '', // 电影类型
										"film_director":  '', // 电影导演
										"film_stars":  '', // 电影主演
										"movie_pictures":  '', // 电影图片
										"film_introduction":  '', // 电影简介
											"film_information_id": 0, // ID
						
				},
				disabledObj:{
								"film_title_isDisabled": false,
										"film_year_isDisabled": false,
										"film_rating_isDisabled": false,
										"country_isDisabled": false,
										"film_type_isDisabled": false,
										"film_director_isDisabled": false,
										"film_stars_isDisabled": false,
										"movie_pictures_isDisabled": false,
										"film_introduction_isDisabled": false,
										},

	
		
		
		
		
		
		
		
		
	
			}
		},
		methods: {


	
	
			
	
			
	
			
	
			
	
			
	
			
	
						/**
			 * 上传电影图片
			 * @param {Object} param 图片参数
			 */
			upload_movie_pictures(param){
						this.uploadFile(param.file, "movie_pictures");
					},
	
	
			
	
		
			/**
			 * 获取对象之前
			 * @param {Object} param
			 */
			get_obj_before(param) {
				var form = "";
										
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
					bl = this.$check_action('/film_information/table','add');
					console.log(bl ? "你有表格添加权限视作有添加权限" : "你没有表格添加权限");
				}
				if(!bl){
					bl = this.$check_action('/film_information/table','set');
					console.log(bl ? "你有表格添加权限视作有修改权限" : "你没有表格修改权限");
				}
				if(!bl){
					bl = this.$check_action('/film_information/view','add');
					console.log(bl ? "你有视图添加权限视作有添加权限" : "你没有视图添加权限");
				}
				if(!bl){
					bl = this.$check_action('/film_information/view','set');
					console.log(bl ? "你有视图修改权限视作有修改权限" : "你没有视图修改权限");
				}
				if(!bl){
					bl = this.$check_action('/film_information/view','get');
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
