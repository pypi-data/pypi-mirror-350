# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250508-164121
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
封装某个定时控制
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from weberFuncs import PrintTimeMsg, GetCurrentTime
from weberFuncs import dict_load_name_value, dict_save_name_value
import os


class control_cron:
    def __init__(self, sWorkDir=''):
        # sWorkDir 工作目录，加上 run 子目录才是 sRunEnvFN
        if sWorkDir:
            self.sWorkDir = sWorkDir
        else:
            self.sWorkDir = os.getcwd()
        PrintTimeMsg(f'control_cron.sWorkDir={self.sWorkDir}=')

        # sEnvDir = GetSrcParentPath(__file__, True)
        self.sRunEnvFN = os.path.join(self.sWorkDir, 'run')
        PrintTimeMsg(f'control_cron.sRunEnvFN={self.sRunEnvFN}=')

    def _load_one_cc_param(self, sParamFN):
        # 加载某个定时控制参数
        sFullFN = os.path.join(self.sRunEnvFN, sParamFN)
        return dict_load_name_value(sFullFN)

    def get_control_cron_param(self, sCcid):
        # 加载全部定时控制参数
        sParamFN = 'ControlCronParam.txt'  # 人为设定的定时控制文件
        dictCC = self._load_one_cc_param(sParamFN)
        if sCcid in dictCC:
            return dictCC[sCcid]

        sParamFN = 'ControlCronByLlm.txt'  # LLM解析出的定时控制文件
        dictCC = self._load_one_cc_param(sParamFN)
        if sCcid in dictCC:
            return dictCC[sCcid]

        PrintTimeMsg(f'get_control_cron_param({sCcid})=NotFound!')
        return ''

    def load_control_cron_log(self, sCcid):
        # 读取 <sControlCronId>_log.txt 某个定时控制执行结果
        sFullFN = os.path.join(self.sRunEnvFN, f'{sCcid}_log.txt')
        return dict_load_name_value(sFullFN)

    def save_control_cron_log(self, sCcid, dictTimeLog):
        # 保存 <sControlCronId>_log.txt 某个定时控制执行结果
        sFullFN = os.path.join(self.sRunEnvFN, f'{sCcid}_log.txt')
        dict_save_name_value(sFullFN, dictTimeLog)


def main_control_cron():
    sWorkDir = r'E:\WeberSrcRoot\Rocky9GogsRoot\RobotAgentMCP\FileIoDumpDeal'
    o = control_cron(sWorkDir)
    sCcid = 'test'
    o.get_control_cron_param(sCcid)
    dictTimeLog = o.load_control_cron_log(sCcid)
    dictTimeLog['YMD2'] = 'ymd,%s' % GetCurrentTime()
    o.save_control_cron_log(sCcid, dictTimeLog)


if __name__ == '__main__':
    main_control_cron()

