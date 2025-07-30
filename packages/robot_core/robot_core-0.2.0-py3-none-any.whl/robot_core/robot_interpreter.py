import base64
import codecs
import importlib
import json
import os
import sys

import debugpy
from robot_base import log_util

if sys.stdout.encoding is None or sys.stdout.encoding.upper() != "UTF-8":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
if sys.stderr.encoding is None or sys.stderr.encoding.upper() != "UTF-8":
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")


def main(raw_input):
    robot_raw_inputs = base64.b64decode(raw_input).decode("utf-8")
    robot_inputs = json.loads(robot_raw_inputs)

    # os_sleep.start_prevent_os_sleep()
    init_log(robot_inputs)
    args = robot_inputs.get("inputs", {})
    if args is None:
        args = {}

    if robot_inputs["environment_variables"] is not None:
        for env_key, env_value in robot_inputs["environment_variables"].items():
            if env_value is not None:
                os.environ[env_key] = env_value

    _insert_sys_path(robot_inputs["sys_path_list"])

    mod = importlib.import_module(robot_inputs["mod"])

    try:
        log_util.Logger.get_logger().info("流程开始运行")
        if robot_inputs.get("debug", False):
            debugpy.listen(("127.0.0.1", robot_inputs.get("debug_port", 5678)))
            debugpy.wait_for_client()
        result = mod.main(**args)
        print(json.dumps(result, default=custom_default))
        log_util.Logger.get_logger().info("流程结束运行")
    except Exception as e:
        log_util.Logger.get_logger().error(e)
        log_util.Logger.get_logger().info("流程运行失败")
        raise e


def init_log(robot_inputs):
    if "log_path" in robot_inputs:
        log_util.Logger(robot_inputs["log_path"], robot_inputs["log_level"])
    else:
        log_util.Logger("", robot_inputs["log_level"])


def _insert_sys_path(sys_path_list):
    for sys_path in sys_path_list:
        sys.path.insert(0, sys_path)


def custom_default(obj):
    if hasattr(obj, "__dict__"):
        # 如果是自定义类实例，只序列化其可序列化的属性
        return {
            k: v
            for k, v in obj.__dict__.items()
            if isinstance(v, (str, int, float, list, dict, bool))
        }
    else:
        # 对于其他不可序列化的对象，返回 None 或其他默认值
        return None
