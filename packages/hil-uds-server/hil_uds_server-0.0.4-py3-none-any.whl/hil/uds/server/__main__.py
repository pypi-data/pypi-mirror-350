'''
Copyright (c) 2023 by Deebug
Author: notmmao@gmail.com
Date: 2023-03-04 10:11:22
LastEditors: notmmao@gmail.com
LastEditTime: 2024-07-12 12:22:19
Description:

==========  =============  ================
When        Who            What and why
==========  =============  ================

==========  =============  ================
'''
import os
import argparse
import uvicorn
from loguru import logger


ECU_YAML = """
name: MCU
cname: 马达控制器
txid: 0x720
rxid: 0x7A0
network: doip
can:
  bustype: vector         # vector, socketcan, pcan, gc, zlg
  channel: 0              # vcan0, can0
  app_name: python_can    # vector only
  fd: true
  receive_own_messages: false
  bitrate: 500000
doip:
  src: 0x0039
  tester: 0xe800 
  ip: '127.0.0.1'
  port: 13400
echo:
  "1001": [0x50, 0x01]
  "1002": [0x50, 0x02]
  "1003": [0x50, 0x03]
  "1101": [0x50, 0x11]
  "22F189": "H1.30"
  "22F188": "04.01.05"
  "22F18A": "1FS"
  "22F187": "8045025CMV0000"
  "22F190": "LJN1A2EEXH1000000"
"""

def main():
    parser = argparse.ArgumentParser("uds_server")
    parser.add_argument("-a", "--action", choices=["init", "start"], default="start")
    parser.add_argument("-f", "--config-file", default="ecu.yaml")
    parser.add_argument("-p", "--port", default=8000, type=int)
    parser.add_argument("-i", "--ip", default="127.0.0.1")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--server", default="RestfulUdsServer")
    args = parser.parse_args()

    fn = args.config_file
    port = args.port
    ip = args.ip
    if args.quiet:
        logger.remove()

    if args.action == "init":
        with open("ecu.yaml", "w", encoding="utf-8") as f:
            f.write(ECU_YAML)
        return

    if args.action == "start":
        if not os.path.exists(fn):
            logger.warning(f"config file {fn} not exists")
            logger.info(f"`python -m hil.uds.server -a init` to create a default config file")
            return
        # 从目标模块中动态导入指定的类. 默认为 RestfulUdsServer, 或子类
        this = __import__("hil.uds.server", fromlist=[args.server])
        server = getattr(this, args.server)()
        server.set_config_file(fn)
        uvicorn.run(server.app, host=ip, port=port)


if __name__ == '__main__':
    main()
