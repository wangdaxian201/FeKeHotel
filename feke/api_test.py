import sys
import requests

base_url = 'http://127.0.0.1:8000/api/'


def add_room():
    func_name = sys._getframe().f_code.co_name + '/'
    data = {
        "room_data": {
            "type_name": "",
            "room_number": "1011",
            "room_id": "",
            "room_status": "no_check_in",
            "remark": "",
            "type_id": 2
        }
    }
    response = requests.post(base_url + func_name, json=data)
    print(response.status_code)
    print(response.json())

def add_room_type():
    func_name = sys._getframe().f_code.co_name + '/'
    data = {
        "type_name": "双人间",
        "type_price": "200",
        "room_type_desc": "test_description",
    }
    response = requests.post(base_url + func_name, json=data)
    print(response.status_code)
    print(response.json())

def update_room_type():
    func_name = sys._getframe().f_code.co_name + '/'
    data = {
        "type_number": "2",
        "type_name": "四人间",
        "price": "200",
        "description": "test_description",
    }
    response = requests.post(base_url + func_name, json=data)
    print(response.status_code)
    print(response.json())


def get_all_rooms():
    """获取所有房间"""
    # 获取当前函数名
    func_name = sys._getframe().f_code.co_name + '/'
    payload = {}
    print(f'get_all_rooms: {base_url + func_name}')
    response = requests.post(base_url + func_name, json={}).json()
    print(f'get_all_rooms: {response}')


def get_all_room_types():
    """获取所有房间类型"""
    # 获取当前函数名
    func_name = sys._getframe().f_code.co_name + '/'
    payload = {}
    print(f'get_all_room_types: {base_url + func_name}')
    response = requests.post(base_url + func_name, json={}).json()
    print(f'get_all_room_types: {response}')

# update_room_type()
# get_all_rooms()
# get_all_room_types()
# add_room()
# add_room_type()

# 办理入住
def check_in():
    func_name = sys._getframe().f_code.co_name + '/'
    data = {
        "order_data": {
            'room_number': '8300',
            'room_description': 'test_description',
            'room_type': "单人间",
            'room_status': "vacant",
            'room_img': '',
        }

    }
    response = requests.post(base_url + func_name, json=data)
    print(response.status_code)
    print(response.json())

# 预定
def create_reservation():
    """预定"""
    func_name = sys._getframe().f_code.co_name + '/'
    data = {
        'room_number': '8300',
        "guest_name": "test_guest_name",
        "guest_phone": "test_guest_phone",
        "start_date": "2023-05-01",
        "end_date": "2023-05-03"
    }
    response = requests.post(base_url + func_name, json=data)
    print(response.status_code)
    print(response.json())


# 删除预定
def delete_reservation(id):
    """删除预定"""
    func_name = sys._getframe().f_code.co_name + '/'
    data = {
        'reservation_id': id,
    }
    response = requests.post(base_url + func_name, json=data)
    print(response.status_code)
    print(response.json())


def get_all_reservations():
    """获取所有预定"""
    # 获取当前函数名
    func_name = sys._getframe().f_code.co_name + '/'
    payload = {}
    print(f'get_all_reservations: {base_url + func_name} \n')
    response = requests.post(base_url + func_name, json={}).json()
    print(f'get_all_reservations: {response} \n')
    if response['result']['code'] == 50000:
        print('没有预定记录')
        return

# get_all_reservations()

# delete_reservation()

def get_order_list():
    """获取订单列表"""
    # 获取当前函数名
    func_name = 'order/' + sys._getframe().f_code.co_name + '/'
    payload = {}
    print(f'get_order_list: {base_url + func_name} \n')
    response = requests.post(base_url + func_name, json={}).json()
    print(f'get_order_list: {response} \n')
    if response['result']['code'] == 50000:
        print('没有订单记录')
        return
    else:
        print(response['result']['data'])
        return response['result']['data']


def create_order():
    """添加订单"""
    func_name = sys._getframe().f_code.co_name + '/'
    data = {
        "data": {
            "user_name": "xiaohei",
            "user_mobile": "12345678910",
            "room_number": "8300",
            "start_date": "2023-05-01",
            "end_date": "2023-05-03",
            "order_status": "unpaid",
            "order_amount": "200",
            "days": 3,
            "check_in_date": "2023-05-01",
            "check_out_date": "2023-05-03",
            "booking_platform": "wechat",
        }
    }
    response = requests.post(base_url + func_name, json=data)
    print(response.status_code)
    print(response.json())


# add_room()
get_order_list()