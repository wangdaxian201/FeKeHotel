from datetime import timedelta
import datetime
from django.db import models
from django.db.models import Q
from utils.tools  import datetime_to_timestamp_in_milliseconds

    
class RoomType(models.Model):
    type_number = models.CharField(max_length=50, verbose_name='房间类型编号')
    type_name = models.CharField(max_length=50, verbose_name='房间类型名称')
    price = models.IntegerField(default=150,  verbose_name='价格')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '房间类型'
        verbose_name_plural = '房间类型'

    def __str__(self):
        return self.type_name
    
    def natural_key(self):
        return (self.some_unique_field,)
    
    # 查询当前房型所有空房
    def vacant_rooms(self):
        return self.room_set.filter(Q(room_status='vacant') & Q(is_deleted=False))
    
    # 查询当前房型是所有入住的房间
    def occupied_rooms(self):
        return self.room_set.filter(Q(room_status='occupied') & Q(is_deleted=False))
    
    # 查询当前房型所有维修中的房间
    def maintenance_rooms(self):
        return self.rooms.filter(Q(room_status='maintenance') & Q(is_deleted=False))
    
    # 查询当前房型所有房间
    def all_rooms(self):
        return self.rooms.filter(is_deleted=False)
    
    # 查询当前房型所有房间数量
    def all_rooms_count(self):
        return self.room_set.filter(is_deleted=False).count()
    
    def available_rooms(self, date_obj):
        total_rooms = self.rooms.count()
        reservations = self.reservations.filter(
            date=date_obj
        ).aggregate(
            num_reserved=models.Sum('num_rooms')
        )['num_reserved'] or 0
        return total_rooms - reservations

    def price_for_date(self, date_obj):
        try:
            price = self.room_type_prices.get(
                start_date__lte=date_obj,
                end_date__gte=date_obj
            ).price
        except RoomTypePrice.DoesNotExist:
            price = self.price
        return price
    
    def json(self):
        return {
            'type_id': self.id,
            'type_number': self.type_number,
            'type_name': self.type_name,
            'price': self.price,
            'description': self.description,
            'created_time': self.created_time,
            'updated_time': self.updated_time
        }



class Room(models.Model):
    room_number = models.CharField(max_length=50, verbose_name='房间号')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms', verbose_name='房间类型')
    status_choices = (
        ('vacant', '未入住'),
        ('occupied', '已入住'),
        ('maintenance', '维修中')
    )
    room_status = models.CharField(max_length=20, choices=status_choices, verbose_name='房间状态')
    room_description = models.TextField(blank=True, null=True, default='', verbose_name='房间描述')
    room_img = models.ImageField(upload_to='room_img', blank=True, null=True, verbose_name='房间图片')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    # 是否被删除
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '房间'
        verbose_name_plural = '房间'

    def __str__(self):
        return self.room_number
    
    def is_available(self, query_date):
        # 获取该房间已有的所有订单
        orders = Order.objects.filter(room=self)
        if not orders:
            return True
        for i in orders:
            if str(i.check_in_date) <= query_date <= str(i.check_out_date):
                return False
        return True

    def is_reserved(self, start_date, end_date):
        # 获取该房间已有的所有订单
        print('start_date: ', start_date)
        if str(start_date) == str(end_date):
            print('start_date == end_date')
            return False
        reservations = Order.objects.filter(room=self)
        if not reservations:
            return True
        # 检查预订时间段是否与现有订单时间段有重叠
        for i in reservations:
            print(i.start_date, i.end_date)
            if str(i.start_date) == start_date or str(i.end_date) == end_date:
                return False
            if str(i.start_date) <= start_date <= str(i.end_date) or str(i.start_date) <= end_date <= str(i.end_date):
                return False
        return True

    @classmethod
    def get_all_rooms_by_room_type(cls, room_type_id):
        return cls.objects.filter(room_type=room_type_id)

    def json(self):
        return {
            'room_id': self.id,
            'room_number': self.room_number,
            'type_name': self.room_type.type_name,
            'type_id': self.room_type.id,
            'room_status': self.room_status,
            'remark': self.room_description,
        }



class RoomTypePrice(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='prices')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('room_type', 'start_date', 'end_date')

    def to_json(self):
        return {
            "type_id": self.id,
            'room_type': self.room_type.to_json(),
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'price': str(self.price)
        }


class Order(models.Model):
    user_name = models.CharField(max_length=50, null=False, verbose_name='用户名')
    user_mobile = models.CharField(max_length=50, null=True, verbose_name='用户电话')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name='预订开始日期')
    end_date = models.DateField(verbose_name='预订结束日期')
    check_in_date = models.DateField(null=True, verbose_name='入住日期')
    check_out_date = models.DateField(null=True, verbose_name='退房日期')
    payment_platform_choices = (
        ('cash', '现金'),
        ('alipay', '支付宝'),
        ('wechat', '微信')
    )
    order_status_choices = (
        ('unpaid', '未付款'),
        ('paid', '已付款'),
        ('canceled', '已取消')
    )
    room_status_choices = (
        ('no_check_in', '未入住'),
        ('occupied', '已入住'),
        ('maintenance', '维修中')
    )
    booking_platform = models.CharField(max_length=50, verbose_name='下单平台')
    payment_platform = models.CharField(max_length=20, null=True, choices=payment_platform_choices, verbose_name='付款方式')
    days = models.IntegerField(verbose_name='入住天数', default=0)
    order_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='订单金额')
    order_status = models.CharField(max_length=20, choices=order_status_choices, default='unpaid', verbose_name='订单状态') # 已付款，未付款
    room_status = models.CharField(max_length=20, choices=room_status_choices, default='no_check_in', verbose_name='房间状态') # 未入住，已入住，已退房
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_canceled = models.BooleanField(default=False, verbose_name='是否取消')

    def __str__(self):
        return f'{self.user.name}订单'

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def json(self):
        # 检查是件是否为 datetime 类型，如果是则转换为字符串
        check_date = lambda x: x.isoformat() if not isinstance(x, str) else x
        print(f'{type(self.start_date)=}')
        print(f'{type(self.end_date)=}')
        print(f'{type(self.check_in_date)=}')
        print(f'{type(self.check_out_date)=}')
        return {
            'order_id': self.id,
            'user_name': self.user_name,
            'user_mobile': self.user_mobile,
            'room': self.room.json(),
            'room_number': self.room.room_number,
            'room_type': self.room.room_type.type_name,
            'start_date':  check_date(self.start_date),
            'end_date': check_date(self.end_date),
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'booking_platform': self.booking_platform,
            'payment_platform': self.payment_platform,
            'days': self.days,
            'order_amount': str(self.order_amount),
            'order_status': self.order_status,
            'room_status': self.room.room_status,
            'created_time': datetime_to_timestamp_in_milliseconds(self.created_time),
            'updated_time': datetime_to_timestamp_in_milliseconds(self.updated_time),
            'is_canceled': self.is_canceled
        }


class Reservation(models.Model):
    """预定表"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255)
    guest_phone = models.CharField(max_length=20)
    start_date = models.DateField(verbose_name='生效日期')
    end_date = models.DateField(verbose_name='到期日期')
    reserve_time = models.DateTimeField(auto_now_add=True, verbose_name='预定时间')

    def __str__(self):
        return f"{self.guest_name} - {self.room.room_name} - {self.start_date} to {self.end_date}"
    
    def json(self):
        return {
            'id': self.id,
            'room_id': self.room.room_type.id,
            'room_type': self.room.room_type.type_name,
            'guest_name': self.guest_name,
            'guest_phone': self.guest_phone,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'reserve_time': str(self.reserve_time)
        }