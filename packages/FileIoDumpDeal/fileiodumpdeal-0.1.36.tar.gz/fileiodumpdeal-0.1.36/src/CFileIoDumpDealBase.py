# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250507-092607
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
Program description
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from weberFuncs import PrintTimeMsg, PrintAndSleep, GetTimeInteger
from weberFuncs import TryForceMakeDir
from weberFuncs import GetCurrentTime, GetTimeStampIntFmYMDHns
import os


class CFileIoDumpDealBase(object):
    # 通过文件输入输出，对接 TaskMcpClient 等应用
    def __init__(self, sMcpTaskDir):
        # sMcpTaskDir 是对应 TaskMcpClient 的Task工作目录，带尾部task
        self.sMcpTaskDir = sMcpTaskDir  # os.path.join(self.sWorkDir, 'task')
        PrintTimeMsg(f'CFileIoDumpDealBase.sMcpTaskDir={self.sMcpTaskDir}=')
        self.sWasteDir = os.path.join(self.sMcpTaskDir, 'waste')
        TryForceMakeDir(self.sWasteDir)

    def DumpFile4Query(self, sQueryDir):
        # 导出到文件到 sQueryDir 目录，作为 TaskMcpClient 的Query输入
        # 返回导出文件数目
        PrintTimeMsg(f'CFileIoDumpDealBase.DumpFile4Query.sQueryDir={sQueryDir}=')
        iDumpCnt = 0
        sNextMatchTime = ''
        return iDumpCnt, sNextMatchTime

    def DealFileResult(self, sNoExtFN, sResultDir):
        # 将sResultDir目录下的回复文件，提交到其它系统，并移动到备份目录
        # sNoExtFN 不带扩展名及_R/_Q的文件名
        # 返回处理成功与否
        PrintTimeMsg(f'CFileIoDumpDealBase.DealFileResult.sNoExtFN={sNoExtFN}={sResultDir}=')
        bDealOk = True
        return bDealOk

    def _ProcessTaskResult(self):
        # 将任务结果文件移到waste目录
        # lsNoExtFN = self._ListTaskResultFile()
        lsNoExtFN = []
        sResultDir = os.path.join(self.sMcpTaskDir, 'result')
        for sFN in os.listdir(sResultDir):
            sNoExtFN, sExt = os.path.splitext(sFN)
            if sExt.lower() != '.md':
                continue
            if sNoExtFN.endswith('_R'):  # 仅关注 _R ，传入不带 _R/_Q 后缀
                lsNoExtFN.append(sNoExtFN[:-2])
        # PrintTimeMsg(f'_ProcessTaskResult({sResultDir}).len(lsNoExtFN)={len(lsNoExtFN)}=')

        iCountFN = len(lsNoExtFN)
        iProcessCnt = 0
        for sNoExtFN in lsNoExtFN:
            bDealOk = self.DealFileResult(sNoExtFN, sResultDir)
            sDealOk = 'ok' if bDealOk else 'err'
            for sTail in ['_R', '_Q']:  # , '_M'
                sFullResultFN = os.path.join(sResultDir, f'{sNoExtFN}{sTail}.md')
                sFullWasteFN = os.path.join(self.sWasteDir, f'{sDealOk}_{sNoExtFN}{sTail}.md')
                os.rename(sFullResultFN, sFullWasteFN)
                iProcessCnt += 1
            if iProcessCnt < iCountFN:
                PrintAndSleep(45, f'_ProcessTaskResult.iProcessCnt={iProcessCnt}<{iCountFN}=Wait45s')
        # PrintTimeMsg(f'_ProcessTaskResult.iProcessCnt={iProcessCnt}=')
        return iProcessCnt

    def _ProcessTaskWaste(self):
        # 将waste目录下1天前的文件删除
        iSecondsRemoveBefore = 60*60*24
        tmNow = GetTimeInteger()
        iRemoveCnt = 0
        for sFN in os.listdir(self.sWasteDir):
            sFullFN = os.path.join(self.sWasteDir, sFN)
            oSt = os.stat(sFullFN)
            tmMod = int(oSt.st_mtime)
            if tmNow - tmMod >= iSecondsRemoveBefore:
                try:
                    os.remove(sFullFN)
                    iRemoveCnt += 1
                except Exception as e:
                    PrintTimeMsg(f"_ProcessTaskWaste({sFullFN}).e={repr(e)}=WARNING!")
        if iRemoveCnt > 0:
            PrintTimeMsg(f'_ProcessTaskWaste.iRemoveCnt={iRemoveCnt}=')
        return iRemoveCnt

    def _LoopDealTaskResult(self):
        # 循环执行Deal
        iSleepSeconds = 60
        iLoopCnt = 0
        while True:
            if iLoopCnt % 60 == 0:  # 每个1小时清理一次垃圾文件
                self._ProcessTaskWaste()
            iDealCnt = 0
            try:
                iDealCnt = self._ProcessTaskResult()
            except Exception as e:
                PrintTimeMsg(f"_LoopDealTaskResult.e={repr(e)}=WARNING!")
            PrintAndSleep(iSleepSeconds, f'_LoopDealTaskResult.iLoopCnt={iLoopCnt}=iDealCnt={iDealCnt}=',
                          iLoopCnt % 10 == 0)
            iLoopCnt += 1

    def _LoopDumpFile4Query(self):
        # 循环执行Dump
        sQueryDir = os.path.join(self.sMcpTaskDir, 'query')
        iLoopCnt = 0
        while True:
            iSleepSecs = 60*60
            iDumpCnt = 0
            try:
                iDumpCnt, sTmNextCheck = self.DumpFile4Query(sQueryDir)
                if sTmNextCheck:
                    iTmChk = GetTimeStampIntFmYMDHns(sTmNextCheck)
                    iTmNow = GetTimeStampIntFmYMDHns(GetCurrentTime())
                    iSleepSecs = iTmChk - iTmNow
                    PrintTimeMsg(f"_LoopDumpFile4Query.sTmNextCheck={sTmNextCheck}=iSleepSecs={iSleepSecs}")
                if iSleepSecs < 60:
                    iSleepSecs = 60
                if iSleepSecs > 60*60:
                    iSleepSecs = 60*60
            except Exception as e:
                PrintTimeMsg(f"_LoopDumpFile4Query.e={repr(e)}=WARNING!")
            PrintAndSleep(iSleepSecs, f'_LoopDumpFile4Query.iLoopCnt={iLoopCnt}=iDumpCnt={iDumpCnt}=',
                          iLoopCnt % 1 == 0)
            iLoopCnt += 1


    def LoopFileIoDumpDeal(self, sTaskType):
        # 按任务类型调用Dump和Deal
        PrintTimeMsg(f"LoopFileIoDumpDeal.sTaskType={sTaskType}=")
        iLoopCnt = 0
        if sTaskType == 'dump':
            return self._LoopDumpFile4Query()
        else:
            return self._LoopDealTaskResult()
        # 由于 DealFileResult 和 DumpFile4Query 共用一个循环框架，休息时间固定是60秒为好
        # 分开后，就可以各自灵活控制。


def mainFileIoDumpDealBase():
    sMcpTaskDir = r'E:\WeberSrcRoot\Rocky9GogsRoot\RobotAgentMCP\TaskMcpClient\task'
    o = CFileIoDumpDealBase(sMcpTaskDir)
    o.LoopFileIoDumpDeal(60)


if __name__ == '__main__':
    mainFileIoDumpDealBase()
