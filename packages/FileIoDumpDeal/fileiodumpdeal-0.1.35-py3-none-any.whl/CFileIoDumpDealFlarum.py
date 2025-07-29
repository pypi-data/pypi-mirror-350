# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250507-143900
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
from weberFuncs import PrintTimeMsg, GetCurrentTime
from weberFuncs import AddSecondsYmdHnsX, GetYYYYMMDDhhnnss
from CFileIoDumpDealBase import CFileIoDumpDealBase
from flarum_api import flarum_api
import os
from calc_match_time import calc_match_time
from control_cron import control_cron


class CFileIoDumpDealFlarum(CFileIoDumpDealBase):
    def __init__(self, sMcpTaskDir, sFlarumWorkDir):
        # sMcpTaskDir 是对应 TaskMcpClient 的Task工作目录，带尾部task
        # sFlarumWorkDir flarum_api对应工作目录，用于加载 flarum.env 等
        # CFileIoDumpDealBase.__init__(self, sMcpTaskDir)
        super().__init__(sMcpTaskDir)
        if not sFlarumWorkDir:
            # sFlarumWorkDir = GetSrcParentPath(__file__, True)
            sFlarumWorkDir = os.getcwd()
        self.oFlarum = flarum_api(sFlarumWorkDir)
        self.oFlarum.bDebugPrint = False
        self.oControlCron = control_cron(sFlarumWorkDir)

    def DumpFile4Query(self, sQueryDir):
        # 导出到文件到 sQueryDir 目录，作为 TaskMcpClient 的Query输入
        # 返回导出文件数目
        # 重写基类同名函数
        # PrintTimeMsg(f'CFileIoDumpDealFlarum.DumpFile4Query.sQueryDir={sQueryDir}=')
        # iDumpCnt = self.oFlarum.dump_file_4_query_discussion(sQueryDir)
        iDumpCnt = 0
        sTmNextCheck = GetYYYYMMDDhhnnss(60*60*24)  # 默认值
        dictTitleByDiscussionId = self.oFlarum.get_discussion_dict_by_tag(self.oFlarum.sFlarumTagFocus)
        for sDiscussionId, sTitle in dictTitleByDiscussionId.items():
            sCcid = f'discussion_%s' % sDiscussionId
            sAtEvery = self.oControlCron.get_control_cron_param(sCcid)
            if not sAtEvery:
                sAtEvery = self.oFlarum.sCronParamDefault
            sTmMatch, sTmCheck = calc_match_time(sAtEvery)
            # sNextMatchTm = AddSecondsYmdHnsX(sMatchTime + '.0', iNextMinute*60)[:15]
            if sTmNextCheck > sTmCheck:
                sTmNextCheck = sTmCheck
            dictTimeLog = self.oControlCron.load_control_cron_log(sCcid)
            if sTmMatch in dictTimeLog:
                sDumpInfo = dictTimeLog[sTmMatch]
                PrintTimeMsg(f"DumpFile4Query({sCcid}={sTmMatch})={sDumpInfo}=Pass!")
            else:
                sPostId, sContent = self.oFlarum.get_post_topic_by_discussion_id(sDiscussionId)
                if not sContent: continue
                sGenTm = GetCurrentTime()  # 加上执行时间后缀，避免不同周期的任务文件被覆盖
                sFN = f'flarum_{sDiscussionId}_{sGenTm}.md'
                sFullFN = os.path.join(sQueryDir, sFN)
                with open(sFullFN, 'w', encoding='utf8') as f:
                    f.write('%s\n' % sContent)
                PrintTimeMsg(f"DumpFile4Query({sFullFN})=OK!")
                sDumpStatus = 'DumpOK'
                iDumpCnt += 1
                dictTimeLog[sTmMatch] = '%s@%s' % (sDumpStatus, GetCurrentTime())
                self.oControlCron.save_control_cron_log(sCcid, dictTimeLog)
        # PrintTimeMsg(f"DumpFile4Query().iDumpCnt={iDumpCnt}=")
        return iDumpCnt, sTmNextCheck

    def DealFileResult(self, sNoExtFN, sResultDir):
        # 将sResultDir目录下的回复文件，提交到其它系统，并移动到备份目录
        # sNoExtFN 不带扩展名及_R/_Q的文件名
        # 返回处理成功与否
        # 重写基类同名函数
        # PrintTimeMsg(f'CFileIoDumpDealFlarum.DumpFile4Query.sNoExtFN={sNoExtFN}={sResultDir}=')
        # bDealOk = self.oFlarum.deal_file_result_reply_to_discussion(sNoExtFN, sResultDir)
        bDealOk = False
        lsParam = sNoExtFN.split('_')
        if len(lsParam) >= 3:
            sDiscussionId = lsParam[1]
            # sGenTm = lsParam[2]
            sFN = f'{sNoExtFN}_R.md'
            sFullFN = os.path.join(sResultDir, sFN)
            with open(sFullFN, 'r', encoding='utf8') as f:
                sContent = f.read()
                oJson = self.oFlarum.reply_discussion_post(sDiscussionId, sContent)
                bDealOk = oJson is not None
            PrintTimeMsg(f"deal_file_result_reply_to_discussion({sNoExtFN})={bDealOk}")
            return bDealOk
        else:
            PrintTimeMsg(f"deal_file_result_reply_to_discussion().sNoExtFN={sNoExtFN}=FmtError!")
            return False
        # return bDealOk


def mainFileIoDumpDealFlarum():
    sTaskType = 'dump' # dump/deal
    sMcpTaskDir = r'E:\WeberSrcRoot\Rocky9GogsRoot\RobotAgentMCP\TaskMcpClient\task'
    # sFlarumWorkDir = r'E:\WeberSrcRoot\Rocky9GogsRoot\RobotAgentMCP\FileIoDumpDeal'
    sFlarumWorkDir = ''  # 默认为空，则取当前工作目录
    if len(sys.argv) >= 2:
        sTaskType = sys.argv[1]
        if len(sys.argv) >= 3:
            sMcpTaskDir = sys.argv[2]
            if len(sys.argv) >= 4:
                sFlarumWorkDir = sys.argv[3]
    else:
        # PrintTimeMsg('Usage: python CFileIoDumpDealFlarum.py <sMcpTaskDir> [<sFlarumWorkDir>]')
        PrintTimeMsg('Usage: DumpDealFlarum dump/deal <sMcpTaskDir> [<sFlarumWorkDir>]')
        if not os.path.exists(sMcpTaskDir):
            sys.exit(-1)
    o = CFileIoDumpDealFlarum(sMcpTaskDir, sFlarumWorkDir)
    o.LoopFileIoDumpDeal(sTaskType)


if __name__ == '__main__':
    mainFileIoDumpDealFlarum()
