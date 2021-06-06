<template>
	<div>
		<!-- <input type="text"  v-model="beginTime"/>
    <input type="text"  v-model="endTime /> -->
		这是房客界面 username:{{username}} room_id:{{room_id}}
	</div>
</template>

<script>
	export default {
		name: 'Tenant',
		data() {
			return {
				username: '',
				password: '',
				room_id: 0
			}
		},
		created: function() {
			this.username = this.$route.params.username
			this.room_id = this.$route.params.room_id
			console.log('params:' + this.room_id)

		}
	}
</script>
