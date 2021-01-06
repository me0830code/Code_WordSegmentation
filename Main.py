def handleMyDict() :
    
    # 處理成自己定義的 Dict { str: set }，value 使用 set 的好處是 find item 時間不隨 size 增加
    myDict = {} 
    
    for eachWord in fileDict :

        # 先判斷 key，若 len(eachWord) == 1 then key = eachWord else key = eachWord[0]
        key = eachWord if len(eachWord) == 1 else eachWord[0]

        # 再判斷 key 是否在 myDict 內
        keyIsExist = True if key in myDict else False

        # 若 key 存在 myDict 內 then value = myDict[key] else value = set()
        value = myDict[key] if keyIsExist else set()
        value.add(eachWord)

        # 最後再塞回去更新 key 對應的 value
        myDict[key] = value

    return myDict


def recordSplitIndex() :

    # 紀錄每一個 Line 中的每一個 Term 所要切的 index
    # Dict { int: list }
    # totalSplitIndex = { eachLineIndex: totalTermSplitIndexOfEachLine }
    # totalTermSplitIndexOfEachLine = [eachTermSplitIndexOfEachLine, eachTermSplitIndexOfEachLine, ...]

    # 初始化個樣參數
    totalSplitIndex = {}
    eachLineIndex = 0 

    totalTermSplitIndexOfEachLine = []
    eachTermSplitIndexOfEachLine = 0

    thisTerm = ''
    resetTerm = False

    for eachLine in fileInput :
        
        for eachStr in eachLine :
            
            # 一開始 thisTerm == '' 則 key = eachStr
            # 之後的 key 都以 thisTerm 的第一個字元為主
            key = eachStr if len(thisTerm) == 0 else thisTerm[0]
            
            # 若這個 Key 存在在 myDict 中，就可以等待繼續切
            # 若這個 Key 不存在在 myDict 中，則直接輸出
            myDictHaveThisKey = True if key in myDict else False

            if myDictHaveThisKey :

                # 先看當前的 Term + 下一個 Str 後，是否還是同一個 Term
                resetTerm = False if thisTerm + eachStr in myDict[key] else True

            # 直接輸出成 Term 的 Case 分兩種
            # Case1. 若這個 Key 沒有在 myDict 中，則直接輸出
            # Case2. 若這個已經是完整的 Term 了，再加下一個 eachStr 也無法成為新的一個 Term ( 沒有在myDict中 )
            if not myDictHaveThisKey or resetTerm :
                totalTermSplitIndexOfEachLine.append(eachTermSplitIndexOfEachLine)
                thisTerm = ''

            # 若是 keep thisTerm ，則 thisTerm 繼續累加
            # 若是 reset thisTerm，則 thisTerm 為下一個 eachStr
            eachTermSplitIndexOfEachLine += 1
            thisTerm += eachStr

        # eachLine 的 splitIndex 都處理完了，則存起來繼續做下一行
        totalSplitIndex[eachLineIndex] = totalTermSplitIndexOfEachLine
        eachLineIndex += 1

        # 剩餘參數初始化
        totalTermSplitIndexOfEachLine = []
        eachTermSplitIndexOfEachLine = 0

        thisTerm = ''
        resetTerm = False
    
    return totalSplitIndex


print('---------- 開始中文斷詞 ----------\n')
# ../input/default/

# 讀取外部中文字典
fileDict = open('Dict.txt', 'r', encoding = 'UTF-8').read().splitlines()

# 處理成自己定義的 Dict { str: set }，value 使用 set 的好處是 find item 時間不隨 size 增加
myDict = handleMyDict()

# 讀取 Input
fileInput = open('Input.txt', 'r', encoding = 'UTF-8').read().splitlines() 

# totalSplitIndex { int: list }，用來記錄每一段 Line 要切得點
totalSplitIndex = recordSplitIndex()

# 將結果寫檔
doneOutput = open('Output.txt', 'w', encoding = 'UTF-8') 

eachLineIndex = 0 
for eachLine in fileInput :

    eachNoStr = '[ ' + str(eachLineIndex + 1) + ' ]\n'

    print(eachNoStr, end = '')
    doneOutput.write(eachNoStr)

    for indexOfLineLength in range(len(eachLine)) :
    
        eachTokenStr = eachLine[indexOfLineLength]

        print(eachTokenStr, end = '')
        doneOutput.write(eachTokenStr)

        if indexOfLineLength + 1 in totalSplitIndex[eachLineIndex] :
            print(', ', end = '')
            doneOutput.write(', ')
    
    eachLineIndex += 1
    doneOutput.write('\n\n')
    print('\n')
    
doneOutput.close()
print('---------- 完成斷詞分析 ----------')
