import yaml


import argparse


class VcgCfg(object):
    def __init__(self, vcgDict=None):
        self.vcgDict_ = vcgDict
        for a, b in vcgDict.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [VcgCfg(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, VcgCfg(b) if isinstance(b, dict) else b)

    @staticmethod
    def fromYaml(cfgFile=None):
        with open(cfgFile, "r") as ymlfile:
            cfgDict = yaml.safe_load(ymlfile)
        return VcgCfg(vcgDict=cfgDict)

    def __str__(self):
        dict_ = {}
        for key, value in self.__dict__.items():
            if isinstance(value, VcgCfg):
                dict_[key] = str(value)
            else:
                dict_[key] = value

        return str(dict_)
