<template>
	<div>
		<el-form :model="openRoomForm" :rules="rules" status-icon ref="myOpenRoomForm">
			<el-form-item label="房间" prop="room_id">
				<el-radio-group v-model="openRoomForm.room_id">
					<el-radio v-for='r in rooms' :label='r.room_id' :disabled="!r.is_free" border></el-radio>
				</el-radio-group>
			</el-form-item>
			<el-form-item label="姓名" prop="username">
				<el-input type="text" v-model="openRoomForm.username" auto-complete="off" placeholder="请输入房客姓名">
				</el-input>
			</el-form-item>
			<el-form-item label="身份证号" prop="password">
				<el-input type="password" v-model="openRoomForm.password" auto-complete="off" placeholder="请输入房客身份证号">
				</el-input>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="handleSubmit" :loading="logining">开房</el-button>
				<el-button @click="resetForm('myOpenRoomForm')">重置</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
	export default {
		name: 'OpenRoom',
		data() {
			return {
				rooms: [], //房间信息  {room_id:   is_free}
				openRoomForm: {
					room_id: '',
					username: '',
					password: '',
				},
				rules: {
					username: [{
						required: true,
						message: '请输入姓名',
						trigger: 'blur'
					}],
					password: [{
						required: true,
						message: '请输入身份证号',
						trigger: 'blur'
					}],
					room_id: [{
						required: true,
						message: '请选择房号',
					}],
				},
				logining: false,
			}
		},
		methods: {
			handleSubmit(event) {
				this.$refs.myOpenRoomForm.validate((valid) => {
					if (valid) {
						let that = this;
						this.logining = true;
						console.log(that.openRoomForm)
						let formdata = new FormData();
						formdata.append('room_id', this.openRoomForm.room_id);
						formdata.append('username', this.openRoomForm.username);
						formdata.append('password', this.openRoomForm.password);
						this.$axios({
							method: 'post',
							url: '/waiter/openRoom',
							data: formdata
						}).then(res => {
							console.log(res.data)
							for(let i=0;i<this.rooms.length;i++){
								if(this.rooms[i].room_id==this.openRoomForm.room_id){
									this.rooms[i].is_free=false
									break
								}
							}
							this.resetForm('myOpenRoomForm')
							this.$alert('开房成功')
							this.$emit('updateSignal',this.rooms)
							this.logining=false
						}).catch(error => {
							console.log(error)
							this.$alert('开房失败')
							this.logining=false
						});
					} else {
						console.log('error submit!');
						return false;
					}
				})
			},
			resetForm(formName) {
				this.$refs[formName].resetFields();
			},

		},
		created: function() {
			//console.log(this.$parent.rooms)
			this.rooms = this.$route.params.rooms
		}
	}
</script>

<style>
</style>
