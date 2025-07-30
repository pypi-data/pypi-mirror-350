'''
Copyright (c) 2023 by HIL Group
Author: notmmao@gmail.com
Date: 2023-07-13 13:51:03
LastEditors: notmmao@gmail.com
LastEditTime: 2023-07-13 16:41:01
Description: General Platform 二进制文件定义

==========  =============  ================
When        Who            What and why
==========  =============  ================
2023-07-13  notmmao        建立文件
==========  =============  ================
'''
import binascii
from typing import Union, IO
from construct import (
    Struct,
    Container,
    GreedyBytes,
    Int8ul,
    Int32ub,
    Array,
    Tell,
    this,
    Checksum,
    Pointer,
    Bytes,
    PaddedString,
)

bin_struct = Struct(
    "HeaderMagic" / Bytes(3),
    "HeaderVersion" / Int8ul,
    "NAME" / PaddedString(8, "ascii"),
    "SWV" / PaddedString(8, "ascii"),
    "HWV" / PaddedString(8, "ascii"),
    "HWPN" / PaddedString(14, "ascii"),
    "_offset" / Tell,
    "CRC" / Int32ub,
    "NOAR" / Int8ul,
    "Segments"
    / Array(
        this.NOAR,
        Struct(
            "Address" / Int32ub,
            "Length" / Int32ub,
        ),
    ),
    "data" / GreedyBytes,
    "_checksum"
    / Pointer(this._offset, Checksum(Int32ub, binascii.crc32, this.data)),
)


def parse_bin(bin_file):
    """解析二进制文件

    Args:
        bin_file (str): 二进制文件名

    Returns:
        Container: 解析后的结构化数据
    """
    return bin_struct.parse_file(bin_file)


def generate_bin(bin_file, name, swv, hwv, hwpn, data_file: Union[str, IO]):
    """生成二进制文件

    Args:
        bin_file (str): 二进制文件名
        name (str): ECU名称
        swv (str): 软件版本
        hwv (str): 硬件版本
        hwpn (str): 硬件零件号
        data_file (Union[str, IO]): 数据文件名或者文件对象

    Returns:
        Container: 生成的结构化数据
    """
    if isinstance(data_file, str):
        with open(data_file, "rb") as f:
            data = f.read()
    else:
        data = data_file.read()
    crc = binascii.crc32(data)

    container = Container(
        HeaderMagic=b"GPB",
        HeaderVersion=1,
        NAME=name,
        SWV=swv,
        HWV=hwv,
        HWPN=hwpn,
        CRC=crc,
        NOAR=1,
        Segments=[
            Container(
                Address=0x30000,
                Length=len(data),
            )
        ],
        data=data,
    )
    bin_data = bin_struct.build(
        container
    )

    with open(bin_file, "wb") as f:
        f.write(bin_data)

    return container


__version__ = '1.0.0'
__author__ = 'notmmao@gmail.com'


def main():
    """命令行入口

    generate_bin:
        python gp_bin.py generate --bin gw_00.00.01.bin --name gw --swv 00.00.01 --hwv 00.00.00 --hw pn S30-0123456789 --data gp.dbc
    parse_bin:
        python gp_bin.py parse --bin gw_00.00.01.bin

    """

    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    parser_parse = subparsers.add_parser("parse", help="解析二进制文件")
    parser_parse.add_argument("--bin", required=True, help="二进制文件")

    parser_generate = subparsers.add_parser("generate", help="生成二进制文件")
    parser_generate.add_argument("--bin", required=True, help="生成的二进制文件")
    parser_generate.add_argument("--name", required=True, help="ECU名称")
    parser_generate.add_argument("--swv", required=True, help="软件版本")
    parser_generate.add_argument("--hwv", required=True, help="硬件版本")
    parser_generate.add_argument("--hwpn", required=True, help="硬件零件号")
    parser_generate.add_argument("--data", required=True, help="数据文件")
    args = parser.parse_args()

    if args.command == "parse":
        container = parse_bin(args.bin)
        print(container)
    elif args.command == "generate":
        container = generate_bin(
            args.bin, args.name, args.swv, args.hwv, args.hwpn, args.data)
        print(container)
        print(f"generate {args.bin} success")


if __name__ == '__main__':
    main()
