#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@File    :   dbcReader.py
@Time    :   2025/2/26 9:58
@Author  :   CLZMFQ
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This package realizes functionality of sending can message
'''

import cantools, logging
from simpleCan.util import dataStructure as ds


class DBCReader:

    def __init__(self, *args):
        self.dbcPaths = args
        self.databaseCan = None
        self.canTxMessageList = []
        try:
            self.loadDBC()
            self.loadAllTxMessage()
        except Exception as e:
            logging.error(f"Some error: {e}")

    def loadDBC(self):
        if self.dbcPaths is not None:
            try:
                if len(self.dbcPaths) == 1:
                    self.databaseCan = cantools.database.load_file(self.dbcPaths[0])
                else:
                    self.databaseCan = cantools.database.load_file(self.dbcPaths[0])
                    for path in self.dbcPaths[1:]:
                        if path is not None:
                            try:
                                dbc = cantools.database.load_file(path)
                                self.databaseCan.messages.extend(dbc.messages)
                                self.databaseCan.nodes.extend(dbc.nodes)
                                self.databaseCan.version = dbc.version
                            except Exception as e:
                                logging.error(f"Read DBC error: {e}")
            except Exception as e:
                logging.error(f"Read DBC error: {e}")

    def loadDBCs(self):
        self.databaseCan = cantools.database.load_file(self.dbcPaths[0])
        for path in self.dbcPaths[1:]:
            if path is not None:
                try:
                    dbc = cantools.database.load_file(path)
                    self.databaseCan.messages.extend(dbc.messages)
                    self.databaseCan.nodes.extend(dbc.nodes)
                    self.databaseCan.version = dbc.version
                except Exception as e:
                    logging.error(f"Read DBC error: {e}")

    def loadAllTxMessage(self):
        try:
            for message in self.databaseCan.messages:
                if message.cycle_time is not None:
                    self.canTxMessageList.append(
                        ds.CanMessage(id=message.frame_id, data=[1, 3, 5], period=message.cycle_time / 1000))
        except Exception as e:
            logging.error(f"Something went wrong: {e}")

    def generateCanMessage(self, message, duration=30, **kwargs) -> ds.CanMessage:
        try:
            message_from_dbc = self.databaseCan.get_message_by_name(message)
            id = message_from_dbc.frame_id
            period = message_from_dbc.cycle_time / 1000
            target_data = {}
            for signal in message_from_dbc.signals:  # If value is assigned from input argument, then get this value. Otherwise get default value from DBC
                if signal.maximum is None:
                    signal.maximum = 0
                if signal.name in kwargs:
                    target_data[signal.name] = kwargs[signal.name]
                else:  # get message data from dbc
                    if signal.raw_initial is not None and signal.scale is not None and signal.raw_initial * signal.scale < signal.maximum:
                        target_data[signal.name] = float(signal.raw_initial * signal.scale)
                    else:
                        target_data[signal.name] = signal.maximum
            data = list(message_from_dbc.encode(target_data))
            return ds.CanMessage(id=id, data=data, period=period,
                                 duration=duration)
        except cantools.database.errors.EncodeError as e:
            logging.error(f"Load can message error: {e}")
            target_data[signal.name] = signal.maximum
            data = list(message_from_dbc.encode(target_data))
            return ds.CanMessage(id=id, data=data, period=period,
                                 duration=duration)
        except Exception as e:
            print(e)

    def decodeCanMessage(self, message_id, data) -> ds.ReceivedCanMessageDecode:
        if self.databaseCan is not None:
            message = self.databaseCan.get_message_by_frame_id(message_id)
            decoded_signals = message.decode(bytes(data))
            decoded_signals_raw = {}
            for signal in message.signals:
                if signal.choices is None:
                    break
                for key, value in signal.choices.items():
                    if isinstance(value,str) and decoded_signals[signal.name] == value:
                        decoded_signals_raw[signal.name] = key
            return ds.ReceivedCanMessageDecode(message=message.name, decode_signals=decoded_signals,
                                               decoded_signals_raw=decoded_signals_raw)

    def getMessageByName(self, messageName):
        return self.databaseCan.get_message_by_name(messageName)

    def getMessageIdByName(self, messageName):
        return self.databaseCan.get_message_by_name(messageName).frame_id

    def getcanTxMessageList(self):
        return self.canTxMessageList
