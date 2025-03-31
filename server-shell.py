#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

# 创建一个MCP服务器
mcp = FastMCP("Linux-Shell")

@mcp.tool()
def shell(binary: str, args: List[str] = None) -> Optional[str]:
    """shell命令行解释, 与操作系统交互, 可以执行各种命令来管理文件/目录/进程等, 还可以编写脚本来自动化任务

    :param binary: 二进制程序的路径或名称(如果在PATH中)
    :param args: 传递给程序的参数列表
    :return: 程序输出的字符串，如果执行失败则返回None
    """
    if args is None:
        args = []

    try:
        # 检查程序是否存在且可执行
        if not os.access(binary, os.X_OK):
            # 尝试在PATH中查找
            path = os.environ.get("PATH", "").split(":")
            for dir in path:
                full_path = os.path.join(dir, binary)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    binary= full_path
                    break

        # 执行程序并捕获输出
        result = subprocess.run(
            [binary] + args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing {binary}: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Binary not found: {binary}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def calculate(expression: str) -> float:
    """计算四则运算表达式
    参数:
      expression: 数学表达式字符串，如 "1 + 2 * 3"
    返回:
      计算结果
    """
    return eval(expression)

def ls(directory: str = ".", long_format: bool = False) -> Optional[str]:
    """
    ls命令，列出目录内容

    :param directory: 要列出的目录路径，默认为当前目录
    :param long_format: 是否使用长格式输出(ls -l)
    :return: 目录内容字符串
    """
    args = []
    if long_format:
        args.append("-l")
    args.append(directory)
    return execute_binary("ls", args)

def cat(file_path: str, number_lines: bool = False) -> Optional[str]:
    """
    cat命令，显示文件内容

    :param file_path: 要显示的文件路径
    :param number_lines: 是否显示行号(cat -n)
    :return: 文件内容字符串
    """
    args = []
    if number_lines:
        args.append("-n")
    args.append(file_path)
    return execute_binary("cat", args)

def dmesg(
    human_readable: bool = True,
    follow: bool = False,
    level: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    n_lines: Optional[int] = None
) -> Optional[str]:
    """
    dmesg命令，获取内核日志

    :param human_readable: 是否使用人类可读的时间戳(可能不准确)
    :param follow: 是否持续等待新消息(类似dmesg -w)
    :param level: 过滤特定级别的消息(emerg/alert/crit/err/warn/notice/info/debug)
    :param since: 显示指定时间之后的消息(格式: "2023-01-01 12:00:00")
    :param until: 显示指定时间之前的消息(格式: "2023-01-01 12:00:00")
    :param n_lines: 显示指定行数的消息
    :return: 内核消息字符串
    """
    args = []

    # 时间格式选项
    if human_readable:
        args.append("--human")
    else:
        args.append("--ctime")

    # 持续监控选项
    if follow:
        args.append("--follow")

    # 日志级别过滤
    if level:
        args.extend(["--level", level])

    # 时间范围过滤
    if since:
        args.extend(["--since", since])
    if until:
        args.extend(["--until", until])

    # 显示行数限制
    if n_lines:
        args.extend(["--nlines", str(n_lines)])

    return execute_binary("dmesg", args)

def tail(file_path: str, lines: int = 10) -> Optional[str]:
    """
    tail命令，显示文件末尾内容

    :param file_path: 要显示的文件路径
    :param lines: 要显示的行数，默认为10行
    :return: 文件末尾内容字符串
    """
    args = ["-n", str(lines)]
    args.append(file_path)
    return execute_binary("tail", args)

def head(file_path: str, lines: int = 10) -> Optional[str]:
    """
    head命令，显示文件开头内容

    :param file_path: 要显示的文件路径
    :param lines: 要显示的行数，默认为10行
    :return: 文件开头内容字符串
    """
    args = ["-n", str(lines), file_path]
    return execute_binary("head", args)

if __name__ == "__main__":
    mcp.run(transport='stdio')
