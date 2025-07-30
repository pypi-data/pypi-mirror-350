import os, regex
import pandas as pd
from tqdm import tqdm
from Bio import SeqIO
from concurrent.futures import ProcessPoolExecutor, as_completed
from src.process import run_FLASH, split_fq_file
from PreKO.utils import splitFASTQ, reverse_complement




class cPEData:
    def __init__(self):
        
        pass


def load_PE_input (sInFile):
    dict_sOutput = {}
    with open(sInFile, 'r') as InFile:
        for sReadLine in InFile:
            ## File Format ##
            ## Target#  | Barcode | WT_Target | Edit_Target
            ## 181      | TTT.... | CTGCC..   | CTGCC...

            if sReadLine.endswith('edit\n'): continue ## SKIP HEADER
            if sReadLine.endswith('#\n'): continue ## SKIP HEADER
            if sReadLine.startswith('#'): continue ## SKIP HEADER

            if ',' in sReadLine:
                list_sColumn = sReadLine.strip('\n').split(',')
            else:
                list_sColumn = sReadLine.strip('\n').split('\t')

            cPE           = cPEData()
            cPE.sBarcode  = list_sColumn[0].upper()
            cPE.sRefSeq   = list_sColumn[1].upper()
            cPE.sWTSeq    = list_sColumn[2].upper()
            cPE.sAltSeq   = list_sColumn[3].upper()

            if len(list_sColumn) == 6:
                cPE.sIntendedOnly = list_sColumn[4].upper()
                cPE.sMisMatchOnly = list_sColumn[5].upper()

            barcode = cPE.sBarcode

            if barcode not in dict_sOutput:
                dict_sOutput[barcode] = ''
            dict_sOutput[barcode] = cPE

    return dict_sOutput
#def END: load_PE_input

def load_read_data (dict_sOutFreq, sInFile):

    with open(sInFile, 'r') as InFile:
        for sReadLine in InFile:

            list_sColumn = sReadLine.strip('\n').split('\t')
            sBarcode     = list_sColumn[0]

            list_WT      = [sReadID for sReadID in list_sColumn[1].split(',') if sReadID]
            list_edited  = [sReadID for sReadID in list_sColumn[2].split(',') if sReadID]
            list_other   = [sReadID for sReadID in list_sColumn[3].split(',') if sReadID]

            dict_sOutFreq[sBarcode][0] += len(list_WT)
            dict_sOutFreq[sBarcode][1] += len(list_edited)
            dict_sOutFreq[sBarcode][2] += len(list_other)


