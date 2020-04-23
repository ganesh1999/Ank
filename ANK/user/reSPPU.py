from .resFunction import *
import re
import PyPDF2


def studInfoX(pdfName):
    noPages = PyPDF2.PdfFileReader(open(r"{}".format(pdfName), 'rb')).numPages
    string0, string1, names, pointer = '', '', '', ''
    # 50 spaces String :spacestr[:40-len(x)]
    spaceStr = '                                                   '
    fullInfo = ''  # Overall information of Students
    subcodes, subCodes2 = [], []
    k, d = 0, 0
    for pageNo in range(noPages):
        string0 = fpdftoStrpg('{}'.format(pdfName), pageNo)
        list1 = fresList0(string0)

        for x in range(len(list1)):
            string1 = ''.join(list1[x])

            names = freStringN(string1)
            prn = freStringP(string1)
            pointer = freStringSp(string1)
            subCodes2 = freStringSc(string1).split('\n')
            for x in subCodes2:
                k = 0
                for y in subCodes2:
                    if x == y:
                        k = k+1
                    if k == 2:
                        d = d+1
                        k = 0
                    if d == 2:
                        x = x+'(o)'
                        d = 0
                subcodes.append(x)
            subgrades = freStringSg(string1).split('\n')
            subpercent = freStringSm(string1).split('\n')
            studpercent = studPercent(string1)
            fullInfo += ' '+names+'\n PRN : '+prn+'\n'

            for x, y, z in zip(subcodes, subgrades, subpercent):
                fullInfo += spaceStr[:30]+x+spaceStr[:13 -
                                                     len(x)]+z+spaceStr[:5-len(z)]+y+'\n'

            fullInfo += '\n'+' SGPA    :' + \
                str(pointer)+'\n'+' Total % :'+str(studpercent)+'\n'
            if float(pointer) >= 7.75:
                fullInfo += ' '+'RESULT : First Class With Distinction.'+'\n\n\n'
            if float(pointer) < 7.75 and float(pointer) >= 6.75:
                fullInfo += ' '+'RESULT : First Class.'+'\n\n\n'
            if float(pointer) < 6.75 and float(pointer) >= 6.25:
                fullInfo += ' '+'RESULT : Higher Second Class.'+'\n\n\n'
            if float(pointer) < 6.25 and float(pointer) >= 5.5:
                fullInfo += ' '+'RESULT : Second Class.'+'\n\n\n'
            if float(pointer) < 5.5 and float(pointer) >= 1:
                fullInfo += ' '+'RESULT : Pass.'+'\n\n\n'
            if float(pointer) < 1:
                fullInfo += ' '+'RESULT : Fail.'+'\n\n\n'
        subcodes.clear()
    # Disposoing useless Lists[],Strings
    list1.clear()
    subcodes.clear()
    subgrades.clear()
    subpercent.clear()
    del names
    del prn
    del pointer
    del string0
    del string1
    return fullInfo  # Total Information :Name,PRN,Subject Info,Pointer,total percentage,Result


def studRanking(pdfName):

    noPages = PyPDF2.PdfFileReader(open(r"{}".format(pdfName), 'rb')).numPages
    string0, string1, names, pointer = '', '', '', ''
    list1 = []
    studRanking = {}

    for pageNo in range(noPages):
        string0 = fpdftoStrpg(pdfName, pageNo)

        list1 = fresList0(string0)
        for x in range(len(list1)):
            string1 = ''.join(list1[x])

            names = freStringN(string1)
            pointer = freStringSp(string1)

            studRanking[names] = float(pointer)

    studRanking = sorted(studRanking.items(),
                         key=lambda k: (k[1], k[0]), reverse=True)

    # Disposing useless Lists[],Strings
    list1.clear()
    del string1
    del names
    del pointer

    return studRanking  # Dictionary of Student Names SGPAwise


