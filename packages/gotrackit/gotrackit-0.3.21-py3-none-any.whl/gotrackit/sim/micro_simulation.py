# -- coding: utf-8 --
# @Time    : 2024/7/21 11:09
# @Author  : TangKai
# @Team    : ZheChengData

from __future__ import absolute_import
from __future__ import print_function


import os
import sys
import traci  # noqa
import sumolib  # noqa
import datetime
from ..log.log import LogRecord
from datetime import timedelta
from sumolib import checkBinary
from ..GlobalVal import GpsField

gps_field = GpsField()

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


class Scene(object):
    def __init__(self, scene_fldr: str = 'Scene1', save_log=True, loc_frequency=5.0, out_fldr: str = r'./'):
        self.scene_fldr = scene_fldr
        self.out_fldr = out_fldr
        self.save_log = save_log
        self.loc_frequency = loc_frequency

    def start_sim(self):
        """
        sumo仿真进程
        :return:
        """
        sumo_binary = checkBinary('sumo-gui')
        assert os.path.exists(os.path.join(self.scene_fldr, "sumo.sumocfg"))
        traci.start([sumo_binary, "-c", os.path.join(self.scene_fldr, "sumo.sumocfg"),
                     "--tripinfo-output", os.path.join(self.out_fldr, "trip_info.xml")])

        sim = MicroSim()
        sim.run()

class MicroSim(object):
    def __init__(self):
        """

        """
        pass

    @staticmethod
    def run(max_steps:int = 2500):
        """"""
        step = 0
        _step = 0
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            step += 1
            if step >= max_steps:
                break
        traci.close()
        sys.stdout.flush()
