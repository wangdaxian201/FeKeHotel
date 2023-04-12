from room.decorator import api
from room.models import Room, RoomType

# 获取所有房间
@api
def get_all_rooms():
    rooms = Room.objects.all()
    return [room.json() for room in rooms]

# 获取所有房间类型
@api
def get_all_room_types():
    room_types = RoomType.objects.all()
    return [room_type.json() for room_type in room_types]

# 添加房间
@api
def add_room(room_name, room_type, room_price, room_desc, room_img, room_num, room_status_name, room_status_desc):
    room = Room.models.get_or_create(
        room_name=room_name, 
        room_type=room_type, 
        room_price=room_price, 
        room_desc=room_desc, 
        room_img=room_img, 
        room_num=room_num, 
        room_status_name=room_status_name, 
        room_status_desc=room_status_desc
    )

    room.save()
    return room.json()

# 修改房间
@api
def update_room(room_id, room_name, room_type, room_price, room_desc, room_img, room_num, room_status_name, room_status_desc):
    room = Room.objects.get(room_id=room_id)
    room.room_name = room_name
    room.room_type = room_type
    room.room_price = room_price
    room.room_desc = room_desc
    room.room_img = room_img
    room.room_num = room_num
    room.room_status_name = room_status_name
    room.room_status_desc = room_status_desc
    room.save()
    return room.json()

# 删除房间
@api
def delete_room(room_id):
    room = Room.objects.get(room_id=room_id)
    room.delete()
    return room.json()

# 添加房间类型
@api
def add_room_type(room_type_name, room_type_desc):
    room_type = RoomType.objects.get_or_create(room_type_name=room_type_name, room_type_desc=room_type_desc)
    room_type.save()
    return room_type.json()

# 修改房间类型
@api
def update_room_type(room_type_id, room_type_name, room_type_desc):
    room_type = RoomType.objects.get(room_type_id=room_type_id)
    room_type.room_type_name = room_type_name
    room_type.room_type_desc = room_type_desc
    room_type.save()
    return room_type.json()

# 删除房间类型
@api
def delete_room_type(room_type_id):
    room_type = RoomType.objects.get(room_type_id=room_type_id)
    room_type.delete()
    return room_type.json()

# 预定房间
@api
def reserve_room(room_id, user_id, reserve_start_time, reserve_end_time, reserve_status_name, reserve_status_desc):
    # 在预定时间段内，房间的状态为已预定
    room = Room.objects.get(room_id=room_id)
    room.room_status_name = '已预定'
    room.room_status_desc = '已被预定'
    room.save()
    