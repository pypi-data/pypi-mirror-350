#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time


class IdWorker(object):
    """
    Component Number Generator
    """

    def __init__(self):
        self.start = int(time.mktime(time.strptime('2019-04-01 00:00:00', "%Y-%m-%d %H:%M:%S")))
        self.last = int(time.time())
        self.countID = 0
        self.dataID = 1
        self.dataBit = 5
        self.machineID = 1
        self.machineBit = 5
        self.sequenceID = 1
        self.sequenceBit = 12
        self.MAX_DATA_ID = -1 ^ (-1 << self.dataBit)
        self.MAX_MACHINE_ID = -1 ^ (-1 << self.machineBit)
        self.MAX_SEQUENCE_ID = -1 ^ (-1 << self.sequenceBit)

        self.MACHINE_LEFT = self.sequenceBit
        self.DATACENTER_LEFT = self.sequenceBit + self.machineBit
        self.TIMESTMP_LEFT = self.DATACENTER_LEFT + self.dataBit

    def generator(self, component_type: str) -> str:
        """
        Suitable for single threaded single service nodes, where there may be duplication between multiple threads or nodes.
        For multiple nodes, it is necessary to ensure that the `dataID` and `machineID` are different.
        The sequence ID number can be incremented by comparing the current timestamp and `self.last`, or a certain number of random digits can be used. Solving multi-threaded problems requires singleton mode
        :param component_type:
        :return:
        """
        if self.dataID >= self.MAX_DATA_ID:
            self.dataID = 1
        if self.machineID >= self.MAX_MACHINE_ID:
            self.machineID = 1
        if self.sequenceID >= self.MAX_SEQUENCE_ID:
            self.sequenceID = 1
        self.dataID += 1
        self.machineID += 2
        self.sequenceID += 3
        return str((int(time.time() - self.start)) << self.TIMESTMP_LEFT
                   | self.dataID << self.DATACENTER_LEFT
                   | self.machineID << self.MACHINE_LEFT
                   | self.sequenceID) + component_type
