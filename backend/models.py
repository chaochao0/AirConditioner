from django.db import models
from django.db.models import Sum, Count, Max
import json
import datetime
from time import sleep
from datetime import timedelta
from django.core.serializers import serialize
from django.utils import timezone
from django.db.models.signals import pre_save, pre_delete

# 制冷制热模式, 默认制冷
temp_mode_choice = (
    (-1, '制冷模式'),
    (1, '制热模式'),
)
# 风速
blow_mode_choice = (
    (0, '低风'),
    (1, '中风'),
    (2, '高风'),
)

# 温度变化速率
temp_rate = [
    0.4 / 60,  # 低风
    0.5 / 60,  # 中风
    0.6 / 60,  # 高风
    0.5 / 60  # 无风
]

# 房间状态
room_state_choice = (
    (0, '关闭'),
    (1, '运行'),
    (2, '挂起'),
    (3, '等待'),
)
# 中央空调状态
ac_state_choice = (
    ('close', '关闭'),
    ('set', '设置模式'),
    ('ready', '就绪'),
    ('none', '备用'),
)

default_temp = 25

# 各档风速耗电量
feerate_choice = (
    (0.01666, '高风单位耗电量(度/秒)'),
    (0.00833, '中风单位耗电量(度/秒)'),  # 缺省风速
    (0.00556, '低风单位耗电量(度/秒)'),
)

# Create your models here.


class RequestRecord(models.Model):
    room_id = models.CharField('房间号', max_length=64)
    room_state = models.SmallIntegerField(
        "房间送风状态", choices=room_state_choice, default=2)
    temp_mode = models.SmallIntegerField(
        '制冷制热模式', choices=temp_mode_choice, default=2)
    blow_mode = models.SmallIntegerField(
        '风速', choices=blow_mode_choice, default=1)
    #start_temp = models.IntegerField('初始温度')
    target_temp = models.IntegerField('目标温度')
    request_time = models.DateTimeField('请求时间')
    finished = models.IntegerField('结束', default=0)  # 可能会用得上


class ServiceRecord(models.Model):
    room_id = models.CharField('房间号', max_length=64)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE)
    blow_mode = models.SmallIntegerField(
        '风速', choices=blow_mode_choice, default=1)
    target_temp = models.IntegerField('目标温度')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # 自动获取以下字段
    service_time = models.DurationField(default=timedelta())
    power_comsumption = models.FloatField('用电度数', default=0.0)
    #now_temp = models.FloatField('当前温度')
    #fee_rate = models.FloatField('费率', choices=feerate_choice, default=2)
    fee = models.FloatField(default=0.0)

# 每次servicerecord.save()时，通过django的信号机制实现自动计算service_time pow_consumption fee


def auto_getExtraData_and_updateRoomDailyRepoter(sender, instance, *args, **kwargs):
    if instance.end_time and instance.start_time:
        instance.service_time = instance.end_time - instance.start_time
    else:
        return False
    fee = 0
    power = 0
    if instance.blow_mode == 0:  # 低风
        power = AC.objects.all()[0].powerrate_L * \
            instance.service_time.total_seconds()
        fee = AC.objects.all()[0].feerate_L * \
            instance.service_time.total_seconds()
    elif instance.blow_mode == 1:
        power = AC.objects.all()[0].powerrate_M * \
            instance.service_time.total_seconds()
        fee = AC.objects.all()[0].feerate_M * \
            instance.service_time.total_seconds()
    elif instance.blow_mode == 2:
        power = AC.objects.all()[0].powerrate_H * \
            instance.service_time.total_seconds()
        # print(AC.objects.all()[0].powerrate_H)
        # print(instance.service_time.seconds)
        fee = AC.objects.all()[0].feerate_H * \
            instance.service_time.total_seconds()
    instance.fee = fee
    # print(AC.objects.all()[0].feerate_H)
    instance.power_comsumption = power

    # update_room_daily_repoter
    room_daily_report = RoomDailyReport.objects.filter(
        room_id=instance.room_id, date=instance.start_time.date())
    if room_daily_report.count() == 0:
        room_daily_report = RoomDailyReport(
            room_id=instance.room_id, date=instance.start_time.date())
    else:
        room_daily_report = room_daily_report[0]
    if(instance.blow_mode == 0):
        room_daily_report.blow_l_time += instance.service_time
    elif (instance.blow_mode == 1):
        room_daily_report.blow_m_time += instance.service_time
    elif(instance.blow_mode == 2):
        room_daily_report.blow_h_time += instance.service_time
    room_daily_report.service_time += instance.service_time
    room_daily_report.service_num += 1
    room_daily_report.fee += instance.fee
    room_daily_report.save()
    return True


