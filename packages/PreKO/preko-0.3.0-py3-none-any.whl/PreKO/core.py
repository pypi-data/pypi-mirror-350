import numpy as np

# CRISPResso 설치 필수
from CRISPResso2 import CRISPResso2Align


class BarcodeHash(object):

    @staticmethod
    def MakeHashList(strSeq, intBarcodeLen):
        listSeqWindow = [strSeq[i:i + intBarcodeLen] for i in range(len(strSeq))[:-intBarcodeLen - 1]]
        return listSeqWindow

    @staticmethod
    def IndexHashList(dictRef, strSeqWindow):
        lCol_ref = dictRef[strSeqWindow]
        strBarcode = strSeqWindow

        return (lCol_ref, strBarcode)


class CoreGotoh(object):

    def __init__(self, strEDNAFULL='', floOg='', floOe=''):
        self.npAlnMatrix = CRISPResso2Align.read_matrix(strEDNAFULL)
        self.floOg       = floOg
        self.floOe       = floOe
    
    def GapIncentive(self, strRefSeqAfterBarcode):
        ## cripsress no incentive == gotoh
        intAmpLen = len(strRefSeqAfterBarcode)
        npGapIncentive = np.zeros(intAmpLen + 1, dtype=np.int_) # intAmpLen range: < 500nt
        return npGapIncentive

    def RunCRISPResso2(self, strQuerySeqAfterBarcode, strRefSeqAfterBarcode, npGapIncentive):
        listResult = CRISPResso2Align.global_align(strQuerySeqAfterBarcode.upper(), strRefSeqAfterBarcode.upper(),
                                                  matrix=self.npAlnMatrix, gap_open=self.floOg, gap_extend=self.floOe,
                                                  gap_incentive=npGapIncentive)
        return listResult

