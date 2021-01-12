import fileinput

resultsForPing = []

for line in fileinput.input():
    resultsForPing.append(line.rstrip())

N = int(input("連続何回以上タイムアウトすれば故障と見なしますか？"))

def getCrashedServer(resultsForPing:list)->dict:
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

# ネットワークアドレス部：[含まれるIPアドレス]

def getSubnet(resultsForPing:list):
    subnet = {}
    for resultForPing in resultsForPing:
        adr = resultForPing.split(',')[1]
        bitsNewwork = int(adr.split('/')[1])
        adrNetwork = '.'.join(adr.split('/')[0].split('.')[:int(bitsNewwork/8)])
        if adrNetwork not in subnet:
            subnet[adrNetwork] = set()
        subnet[adrNetwork].add(adr)
    
    return subnet

serversCrashed = getCrashedServer(resultsForPing)
subnet = getSubnet(resultsForPing)

# ネットワーク内全部故障してたら、サブネットのサーバーアドレスの集合は故障したサーバーの部分集合のはず

