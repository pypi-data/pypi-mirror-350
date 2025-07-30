#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.

from pydantic import Field

from py3comtrade.model.channel import Channel
from py3comtrade.model.digital_change_status import DigitalChangeStatus
from py3comtrade.model.type.digital_enum import Contact


class Digital(Channel):
    """
    开关量通道类
    """
    contact: Contact = Field(default=Contact.NORMALLYOPEN, description="状态通道正常状态")
    change_status: DigitalChangeStatus = Field(default=DigitalChangeStatus(timestamp=[], status=[]),
                                               description="变位记录")

    def clear(self) -> None:
        """清除模型中所有字段"""
        super().clear()
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def __str__(self):
        return super().__str__() + f",{self.contact.code}"
