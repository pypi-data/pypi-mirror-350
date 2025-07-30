# -*- coding:utf8 -*-
import base64
import codecs
import json
import logging
import os
import sys
from io import StringIO
from typing import Dict, Optional

from pydantic import BaseModel, Field

if sys.stdout.encoding is None or sys.stdout.encoding.upper() != "UTF-8":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
if sys.stderr.encoding is None or sys.stderr.encoding.upper() != "UTF-8":
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")


class PythonREPL(BaseModel):
    """Simulates a standalone Python REPL."""

    globals: Optional[Dict] = Field(default_factory=dict, alias="_globals")
    locals: Optional[Dict] = Field(default_factory=dict, alias="_locals")

    def run(self, command: str) -> str:
        """Run command with own globals/locals and returns anything printed."""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, self.globals, self.locals)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            output = str(e)
        finally:
            sys.stdout = old_stdout
        return output


def main(input_param):
    robot_raw_inputs = base64.b64decode(input_param).decode("utf-8")
    robot_inputs = json.loads(robot_raw_inputs)

    init_log()
    args = robot_inputs.get("inputs", {})
    if args is None:
        args = {}

    if (
        "environment_variables" in robot_inputs
        and robot_inputs["environment_variables"] is not None
    ):
        for env_key, env_value in robot_inputs["environment_variables"].items():
            if env_value is not None:
                os.environ[env_key] = env_value
    if "sys_path_list" in robot_inputs and robot_inputs["sys_path_list"] is not None:
        _insert_sys_path(robot_inputs["sys_path_list"])
    repl = PythonREPL()
    while True:
        code = input(">>>")
        # code = base64.b64decode(code).decode("utf-8")
        result = repl.run(code)
        if result:
            print(result)


def init_log():
    # 创建一个日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    # 创建一个格式化器
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.ERROR)
    # 将格式化器添加到文件处理器
    stream_handler.setFormatter(formatter)
    # 将文件处理器添加到日志记录器
    logger.addHandler(stream_handler)


def _insert_sys_path(sys_path_list):
    for sys_path in sys_path_list:
        sys.path.insert(0, sys_path)


if __name__ == "__main__":
    main("e30=")
