import fileinput

resultsForPing = []

for line in fileinput.input():
    resultsForPing.append(line.rstrip())

N = int(input("連続何回以上タイムアウトすれば故障と見なしますか？"))

def getCrashedServer(resultsForPing:list):
    serversCrashed = {} #故障アドレス：故障日時 
    counterNoreply = {} #故障候補アドレス：タイムアウト回数

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
    return serversCrashed


