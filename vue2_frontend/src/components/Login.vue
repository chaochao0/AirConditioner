<!-- // <template>
// 	<el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
// 	<el-input v-model="loginForm.password" placeholder="请输入密码" show-password></el-input>
	
// </template> -->


<!-- <script>
	export default {
		data() {
			return {
				loginForm: {
					username: '',
					password: ''
				}
			};
		},
		methods: {
		    login() {
				let _this = this
				if (this.loginForm.username === '' || this.loginForm.password === '') {
					alert('账号或密码不能为空');
				} else {
					let formdata = new FormData();
					formdata.append('username', this.loginForm.username);
					formdata.append('password', this.loginForm.password);
					this.$axios({
						method: 'post',
						url: '/login/',
						data: formdata
					}).then(res => {
						console.log(res.data)
						let role = res.data.role
						if (role == "Tenant") {
							/*  */
							let room_id = res.data.room_id
							console.log(room_id)
							_this.$router.push({name:'tenant', params: {username: this.loginForm.username,room_id:room_id}})
						}
						else if(role=="Manager"){
							_this.$router.push('/manager');
						}
						// _this.userToken = 'Bearer ' + res.data.data.body.token;
						//   // 将用户token保存到vuex中
						//   _this.changeLogin({ Authorization: _this.userToken });
						alert('登陆成功')
					}).catch(error => {
						console.log(error)
						alert('账号或密码错误')
					});
				}
			}
		}
	};
</script>
 -->

<template>
	<div class="login-container">
		<el-form :model="ruleForm2" :rules="rules2" status-icon ref="ruleForm2" label-position="left" label-width="0px"
			class="demo-ruleForm login-page">
			<h3 class="title">系统登录</h3>
			<el-form-item prop="username">
				<el-input type="text" v-model="ruleForm2.username" auto-complete="off" placeholder="用户名"></el-input>
			</el-form-item>
			<el-form-item prop="password">
				<el-input type="password" v-model="ruleForm2.password" auto-complete="off" placeholder="密码"></el-input>
			</el-form-item>
			<el-checkbox v-model="checked" class="rememberme">记住密码</el-checkbox>
			<el-form-item style="width:100%;">
				<el-button type="primary" style="width:100%;" @click="handleSubmit" :loading="logining">登录</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				logining: false,
				ruleForm2: {
					username: 'manager',
					password: 'manager',
				},
				rules2: {
					username: [{
						required: true,
						message: 'please enter your account',
						trigger: 'blur'
					}],
					password: [{
						required: true,
						message: 'enter your password',
						trigger: 'blur'
					}]
				},
				checked: false
			}
		},
		methods: {
			handleSubmit(event) {
				this.$refs.ruleForm2.validate((valid) => {
					if (valid) {
						this.logining = true;
						let formdata = new FormData();
						formdata.append('username', this.ruleForm2.username);
						formdata.append('password', this.ruleForm2.password);
						this.$axios({
							method: 'post',
							url: '/login/',
							data: formdata
						}).then(res => {
							console.log(res.data)
							let role = res.data.role
							this.$alert('登陆成功')
							if (role == "Tenant") {
								/*  */
								let room_id = res.data.room_id
								console.log(room_id)
								this.$router.push({
									name: 'tenant',
									params: {
										username: this.ruleForm2.username,
										room_id: room_id
									}
								})
							} else if (role == "Manager") {
								this.$router.push({
									name: 'manager',
									params: {
										username: this.ruleForm2.username
									}
								});
							} else if (role == "Waiter") {
								this.$router.push({
									name: 'waiter',
									params: {
										username: this.ruleForm2.username
									}
								});
							}
							// _this.userToken = 'Bearer ' + res.data.data.body.token;
							//   // 将用户token保存到vuex中
							//   _this.changeLogin({ Authorization: _this.userToken });
						}).catch(error => {
							console.log(error)
							this.$alert('账号或密码错误')
						});
						// if (this.ruleForm2.username === 'admin' &&
						// 	this.ruleForm2.password === '123456') {
						// 	this.logining = false;
						// 	sessionStorage.setItem('user', this.ruleForm2.username);
						// 	this.$router.push({
						// 		path: '/manager'
						// 	});
						// } else {
						// 	this.logining = false;
						// 	this.$alert('username or password wrong!', 'info', {
						// 		confirmButtonText: 'ok'
						// 	})
						// }
					} else {
						console.log('error submit!');
						return false;
					}
				})
			}
		}
	};
</script>

<style scoped>
	.login-container {
		width: 100%;
		height: 100%;
	}

	.login-page {
		-webkit-border-radius: 5px;
		border-radius: 5px;
		margin: 180px auto;
		width: 350px;
		padding: 35px 35px 15px;
		background: #fff;
		border: 1px solid #eaeaea;
		box-shadow: 0 0 25px #cac6c6;
	}

	label.el-checkbox.rememberme {
		margin: 0px 0px 15px;
		text-align: left;
	}
</style>
