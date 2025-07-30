import importlib
import platform
import random
import time

from robot_base import log_decorator, log_util, ParamException


@log_decorator
def basic_condition(expression1, relation: str, expression2, **kwargs):
    if relation == "equal":
        return expression1 == expression2
    elif relation == "notEqual":
        return expression1 != expression2
    elif relation == "greaterThan":
        return expression1 > expression2
    elif relation == "greaterThanOrEqual":
        return expression1 >= expression2
    elif relation == "lessThan":
        return expression1 < expression2
    elif relation == "lessThanOrEqual":
        return expression1 <= expression2
    elif relation == "contains":
        return expression1 in expression2
    elif relation == "notContains":
        return expression1 not in expression2
    elif relation == "startWith":
        return expression1.startswith(expression2)
    elif relation == "endWith":
        return expression1.endswith(expression2)
    elif relation == "notStartWith":
        return not expression1.startswith(expression2)
    elif relation == "notEndWith":
        return not expression1.endswith(expression2)
    elif relation == "isNone":
        return expression1 is None or expression1 == ""
    elif relation == "isNotNone":
        return expression1 is not None and expression1 != ""
    elif relation == "isTrue":
        return expression1 is True
    elif relation == "isFalse":
        return expression1 is False
    return True


@log_decorator
def print_log(log_level: str, expression, **kwargs):
    if log_level == "debug":
        log_util.Logger.get_logger().debug(f"【流程输出】:{expression}")
    elif log_level == "info":
        log_util.Logger.get_logger().info(f"【流程输出】:{expression}")
    elif log_level == "warning":
        log_util.Logger.get_logger().warn(f"【流程输出】:{expression}")
    elif log_level == "error":
        log_util.Logger.get_logger().error(f"【流程输出】:{expression}")
    else:
        log_util.Logger.get_logger().info(f"【流程输出】:{expression}")


@log_decorator
def delay(expression, **kwargs):
    time.sleep(float(expression))


@log_decorator
def set_param(variable_type, variable_value, **kwargs):
    if variable_type == "string":
        return str(variable_value)
    elif variable_type == "int":
        return int(variable_value)
    elif variable_type == "float":
        return float(variable_value)
    elif variable_type == "bool":
        return bool(variable_value)
    return variable_value


@log_decorator
def generate_random(min_number, max_number, **kwargs):
    min_number = int(min_number)
    max_number = int(max_number)
    if min_number > max_number:
        raise ParamException("最小值不能大于最大值")
    if min_number == max_number:
        return min_number
    return random.randint(min_number, max_number)


@log_decorator
def invoke_flow(flow_data, **kwargs):
    flow_name = flow_data["flow_name"]
    inputs = flow_data["inputs"]
    mod = importlib.import_module(flow_name)
    return mod.main(**inputs)


@log_decorator
def invoke_module_method(invoke_data, **kwargs):
    module_name = invoke_data["module_name"]
    function_name = invoke_data["function_name"]
    inputs = invoke_data["inputs"]
    mod = importlib.import_module(module_name)
    if function_name in mod.__dict__:
        func = mod.__dict__[function_name]
        return func(**inputs)
    else:
        raise ParamException(f"{function_name}方法未找到")


@log_decorator
def for_each_list(array, **kwargs):
    for loop_value in array:
        yield loop_value


@log_decorator
def for_each_map(map, **kwargs):
    for key, value in map.items():
        yield key, value


@log_decorator
def for_i_loop(start, end, add, **kwargs):
    start = int(start)
    end = int(end)
    add = int(add)
    for i in range(start, end, add):
        yield i


@log_decorator
def get_system_type(**kwargs):
    return platform.system()
