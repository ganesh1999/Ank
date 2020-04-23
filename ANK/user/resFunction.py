import re
import PyPDF2


def fpdftoStrpg(x, y):        # x is file name
    # PDF -->Text---------------------------------------->pdf-->reString0
    pdfObject = open(r"{}".format(x), 'rb')
    # alternate for above :pdfObject=open(r"%s"%(x),'rb')
    pdfRead = PyPDF2.PdfFileReader(pdfObject)
    reString = pdfRead.getPage(y).extractText()
    pdfObject.close()
    return reString


def fresList0(x):      # x is String O/P from fpdftoStr
    # Sort to minimum------------------------------------>reString0-->reString0
    # Pattern 0 : patRegex0
    patRegex0 = re.compile(
        r'([\w]?\d{7,12}[\w]? .*? TOTAL CREDITS EARNED . ..)')
    resList0 = patRegex0.findall(x)
    # O/P List -->reString0
    return resList0


def freStringID(x):     # x is O/P from freString0
    patRegex1 = re.compile(
        r'([\w]?\d{7,}?[\w]?\s{1,}\w{1,}(\.)?\s{1,3}?\w{1,}(\.)?\s{1,3}?\w{1,}(\.)?)|([\w]?\d{7,}[\w]?\s{1,}\w{1,}(\.)?\s{1,3}?\w{1,}(\.)?)|([\w]?\d{7,}[\w]?\s{2,}\w{1,}(\.)?)')
    resList = patRegex1.findall(x)
    resListI = []
    # List Created --> resListI[]
    # Tupled list to List
    for x in resList:
        for xx in x:
            if xx not in ['', ' ', '.']:
                resListI.append(xx)
    reStringI = '\n'.join(resListI)
    # O/P String --> reStringI
    resListI.clear()  # List Cleared -->resListI[]
    resList.clear()  # List Cleared -->resList[]
    return reStringI


def freStringN(x):      # x is O/P from freString0
    patRegex2 = re.compile(r'\s{2,}(.*)?')
    resList = patRegex2.findall(freStringID(x))
    reStringN = '\n'.join(resList)
    # O/P String of Names --> reStringN
    resList.clear()  # List Cleared -->resList[]
    return reStringN


def freStringP(x):      # x is O/P from freString0
    patRegex3 = re.compile(r'[\w]?\d{7,14}?[\w]?')
    resList = patRegex3.findall(freStringID(x))
    reStringP = '\n'.join(resList)
    # O/P String of PRN --> reStringP
    resList.clear()  # List Cleared -->resList[]
    return reStringP


def freStringSp(x):     # x is O/P from freString0
    patRegex4 = re.compile(r'SGPA.?.?.? (.*?) TOTAL CREDITS EARNED')
    resList = patRegex4.findall(x)
    reStringSp = '\n'.join(resList).replace(',', '')
    patRegexx = re.compile(r'[-]{1,}')
    reStringSp = patRegexx.sub('00', reStringSp)
    # O/P String of SGPA --> reStringSp
    resList.clear()
    return reStringSp


def freStringScg(x):
    patRegex5 = re.compile(
        r'\s{1,}?\d{5,7}?[\w]?\s{1,}.*?\s{1,}[A-Z][+]?\s{1,}?')
    reStringScg = '\n'.join(patRegex5.findall(x))
    patRegex6 = re.compile(r'(\d{5,8}?[\w]?)\s+?|\s+?([A-Z][+]?\s+?)')
    resList = patRegex6.findall(reStringScg)
    resList1 = []
    for xx in resList:
        for x in xx:
            if x != '':
                resList1.append(x)
    reStringScg = ' '.join(resList1)
    return reStringScg


def freStringSc(x):         # x in O/P from freString0
    patRegex8 = re.compile(r'\d{5,8}[\w]?')
    reStringSc = '\n'.join(patRegex8.findall(freStringScg(x)))
    # O/P String of SubCodes --> reStringSc
    return reStringSc


def freStringSm(x):         # x in O/P from freString0
    patRegex5 = re.compile(
        r'\s{1,}?\d{5,7}?[\w]?\s{1,}.*?\s{1,}[A-Z][+]?\s{1,}?')
    reStringScg = '\n'.join(patRegex5.findall(x))
    patRegex9 = re.compile(r'\s+(\w\w)\s+?\d+?\s+?')
    reStringSm = '\n'.join(patRegex9.findall(reStringScg))
    # O/P List of SubMarks --> reStringSm
    return reStringSm


def freStringSg(x):          # x in O/P from freString0
    patRegex10 = re.compile(r'\s[A-Z][+]?')
    reStringSg = '\n'.join(patRegex10.findall(freStringScg(x)))
    # O/P String of Grades --> reStringSg
    return reStringSg


def studPercent(x):
    string1 = re.compile(r'FF').sub('00', freStringSm(x))
    listt = string1.split('\n')
    listt2 = []
    for x in listt:
        if x == 'PP':
            listt.remove(x)
    for x in listt:
        listt2.append(int(x))
    percent = round((sum(listt2)/len(listt2)), 2)
    listt.clear()
    listt2.clear()
    return percent