def passRatio(pdfName):

    noPages = PyPDF2.PdfFileReader(open(r"{}".format(pdfName), 'rb')).numPages
    string0, string1, names = '', '', ''
    list1, listt, faiList, subCodes, subCodes2, subCodesX, listt3, listt4 = [
    ], [], [], [], [], [], [], []
    k, l, d = 0, 0, 0
    studFailed = {}

    for pageNo in range(noPages):
        string0 = fpdftoStrpg(pdfName, pageNo)
        list1 = fresList0(string0)

        for x in range(len(list1)):
            string1 = ''.join(list1[x])
            names = freStringN(string1)
            subCodes2 = freStringSc(string1).split('\n')
            for x in subCodes2:
                k = 0
                for y in subCodes2:
                    if x == y:
                        k = k+1
                    if k == 2:
                        d = d+1
                        k = 0
                    if d == 2:
                        x = x+'(o)'
                        d = 0
                subCodes.append(x)
                subCodesX.append(x)
            subGrades = freStringSg(string1).split('\n')
            for x, y in zip(subCodes, subGrades):
                stringxy = x+' '+y
                patRegex = re.compile(r'(\d.+?)\s+F')
                listt = patRegex.findall(stringxy)
                if listt:
                    for x in listt:
                        faiList.append(x)

        listt.clear()
        subCodes.clear()
        subGrades.clear()

    listt3 = sorted(list(dict.fromkeys(subCodesX)))  # Subcodes
    listt4 = sorted(list(dict.fromkeys(faiList)))  # failCodes

    for x in listt3:
        for xx in subCodesX:
            if x == xx:
                k = k+1
        for yy in faiList:
            if x == yy:
                l = l+1
        studFailed[x] = [l, k, round(((k-l)/k)*100, 2)]
        k = 0
        l = 0

    # Disposing useless Lists[],Strings
    listt3.clear()
    listt4.clear()
    subCodesX.clear()
    faiList.clear()
    list1.clear()
    del string0
    del string1
    del names
    del stringxy

    return studFailed  # Dictionary of Subcode : Failed , Overall


def infoFailed(pdfName):

    noPages = PyPDF2.PdfFileReader(open(r"{}".format(pdfName), 'rb')).numPages
    string0, string1, names, stringFail = '', '', '', ''
    list1, listt, faiList, subCodes, subCodes2 = [], [], [], [], []
    # for PrettyPrinting Spacelength 40
    spaceString = '                                             '
    k, d = 0, 0
    for pageNo in range(noPages):
        string0 = fpdftoStrpg(pdfName, pageNo)
        list1 = fresList0(string0)

        for x in range(len(list1)):
            string1 = ''.join(list1[x])
            names = freStringN(string1)
            subCodes2 = freStringSc(string1).split('\n')
            for x in subCodes2:
                k = 0
                for y in subCodes2:
                    if x == y:
                        k = k+1
                    if k == 2:
                        d = d+1
                        k = 0
                    if d == 2:
                        x = x+'(o)'
                        d = 0
                subCodes.append(x)
            subGrades = freStringSg(string1).split('\n')
            for x, y in zip(subCodes, subGrades):
                stringxy = x+' '+y
                # print(stringxx)
                patRegex = re.compile(r'.*F')
                listt = patRegex.findall(stringxy)
                # print(listt)
                if listt:
                    for x in listt:
                        faiList.append((names, x))
        subCodes.clear()
    for x in faiList:
        le = len(x[0])
        stringFail = stringFail+' '+x[0]+spaceString[:(40-le)]+x[1]+'\n'

    # Disposoing useless Lists[],Strings
    list1.clear()
    listt.clear()
    faiList.clear()
    del string0
    del string1
    del stringxy
    del names
    del spaceString

    return stringFail  # String Of StudentName and SubCodes,Grade Fs


def infoFailed2(pdfName):

    noPages = PyPDF2.PdfFileReader(open(r"{}".format(pdfName), 'rb')).numPages
    string0, string1, names, stringxx = '', '', '', ''
    list1, listt, listt3, listt4, subCodesX, subCodes, subCodes2, faiListN, faiList = [
    ], [], [], [], [], [], [], [], []
    studFailed = {}
    k, d = 0, 0
    for pageNo in range(noPages):
        string0 = fpdftoStrpg(pdfName, pageNo)
        list1 = fresList0(string0)

        for x in range(len(list1)):
            string1 = ''.join(list1[x])
            names = freStringN(string1)
            subCodes2 = freStringSc(string1).split('\n')
            for x in subCodes2:
                k = 0
                for y in subCodes2:
                    if x == y:
                        k = k+1
                    if k == 2:
                        d = d+1
                        k = 0
                    if d == 2:
                        x = x+'(o)'
                        d = 0
                subCodes.append(x)
                subCodesX.append(x)
            subGrades = freStringSg(string1).split('\n')
            for x, y in zip(subCodes, subGrades):
                stringxy = x+' '+y
                patRegex = re.compile(r'(\d.+?)\s+F')
                listt = patRegex.findall(stringxy)
                if listt:
                    for x in listt:
                        faiList.append(x)
                        faiListN.append((names, x))
        listt.clear()
        subCodes.clear()
        subGrades.clear()

    listt3 = sorted(list(dict.fromkeys(subCodesX)))  # Subcodes
    listt4 = sorted(list(dict.fromkeys(faiList)))  # failCodes
    for x in listt3:
        for xx in faiListN:
            if x == xx[1]:
                stringxx += xx[0]+'  ,  '
        studFailed[x] = stringxx
        stringxx = ''
    # Disposoing useless Lists[],Strings
    list1.clear()
    listt3.clear()
    listt4.clear()
    faiList.clear()
    faiListN.clear()
    del string0
    del string1
    del stringxy
    del stringxx
    del names

    return studFailed  # Dictionary of Subcode : Failed Names.
