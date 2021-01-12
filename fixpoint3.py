#過負荷期間＝最初にpingの平均応答時間がtを超えてから次にpingの平均応答時間がtを下回るまでの期間
import fileinput

resultsForPing = []
for line in fileinput.input():
    resultsForPing.append(line.rstrip())

N = int(input("連続何回以上タイムアウトすれば故障と見なしますか？"))
m = int(input("直近何回で平均応答時間を計算しますか？"))
t = int(input("平均応答時間が何ミリ秒を超えたら過負荷とみなしますか？"))

def getCrashedServer(resultsForPing:list):
    serversCrashed = {} #故障アドレス：故障日時 
    counterNoreply = {}
    for resultForPing in resultsForPing:
        dt,resServerAdr,resServerState= resultForPing.split(',')
        if resServerState=='-':
            if resServerAdr not in serversCrashed:
                serversCrashed[resServerAdr] = dt
                counterNoreply[resServerAdr] = 1
            else:
                counterNoreply[resServerAdr]+=1

        elif resServerState!='-' and resServerAdr in serversCrashed:
            if counterNoreply[resServerAdr]<N:
                del serversCrashed[resServerAdr]
                del counterNoreply[resServerAdr]

            else:
                print(f"{resServerAdr}の故障期間は{serversCrashed[resServerAdr]}から{dt}まで")
                del serversCrashed[resServerAdr]

def getOverloadServer(resultsForPing:list):
    timesResponse={}
    dtResponse={}
    for resultForPing in resultsForPing:
        dt,resServerAdr,resServerState = resultForPing.split(',')
        if resServerAdr not in timesResponse:
            timesResponse[resServerAdr]=[]
        
        if resServerState!='-':
            timesResponse[resServerAdr].append(int(resServerState))

        responses = timesResponse[resServerAdr]
        if len(responses)>=m:
            if sum(responses[len(responses)-m:])/m >= t and resServerAdr not in dtResponse:
                dtResponse[resServerAdr]=dt
            elif sum(responses[len(responses)-m:])/m < t and resServerAdr in dtResponse:
                print(f"{resServerAdr}の過負荷期間は{dtResponse[resServerAdr]}から{dt}まで")
                del dtResponse[resServerAdr]
                del timesResponse[resServerAdr]

getOverloadServer(resultsForPing)
getCrashedServer(resultsForPing)