pre_save.connect(auto_getExtraData_and_updateRoomDailyRepoter,
                 sender=ServiceRecord)


# 房间日报表
class RoomDailyReport(models.Model):
    room_id = models.CharField('房间号', max_length=64)
    date = models.DateField('日期')
    blow_l_time = models.DurationField('低风送风时间', default=timedelta())
    blow_m_time = models.DurationField('中风送风时间', default=timedelta())
    blow_h_time = models.DurationField('高风送风时间', default=timedelta())
    service_num = models.IntegerField('总送风次数(服务记录数)', default=0)
    service_time = models.DurationField('总送风时间', default=timedelta())
    fee = models.FloatField('总费用', default=0.0)
    # 以上不需要手动计算，在serviceRecord 保存时自动计算

    #temp_often_use = models.IntegerField('使用时间最长的目标温度', default=0)
    # 这个域好像我实现不了，目前想法是在每次获得日报表时，都查询那一天的服务记录，统计出那一天的使用时间最长的目标温度。
    # 或者，实现个定时器，每次到24点自动执行，获得使用时间最长的目标温度
    switch_num = models.IntegerField('开关次数', default=0)  # 开关次数
    upto_target_count = models.IntegerField('达到目标温度次数', default=0)  # 达到目标温度次数
    schedule_count = models.IntegerField('被调度次数', default=0)
    # change_temp_count = models.IntegerField('调温次数', default=0)
    # change_speed_count = models.IntegerField('调风次数', default=0)

    class Meta:
        unique_together = ("room_id", "date")


class RequestQueue(models.Model):
    room_id = models.CharField('房间号', max_length=64, primary_key=True)
    room_state = models.SmallIntegerField(
        "房间空调状态", choices=room_state_choice, default=2)
    temp_mode = models.SmallIntegerField(
        '制冷制热模式', choices=temp_mode_choice, default=-1)
    blow_mode = models.SmallIntegerField(
        '风速', choices=blow_mode_choice, default=1)
    target_temp = models.IntegerField('目标温度')
    request_timestamp = models.DateTimeField('请求送风时间戳', auto_now_add=True)


class ServiceQueue(models.Model):
    room_id = models.CharField('房间号', max_length=64, primary_key=True)
    room_state = models.SmallIntegerField(
        "房间送风状态", choices=room_state_choice, default=2)
    temp_mode = models.SmallIntegerField(
        '制冷制热模式', choices=temp_mode_choice, default=-1)  # 没有用
    blow_mode = models.SmallIntegerField(
        '风速', choices=blow_mode_choice, default=1)
    target_temp = models.IntegerField('目标温度')
    service_timestamp = models.DateTimeField('开始送风时间戳', null=True)

    class Meta:
        ordering = ['-blow_mode', 'service_timestamp']


def auto_create_service_record(sender, instance, *args, **kwargs):
    new_serviceRecord = (ServiceRecord(room_id=instance.room_id, tenant=Tenant.objects.filter(
        date_out=None, room_id=instance.room_id)[0], blow_mode=instance.blow_mode, target_temp=instance.target_temp, start_time=instance.service_timestamp, end_time=timezone.now()))
    new_serviceRecord.save()


# 在删除一个服务队列时，都自动生成一条服务记录
pre_delete.connect(auto_create_service_record, sender=ServiceQueue)


class User(models.Model):
    username = models.CharField("用户名", max_length=128)
    password = models.CharField(
        "密码", max_length=128, default='')  # 创建时设置为其身份证号
    c_time = models.DateTimeField(auto_now_add=True)  # 自动记录角色添加时间，方便管理排序

    class Meta:
        ordering = ['-c_time']
        abstract = True


