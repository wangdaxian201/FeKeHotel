from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, verbose_name='姓名')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    gender_choices = (
        ('male', '男'),
        ('female', '女')
    )
    gender = models.CharField(max_length=10, choices=gender_choices, verbose_name='性别')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name='地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.name
    
    def json(self):
        return {
            'name': self.name,
            'mobile': self.mobile,
            'id_card': self.id_card,
            'gender': self.gender,
            'email': self.email,
            'address': self.address
        }
    
    
class RoomType(models.Model):
    type_name = models.CharField(max_length=50, verbose_name='房间类型名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '房间类型'
        verbose_name_plural = '房间类型'

    def __str__(self):
        return self.type_name

    def json(self):
        return {
            'type_name': self.type_name,
            'price': self.price,
            'description': self.description,
            'created_time': self.created_time,
            'updated_time': self.updated_time
        }


class Room(models.Model):
    room_number = models.CharField(max_length=50, verbose_name='房间号')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='房间类型')
    status_choices = (
        ('vacant', '未入住'),
        ('occupied', '已入住'),
        ('maintenance', '维修中')
    )
    room_status = models.CharField(max_length=20, choices=status_choices, verbose_name='房间状态')
    checkout_time = models.DateTimeField(blank=True, null=True, verbose_name='退房时间')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '房间'
        verbose_name_plural = '房间'

    def __str__(self):
        return self.room_number

    def json(self):
        return {
            'room_number': self.room_number,
            'room_type': self.room_type,
            'room_status': self.room_status,
            'checkout_time': self.checkout_time,
            'created_time': self.created_time,
            'updated_time': self.updated_time
        }



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    payment_platform_choices = (
        ('cash', '现金'),
        ('alipay', '支付宝'),
        ('wechat', '微信')
    )
    booking_platform = models.CharField(max_length=50, verbose_name='下单平台')
    payment_platform = models.CharField(max_length=20, choices=payment_platform_choices, verbose_name='付款平台')
    days = models.IntegerField(verbose_name='入住天数', default=0)
    order_amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_status = models.CharField(max_length=10, default='unpaid')
    income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='收入', default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_canceled = models.BooleanField(default=False, verbose_name='是否取消')

    def __str__(self):
        return f'{self.user.username}订单'

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def json(self):
        return {
            'user': self.user,
            'room': self.room,
            'check_in_date': self.check_in_date,
            'check_out_date': self.check_out_date,
            'payment_platform': self.payment_platform,
            'order_amount': self.order_amount,
            'order_status': self.order_status,
            'created_time': self.created_time,
            'updated_time': self.updated_time,
            'is_canceled': self.is_canceled,
            'income': self.income,
            'days': self.days
            
        }

# 记录房型的价格变动
class RoomTypePriceChange(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'room_type_price_change'
        verbose_name = '房型价格变动'
        verbose_name_plural = '房型价格变动'

    def __str__(self):
        return f'{self.room_type}价格变动'

    def json(self):
        return {
            'room_type': self.room_type,
            'price': self.price,
            'created_time': self.created_time
        }