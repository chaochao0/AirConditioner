# Generated by Django 3.1.7 on 2021-06-01 00:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ac_state', models.CharField(choices=[('close', '关闭'), ('set', '设置模式'), ('ready', '就绪'), ('none', '备用')], default='close', max_length=64, verbose_name='中央空调状态')),
                ('temp_mode', models.SmallIntegerField(choices=[(-1, '制冷模式'), (1, '制热模式')], default=1, verbose_name='制冷制热模式')),
                ('cool_temp_highlimit', models.IntegerField(default=25, verbose_name='制冷温控范围最高温')),
                ('cool_temp_lowlimit', models.IntegerField(default=18, verbose_name='制冷温控范围最低温')),
                ('heat_temp_highlimit', models.IntegerField(default=30, verbose_name='制热温控范围最高温')),
                ('heat_temp_lowlimit', models.IntegerField(default=25, verbose_name='制热温控范围最低温')),
                ('default_temp', models.IntegerField(default=25, verbose_name='缺省温度')),
                ('electric_price', models.FloatField(default=1, verbose_name='单位电价(元/度)')),
                ('powerrate_H', models.FloatField(default=0.016666666666666666, verbose_name='高风耗电量(度/秒)')),
                ('powerrate_M', models.FloatField(default=0.008333333333333333, verbose_name='中风耗电量(度/秒)')),
                ('powerrate_L', models.FloatField(default=0.005555555555555556, verbose_name='低风耗电量(度/秒)')),
                ('feerate_H', models.FloatField(default=0.016666666666666666, verbose_name='高风费率')),
                ('feerate_M', models.FloatField(default=0.008333333333333333, verbose_name='中风费率')),
                ('feerate_L', models.FloatField(default=0.005555555555555556, verbose_name='低风费率')),
                ('max_load', models.IntegerField(default=3, verbose_name='最大带机量')),
                ('sss_time', models.IntegerField(default=120, verbose_name='同级请求切换时间')),
            ],
        ),
        migrations.CreateModel(
            name='ACAdministrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='用户名')),
                ('password', models.CharField(default='', max_length=128, verbose_name='密码')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '空调管理员',
                'verbose_name_plural': '空调管理员',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='用户名')),
                ('password', models.CharField(default='', max_length=128, verbose_name='密码')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '酒店经理',
                'verbose_name_plural': '酒店经理',
            },
        ),
        migrations.CreateModel(
            name='RequestQueue',
            fields=[
                ('room_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='房间号')),
                ('room_state', models.SmallIntegerField(choices=[(0, '关闭'), (1, '运行'), (2, '挂起'), (3, '等待')], default=2, verbose_name='房间空调状态')),
                ('temp_mode', models.SmallIntegerField(choices=[(-1, '制冷模式'), (1, '制热模式')], default=-1, verbose_name='制冷制热模式')),
                ('blow_mode', models.SmallIntegerField(choices=[(0, '低风'), (1, '中风'), (2, '高风')], default=1, verbose_name='风速')),
                ('target_temp', models.IntegerField(verbose_name='目标温度')),
                ('request_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='请求送风时间戳')),
            ],
        ),
        migrations.CreateModel(
            name='RequestRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(max_length=64, verbose_name='房间号')),
                ('room_state', models.SmallIntegerField(choices=[(0, '关闭'), (1, '运行'), (2, '挂起'), (3, '等待')], default=2, verbose_name='房间送风状态')),
                ('temp_mode', models.SmallIntegerField(choices=[(-1, '制冷模式'), (1, '制热模式')], default=2, verbose_name='制冷制热模式')),
                ('blow_mode', models.SmallIntegerField(choices=[(0, '低风'), (1, '中风'), (2, '高风')], default=1, verbose_name='风速')),
                ('target_temp', models.IntegerField(verbose_name='目标温度')),
                ('request_time', models.DateTimeField(verbose_name='请求时间')),
                ('finished', models.IntegerField(default=0, verbose_name='结束')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True, verbose_name='房间号')),
                ('is_free', models.BooleanField(default=True, verbose_name='是否空闲')),
                ('room_state', models.SmallIntegerField(choices=[(0, '关闭'), (1, '运行'), (2, '挂起'), (3, '等待')], default=0, verbose_name='房间从控机状态')),
                ('temp_mode', models.SmallIntegerField(choices=[(-1, '制冷模式'), (1, '制热模式')], default=-1, verbose_name='制冷制热模式')),
                ('blow_mode', models.SmallIntegerField(choices=[(0, '低风'), (1, '中风'), (2, '高风')], default=-1, verbose_name='风速')),
                ('current_temp', models.FloatField(default=25, verbose_name='当前温度')),
                ('target_temp', models.IntegerField(default=25, verbose_name='目标温度')),
                ('fee', models.FloatField(default=0, verbose_name='总费用')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceQueue',
            fields=[
                ('room_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='房间号')),
                ('room_state', models.SmallIntegerField(choices=[(0, '关闭'), (1, '运行'), (2, '挂起'), (3, '等待')], default=2, verbose_name='房间送风状态')),
                ('temp_mode', models.SmallIntegerField(choices=[(-1, '制冷模式'), (1, '制热模式')], default=-1, verbose_name='制冷制热模式')),
                ('blow_mode', models.SmallIntegerField(choices=[(0, '低风'), (1, '中风'), (2, '高风')], default=1, verbose_name='风速')),
                ('target_temp', models.IntegerField(verbose_name='目标温度')),
                ('service_timestamp', models.DateTimeField(null=True, verbose_name='开始送风时间戳')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='用户名')),
                ('password', models.CharField(default='', max_length=128, verbose_name='密码')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('room_id', models.CharField(max_length=64, verbose_name='房间号')),
                ('date_in', models.DateTimeField(blank=True, null=True, verbose_name='入住日期')),
                ('date_out', models.DateTimeField(blank=True, null=True, verbose_name='登出日期')),
            ],
            options={
                'verbose_name': '房客',
                'verbose_name_plural': '房客',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='Waiter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='用户名')),
                ('password', models.CharField(default='', max_length=128, verbose_name='密码')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '前台服务员',
                'verbose_name_plural': '前台服务员',
            },
        ),
        migrations.CreateModel(
            name='ServiceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(max_length=64, verbose_name='房间号')),
                ('blow_mode', models.SmallIntegerField(choices=[(0, '低风'), (1, '中风'), (2, '高风')], default=1, verbose_name='风速')),
                ('target_temp', models.IntegerField(verbose_name='目标温度')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('service_time', models.DurationField(default=datetime.timedelta(0))),
                ('power_comsumption', models.FloatField(default=0.0, verbose_name='用电度数')),
                ('fee', models.FloatField(default=0.0)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='RoomDailyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(max_length=64, verbose_name='房间号')),
                ('date', models.DateField(verbose_name='日期')),
                ('blow_l_time', models.DurationField(default=datetime.timedelta(0), verbose_name='低风送风时间')),
                ('blow_m_time', models.DurationField(default=datetime.timedelta(0), verbose_name='中风送风时间')),
                ('blow_h_time', models.DurationField(default=datetime.timedelta(0), verbose_name='高风送风时间')),
                ('service_num', models.IntegerField(default=0, verbose_name='总送风次数(服务记录数)')),
                ('service_time', models.DurationField(default=datetime.timedelta(0), verbose_name='总送风时间')),
                ('fee', models.FloatField(default=0.0, verbose_name='总费用')),
                ('upto_target_count', models.IntegerField(default=0, verbose_name='达到目标温度次数')),
                ('schedule_count', models.IntegerField(default=0, verbose_name='被调度次数')),
            ],
            options={
                'unique_together': {('room_id', 'date')},
            },
        ),
    ]
