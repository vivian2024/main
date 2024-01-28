<template>
  <div class="page_search">
	<div class="warp">
	  <div class="container">
		<div class="row">
		  <div class="col-12">
			<div class="card_result_search">
			  <div class="title">搜索结果</div>

				<!-- 文章搜索结果 -->
			  <list_result_search
				:list="result_article"
				title="电影资讯"
				source_table="article"
			  ></list_result_search>

				<!-- 论坛搜索结果 -->
			  <list_result_search
				:list="result_forum"
				title="交流论坛"
				source_table="forum"
			  ></list_result_search>

						  <list_result_search
				v-if="$check_action('/system_user/list', 'get')"
				:list="result_system_user_user_name"
				title="系统用户用户姓名"
				source_table="system_user"
			  ></list_result_search>
								  <list_result_search
				v-if="$check_action('/system_user/list', 'get')"
				:list="result_system_user_user_gender"
				title="系统用户用户性别"
				source_table="system_user"
			  ></list_result_search>
									  <list_result_search
				v-if="$check_action('/film_information/list', 'get')"
				:list="result_film_information_film_title"
				title="电影信息电影名称"
				source_table="film_information"
			  ></list_result_search>
																	  <list_result_search
				v-if="$check_action('/film_information/list', 'get')"
				:list="result_film_information_film_type"
				title="电影信息电影类型"
				source_table="film_information"
			  ></list_result_search>
																					  <list_result_search
				v-if="$check_action('/scoring_analysis/list', 'get')"
				:list="result_scoring_analysis_film_title"
				title="评分分析电影名称"
				source_table="scoring_analysis"
			  ></list_result_search>
																					  <list_result_search
				v-if="$check_action('/regional_analysis/list', 'get')"
				:list="result_regional_analysis_film_title"
				title="地区分析电影名称"
				source_table="regional_analysis"
			  ></list_result_search>
																		</div>
		  </div>
		</div>
	  </div>
	</div>
  </div>
</template>

<script>
import mixin from "../../mixins/page.js";
import list_result_search from "../../components/diy/list_result_search.vue";

export default {
  mixins: [mixin],
  data() {
	return {
	  "query": {
		word: "",
	  },
	  "result_article": [],
	  "result_forum": [],
						"result_system_user_user_name":[],
								"result_system_user_user_gender":[],
									"result_film_information_film_title":[],
																	"result_film_information_film_type":[],
																					"result_scoring_analysis_film_title":[],
																					"result_regional_analysis_film_title":[],
																};
  },
  methods: {
	/**
	 * 获取文章
	 */
	get_article() {
	  this.$get("~/api/article/get_list?like=0", { page: 1, size: 10, title: this.query.word }, (json) => {
		if (json.result) {
		  this.result_article = json.result.list;
		}
	  });
	},
	/**
	 * 获取交流论坛
	 */
	get_forum() {
	  this.$get("~/api/forum/get_list?like=0", { page: 1, size: 10, title: this.query.word }, (json) => {
		if (json.result) {
		  this.result_forum = json.result.list;
		}
	  });
	},

				/**
	 * 获取user_name
	 */
	get_system_user_user_name(){
		this.$get("~/api/system_user/get_list?like=0", { page: 1, size: 10, "user_name": this.query.word }, (json) => {
		  if (json.result) {
			var result_system_user_user_name = json.result.list;
			result_system_user_user_name.map(o => o.title = o['user_name'])
	  			this.result_system_user_user_name = result_system_user_user_name
		 	}
		});
	},
						/**
	 * 获取user_gender
	 */
	get_system_user_user_gender(){
		this.$get("~/api/system_user/get_list?like=0", { page: 1, size: 10, "user_gender": this.query.word }, (json) => {
		  if (json.result) {
			var result_system_user_user_gender = json.result.list;
			result_system_user_user_gender.map(o => o.title = o['user_gender'])
	  			this.result_system_user_user_gender = result_system_user_user_gender
		 	}
		});
	},
							/**
	 * 获取film_title
	 */
	get_film_information_film_title(){
		this.$get("~/api/film_information/get_list?like=0", { page: 1, size: 10, "film_title": this.query.word }, (json) => {
		  if (json.result) {
			var result_film_information_film_title = json.result.list;
			result_film_information_film_title.map(o => o.title = o['film_title'])
	  			this.result_film_information_film_title = result_film_information_film_title
		 	}
		});
	},
															/**
	 * 获取film_type
	 */
	get_film_information_film_type(){
		this.$get("~/api/film_information/get_list?like=0", { page: 1, size: 10, "film_type": this.query.word }, (json) => {
		  if (json.result) {
			var result_film_information_film_type = json.result.list;
			result_film_information_film_type.map(o => o.title = o['film_type'])
	  			this.result_film_information_film_type = result_film_information_film_type
		 	}
		});
	},
																			/**
	 * 获取film_title
	 */
	get_scoring_analysis_film_title(){
		this.$get("~/api/scoring_analysis/get_list?like=0", { page: 1, size: 10, "film_title": this.query.word }, (json) => {
		  if (json.result) {
			var result_scoring_analysis_film_title = json.result.list;
			result_scoring_analysis_film_title.map(o => o.title = o['film_title'])
	  			this.result_scoring_analysis_film_title = result_scoring_analysis_film_title
		 	}
		});
	},
																			/**
	 * 获取film_title
	 */
	get_regional_analysis_film_title(){
		this.$get("~/api/regional_analysis/get_list?like=0", { page: 1, size: 10, "film_title": this.query.word }, (json) => {
		  if (json.result) {
			var result_regional_analysis_film_title = json.result.list;
			result_regional_analysis_film_title.map(o => o.title = o['film_title'])
	  			this.result_regional_analysis_film_title = result_regional_analysis_film_title
		 	}
		});
	},
															
  },
  components: { list_result_search },
	created(){
    this.query.word = this.$route.query.word || "";
  },
  mounted() {
	this.get_article();
	this.get_forum();
					this.get_system_user_user_name();
							this.get_system_user_user_gender();
								this.get_film_information_film_title();
																this.get_film_information_film_type();
																				this.get_scoring_analysis_film_title();
																				this.get_regional_analysis_film_title();
															  },
  watch: {
	$route() {
	  $.push(this.query, this.$route.query);
	  this.get_article();
	  this.get_forum();
				  this.get_system_user_user_name();
						  this.get_system_user_user_gender();
							  this.get_film_information_film_title();
															  this.get_film_information_film_type();
																			  this.get_scoring_analysis_film_title();
																			  this.get_regional_analysis_film_title();
																},
  },
};
</script>

<style scoped>
.card_search {
  text-align: center;
}
.card_result_search>.title {
  text-align: center;
  padding: 10px 0;
}
</style>
