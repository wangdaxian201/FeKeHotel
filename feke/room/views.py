from pstats import Stats
import statistics
from django.core import serializers
from django.db import transaction
from requests import Response
from django.views.decorators.csrf import csrf_exempt

from utils.error import APIError

from .models import Reservation, Room, RoomType,  Order
import datetime
import csv
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum

from .decorators import api


@csrf_exempt
def login(request):
    return JsonResponse({"code":20000,"data":{"token":"admin-token"}})

@csrf_exempt
def info(request):
    print(f'list_api=====')
    return JsonResponse({
        "roles": ['admin'],
        "introduction": 'I am a super administrator',
        "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        "name": 'Super Admin'
    })


# 获取所有房间
@api
def get_all_rooms():
    print('get_all_rooms view')
    rooms = Room.objects.filter(is_deleted=False)
    data = [room.json() for room in rooms]
    print(f'{data=}')
    return {'data': data}

# 获取所有房间类型
@api
def get_all_room_types():
    room_types = RoomType.objects.filter(is_deleted=False)
    data = [room_type.json() for room_type in room_types]

    return {'data': data}


# 添加房间
@api
def add_room(room_data):
    print(f'bbbbbbbb')
    try:
        room_type = RoomType.objects.filter(type_name=room_data.get('room_type'))
    except RoomType.DoesNotExist:
        print(f'room_type 不存在')
        room_type = RoomType.objects.create(
            type_name='单人间',
            price=100,
            description="默认房间"
        )
    room_type_obj = RoomType.objects.get(type_name=room_data.get('room_type'))
    print(f'{room_type=}')
    try:
        room = Room.objects.create(
            room_number=room_data.get('room_number'),
            room_type=room_type_obj,
            room_description=room_data.get('room_description'),
            room_img=room_data.get('room_img'),
            room_status=room_data.get('room_status')
        )
        print(f'room: {room=}')
    except Exception as e:
        print(f'create room {e}')
    else:
        print(f'room: {room.room_number=}')
        return room.json()

# 修改房间
@api
def update_room(room_data):
    defaults = {
        'room_name': room_data.get('room_name'),
        'room_type': room_data.get('room_type'),
        'room_description': room_data.get('room_description'),
        'room_img': room_data.get('room_img'),
        'room_status': room_data.get('room_status'),
        'checkout_time': room_data.get('checkout_time'),
        'updated_time': datetime.datetime.now(),
    }
    room, created = Room.objects.update_or_create(
        room_id=room_data.get('room_id'),
        defaults=defaults,
    )
    return room.to_dict()

# 删除房间
@api
def delete_room(room_id):
    room = Room.objects.get(room_id=room_id)
    room.delete()
    return room.json()


# 添加房间类型
@api
def add_room_type(type_number, type_name, price, description):
    defaults = {
        "price": price,
        "description": description,
    }
    room_type, _ = RoomType.objects.get_or_create(
        type_number=type_number,
        type_name=type_name,
        defaults=defaults
    )
    return room_type.json()


