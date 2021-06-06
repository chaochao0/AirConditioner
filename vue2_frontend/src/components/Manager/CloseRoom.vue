<template>
	<div>
		<el-form>
			<el-form-item label="房间">
				<el-radio-group v-model="room_id">
					<el-radio v-for='r in rooms' :label='r.room_id' :disabled="r.is_free" border></el-radio>
				</el-radio-group>
			</el-form-item>
			<el-form-item label="选项">
				<el-checkbox v-model="bill_choosed" label="打印账单" border></el-checkbox>
				<el-checkbox v-model="detail_choosed" label="打印详单" border></el-checkbox>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="handleSubmit" :loading="logining">退房</el-button>
			</el-form-item>
		</el-form>
		<div v-if="bill_choosed" >
			<span class="demonstration"></span>
			<el-table :data="bill" height="250" show-header fit border style="width: 34%">
				<el-table-column prop="power_comsumption_sum" label="总用电度数" width="180">
				</el-table-column>
				<el-table-column prop="fee_sum" label="空调总费用" width="180">
				</el-table-column>
			</el-table>
			<br>
		</div>
		<div v-if="detail_choosed">
			<span class="demonstration"></span>
			<el-table :data="detail" height="250" border style="width: 100%">
				<el-table-column prop="start_time" label="开始时间" width="180">
				</el-table-column>
				<el-table-column prop="end_time" label="结束时间" width="180">
				</el-table-column>
				<el-table-column prop="blow_mode" label="风速" width="180">
				</el-table-column>
				<el-table-column prop="service_time" label="送风时长" width="180">
				</el-table-column>
				<el-table-column prop="power_comsumption" label="用电量" width="180">
				</el-table-column>
				<el-table-column prop="fee" label="费用" width="180">
				</el-table-column>
			</el-table>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'CloseRoom',
		data() {
			return {
				rooms: [], //房间信息  {room_id:   is_free}
				room_id: '',
				logining: false,
				bill_choosed: false,
				detail_choosed: false,
				bill:[],
				detail:[],
			}
		},
		methods: {
			handleSubmit(event) {
				if (this.room_id) {
					let that = this
					this.logining = true
					this.$axios({
						method: 'get',
						url: '/waiter/closeRoom',
						params: {
							'room_id': that.room_id
						}
					}).then(res => {
						console.log(res.data)
						for (let i = 0; i < this.rooms.length; i++) {
							if (this.rooms[i].room_id == this.room_id) {
								this.rooms[i].is_free = true
								break
							}
						}
						if(this.bill_choosed){
							this.getBill()
						}
						if(this.detail_choosed){
							this.getDetail()
						}
						this.$alert('退房成功')
						this.$emit('updateSignal', this.rooms)
						this.logining = false
					}).catch(error => {
						console.log(error)
						this.$alert('退房失败')
						this.logining = false
					});
					
				} else {
					console.log('error submit!');
					return false;
				}
			},
			getBill:function(){
				let room_id = this.room_id
				this.$axios({
					method: 'get',
					url: '/waiter/getBill',
					params: {
						'room_id': room_id
					}
				}).then(res => {
					console.log(res.data)
					this.bill.push(res.data)
					console.log("bill:" + this.bill)
				}).catch(error => {
					console.log(error)
					//this.$alert('获得账单失败')
					throw new Error("获得账单失败")
				});
			},
			getDetail:function(){
				let room_id = this.room_id
				this.$axios({
					method: 'get',
					url: '/waiter/getDetail',
					params: {
						'room_id': room_id
					}
				}).then(res => {
					console.log(res.data)
					this.detail=res.data
					console.log("detail:" + this.detail)
				}).catch(error => {
					console.log(error)
					//this.$alert('获得详单失败')
					throw new Error("获得详单失败")
				});
			}
		},
		created: function() {
			this.rooms = this.$route.params.rooms
		}
	}
</script>

<style>
</style>