class TargetAnalyzer:
    def __init__(self,):
        # flash 있는지 확인
        self.flash = '/extdata1/GS/flash'

        pass

    def setup(self, sAnalysis:str, file1:str, file2:str, barcode_file:str, sRE:str='[T]{4}[ACGT]{14}', min_overlap:int=5, overwrite:bool=False):
        
        ## 지금 돌릴 분석 (run)의 결과를 담을 경로 세팅
        self.sAnalysis = sAnalysis
        self.Out_DIR   = f'{self.sAnalysis}_results'
        self.Tmp_DIR   = f'{self.Out_DIR}/tmp'
        self.Log_File  = f'{self.Out_DIR}/log.log'
        os.makedirs(self.Tmp_DIR, exist_ok=True)

        ## Options
        self.sRE  = sRE
        
        ## Load Barcode Data -> Dict에서 DataFrame으로 변경하기
        self.dict_cPE = load_PE_input(barcode_file)

        ## Step 1: Run FLASH; Paired-end NGS read combining
        flash_log = run_FLASH(self.flash, file1, file2, self.Tmp_DIR, out_prefix=self.sAnalysis, min_overlap=min_overlap, overwrite=overwrite)
        with open(self.Log_File, 'a') as outfile:
            outfile.write(flash_log)

        ## Step 2: Split FASTQ files
        sFastqTag = f'{self.sAnalysis}.extendedFrags'
        self.list_sSplitFile = splitFASTQ(fastq_file=f'{self.Tmp_DIR}/{sFastqTag}', output_dir=self.Tmp_DIR)


    def run(self, error_type:str='SwitchingFree', nRefBuffer=24, nCores:int=30):
        # nRefBuffer설정: SF인 경우, 앞에서부터 spacer 위치까지, EF인 경우, pegRNA 전체 길이까지
        # Barcode list를 보고, SF인 경우에 자동으로 RefBuffer를 설정하는 코드를 추가하기

        ## 설정 1: Error Type: BarcodeOnly, ErrorFree (error가 있는 pegRNA를 filtering 하는 여부에 대한 설정)
        ## BarcodeOnly = pegRNA (spacer+scaffold+RTPBS+polyT) 부분에 error나 mismatch가 있어도 barcode counting 하겠다.
        ## ErrorFree   = pegRNA (spacer+scaffold+RTPBS+polyT) 부분이 우리가 디자인한대로 완벽히 일치하는 경우만 barcode counting.
        if error_type not in ['SwitchingFree', 'ErrorFree', 'BarcodeOnly']:
            raise KeyError(f'Not available key. Please select SwitchingFree, ErrorFree, or BarcodeOnly')

        ## Run Analysis ##
        self._barcode_sorter (error_type, nRefBuffer, nCores)
        self._combine_output_pickle (error_type)


    def _barcode_sorter(self, error_type, nRefBuffer, nCores):
    
        # Create parameters list
        list_sParameters = []
        
        for sSplitFile in self.list_sSplitFile:
            
            split_dir = f'{self.Tmp_DIR}/split'
            sInFastq  = f'{split_dir}/{sSplitFile}'
            sSplitTag = sSplitFile.replace('.fq', '').split('extendedFrags_')[1] # sSplitTag 예시: fastq_0001

            list_sParameters.append({
                'split_dir'  : split_dir,
                'split_tag'  : sSplitTag,
                'split_fq'   : sInFastq,
                'barcode'    : self.dict_cPE,
                're_pattern' : self.sRE,
                'error_type' : error_type,
                'nRefBuffer' : nRefBuffer,
            })

        # Use ProcessPoolExecutor for parallel processing
        with ProcessPoolExecutor(max_workers=nCores) as executor:
            # Submit tasks for `worker` and track progress
            list_work = [executor.submit(self._worker, params) for params in list_sParameters]
            for _ in tqdm(as_completed(list_work), total=len(list_work), desc="Sorting by Barcode", ncols=100, ascii=' ='):
                pass  # Wait for all worker tasks to complete


    def _worker (self, params):

        split_dir  = params['split_dir']
        sSplitTag  = params['split_tag']
        sInFastq   = params['split_fq']
        dict_cPE   = params['barcode']
        sRE        = params['re_pattern']
        sError     = params['error_type']
        nRefBuffer = params['nRefBuffer']

        dict_sBarcodes = {}
        
        if sError == 'ErrorFree':
            nRefBuffer = -nRefBuffer  # Barcode length to subtract from back of RefSeq
        elif sError == 'SwitchingFree':
            nRefBuffer = nRefBuffer

        # Process input FASTQ file
        # 이 부분을 나중에 gzip 파일로 작업하는 것으로 변경하기? 
        # Tmp file의 크기를 줄일 수 있는 방법을 고민해보자
        with open(sInFastq, 'r') as InFile:
            for sSeqData in SeqIO.parse(InFile, 'fastq'):

                sReadID = str(sSeqData.id)
                sNGSSeq = str(sSeqData.seq)

                for sReIndex in regex.finditer(sRE, sNGSSeq, overlapped=True):
                    nIndexStart   = sReIndex.start()
                    nIndexEnd     = sReIndex.end()
                    sBarcodeMatch = sNGSSeq[nIndexStart:nIndexEnd] # sRGN
                    sRefSeqCheck  = sNGSSeq[:nIndexStart]
                    
                    ### Skip Non-barcodes ###
                    try: cPE = dict_cPE[sBarcodeMatch]
                    except KeyError:continue

                    ### Skip error in Refseq ###
                    if sError != 'ErrorProne':
                        if cPE.sRefSeq[:nRefBuffer] not in sRefSeqCheck:
                            continue

                    if sBarcodeMatch not in dict_sBarcodes:
                        dict_sBarcodes[sBarcodeMatch] = []
                    dict_sBarcodes[sBarcodeMatch].append([sReadID, sNGSSeq, nIndexEnd])

        # Generate output dictionary
        dict_sOutput = {sBarcode: {'WT': [], 'Alt': [], 'Other': []} for sBarcode in dict_sBarcodes}
        for sBarcode, read_info in dict_sBarcodes.items():
            cPE = dict_cPE[sBarcode]

            for sReadID, sNGSSeq, sIndexS in read_info:
                sTargetCheck  = reverse_complement(sNGSSeq[sIndexS-1:])

                if cPE.sWTSeq in sTargetCheck:
                    dict_sOutput[sBarcode]['WT'].append(cPE.sWTSeq)
                elif cPE.sAltSeq in sTargetCheck:
                    dict_sOutput[sBarcode]['Alt'].append(cPE.sAltSeq)
                else:
                    dict_sOutput[sBarcode]['Other'].append(cPE.sAltSeq)
                
        # Write output to file
        sOutFile   = f'{split_dir}/{sSplitTag}.reads.txt'
        list_Types = ['WT', 'Alt', 'Other']

        with open(sOutFile, 'w') as OutFile:
            for sBarcode in dict_sOutput:
                sOut = '%s\t%s\n' % (sBarcode, '\t'.join([','.join(dict_sOutput[sBarcode][sAltType]) for sAltType in list_Types]))
                OutFile.write(sOut)

    #def END: worker
    

    def _combine_output_pickle (self, error_type):

        nSplitNo   = 4
        nFileCnt   = len(self.list_sSplitFile)
        list_nBins = [[int(nFileCnt * (i + 0) / nSplitNo), int(nFileCnt * (i + 1) / nSplitNo)] for i in range(nSplitNo)]

        list_sKeys     = ['WT', 'Alt', 'Other',]
        dict_sOutFreq  = {sBarcode: [0 for i in list_sKeys] for sBarcode in self.dict_cPE}
        
        for nStart, nEnd in tqdm(list_nBins, total=len(list_nBins), desc='Make temp output', ncols=100, ascii=' ='):
            list_sSubSplit  = self.list_sSplitFile[nStart:nEnd]
            dict_sOutFreq_Tmp = {sBarcode: [0, 0, 0,] for sBarcode in self.dict_cPE}

            for sSplitFile in list_sSubSplit:
                sSplitTag = sSplitFile.split('extendedFrags_')[1].replace('.fq', '') # sSplitTag 예시: fastq_0001
                sInFile   = f'{self.Tmp_DIR}/split/{sSplitTag}.reads.txt'
                
                assert os.path.isfile(sInFile)
                load_read_data (dict_sOutFreq_Tmp, sInFile)

            for sBarcode in self.dict_cPE:

                dict_sOutFreq[sBarcode][0] += dict_sOutFreq_Tmp[sBarcode][0]
                dict_sOutFreq[sBarcode][1] += dict_sOutFreq_Tmp[sBarcode][1]
                dict_sOutFreq[sBarcode][2] += dict_sOutFreq_Tmp[sBarcode][2]

        sHeader  = '%s\t%s\t%s\n' % ('Barcode', '\t'.join(list_sKeys), 'Total')
        sOutFile = f'{self.Out_DIR}/{self.sAnalysis}_{error_type}.combinedFreq.txt'
        
        with open(sOutFile, 'w') as OutFile:
            OutFile.write(sHeader)
            
            for sBarcode in self.dict_cPE:

                list_sOut = [str(sOutput) for sOutput in dict_sOutFreq[sBarcode]]
                nTotal  = sum(dict_sOutFreq[sBarcode])
                sOut    = '%s\t%s\t%s\n' % (sBarcode, '\t'.join(list_sOut), nTotal)
                OutFile.write(sOut)
                
    #def END: combine_output
#def END: TargetAnalyzer