class Tenant(User):
    room_id = models.CharField(verbose_name="房间号", max_length=64)
    date_in = models.DateTimeField(verbose_name='入住日期', null=True, blank=True)
    date_out = models.DateTimeField(verbose_name='登出日期', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-c_time']
        verbose_name = '房客'
        verbose_name_plural = '房客'

    # 打开空调
    def requestOn(self):
        # 设置该顾客房间空调状态为挂起，等待中央空调调度后才会为运行模式

        room = Room.objects.get(room_id=self.room_id)
        room.room_state = 2  # 挂起状态
        room.save()

        room_daily_report = RoomDailyReport.objects.filter(
            room_id=self.room_id, date=timezone.now().date())
        if room_daily_report.count() == 0:
            room_daily_report = RoomDailyReport(
                room_id=self.room_id, date=timezone.now().date())
        else:
            room_daily_report = room_daily_report[0]
        room_daily_report.switch_count += 1
        room_daily_report.save()
        room.requestAir()  # 调用对应room的请求送风函数

    # 改变温度

    def changeTargetTemp(self, target_temp):
        # 类似上面的requestOn
        pass

    # 改变风速
    def changeBlowMode(self, blow_mode):
        pass

    # 关闭空调
    def requestOff(self):
        pass


class ACAdministrator(User):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "空调管理员"  # 可读性佳的名字
        verbose_name_plural = "空调管理员"  # 复数形式


class Waiter(User):
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "前台服务员"  # 可读性佳的名字
        verbose_name_plural = "前台服务员"  # 复数形式

    # 返回空闲房间字典列表（每个元素为字典）
    def getFreeRooms(self):
        rooms = Room.objects.filter(is_free=True)
        json_data = serialize('json', rooms)  # 序列化成str形的json
        json_data = json.loads(json_data)  # load成python json对象
        return json_data

    def getRoomsData(self):
        rooms = Room.objects.all()
        json_data = serialize('json', rooms)
        json_data = json.loads(json_data)
        rooms_data = []
        for i in json_data:
            room_data = {}
            room_data["room_id"] = i['pk']
            room_data["is_free"] = i['fields']['is_free']
            rooms_data.append(room_data)
        return rooms_data

    def openRoom(self, _room_id, _username, _password):
        newTenant = Tenant(username=_username, password=_password,
                           room_id=_room_id, date_in=timezone.now())
        newTenant.save()
        room = Room.objects.get(pk=_room_id)
        room.is_free = False
        room.save()

    def closeRoom(self, _room_id):
        room = Room.objects.get(room_id=_room_id)
        room.clearData()
        return True

    # 获得账单 返回账单字典
    def getBill(self, _tenant_id):
        serRecords = ServiceRecord.objects.filter(
            tenant__id=_tenant_id).values('power_comsumption', 'fee')
        bill = {"power_comsumption_sum": 0, "fee_sum": 0}
        print(serRecords)
        for s in serRecords:
            bill["power_comsumption_sum"] += s["power_comsumption"]
            bill["fee_sum"] += s["fee"]
        return bill

    # 获得详单 返回详单字典列表
    def getDetail(self, _tenant_id):
        # Django序列化程序只能序列化查询集，values()并不返回queryset而是ValuesQuerySet对象。
        # 所以，避免使用values()。而是values()在serialize方法中指定希望使用的字段，如下所示：
        # serRecords = ServiceRecord.objects.filter(tenant__pk=_tenant_id).values(
        #       'blow_mode','service_time','power_comsumption', 'fee')
        # detail = serialize('json', serRecords) #出错
        #detail = json.loads(detail)
        serRecords = ServiceRecord.objects.filter(tenant__pk=_tenant_id)
        detail = serialize('json', list(serRecords), fields=(
            'blow_mode', 'start_time', 'end_time', 'service_time', 'power_comsumption', 'fee'))
        detail = json.loads(detail)
        result = []
        for d in detail:
            d["fields"]["temp_mode"] = AC.objects.all()[0].temp_mode
            result.append(d["fields"])
        return result


class Manager(User):
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "酒店经理"  # 可读性佳的名字
        verbose_name_plural = "酒店经理"  # 复数形式

    def getReporter(self, date_begin, date_end):
        reporter = RoomDailyReport.objects.filter(date__range=(date_begin, date_end)).values(
            'room_id').annotate(Sum('blow_l_time'), Sum('blow_m_time'), Sum('blow_h_time'), Sum('service_num'), Sum('service_time'), Sum('fee'), Sum('switch_num'), Sum('upto_target_count'), Sum('schedule_count')).order_by('room_id').values('room_id', 'blow_l_time__sum', 'blow_m_time__sum', 'blow_h_time__sum', 'service_num__sum', 'service_time__sum', 'fee__sum', 'switch_num__sum', 'upto_target_count__sum', 'schedule_count__sum')

        for i in reporter:
            i["blow_l_time__sum"] = round(
                i["blow_l_time__sum"].total_seconds()/3600, 2)
            i["blow_m_time__sum"] = round(
                i["blow_m_time__sum"].total_seconds()/3600, 2)
            i["blow_h_time__sum"] = round(
                i["blow_h_time__sum"].total_seconds()/3600, 2)
            i["service_time__sum"] = round(
                i["service_time__sum"].total_seconds()/3600, 2)
            i["fee__sum"] = round(i["fee__sum"], 2)
        # reporter = serialize('json', list(reporter), fields=(
        #     'room_id', 'blow_l_time__sum', 'blow_m_time__sum', 'blow_h_time__sum', 'service_num__sum', 'service_time__sum'))
        # Django的serializers无法处理ValuesQuerySet。但是，您可以使用标准json.dumps()进行序列化，
        # 并使用list()将ValuesQuerySet转换为列表。如果您的集合包含Django字段(如Decimals)，则需要传入DjangoJSONEncoder
        room_temp_usetime = ServiceRecord.objects.filter(start_time__date__range=(date_begin, date_end)).values(
            'room_id', 'target_temp').annotate(Sum('service_time')).order_by('room_id', '-service_time__sum').values('room_id', 'target_temp', 'service_time__sum')  # .annotate(Max('service_time__sum')).values('room_id','target_temp')#aggregate(Max('service_time__sum')) #values('room_id','target_temp','service_time__sum')
        room_temp_often_use = []
        last_room_id = room_temp_usetime[0]['room_id']
        room_temp_often_use.append(
            {'room_id': last_room_id, 'temp_often_use': room_temp_usetime[0]['target_temp']})
        for i in room_temp_usetime:
            if i['room_id'] == last_room_id:
                continue
            last_room_id = i['room_id']
            room_temp_often_use.append(
                {'room_id': last_room_id, 'temp_often_use': i['target_temp']})

        from django.core.serializers.json import DjangoJSONEncoder
        reporter = json.dumps(list(reporter), cls=DjangoJSONEncoder)
        # room_temp_often_use = json.dump(
        #     list(room_temp_often_use), cls=DjangoJSONEncoder)

        reporter = json.loads(reporter)
        # room_temp_often_use=json.loads(room_temp_often_use)
        for i in range(len(reporter)):
            reporter[i]['temp_often_use'] = room_temp_often_use[i]['temp_often_use']
        reporter = json.dumps(reporter)
        print(reporter)
        print(type(reporter))
        return reporter


class Room(models.Model):
    room_id = models.CharField(
        '房间号', max_length=64, unique=True, primary_key=True)
    is_free = models.BooleanField('是否空闲', default=True)
    room_state = models.SmallIntegerField(
        "房间从控机状态", choices=room_state_choice, default=0)
    temp_mode = models.SmallIntegerField(
        '制冷制热模式', choices=temp_mode_choice, default=-1)
    blow_mode = models.SmallIntegerField(
        '风速', choices=blow_mode_choice, default=-1)
    current_temp = models.FloatField('当前温度', default=default_temp)
    target_temp = models.IntegerField('目标温度', default=default_temp)
    # fee_rate = models.FloatField('费率')
    fee = models.FloatField('总费用', default=0)
    #duration = models.IntegerField('服务时长(秒)', default=0)

    def __str__(self):
        return "room_" + str(self.room_id)

    def requestAir(self):
        # new_request_record = RequestRecord(  # 创建请求记录
        #     room_id=self.room_id, room_state=self.room_state, blow_mode=self.blow_mode,
        #     target_temp=self.target_temp, request_time=timezone.now()
        # )
        # new_request_record.save()
        pass

    # 客户退房后 房间数据清零
    def clearData(self):
        self.is_free = True
        self.room_state = 0
        self.temp_mode = -1
        self.blow_mode = 1
        #self.current_temp = default_temp
        self.target_temp = default_temp
        self.fee = 0
        self.duration = 0
        self.save()


class AC(models.Model):
    ac_state = models.CharField(
        "中央空调状态", choices=ac_state_choice, max_length=64, default='close')
    temp_mode = models.SmallIntegerField(
        '制冷制热模式', choices=temp_mode_choice, default=1)

    cool_temp_highlimit = models.IntegerField('制冷温控范围最高温', default=25)
    cool_temp_lowlimit = models.IntegerField('制冷温控范围最低温', default=18)
    heat_temp_highlimit = models.IntegerField('制热温控范围最高温', default=30)
    heat_temp_lowlimit = models.IntegerField('制热温控范围最低温', default=25)
    default_temp = models.IntegerField('缺省温度', default=25)

    electric_price = models.FloatField("单位电价(元/度)", default=1)
    powerrate_H = models.FloatField('高风耗电量(度/秒)', default=1.0 / 60)
    powerrate_M = models.FloatField('中风耗电量(度/秒)', default=1.0 / 120)
    powerrate_L = models.FloatField('低风耗电量(度/秒)', default=1.0 / 180)

    # 由电价和各模式耗电速度自动得出
    feerate_H = models.FloatField('高风费率', default=1.0 / 60)
    feerate_M = models.FloatField('中风费率', default=1.0 / 120)
    feerate_L = models.FloatField('低风费率', default=1.0 / 180)

    max_load = models.IntegerField('最大带机量', default=3)
    sss_time = models.IntegerField(
        '同级请求切换时间', default=120)  # 默认120s后切换同级其他请求

    # 更新房间温度和费用，并完成调度
    def schedule(self):

        req = RequestQueue.objects.all().order_by(
            '-blow_mode', 'request_timestamp')  # 按照风速降序，请求时间增序排序
        seq = ServiceQueue.objects.all().order_by('-blow_mode', 'service_timestamp')
        #print(f"req:{req.count()} seq:{seq.count()} ")
        # 更新房间温度和计费
        rooms = Room.objects.all()
        for room in rooms:
            if room.room_state == 1:  # 运行
                if room.blow_mode == 0:  # 低风
                    room.current_temp += self.temp_mode * \
                        temp_rate[0]
                    room.fee += self.feerate_L
                elif room.blow_mode == 1:  # 中风
                    room.current_temp += self.temp_mode * \
                        temp_rate[1]
                    room.fee += self.feerate_M
                elif room.blow_mode == 2:
                    room.current_temp += self.temp_mode * \
                        temp_rate[2]
                    room.fee += self.feerate_H

                """
                这一块用于在服务器检测房间温度是否到达目标温度,到达后改变温度
                # 到达目标温度 
                if int(room.current_temp) == room.target_temp:

                    seq_out = ServiceQueue.objects.get(
                        room_id=room.room_id)
                    new_serviceRecord = (ServiceRecord(room_id=seq_out.room_id, tenant=Tenant.objects.filter(
                        date_out=None, room_id=seq_out.room_id)[0], blow_mode=seq_out.blow_mode, target_temp=seq_out.target_temp, start_time=seq_out.service_timestamp, end_time=timezone.now()))
                    new_serviceRecord.save()

                    room.room_state=2

                    room_daily_report = RoomDailyReport.objects.filter(
                        room_id=seq_out.room_id, date=seq_out.service_timestamp.date())
                    if room_daily_report.count() == 0:
                        room_daily_report = RoomDailyReport(
                            room_id=seq_out.room_id, date=seq_out.service_timestamp.date())
                    else:
                        room_daily_report = room_daily_report[0]

                    room_daily_report.schedule_count += 1
                    room_daily_report.upto_target_count+=1
                    room_daily_report.save()

                    seq_out.delete()
                    """

            else:  # 没有运行
                if int(room.current_temp) != self.default_temp:
                    # 向默认温度回温
                    room.current_temp += (-self.temp_mode * temp_rate[3])
            room.save()

        # 调度
        # 如果还可以服务
        if req.count() and self.max_load - seq.count():
            # 选出一个高优先级的送入服务队列
            req_in = []  # 存储可以服务的请求队列
            num = min(self.max_load - seq.count(), req.count())
            for i in range(num):

                req_in.append(req[i])
                new_seq = ServiceQueue(
                    room_id=req[i].room_id, room_state=1, temp_mode=self.temp_mode, blow_mode=req[i].blow_mode, target_temp=req[i].target_temp, service_timestamp=timezone.now())
                new_seq.save()

            for i in req_in:
                room = Room.objects.get(room_id=i.room_id)
                room.room_state = 1
                room.save()

                # 房间日报表调度次数加一
                room_daily_report = RoomDailyReport.objects.filter(
                    room_id=i.room_id, date=i.request_timestamp.date())
                if room_daily_report.count() == 0:
                    room_daily_report = RoomDailyReport(
                        room_id=i.room_id, date=i.request_timestamp.date())
                else:
                    room_daily_report = room_daily_report[0]

                room_daily_report.schedule_count += 1
                room_daily_report.save()

                i.delete()

        # 如果满了
        if req.count():
            req_in = []  # 存储可以替换的请求队列
            seq_out = []  # 存储被替换的服务队列
            new_seq = []  # 存储新建的服务队列，最终一起save
            new_req = []  # 存储新建的请求队列，最终一起save
            # new_serviceRecord = []  # 存储新建的服务记录
            # 优先级判断
            j = 0
            for i in range(req.count()):
                while j < seq.count():
                    if req[i].blow_mode > seq[j].blow_mode:
                        req_in.append(req[i])
                        seq_out.append(seq[j])
                        j += 1
                        break
                    j += 1

            if len(req_in):
                for i in range(len(req_in)):

                    new_seq.append(ServiceQueue(
                        room_id=req_in[i].room_id, room_state=1, temp_mode=self.temp_mode, blow_mode=req_in[i].blow_mode, target_temp=req_in[i].target_temp, service_timestamp=timezone.now()))
                    new_req.append(RequestQueue(
                        room_id=seq_out[i].room_id, room_state=3, temp_mode=self.temp_mode, blow_mode=seq_out[i].blow_mode, target_temp=seq_out[i].target_temp, request_timestamp=timezone.now()))

                    # new_serviceRecord.append(ServiceRecord(room_id=seq_out[i].room_id, tenant=Tenant.objects.filter(
                    #     date_out=None, room_id=seq_out[i].room_id)[0], blow_mode=seq_out[i].blow_mode, target_temp=seq_out[i].target_temp, start_time=seq_out[i].service_timestamp, end_time=timezone.now()))

                # 删除双方替换的请求
                for i in range(len(req_in)):
                    req_in[i].delete()
                    seq_out[i].delete()

            # 时间片判断
            req_in = []  # 存储可以替换的请求队列
            seq_out = []  # 存储被替换的服务队列
            j = seq.count()-1
            for i in range(req.count()):
                if (timezone.now() - req[i].request_timestamp).total_seconds() > self.sss_time:
                    if j >= 0:
                        if req[i].blow_mode == seq[j].blow_mode:
                            req_in.append(req[i])
                            seq_out.append(seq[j])
                            j -= 1
                        else:
                            break
                    else:
                        break
                else:
                    break

            if len(req_in):
                for i in range(len(req_in)):

                    new_seq.append(ServiceQueue(
                        room_id=req_in[i].room_id, room_state=1, temp_mode=self.temp_mode, blow_mode=req_in[i].blow_mode, target_temp=req_in[i].target_temp, service_timestamp=timezone.now()))
                    new_req.append(RequestQueue(
                        room_id=seq_out[i].room_id, room_state=3, temp_mode=self.temp_mode, blow_mode=seq_out[i].blow_mode, target_temp=seq_out[i].target_temp, request_timestamp=timezone.now()))

                    # new_serviceRecord.append(ServiceRecord(room_id=seq_out[i].room_id, tenant=Tenant.objects.filter(
                    #     date_out=None, room_id=seq_out[i].room_id)[0], blow_mode=seq_out[i].blow_mode, target_temp=seq_out[i].target_temp, start_time=seq_out[i].service_timestamp, end_time=timezone.now()))

                for i in range(len(req_in)):
                    req_in[i].delete()
                    seq_out[i].delete()

            # save队列，并更新room状态、dailyRoomReport
            print(len(new_seq))
            for i in range(len(new_seq)):
                new_seq[i].save()
                new_req[i].save()
                # new_serviceRecord[i].save()
                room = Room.objects.get(room_id=new_seq[i].room_id)
                room.room_state = 1
                room.save()
                room = Room.objects.get(room_id=new_req[i].room_id)
                room.room_state = 3
                room.save()

                room_daily_report = RoomDailyReport.objects.filter(
                    room_id=new_seq[i].room_id, date=new_seq[i].service_timestamp.date())
                if room_daily_report.count() == 0:
                    room_daily_report = RoomDailyReport(
                        room_id=new_seq[i].room_id, date=new_seq[i].service_timestamp.date())
                else:
                    room_daily_report = room_daily_report[0]

                room_daily_report.schedule_count += 1
                room_daily_report.save()

                room_daily_report = RoomDailyReport.objects.filter(
                    room_id=new_req[i].room_id, date=new_req[i].request_timestamp.date())[0]
                room_daily_report.schedule_count += 1
                room_daily_report.save()


def auto_set_feerate(sender, instance, *args, **kwargs):
    instance.feerate_H = instance.electric_price * instance.powerrate_H
    instance.feerate_M = instance.electric_price * instance.powerrate_M
    instance.feerate_L = instance.electric_price * instance.powerrate_L


pre_save.connect(auto_set_feerate, sender=AC)
