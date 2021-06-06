from django.contrib import admin
from . import models
# Register your models here.


class tenantAdmin(admin.ModelAdmin):
    # 设置管理后台数据库显示哪些字段
    list_display = ['id', 'username', 'password']


admin.site.register(models.Tenant, tenantAdmin)
admin.site.register(models.Waiter)
admin.site.register(models.ACAdministrator)
admin.site.register(models.Manager)

admin.site.register(models.Room)
admin.site.register(models.RequestRecord)
admin.site.register(models.AC)
admin.site.register(models.RequestQueue)
admin.site.register(models.ServiceQueue)
admin.site.register(models.ServiceRecord)
admin.site.register(models.RoomDailyReport)
