# 故障と判定した場合　一番最初の故障日時と復旧日時の差を故障時間とする
import fileinput

resultsForPing = []
serversCrashed = {} #故障アドレス：故障日時 
counterNoreply = {} #故障候補アドレス：タイムアウト回数


for line in fileinput.input():
    resultsForPing.append(line.rstrip())
N = int(input("連続何回以上タイムアウトすれば故障と見なしますか？"))

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
            del counterNoreply[resServerAdr]
