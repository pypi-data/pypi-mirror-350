'''
Copyright (c) 2023 by HIL Group
Author: notmmao@gmail.com
Date: 2023-04-16 10:46:39
LastEditors: notmmao@gmail.com
LastEditTime: 2024-07-12 12:23:32
Description: 

==========  =============  ================
When        Who            What and why
==========  =============  ================

==========  =============  ================
'''
import os
from typing import Union, Union
from hil.core import Cantp, UdsServer
from hil.core.doip_server import DoipServer
from hil.common import utils
from fastapi import FastAPI, APIRouter
from can.interface import Bus
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from loguru import logger
from .models import Ecu, Response, load_ecu_config


class ConfigurableUdsServer(object):
    ecu: Ecu
    server : Union[UdsServer, DoipServer]
    config_file: str

    def __init__(self):
        '''
        Args:
            config_file (str): 配置文件路径
        '''
        super(ConfigurableUdsServer, self).__init__()

    def set_config_file(self, config_file: str):
        self.config_file = config_file
        self.reload()

    def reload(self):
        '''重新加载配置文件'''
        self.ecu = ecu = load_ecu_config(self.config_file)

        if ecu.network == 'doip':
            logger.info("doip: {}", ecu.doip)
            self.server =  DoipServer(**ecu.doip)
        else:
            bus = Bus(**ecu.can)
            tp = Cantp(bus, ecu.txid, ecu.rxid)
            self.server = UdsServer(tp)
        self.server.service_default_handle = self.handle
        self.server.live = 70 * 365 * 24 * 3600

    def handle(self, req_bytes: bytearray) -> bytearray:
        try: 
            resp_bytes = self._h(req_bytes)
            return resp_bytes
        except Exception as e:
            logger.error(f"Error in handle: {e}")
            return bytearray([0x7F, 0xFF, 0xFF])

    def _h(self, req_bytes: bytearray) -> bytearray:
        '''
        根据请求报文，返回响应报文

        Args:
            req_bytes (bytearray): 请求报文

        Returns:
            bytearray: 响应报文
        '''
        req = req_bytes.hex().upper()
        sid = req_bytes[0]
        if sid == 0x36:
            index = req_bytes[1]
            if index % 32 == 1:
                logger.info(f"req: {req[:4]}")
        else:
            logger.info(f"req: {req}")

        if req in self.ecu.echo:
            resp = self.ecu.echo[req]
            if isinstance(resp, list):
                resp_bytes = bytearray(resp)
            elif isinstance(resp, Response):
                resp_bytes = bytearray.fromhex(resp.hexstring)
            else:
                req_bytes[0] = sid + 0x40
                resp_bytes = bytearray(req_bytes)
                resp_bytes.extend(resp.encode())
        else:
            if sid == 0x34:
                if "34" in self.ecu.echo:
                    resp = self.ecu.echo["34"]
                else:
                    # default 34 response
                    resp = [0x74, 0x20, 0x0F, 0xFF]
            elif sid == 0x36:
                index = req_bytes[1]
                resp = [0x76, index]
            elif sid == 0x37:
                resp = [0x77]
            elif req.startswith("2712"):
                resp = [0x67, 0x12]
            elif req.startswith("220107"):
                self.progress = (self.progress + 1) % 101
                resp = [0x62, 0x01, 0x07, self.progress]
            elif req.startswith("31010202"):
                # start checkRoutine
                rid = req_bytes[2:4]
                resp = [0x71, 0x01, *rid, 0x00]
            elif req.startswith("3101FF00"):
                # e. start eraseMemory
                rid = req_bytes[2:4]
                resp = [0x71, 0x01, *rid, 0x00]
            elif req.startswith("3101FF01"):
                # f. start checkProgrammingDependencies
                rid = req_bytes[2:4]
                resp = [0x71, 0x01, *rid, 0x00]
            elif req.startswith("2EF199"):
                # Write Programming date
                did = req_bytes[1:3]
                resp = [0x6E, *did]
                # 2EF199 通常出现在刷写完成最后阶段, 这里把预设的`目标版本`与`22F189`置换
                if 'target' in self.ecu.echo:
                    self.ecu.echo['target'], self.ecu.echo['22F189'] = self.ecu.echo['22F189'], self.ecu.echo['target']
                    logger.info("version switch {}", self.ecu.echo['22F189'])
            elif sid == 0x2E:
                if len(req_bytes) < 3:
                    resp = [0x7f, sid, 0x13]
                did = req_bytes[1:3]
                resp = [0x6E, *did]
            else:
                resp = [sid + 0x40]
                resp.extend(req_bytes[1:])

            if isinstance(resp, list):
                resp_bytes = bytearray(resp)
            else:
                req_bytes[0] = sid + 0x40
                resp_bytes = bytearray(req_bytes)
                resp_bytes.extend(resp.encode())
        
        # 记录响应报文
        if sid == 0x36:
            index = req_bytes[1]
            if index % 32 == 1:
                logger.info(f"resp: {resp_bytes.hex()}")
        else:
            logger.info(f"resp: {resp_bytes.hex()}")
        return resp_bytes


