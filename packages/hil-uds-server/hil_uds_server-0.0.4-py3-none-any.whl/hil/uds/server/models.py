'''
Copyright (c) 2023 by HIL Group
Author: notmmao@gmail.com
Date: 2023-04-16 15:57:28
LastEditors: notmmao@gmail.com
LastEditTime: 2024-01-29 14:31:51
Description: 

==========  =============  ================
When        Who            What and why
==========  =============  ================

==========  =============  ================
'''
from pydantic import BaseModel
from pydantic_yaml import parse_yaml_file_as
from typing import Dict, Union, List

class Response(BaseModel):
    name: str = None
    hexstring: str

class Ecu(BaseModel):
    name: str
    cname: str
    txid: int
    rxid: int
    network: str = 'doip'
    doip: Dict
    can: Dict
    fd: bool = True
    dids: Dict[str, str] = {}
    echo: Dict[str, Union[List[int], str, 'Response']] = {}

    def __str__(self) -> str:
        return f'{self.name}-{self.cname} {hex(self.txid)}-{hex(self.rxid)}'

def load_ecu_config(config_file: str) -> Ecu:
    with open(config_file, mode="r", encoding="utf-8") as f:
        ecu = parse_yaml_file_as(Ecu, f)
        
        #将echo的key转换为大写
        ecu.echo = {k.upper(): v for k, v in ecu.echo.items()}

        return ecu