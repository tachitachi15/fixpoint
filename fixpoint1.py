import fileinput

resultsForPing = []
serversCrashed = {} #故障アドレス：故障日時
for line in fileinput.input():
    resultsForPing.append(line.rstrip())

for resultForPing in resultsForPing:
    dt,resServerAdr,resServerState= resultForPing.split(',')
    if resServerState=='-' and resServerAdr not in serversCrashed:
        serversCrashed[resServerAdr] = dt


    elif resServerState!='-' and resServerAdr in serversCrashed:
        print(f"{resServerAdr}の故障期間は{serversCrashed[resServerAdr]}から{dt}まで")
        del serversCrashed[resServerAdr]
    

        
        
    