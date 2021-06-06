from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from . import forms
from .models import Waiter, Tenant, Manager, ACAdministrator,AC
from datetime import date
# Create your views here.

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
    # ('scheduler',"interval", seconds=1) #用interval方式循环，每一秒执行一次
    #@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10', id='task_time')

    @register_job(scheduler, 'interval', seconds=10, replace_existing=True)
    def my_schedule_task():
        ac = AC.objects.all()

        if ac.count():
            ac = ac[0]
        else:
            ac = AC()
            ac.save()
        ac.schedule()

   # 监控任务    
    register_events(scheduler)

   # 调度器开始
    scheduler.start()
except Exception as e:
    print(e)
  # 报错则调度器停止执行
    scheduler.shutdown()

 

def index(request):
    # if not request.session.get('is_login', None):
    #     return redirect('/login/')
    print("nlsdfkja")
    return render(request, 'index.html')

# 登录界面


def login(request):
    # if request.session.get('is_login', None):  # 不允许重复登录
    #     return HttpResponse("< script >alert('不允许重复登录')< /script >")
    #     return redirect('/index/')
    if request.method == "POST":
        # 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值
        username_ = request.POST.get('username')
        password_ = request.POST.get('password')
        print(username_)
        print(password_)
        # 房客
        try:
            tenant = Tenant.objects.get(username=username_)
        except:
            tenant = None
        if tenant:
            print("2")
            if tenant.password == password_:
                request.session['is_login'] = True
                request.session['user_id'] = tenant.id
                request.session['user_name'] = tenant.username
                print("3")
                return JsonResponse({"role": "Tenant", "room_id": tenant.room_id}, safe=False)
        # 经理
        try:
            manager = Manager.objects.get(username=username_)
        except:
            print("4")
            manager = None
        if manager:
            print("5")
            if manager.password == password_:
                print("6")
                request.session['is_login'] = True
                request.session['user_id'] = manager.id
                request.session['user_name'] = manager.username
                return JsonResponse({"role": "Manager"}, safe=False)
        # 前台
        try:
            waiter = Waiter.objects.get(username=username_)
        except:
            print("4")
            waiter = None
        if waiter:
            print("5")
            if waiter.password == password_:
                print("6")
                request.session['is_login'] = True
                request.session['user_id'] = waiter.id
                request.session['user_name'] = waiter.username
                return JsonResponse({"role": "Waiter"}, safe=False)
        # 管理员
        try:
            min = ACAdministrator.objects.get(username=username_)
        except:
            print("4")
            min = None
        if min:
            print("5")
            if min.password == password_:
                print("6")
                request.session['is_login'] = True
                request.session['user_id'] = min.id
                request.session['user_name'] = min.username
                return JsonResponse({"role": "Administrator"}, safe=False)

        else:
            return HttpResponse(status=404)

    # 对于非POST方法发送数据时（比如GET方法请求页面），返回空的表单，让用户可以填入数据
    return render(request, 'index.html')


def register(request):
    pass
    return render(request, 'backend/register.html')


def logout(request):
    pass
    return redirect('/index/')

# 返回给浏览器空闲房间id 若为空则返回空字符串


def freeRoomList(request):
    w = Waiter.objects.all()[0]
    rooms = "-"
    print(w.getFreeRooms())
    rooms = rooms.join([i["pk"] for i in w.getFreeRooms()])
    return HttpResponse(rooms)  # "2-3-4-5"
    return JsonResponse(w.getFreeRooms(), safe=False)  # 非字典类型序列化要设置安全模式为False


def getRoomsData(request):
    w = Waiter.objects.all()[0]
    print(w.getRoomsData())
    return JsonResponse(w.getRoomsData(), safe=False)


def openRoom(request):
    w = Waiter.objects.all()[0]
    room_id = request.POST.get('room_id', False)
    if room_id == False:
        return HttpResponse("room_id未成功post", status=404)
    username = request.POST['username']
    password = request.POST['password']
    print(username)
    print(password)
    w.openRoom(room_id, username, password)
    return HttpResponse("success")


def closeRoom(request):
    w = Waiter.objects.all()[0]
    room_id = request.GET.get('room_id', False)
    if room_id == False:
        return HttpResponse("room_id未成功通过get方法发送给服务器", status=404)
    w.closeRoom(room_id)
    return HttpResponse("success")


def getBill(request):
    room_id = request.GET.get("room_id", False)
    tenant = Tenant.objects.filter(date_out=None, room_id=room_id)[0]
    tenant_id = tenant.pk
    print(tenant_id)
    # tenant_id = request.GET.get("tenant_id", False)  #原本想直接传tenant_id主键，后来发现前端没有保存，只能传room_id
    if tenant_id == False:
        return HttpResponse("tenant_id未成功通过get方法发送给服务器", status=404)
    w = Waiter.objects.all()[0]
    bill = w.getBill(tenant_id)
    return JsonResponse(bill)


def getDetail(request):
    room_id = request.GET.get("room_id", False)
    tenant = Tenant.objects.filter(date_out=None, room_id=room_id)[0]
    tenant_id = tenant.pk
    #tenant_id = request.GET.get("tenant_id", False)
    if tenant_id == False:
        return HttpResponse("tenant_id未成功通过get方法发送给服务器", status=404)
    w = Waiter.objects.all()[0]
    detail = w.getDetail(tenant_id)
    print(detail)

    for i in detail:
        if(i["temp_mode"] == -1):
            i["temp_mode"] = "制冷模式"
        elif(i["temp_mode"] == 1):
            i["temp_mode"] = "制热模式"
        if(i["blow_mode"] == 0):
            i["blow_mode"] = "低风"
        elif(i["blow_mode"] == 1):
            i["blow_mode"] = "中风"
        elif(i["blow_mode"] == 2):
            i["blow_mode"] = "高风"
    print(detail)
    return JsonResponse(detail, safe=False)


# Manager api

def getReporter(request):
    date_begin = request.GET.get("date_begin", False)
    date_end = request.GET.get("date_end", False)
    import time
    t = time.strptime(date_begin, "%Y-%m-%d")
    y, m, d = t[0:3]
    date_begin = date(y, m, d)
    t = time.strptime(date_end, "%Y-%m-%d")
    y, m, d = t[0:3]
    date_end = date(y, m, d)
    if not date_begin or not date_end:
        return HttpResponse("dateRange未成功通过get方法发送给服务器", status=404)
    m = Manager.objects.all()[0]
    reporter = m.getReporter(date_begin, date_end)
    return JsonResponse(reporter, safe=False)
