"""
:author: Thomas Delaet <thomas@delaet.org>
"""
from velbus.message import Message
from velbus.command_registry import register_command
import json

COMMAND_CODE = 0xf0


class ChannelNamePart1Message(Message):
    """
    send by: VMB6IN, VMB4RYLD
    received by:
    """

    def __init__(self, address=None):
        Message.__init__(self)
        self.channel = 0
        self.name = ""
        self.set_defaults(address)

    def populate(self, priority, address, rtr, data):
        """
        :return: None
        """
        assert isinstance(data, bytes)
        self.needs_low_priority(priority)
        self.needs_no_rtr(rtr)
        self.needs_data(data, 7)
        self.set_attributes(priority, address, rtr)
        channels = self.byte_to_channels(data[0])
        self.needs_one_channel(channels)
        self.channel = channels[0]
        self.name = "".join([chr(x) for x in data[1:]])

    def data_to_binary(self):
        """
        :return: bytes
        """
        return bytes([
            COMMAND_CODE,
            self.channels_to_byte([self.channel])
            ]) + bytes(self.name, 'utf-8')

    def to_json(self):
        """
        :return: str
        """
        json_dict = self.to_json_basic()
        json_dict['channel'] = self.channel
        return json.dumps(json_dict)

 
class ChannelNamePart1Message2(ChannelNamePart1Message):
    """
    send by: VMBGP*
    received by:
    """
    def populate(self, priority, address, rtr, data):
        """
        :return: None
        """
        assert isinstance(data, bytes)
        self.needs_low_priority(priority)
        self.needs_no_rtr(rtr)
        self.needs_data(data, 7)
        self.set_attributes(priority, address, rtr)
        self.channel = data[0]
        self.name = "".join([chr(x) for x in data[1:]])


class ChannelNamePart1Message3(ChannelNamePart1Message):
    """
    send by: VMBGP*
    received by:
    """
    def populate(self, priority, address, rtr, data):
        """
        :return: None
        """
        assert isinstance(data, bytes)
        self.needs_low_priority(priority)
        self.needs_no_rtr(rtr)
        self.needs_data(data, 5)
        self.set_attributes(priority, address, rtr)
        self.channel = (data[0] >> 1) & 0x03
        self.name = "".join([chr(x) for x in data[1:]])

 
register_command(COMMAND_CODE, ChannelNamePart1Message)
register_command(COMMAND_CODE, ChannelNamePart1Message2, 'VMBGP1')
register_command(COMMAND_CODE, ChannelNamePart1Message2, 'VMBGP2')
register_command(COMMAND_CODE, ChannelNamePart1Message2, 'VMBGP4')
register_command(COMMAND_CODE, ChannelNamePart1Message2, 'VMBGP0')
register_command(COMMAND_CODE, ChannelNamePart1Message2, 'VMBGPOD')
register_command(COMMAND_CODE, ChannelNamePart1Message2, 'VMBGP4PIR')
register_command(COMMAND_CODE, ChannelNamePart1Message3, 'VMB1BL')
register_command(COMMAND_CODE, ChannelNamePart1Message3, 'VMB2BL')

