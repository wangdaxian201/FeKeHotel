import datetime

from django.db import transaction
from .decorators import api

from room.models import Order, Room
from utils.error import APIError
from utils.tools import compute_checkin_days



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
        order_amount = order.order_amount
        if days:
            order_amount = order_amount / days
        data = {
            'check_in_time': order.check_in_date.strftime('%Y-%m-%d %H:%M:%S'),
            'room_number': order.room.room_number,
            'room_type': order.room.room_type.type_name,
            'booking_platform': order.booking_platform,
            'payment_platform': order.payment_platform,
            'user_name': order.user_name,
            'order_amount': order.order_amount,
            'days': days,
            'daily_price': order_amount,
            'check_out_time': order.check_out_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        result.append(data)
    return result


@api
def get_order_list():
    """获取订单列表"""
    print(f'{datetime.datetime.now()} get_order_list')
    orders = Order.objects.all()
    result = []
    result = [order.json() for order in orders]
    return {"data": result}


def check_availability(room_number, start_date, end_date):
    """检查预定时间是否冲突和房间是否可用"""
    try:
        room = Room.objects.get(room_number=room_number)
    except Room.DoesNotExist:
        raise APIError(APIError.room_not_found)

    # 检查预定时间是否冲突
    if not room.is_reserved(start_date, end_date):
        raise APIError(APIError.room_not_reserved)

    return room


@api
def create_order(data):
    """
        创建订单 订单时间不可以与已有订单冲突 入住时间不能和当前房间的所有订单中的开始时间重复
        入住时间不能在当前房间的所有订单中有效期内
        args:
            room_number: 房间号
            user_name: 客户姓名
            user_mobile: 客户手机号
            start_date: 入住时间
            end_date: 离店时间
            booking_platform: 预定平台
            order_status: 订单状态
    """
    print(f'{datetime.datetime.now()} create_order')
    checkin_days = compute_checkin_days(data['start_date'], data['end_date'])

    # 检查预定时间是否冲突
    room = check_availability(data['room_number'], data['start_date'], data['end_date'])
    if not room:
        return {'message': 'Room is not available.'}
    try:
        room = Room.objects.get(room_number=data['room_number'])
        # 计算订单金额 根据房间类型的价格和入住天数计算
        order_amount = room.room_type.price * checkin_days

        order, _ = Order.objects.get_or_create(
            room=room,
            user_name=data['user_name'],
            user_mobile=data['user_mobile'],
            start_date=data.get('start_date'),
            end_date=data['end_date'],
            booking_platform=data['booking_platform'],
            order_amount=order_amount,
            order_status=data['order_status'],
            payment_platform=data['payment_platform'],
        )
        if not _:
            return {'message': 'order already exists'}
        return order.json()
    except Exception as e:
        return {'create order error': str(e)}


@api
def delete_order(order_id):
    """删除订单"""
    print(f'{datetime.datetime.now()} delete_order')
    order = Order.objects.get(id=order_id)
    order.delete()
    return order.json()


@api
def update_order(data):
    """办理入住"""
    print(f'{datetime.datetime.now()} update_order')
    try:
        with transaction.atomic():
            order = Order.objects.filter(id=data.get("order_id"), ).first()
            order.check_in_date = datetime.datetime.now()
            order.order_status = data.get('order_status', "unpaid")
            order.save()
            room = order.room
            # 如果有人入住，且房间为未入住状态 房间状态改为已入住
            if order.order_status == "no_check_in":
                room.room_status = "check_in"
                room.save()
            else:
                return {'message': 'order status is not no_check_in'}
            return order.json()
    except Exception as e:
        # 回滚
        transaction.set_rollback(True)
        return {'update order error': str(e)}

