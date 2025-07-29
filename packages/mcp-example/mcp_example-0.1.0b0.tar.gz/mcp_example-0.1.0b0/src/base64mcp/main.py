import os

from .server import Env, serve


def main_cli():
    """
    从环境变量中读取 server.py 中定义的 Env 类所需的参数，
    并创建 Env 实例。如果环境变量不存在，则报错。
    """
    env_to_low_name = 'TO_LOW'  # 定义 to_low 对应的环境变量名
    env_to_upper_name = 'TO_UPPER'  # 定义 to_upper 对应的环境变量名

    to_low_value = os.getenv(env_to_low_name)
    to_upper_value = os.getenv(env_to_upper_name)

    error_messages = []
    if to_low_value is None:
        error_messages.append(f"错误：环境变量 '{env_to_low_name}' 未设置。")

    if to_upper_value is None:
        error_messages.append(f"错误：环境变量 '{env_to_upper_name}' 未设置。")

    if error_messages:
        for msg in error_messages:
            print(msg)
        # 在实际应用中，您可能希望在这里通过 sys.exit(1) 退出或引发一个异常
        return

    env_instance = Env(to_low=to_low_value, to_upper=to_upper_value)

    serve(env_instance)


if __name__ == '__main__':
    main_cli()
