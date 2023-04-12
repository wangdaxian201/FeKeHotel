from django.db import models

# Create your models here.

# 房间表
class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=30)
    # 关联房间类型表 多对一
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    room_price = models.IntegerField()
    room_status = models.CharField(max_length=30)
    room_desc = models.CharField(max_length=30)
    room_img = models.CharField(max_length=30)
    room_num = models.IntegerField()
    room_status_name = models.CharField(max_length=30)
    room_status_desc = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'room'
    
    def __str__(self):
        return self.room_name
    
    def search_room_type_name(self):
        return RoomType.objects.filter(room_type_id=self.room_type.id).name
    
    def json(self):
        return {
            'room_id':self.room_id,
            'room_name':self.room_name,
            'room_type': self.search_room_type_name(),
            'root_type_desc':self.room_type.room_type_desc,
            'room_price':self.room_price,
            'room_status':self.room_status,
            'room_desc':self.room_desc,
            'room_img':self.room_img,
            'room_num':self.room_num,
            'room_status_name':self.room_status_name,
            'room_status_desc':self.room_status_desc
        }

# 房间类型表
class RoomType(models.Model):
    room_type_id = models.AutoField(primary_key=True)
    room_type_name = models.CharField(max_length=30)
    room_type_desc = models.CharField(max_length=30)
    # 关联房间表 一对多
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'room_type'
    
    def __str__(self):
        return self.room_type_name
    
    def json(self):
        return {
            'room_type_id':self.room_type_id,
            'room_type_name':self.room_type_name,
            'room_type_desc':self.room_type_desc
        }

# 房间预定表
class RoomOrder(models.Model):
    room_order_id = models.AutoField(primary_key=True)
    # 关联房间表 多对一
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # 关联用户表 多对一
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    room_order_time = models.DateTimeField()
    room_order_status = models.CharField(max_length=30)
    room_order_status_desc = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'room_order'
    
    def __str__(self):
        return self.room_order_id
    
    def json(self):
        return {
            'room_order_id':self.room_order_id,
            'room_name':self.room.room_name,
            'user_name':self.user.user_name,
            'room_order_time':self.room_order_time,
            'room_order_status':self.room_order_status,
            'room_order_status_desc':self.room_order_status_desc
        }

