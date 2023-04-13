from room.decorator import api
from room.models import Room, RoomType, RoomTypePriceChange, Order, User
import datetime
import csv
from django.http import HttpResponse
from django.db.models import Sum


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
def add_room(room_data):
    room = Room.models.get_or_create(
        room_name=room_data.get('room_name'), 
        room_type=room_data.get('room_type'),
        room_description=room_data.get('room_description'),
        room_img=room_data.get('room_img'),
        room_status=room_data.get('room_status'),
        checkout_time=room_data.get('checkout_time')
    )

    room.save()
    return room.json()

# 修改房间
@api
def update_room(room_data):
    room = Room.objects.get(room_id=room_data.get('room_id'))
    room.room_number = room_data.get('room_number') or room.room_number
    room.room_type = room_data.get('room_type') or room.room_type
    room.room_description = room_data.get('room_description') or room.room_description
    room.room_img = room_data.get('room_img') or room.room_img
    room.room_status = room_data.get('room_status') or room.room_status
    room.checkout_time = room_data.get('checkout_time') or room.checkout_time
    room.updated_time = datetime.datetime.now()
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
    room_type = RoomType.objects.get_or_create(
        room_type_name=room_type_name, 
        room_type_desc=room_type_desc
    )
    room_type.save()
    return room_type.json()


# 修改房间类型
@api
def update_room_type(room_type_id, room_type_name, room_price, room_type_desc):
    room_type = RoomType.objects.get(room_type_id=room_type_id)
    room_type.price = room_price if room_price else room_type.price
    room_type.type_name = room_type_name if room_type_name else room_type.type_name
    room_type.type_desc = room_type_desc if room_type_desc else room_type.type_desc
    room_type.updated_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    room_type.save()
    if room_price != room_type.price:
        # 价格变动记录
        RoomTypePriceChange.objects.create(
            room_type=room_type,
            price=room_type.price,
            created_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    return room_type.json()


@api
def delete_room_type(room_type_id):
    """删除房间类型"""
    room_type = RoomType.objects.get(room_type_id=room_type_id)
    room_type.delete()
    return room_type.json()


def daily_report(request):
    # 获取今天的日期
    today = datetime.datetime.now().date()

    # 查询今天的订单
    orders = Order.objects.filter(checkin_date__lte=today, checkout_date__gte=today)

    # 计算当日房费总收入和订单数
    total_income = orders.aggregate(Sum('income'))['income__sum']
    total_orders = orders.count()

    # 构造 CSV 数据
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="daily_report_{today}.csv"'

    writer = csv.writer(response)
    writer.writerow(['入住时间', '房间号', '房间类型', '下单平台', '入住姓名', '订单收入', '入住天数', '当日房费', '退房时间'])

    for order in orders:
        # 计算当日房费
        daily_rate = round(order.income / order.days, 2)

        writer.writerow([
            order.check_in_date,
            order.room.room_number,
            order.room.room_type.type_name,
            order.booking_platform,
            order.user.name,
            order.income,
            order.days,
            daily_rate,
            order.check_out_date
        ])

    # 添加当日房费总收入和订单数统计
    writer.writerow([])
    writer.writerow(['', '', '', '', '', '总收入：', total_income])
    writer.writerow(['', '', '', '', '', '订单数：', total_orders])

    return response


@api
def get_today_order_list(date):
    """获取当日订单列表"""
    if not date:
        return {'error': 'date is required'}
    try:
        check_in_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return {'error': 'invalid date format, should be YYYY-MM-DD'}
    
    orders = Order.objects.filter(check_in_date__lte=check_in_date, check_out_date__gte=check_in_date, is_canceled=False)
    result = []
    for order in orders:
        days = (order.check_out_date - order.check_in_date).days
        income = order.income
        if days:
            income = income / days
        data = {
            'check_in_time': order.check_in_date.strftime('%Y-%m-%d %H:%M:%S'),
            'room_number': order.room.room_number,
            'room_type': order.room.room_type.type_name,
            'booking_platform': order.booking_platform,
            'payment_platform': order.payment_platform,
            'user_name': order.user.name,
            'total_income': order.income,
            'days': days,
            'daily_price': income,
            'check_out_time': order.check_out_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        result.append(data)
    return result


@api
def get_order_list():
    """获取订单列表"""
    orders = Order.objects.all()
    result = []
    for order in orders:
        data = {
            'check_in_time': order.check_in_date.strftime('%Y-%m-%d %H:%M:%S'),
            'room_number': order.room.room_number,
            'room_type': order.room.room_type.type_name,
            'booking_platform': order.booking_platform,
            'payment_platform': order.payment_platform,
            'user_name': order.user.name,
            'total_income': order.income,
            'days': (order.check_out_date - order.check_in_date).days,
            'daily_price': order.income / (order.check_out_date - order.check_in_date).days,
            'check_out_time': order.check_out_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        result.append(data)
    return result


@api
def create_user(name, mobile, email, id_card, gender, address):
    """创建用户"""
    user = User.objects.get_or_create(
        name=name,
        mobile=mobile,
        id_card=id_card,
        email=email,
        gender=gender,
        address=address
    )
    user.save()
    return user.json()