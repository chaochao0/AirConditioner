<template>
	<div>
		<el-form style="width:40%;text-align:center;margin:0 auto">
			<el-form-item label="选择时间">
				<el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd" unlink-panels
					range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" :picker-options="pickerOptions">
				</el-date-picker>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="handleSubmit" :loading="logining">打印报表</el-button>
			</el-form-item>
		</el-form>
		<div v-if="showReporter">
			<span class="demonstration"></span>
			<el-table :data="reporter" height="300" fit border style="width: 93%;vertical-align: middle;margin:0 auto">
				<el-table-column prop="room_id" label="房间号" width="180">
				</el-table-column>
				<el-table-column prop="blow_l_time__sum" label="低风送风时间(时)" width="180">
				</el-table-column>
				<el-table-column prop="blow_m_time__sum" label="中风送风时间(时)" width="180">
				</el-table-column>
				<el-table-column prop="blow_h_time__sum" label="高风送风时间(时)" width="180">
				</el-table-column>
				<el-table-column prop="service_num__sum" label="总送风次数" width="180">
				</el-table-column>
				<el-table-column prop="service_time__sum" label="总送风时长" width="180">
				</el-table-column>
				<el-table-column prop="fee__sum" label="总费用" width="175">
				</el-table-column>
			</el-table>
		</div>
		<!-- <litepie-datepicker ref="myRef" v-model="dateValue"> -->
	</div>
</template>

<script>
	export default {
		name: 'Manager',
		components: {},
		data() {
			return {
				username: '',
				password: '',

				dateRange: [],

				reporter: [],
				showReporter: false,
				logining: false,
				pickerOptions: {
					//禁用未来时间
					disabledDate(time) {
						return time.getTime() > Date.now()
					},
					shortcuts: [{
						text: '最近一周',
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
							picker.$emit('pick', [start, end]);
						}
					}, {
						text: '最近一月',
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
							picker.$emit('pick', [start, end]);
						}
					}, {
						text: '最近一年',
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 360);
							picker.$emit('pick', [start, end]);
						}
					}]
				},

			}
		},

		methods: {
			handleSubmit(event) {
				console.log(this.dateRange)

				let that = this;
				this.logining = true;
				this.$axios({
					method: 'get',
					url: '/manager/getReporter',
					params: {
						'date_begin': that.dateRange[0],
						'date_end': that.dateRange[1]
					}
				}).then(res => {
					console.log(res.data)
					this.reporter = JSON.parse(res.data) //将json 字符串转为 json数据
					console.log(this.reporter)
					this.$alert('查询成功')
					this.logining = false
					this.showReporter = true
				}).catch(error => {
					console.log(error)
					this.$alert('查询报表失败')
					this.logining = false
				});

			},
		},
		watch: {
			dateRange: function(val) {
				console.log(this.dateRange)
			},
		},
		created: function() {
			this.username = this.$route.params.username
			//初始化时间为过去一周
			const end = new Date();
			const start = new Date();
			start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
			var year = start.getFullYear();
			var month = (start.getMonth() + 1).toString();
			var day = (start.getDate()).toString();
			if (month.length == 1) {
				month = "0" + month;
			}
			if (day.length == 1) {
				day = "0" + day;
			}
			var date_begin = year + "-" + month + "-" + day;

			year = end.getFullYear();
			month = (end.getMonth() + 1).toString();
			day = (end.getDate()).toString();
			if (month.length == 1) {
				month = "0" + month;
			}
			if (day.length == 1) {
				day = "0" + day;
			}
			var date_end = year + "-" + month + "-" + day;
			this.dateRange = [date_begin, date_end]
			console.log(this.dateRange)
			console.log('params:' + this.room_id)

		}
	}
</script>