class AutoReloadUdsServer(ConfigurableUdsServer, FileSystemEventHandler):
    observer = Observer()

    def __init__(self):
        super().__init__()

    def start(self):
        path = os.path.dirname(os.path.abspath(self.config_file))
        self.observer.schedule(self, path=path, recursive=False)
        self.observer.start()
        self.server.start()

    def stop(self) -> None:
        self.observer.stop()
        self.server.stop()


    @utils.debounce(1)
    def on_modified(self, event: FileSystemEvent):
        if event.src_path.endswith(self.config_file):
            logger.info("on_modified")
            self.reload()


class RestfulUdsServer(AutoReloadUdsServer):
    app: FastAPI
    router: APIRouter

    def __init__(self):
        super(RestfulUdsServer, self).__init__()
        self.app = FastAPI()
        self.router = APIRouter()
        self.app.add_event_handler("startup", self.start)
        self.app.add_event_handler("shutdown", self.stop)
        self.router.add_api_route("/ecu", self.get_ecu, methods=["GET"])
        self.router.add_api_route("/ecu", self.set_ecu, methods=["POST"])
        self.router.add_api_route(
            "/ecu/echo/{key}", self.get_ecu_echo, methods=["GET"])
        self.router.add_api_route(
            "/ecu/echo/{key}/ascii", self.set_ecu_echo_ascii, methods=["POST"])
        self.router.add_api_route(
            "/ecu/echo/{key}/hex", self.set_ecu_echo_hex, methods=["POST"])
        self.app.include_router(self.router)

    def get_ecu(self):
        return self.ecu

    def set_ecu(self, ecu: Ecu):
        self.ecu = ecu
        return self.ecu

    def get_ecu_echo(self, key: str):
        """获取echo值 (hexstring)"""
        return self.ecu.echo.get(key.upper(), {"error": "key not found"})

    def set_ecu_echo_ascii(self, key: str, value: str):
        """设置echo值 (ascii), 例如: 22F189=H1.30, 适用于payload为ascii的情况"""
        try:
            key = key.upper()
            self.ecu.echo[key] = value
            return self.ecu.echo[key]
        except Exception as e:
            return {"error": str(e)}


    def set_ecu_echo_hex(self, key: str, value: str):
        """设置echo值 (hexstring), 要包括完整返回, 例如: 22F189=62F189312E33 30, 支持空格"""
        try:
            key = key.upper()
            # 去掉value空白字符
            _value = value.replace(" ", "")
            _value = bytes.fromhex(value)
            self.ecu.echo[key] = list(_value)
            return self.ecu.echo[key]
        except Exception as e:
            return {"error": str(e)}
                