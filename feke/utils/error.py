class APIError(Exception):
    SERVER_ERROR = (50001, 'Server Inner Error')
    INVALID_PARAM = (50002, 'Invalid Parameter: %s')
    PARAM_MISSING = (50003, 'Parameter is Missing: %s')
    FILE_MISSING = (50004, 'Task File Missing %s')
    SHARD_NOT_FOUND = (50005, 'No Available Shard')
    REQUEST_BODY_ERROR = (50007, 'Request Body Error')
    AUTH_FAILED = (50008, 'Auth Failed!')
    INVALID_MONITOR = (50009, 'Invalid Monitor: %s')
    SWEEP_AXIS_DONT_AGREE = (50010, 'Sweep Error: %s')
    UNEXPECT_PARAM = (50011, 'Unexpected Keyword Argument : %s')
    MONITOR_OUT_RANGE = (50012, 'Monitor Index Out of Range')
    INDEX_OUT_OF_RANGE = (50013, 'Index Out of Range')
    FAILED_GET_SPACE = (50014, 'Failed to Get User Space')
    SPACE_NOT_ENOUGH = (50015, 'User Space Not Enough')
    SOLVER_JSON_KEY_NOTFOUND = (50017, "solver json not key %s")
    SOLVER_TRY_ERROR = (50018, "%s")
    room_not_found = (50019, "Room Not Found")
    room_not_available = (50020, "Room Not available")
    room_not_reserved = (50021, "Room Not reserved")
    room_update_failed = (50022, "Room Update Failed")
    room_type_not_found = (50023, "Room Type Not Found")
    room_add_failed = (50024, "Room Add Failed")
    # 59001 - 59999 用户级提示
    MODE_EXPANSION_SWEEP_PARAM_ERROR = (
        50016,
        "Mode expansion result missing possibly because the parameters were incorrect. "
        "Please check project before simulation. ")
    USER_IMPORT = (50020, "not support user import mode information!")
    RESULTS_LENGTH_NOT_EQUAL = (59001, 'Sweep Results are Not the Same Length')

    def __init__(self, error, *args):
        self.code = error[0]
        self.msg = error[1] if not args else error[1] % args


# 定义成功信息类
class Success(object):
    # 定义4种响应码 添加成功，添加失败，删除成功，删除失败, 更新成功, 更新失败
    add_success = (20001, '%s Add Success')
    add_failed = (20002, '%s Add Failed')
    delete_success = (20003, '%s Delete Success')
    delete_failed = (20004, '%s Delete Failed')
    update_success = (20005, '%s Update Success')
    update_failed = (20006, '%s Update Failed')

    # 定义一个初始化方法
    def __init__(self, error, *args):
        self.code = error[0]
        self.msg = error[1] if not args else error[1] % args
