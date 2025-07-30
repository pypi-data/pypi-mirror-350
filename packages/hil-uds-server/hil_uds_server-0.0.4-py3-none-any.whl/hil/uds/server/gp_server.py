import random
import typing

from loguru import logger
from io import BytesIO

from . import RestfulUdsServer
from . import gp_bin


def randbytes(n):
    return bytearray(random.getrandbits(8) for _ in range(n))


class GpUdsServer(RestfulUdsServer):
    dids: dict
    ctx: dict
    software: str
    hardward: str

    def load_bin(self, ecu):
        name = ecu.name
        bin_file = f"{name}_cache.bin"
        retry = 2
        while retry > 0:
            try:
                container = gp_bin.parse_bin(bin_file)
                if container is not None:
                    self.software = container.SWV
                    self.hardware = container.HWPN
                    logger.info(f"{name} load bin file success: {bin_file}")
                    logger.info(f"{name} name: {ecu.name}")
                    logger.info(f"{name} software: {self.software}")
                    logger.info(f"{name} hardware: {self.hardware}")
                    break
            except:
                logger.warning(f"load bin file failed: {bin_file}")
                logger.warning(f"generate dummy bin file: {bin_file}")
                
                # generate dummy bin file
                f = BytesIO(initial_bytes=randbytes(1024*32))
                gp_bin.generate_bin(bin_file, ecu.name, self.software, self.hardware, self.hardware, f)
            finally:
                retry -= 1

    def reload(self):
        '''重新加载配置文件'''
        super().reload()

        self.software = "1.0"  # ecu.echo['22F188']
        self.hardware = "H1.0"  # ecu.echo['22F189']
        self.load_bin(self.ecu)
        
        self.ctx = {
            "key": "",
            "block_size": 1024,
            "crc8": 0,
            "can_logger": "can.asc"
        }
        self.dids = {}
        self.server.service_default_handle = self.service_default_handle

    def service_22_handle(self, did: bytearray) -> typing.List[int]:
        did_hex = did.hex().upper()
        if did_hex == "F188":
            payload_resp = list(bytearray(self.software.encode()))
        elif did_hex == "F187":
            payload_resp = list(bytearray(self.hardware.encode()))
        else:
            if did_hex not in self.dids:
                self.dids[did_hex] = randbytes(10)
            payload_resp = list(self.dids[did_hex])
        return payload_resp

    def service_default_handle(self, req: bytearray):
        sid = req[0]
        payload_resp = []

        if sid == 0x34:
            self.ctx['crc8'] = 0
            self.ctx['file'] = open(f"{self.ecu.name}_cache.bin", "wb")
            payload_resp = [0x20, 0x04, 0x82]
            resp = [sid + 0x40, *payload_resp]
        elif sid == 0x36:
            index = req[1]
            payload = req[2:]
            crc8 = self.ctx['crc8']
            self.ctx['file'].write(payload)
            for d in payload:
                crc8 = crc8 + d
            crc8 = ~crc8 & 0xff
            self.ctx['crc8'] = crc8
            resp = [sid + 0x40, index]
        elif sid == 0x37:
            crc8 = self.ctx['crc8']
            crc8 = ~crc8 & 0xff
            resp = [sid + 0x40, crc8]
            self.ctx['file'].close()
        elif sid == 0x2E:
            if len(req) < 3:
                resp = [0x7f, sid, 0x13]
            did = req[1:3]
            did_code = int.from_bytes(did, 'big')
            if did_code in [0xf187, 0xf188]:
                resp = [0x7f, sid, 0x11]
            else:
                did_hex = did.hex().upper()
                self.dids[did_hex] = req[3:]
                resp = [sid + 0x40, *did, *payload_resp]
        elif sid == 0x22:
            if len(req) < 3:
                resp = [0x7f, sid, 0x13]
            else:
                did = req[1:3]
                payload_resp = self.service_22_handle(did)

                resp = [sid + 0x40, *did, *payload_resp]

        elif sid == 0x27:
            if len(req) < 2:
                resp = [0x7f, sid, 0x13]
            else:
                level = int(req[1])
                if level % 2 == 1:
                    seed = randbytes(4)
                    resp = [sid + 0x40, level, *seed]
                else:
                    resp = [sid + 0x40, level]
        elif sid == 0x11:
            resp = [sid + 0x40, req[1]]
            # 复位
            self.load_bin(self.ecu)
        else:
            if len(req) > 1:
                sub_func = req[1]
                resp = [sid + 0x40, sub_func, *payload_resp]
            else:
                resp = [sid + 0x40, *payload_resp]
        return bytearray(resp)
