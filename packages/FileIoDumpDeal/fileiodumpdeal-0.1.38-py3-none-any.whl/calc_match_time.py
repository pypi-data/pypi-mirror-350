# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250509-100600
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
计算某个定时控制匹配的时间
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from weberFuncs import PrintTimeMsg, GetYYYYMMDDhhnnss, AddSubDayYYYYMMDD, YMDhnsAddSeconds


def str_to_int_default(sVal, iDefault=0):
    # 将字符串转为整数，提供缺省值以避免异常
    try:
        iResult = int(sVal)
    except ValueError:
        iResult = iDefault
    return iResult


def calc_match_time(sAtEvery, iMinMinute=5):
    # 依据定时控制计算当前匹配的时间
    # sAtEvery定时控制，取值：
    #    every 1h 每小时
    #    at 09:45 定时
    #    once 仅一次
    # iMinMinute 最小粒度，默认5分钟，可大不可小，必须是5/10/15/20/30/60
    # 20250509-091857  every 1h  ->  20250509-090000
    # 20250509-093857  every 0.5h  ->  20250509-093000
    # 20250509-091857  every 2h  ->  20250509-080000
    # 20250509-091857  at 09:45   ->  20250509-094500
    # 20250509-091857  once ->  YYYYMMDD-hhnnss
    # 返回“匹配执行时间串”，以及“下次检查时间串”
    # 匹配执行时间串：用于控制该任务执行的上一个匹配时间
    # 下次检查时间串：用于控制计算循环sleep时间
    if iMinMinute not in [5, 10, 15, 20, 30, 60]:
        if iMinMinute < 5:
            iMinMinute = 5
        elif iMinMinute > 60:
            iMinMinute = 60
        else:
            iMinMinute = iMinMinute // 5 * 5

    sTmMatch = 'YYYYMMDD-hhnnss'  # once
    sTmCheck = GetYYYYMMDDhhnnss(60 * iMinMinute)
    sYmdHns = GetYYYYMMDDhhnnss(0)
    sNowYmd = sYmdHns[0:8]
    if sAtEvery.startswith('at '):
        sHN = sAtEvery[3:]
        sH, cSep, sN = sHN.partition(':')
        iH = str_to_int_default(sH)
        iN = str_to_int_default(sN) // iMinMinute * iMinMinute
        sHHNNSS = '%.2d%.2d00' % (iH, iN)
        sTodayAt = '%s-%s' % (sNowYmd, sHHNNSS)
        sChkTm = YMDhnsAddSeconds(sTodayAt, 15)  # 宽限15分钟
        # 时间未到，则取昨天时间
        sYmd = sNowYmd if sYmdHns >= sChkTm else AddSubDayYYYYMMDD(sNowYmd, -1)
        sTmMatch = '%s-%s' % (sYmd, sHHNNSS)

        sYmd = sNowYmd if sYmdHns < sChkTm else AddSubDayYYYYMMDD(sNowYmd, +1)
        iHN = iH * 60 + iN - iMinMinute  # 提前一个周期
        if iHN >= 0:
            iH = iHN // 60
            iN = iHN % 60
            sHHNNSS = '%.2d%.2d00' % (iH, iN)
        else:
            iHN += 60 * 24
            iH = iHN // 60
            iN = iHN % 60
            sHHNNSS = '%.2d%.2d00' % (iH, iN)
            sYmd = AddSubDayYYYYMMDD(sYmd, -1)
        sTmCheck = '%s-%s' % (sYmd, sHHNNSS)
    elif sAtEvery.startswith('every '):
        sEveryParam = sAtEvery[6:]
        if not sEveryParam:
            sEveryParam = '1h'
        elif sEveryParam == '0.5h':
            sEveryParam = '30m'  # 转为整数
        sUnit = sEveryParam[-1:]
        if sUnit == 'h':  # 按小时处理
            iHour = str_to_int_default(sEveryParam[:-1])
            lsHourV = [1, 2, 3, 4, 6, 8, 12]
            if iHour not in lsHourV:
                for i in range(len(lsHourV)):
                    if lsHourV[i] <= iHour < lsHourV[i + 1]:
                        iHour = lsHourV[i]
                        break
                else:
                    if iHour > 12:
                        iHour = 12
                    else:
                        iHour = 1
            iH = str_to_int_default(sYmdHns[9:11])
            iH = iH // iHour * iHour
            sHHNNSS = '%.2d0000' % iH
            sTmMatch = '%s-%s' % (sNowYmd, sHHNNSS)
            iHN = (iH + iHour) * 60 - iMinMinute  # 提前一个周期
        else:  # 按分钟处理
            iN = str_to_int_default(sEveryParam[:-1])
            iN = iN // iMinMinute * iMinMinute
            iHN = str_to_int_default(sYmdHns[9:11]) * 60 + str_to_int_default(sYmdHns[11:13])
            iHN = iHN // iN * iN
            sHHNNSS = '%.2d%.2d00' % (iHN // 60, iHN % 60)
            sTmMatch = '%s-%s' % (sNowYmd, sHHNNSS)
            iHN = iHN + iN - iMinMinute  # 提前一个周期
        sYmd = sNowYmd
        if iHN >= 0:
            iH = iHN // 60
            iN = iHN % 60
            sHHNNSS = '%.2d%.2d00' % (iH, iN)
        else:
            iHN += 60 * 24
            iH = iHN // 60
            iN = iHN % 60
            sHHNNSS = '%.2d%.2d00' % (iH, iN)
            sYmd = AddSubDayYYYYMMDD(sYmd, -1)
        sTmCheck = '%s-%s' % (sYmd, sHHNNSS)
        # every
    PrintTimeMsg(f'calc_match_time({sAtEvery},{iMinMinute}).sTmMatch={sTmMatch},sTmCheck={sTmCheck}')
    return sTmMatch, sTmCheck


def mainClassOne():
    calc_match_time('every 1h')
    calc_match_time('every 20m')
    calc_match_time('every 120m')
    calc_match_time('every 6h')
    calc_match_time('every 4h')
    calc_match_time('every 5h')
    calc_match_time('every 8h')
    calc_match_time('every 12h')
    calc_match_time('once')
    calc_match_time('at 10:18')
    calc_match_time('at 3:8')
    calc_match_time('at 23:58')
    calc_match_time('at 0:59')
    calc_match_time('at 9:')
    calc_match_time('at :9')
    calc_match_time('at 9.')
    calc_match_time('at 9:35')
    calc_match_time('at 9:30')
    calc_match_time('at 9:45')
    calc_match_time('at 9:50')
    calc_match_time('at 10:00')
    calc_match_time('at 8:00')
    calc_match_time('at 0:00')
    calc_match_time('at 0:05')
    calc_match_time('at 23:55')
    calc_match_time('at 22:00')


if __name__ == '__main__':
    mainClassOne()