# 修改房间类型
@api
def update_room_type(type_number, type_name, price, description):
    defaults = {
        "price": price,
        "description": description,
    }
    room_type, _ = RoomType.objects.update_or_create(
        type_number=type_number,
        type_name=type_name,
        defaults=defaults
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
    order_amount = orders.aggregate(Sum('order_amount'))['order_amount__sum']
    total_orders = orders.count()

    # 构造 CSV 数据
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="daily_report_{today}.csv"'

    writer = csv.writer(response)
    writer.writerow(['入住时间', '房间号', '房间类型', '下单平台', '入住姓名', '订单收入', '入住天数', '当日房费', '退房时间'])

    for order in orders:
        # 计算当日房费
        daily_rate = round(order.order_amount / order.days, 2)

        writer.writerow([
            order.check_in_date,
            order.room.room_number,
            order.room.room_type.type_name,
            order.booking_platform,
            order.user.name,
            order.order_amount,
            order.days,
            daily_rate,
            order.check_out_date
        ])

    # 添加当日房费总收入和订单数统计
    writer.writerow([])
    writer.writerow(['', '', '', '', '', '总收入：', order_amount])
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


@api
def create_order(data):
    """创建订单"""
    print(f'{datetime.datetime.now()} create_order')
    try:

        room = Room.objects.get(room_number=data['room_number'])
        # 查看当前房间对应房型的价格
        order_amount = room.room_type.price * data['days']
        print(f'order_amount: {order_amount}')
        order, _ = Order.objects.get_or_create(
            room=room,
            user_name=data['user_name'],
            user_mobile=data['user_mobile'],
            start_date=data.get('start_date'),
            end_date=data['end_date'],
            booking_platform=data['booking_platform'],
            order_amount=order_amount,
            order_status=data['order_status']
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
            order = Order.objects.get(id=data['id'])
            order.check_in_date = datetime.datetime.now()
            order.order_status = data.get('order_status', '已入住')
            order.save()
            room = order.room
            room.room_status = '已入住'
            room.save()
            return order.json()
    except Exception as e:
        # 回滚
        transaction.set_rollback(True)
        return {'update order error': str(e)}


"""预定"""


@api
def get_all_reservations():
    """获取预定信息"""
    try:
        reservation = Reservation.objects.all()
        if reservation:
            return {"data": [r.json() for r in reservation]}
        else:
            return {'message': 'No reservation found.'}
    except Exception as e:
        return {'message': str(e)}


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
def create_reservation(room_number, start_date, end_date, guest_name, guest_phone):
    """创建预定"""
    # 检查预定时间是否冲突
    room = check_availability(room_number, start_date, end_date)
    if not room:
        return {'message': 'Room is not available.'}

    # 检查预订时间是否大于或等于今天
    today = datetime.date.today().strftime('%Y-%m-%d')
    if start_date < today or end_date < today:
        return {'message': 'Start date should be greater than or equal to today.'}
    elif start_date > end_date:
        return {'message': '开始时间不能小于结束时间'}

    try:
        with transaction.atomic():
            reservation, status = Reservation.objects.get_or_create(
                room=room, # 房间
                start_date=start_date, # 预定开始时间
                end_date=end_date,  # 预定结束时间
                guest_name=guest_name,  # 预定人姓名
                guest_phone=guest_phone # 预定人电话
            )
            if status:
                print('Reservation created successfully.')
                print(reservation.json())
                # 预定成功
                return {'message': 'Reservation created successfully.'}
            elif not status and reservation:
                # 预定失败
                return {'message': 'Reservation exist.'}
    except Exception as e:
        # 异常发生时回滚
        transaction.rollback()
        return {'message': str(e)}


@api
def delete_reservation(reservation_id):
    """删除预定"""
    try:
        with transaction.atomic():
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.delete()
            return {'message': 'Reservation deleted successfully.'}
    except Reservation.DoesNotExist:
        return {'message': 'Reservation not found.'}
    except Exception as e:
        t = transaction.savepoint()
        transaction.savepoint_rollback(t)
        return {'message': str(e)}

@api
def update_reservation(request, reservation_id):
    """更新预定"""
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.guest_name = request.data.get('guest_name', reservation.guest_name)
        reservation.guest_phone = request.data.get('guest_phone', reservation.guest_phone)
        reservation.start_date = request.data.get('start_date', reservation.start_date)
        reservation.end_date = request.data.get('end_date', reservation.end_date)
        reservation.save()
        return Response(reservation.json())
    except Reservation.DoesNotExist:
        return Response({'message': 'Reservation not found.'}, status=statistics.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=statistics.HTTP_500_INTERNAL_SERVER_ERROR)


@api
def checkin_reservation(request, reservation_id):
    """入住"""
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        room = reservation.room
        if room.room_status != 'vacant':
            return Response({'message': 'Room is not available.'}, status=statistics.HTTP_400_BAD_REQUEST)
        room.room_status = 'occupied'
        room.save()
        return Response(reservation.json())
    except Reservation.DoesNotExist:
        return Response({'message': 'Reservation not found.'}, status=statistics.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=statistics.HTTP_500_INTERNAL_SERVER_ERROR)

