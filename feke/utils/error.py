class APIError(Exception):
    SERVER_ERROR = (50001, 'Server Inner Error')
    INVALID_PARAM = (50002, 'Invalid Parameter: %s')
    PARAM_MISSING = (50003, 'Parameter is Missing: %s')
    FILE_MISSING = (50004, 'Task File Missing %s')
    SHARD_NOT_FOUND = (50005, 'No Available Shard')
    TASK_NOT_FOUND = (50006, 'Invalid Taskid: %s')
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
