后端：

* 删除

![image-20210606204647050](C:\Users\王梦超\AppData\Roaming\Typora\typora-user-images\image-20210606204647050.png)

* 删除 /backend/migrations，只保留init

  ![image-20210606204839144](C:\Users\王梦超\AppData\Roaming\Typora\typora-user-images\image-20210606204839144.png)

* 修改 /mysite/setting.py文件，设置为自己mysql的密码，

  （可能报错没有django这个数据库，那就去mysql shell里手动建立这个数据库）

![image-20210606205053700](C:\Users\王梦超\AppData\Roaming\Typora\typora-user-images\image-20210606205053700.png)

* 打开cmd ，cd 到有manage.py这个文件的目录下
* 执行  python manage.py makemigtations
* 执行 python manage.py  migrate   迁移数据库
* 执行 python manage.py createsuperuser,  输入用户名密码，然后就可以在django自带的管理页面（127.0.0.1/8000/admin）上管理数据库
* 执行  python manage.py runserver 运行后端服务器



前端：

文件名是：vue2_frontend (瞎起的)

这是vue2生成的项目脚手架

* 额，好像能直接运行
* 我是用![image-20210606210024991](C:\Users\王梦超\AppData\Roaming\Typora\typora-user-images\image-20210606210024991.png)打开该项目直接运行
* 但好像需要安装npm之类的东西，忘记了。