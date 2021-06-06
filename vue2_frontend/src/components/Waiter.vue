<template>
	<div class='waiter'>
		<!-- <div>
			<el-radio-group v-model="openRoomRadio">
				<el-radio v-for='r in rooms' :label='r.room_id' :disabled="!r.is_free" border></el-radio>
			</el-radio-group>
		</div>
		<h1>这是前台界面</h1>
		<ol>
			<li v-for="site in rooms">
				{{ site }}
			</li>
		</ol> -->
		<el-container style="height: 1000px; border: 1px solid #eee">
			<el-aside width="250px" style="background-color: rgb(238, 241, 246)">
				<el-menu @select="openMenu">
					<el-menu-item index="1">
						<template slot="title"><i class="el-icon-message"></i>开房</template>
					</el-menu-item>
					<el-menu-item index="2">
						<template slot="title"><i class="el-icon-menu"></i>退房</template>
					</el-menu-item>
				</el-menu>
			</el-aside>

			<el-main>
				<router-view @updateSignal="updateRooms"></router-view>
			</el-main>
		</el-container>
	</div>
</template>
<style>

	.el-aside {
		color: #333;
	}
</style>


<script>
	export default {
		name: 'Manager',
		components: {},
		data() {
			return {
				username: '',
				password: '',
				rooms: [], //房间信息  {room_id:   is_free}
				bill: {},
				detail: {},
				openRoomRadio: ''
			}
		},
		methods: {
			getRoomsData: function() {
				this.$axios({
					method: 'get',
					url: '/waiter/getRoomsData'
				}).then(res => {
					this.rooms = res.data
					console.log("rooms:" + this.rooms)
				}).catch(error => {
					console.log(error)
					this.$alert('请求房间数据错误')
				});
			},
			openMenu:function(index, indexPath) {
				console.log(index, indexPath)
				if (index == 1){
					this.$router.push({name:'openRoom',params:{rooms:this.rooms}})
				}
				else if(index==2){
					this.$router.push({name:'closeRoom',params:{rooms:this.rooms}})
				}
			},
			updateRooms:function(data){
				this.rooms = data
			}
		},
		watch: {},
		created: function() {
			this.username = this.$route.params.username
			this.getRoomsData()
		}
	}
</script>
