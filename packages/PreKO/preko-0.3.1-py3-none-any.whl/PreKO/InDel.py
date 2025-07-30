import os, logging, pickle
import numpy as np
import pandas as pd

from pathlib import Path
from typing import Optional
from PreKO.utils import FastqOpener, ParallelExecutor, ParallelExecutorConfig, splitFASTQ, setup_logging
from PreKO.params import InDelSearcherOptions

# CRISPResso 설치 필수
from CRISPResso2 import CRISPResso2Align

class InDelSearcher:
    def __init__(
            self,
            chunk_size: int = 100000,           # 1M reads / chunk
            base_quality: int = 20,             # NGS read qulity filter
            gap_open: float = -10,              # Alignment 
            gap_extend: float = 1,              # Alignment 
            insertion_window: int = 4,          # Insertion quatification window
            deletion_window: int = 4,           # Deletion quatification window
            pam_type: str = 'Cas9',             # 
            pam_pos: str = 'Forward',           # 
            save_pickle: bool = False,          # temp file
            save_split: bool = False,           # temp file
            save_classfied_FASTQ: bool = False, # temp file
            ):
        """주어진 barcode 파일과 FASTQ 파일에서 각 barcode (sgRNA-target)에서의 indel frequency를 분석해주는 파이프라인.

        Args:
            chunk_size (int, optional): FASTQ 파일의 reads를 얼마 단위로 쪼개서 processing 할지 결정. Defaults to 100000.
            base_quality (int, optional): NGS의 read quality score를 몇 점에서 filtering 할지 결정. Defaults to 20.
            gap_open (float, optional): _description_. Defaults to -10.
            gap_extend (float, optional): _description_. Defaults to 1.
            insertion_window (int, optional): _description_. Defaults to 4.
            deletion_window (int, optional): _description_. Defaults to 4.
            pam_type (str, optional): _description_. Defaults to 'Cas9'.
            pam_pos (str, optional): Target sequence에서 PAM의 방향 (Forward / Reverse). Defaults to 'Forward'.
            logger (str, optional): Logger의 ID를 지정. Defaults to 'InDelSearcher'.
            save_pickle (bool, optional): 임시파일로 생성되는 pickle을 삭제하지 않고 유지함. Defaults to False.
            save_split (bool, optional): 임시파일로 생성되는 splited FASTQ 파일을 삭제하지 않고 유지함. Defaults to False.
            save_classfied_FASTQ (bool, optional): InDel이 발견된 read를 pattern별로 구분한 FASTQ 파일을 생성. Defaults to False.
        """     

        # EDNAFULL path
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        self.strEDNAFULL = f'{script_dir}/EDNAFULL'

        ## Params setting ##
        self.options = InDelSearcherOptions(
            chunk_size        = chunk_size,
            base_quality      = base_quality,
            gap_open          = gap_open,
            gap_extend        = gap_extend,
            insertion_window  = insertion_window,
            deletion_window   = deletion_window,
            pam_type          = pam_type.upper(),
            pam_pos           = pam_pos,

            # Options for temp files 
            save_pickle            = save_pickle,
            save_split             = save_split,
            save_classfied_FASTQ   = save_classfied_FASTQ,
            )

    # End: def __init__


    def run(self, strFq: str, barcode:str, sample_name: str, thread: int = 15) -> pd.DataFrame:
        """InDel Searcher의 실제 분석 파이프라인을 실행하는 함수. 
        분석하려는 FASTQ 파일과 분석할 barcode 정보가 담긴 파일을 지정해서 실행한다.

        Args:
            strFq (str): 분석하고자 하는 FASTQ 파일의 경로. 
            barcode (str): Barcode / Target이 정리된 reference file. 기존에는 따로따로 파일이 있던 것을 csv 파일로 통합.
            sample_name (str): 분석 샘플의 이름. 결과 파일이 저장되는 directory의 이름으로 사용된다.
            thread (int, optional): Multiprocessing을 하기 위해 사용할 thread 개수를 지정. Defaults to 15.

        Raises:
            NameError: 만약 sample_name으로 만들어진 directory가 이미 있으면, 덮어쓸 것인지 물어본다. 덮어쓰지 않으면 error 발생.
        """        

        # Setting: Directory and Logger
        strOutputdir        = sample_name
        self.options.logger = f'{sample_name}_InDelSearcher'

        try:
            os.makedirs(strOutputdir)
        except:
            exist_ok = input('This sample_name already exist. Do you want to remove previous results and make new results? [y/n]')

            if exist_ok=='y': os.makedirs(strOutputdir, exist_ok=True)
            else: raise NameError('Please set different sample_name.')

        # Setting: Logging
        self.logger = setup_logging(logger_id=self.options.logger, logger_path=strOutputdir, consol_level=logging.INFO)
        self.logger.info('InDelSearcher Start')
        self.logger.info(f'Options: {str(self.options)}')

        # ToDo: Barcode들의 길이를 확인하고, 전부다 동일한지 체크하는 validation 넣기
        # 예를 들어, 모든 barcode의 길이 분포를 파악하고, 가장 많은 수의 길이가 분포하는 것을 찾고, 이와 다른 길이인 barcode를 출력해주기.

        # ToDo: 이 내용은 생략해도 될듯?
        if thread > 15:
            self.logger.warning('Optimal treads <= 15')
        
        self.logger.info('Start Alignment')
        ## ToDo: 함수의 입력값을 전부 불러오는 함수 찾아서 대체하기
        # self.logging.info(str(options))
        
        analyzer = InDelPatternAnalizer(
            strFq        = strFq,
            barcode      = barcode,
            options      = self.options,
            strOutputdir = strOutputdir,
            strEDNAFULL  = self.strEDNAFULL,
            )

        # 여러개의 job을 multiprocessing 하도록 설정
        df_frequency = analyzer.run(thread=thread)
        
        # Finish InDelSearcher
        self.logger.info('InDelSearcher End')

        return df_frequency

    #END:def


class InDelPatternAnalizer:
    """IndelSearcher에 특화된 alignment 파이프라인. 
    나중에는 general한 alignment에 대해서만 모듈을 구분하고,
    InDel 분석 외의 alignment가 필요한 곳에서도 사용할 수 있게 활용하면 좋겠다. 
    """    

    def __init__(self, strFq:str, barcode:str, strOutputdir:str, strEDNAFULL:str, options: Optional[InDelSearcherOptions]):
        """Total FASTQ(fq) lines / 4 = remainder 0.

        Args:
            strFq (str): 분석 대상이 되는 FASTQ 파일 경로
            barcode (str): 분석할 NGS 파일에 대응하는 barcode-target 정보가 담긴 파일 (.csv)
            strOutputdir (str): 임시파일 및 결과 파일이 저장될 디렉토리 경로. 주로 project name을 사용.
            strEDNAFULL (str): Alignment 알고리즘에서 사용하는 score table
            options (InDelSearcherOptions): Pydantic으로 정의된 InDelSearcher input parameters
        """

        # Setting: Directory
        # self.strTempdir = f'{strOutputdir}/tmp' # 지울 예정
        self.DirTemp    = Path(f'{strOutputdir}/tmp')
        self.DirTemp.mkdir(parents=True, exist_ok=True)

        # Setting: parameters
        self.strFq         = strFq
        self.barcode       = barcode
        self.strEDNAFULL   = strEDNAFULL
        self.options       = options or InDelSearcherOptions()

        # barcode 정보가 여기 들어있음
        self.df_info     = self._make_template(barcode) 

        # Setting: Logger
        self.logger = logging.getLogger(self.options.logger)
        self.logger.info('Aligner start')


    def run(self, thread:int) -> pd.DataFrame:
        """입력된 FASTQ 파일을 alignment 하는 함수. 
        전체 read 데이터를 split 해서 multiprocessing으로 할당해주는 것이 통합적으로 작동하도록 구현.

        Args:
            thread (int): Multiprocessing으로 몇 개 core를 사용할지 지정. 
        """        

        ## Split files를 여기 안에 submodule로 넣기
        self.logger.info(f'Split FASTQ File per 1M reads: {self.strFq}')
        splited_files = splitFASTQ(fastq_file=self.strFq, 
                                   output_dir=self.DirTemp,
                                   chunk_size=self.options.chunk_size, 
                                   file_prefix='chunk')

        self.logger.info(f'Total {len(splited_files)} splited files generated.')

        # Parallelizer
        self.logger.info(f'Start parallel executor: {thread} thread used.')
        p_config = ParallelExecutorConfig(n_jobs=thread, max_retries=1)
        executor = ParallelExecutor(p_config, logger=self.options.logger)
        success, errors = executor.run(splited_files, self._worker, desc="InDel Pattern Analysis")

        self.logger.info(f"Number of complted job: {len(success)}")
        self.logger.info(f"Number of failed job: {len(errors)}")

        if errors:
            error_msg = ''.join([
                f"\nTask {task} 실패\n{error_msg}\n" for task, error_msg in errors])
            self.logger.error(f'Error occured: {error_msg}')

        # 만들어진 temp 결과 파일들을 하나로 합치는 함수 구현하기
        self.logger.info('Make output')
        df_summary = self._make_output()
        
        df_freq = df_summary[[
            'Target_region', 'intSwitching', 'intNumOfTotal', 'intNumOfIns', 'intNumOfDel', 'intNumofCom', 
            'intFrame_0', 'intFrame_1', 'intFrame_2', 'IndelFrequency'
            ]]

        return df_freq
        

    def _worker(self, splited_fq) -> dict:
        # Splited FASTQ 파일을 열어서 
        InstFileOpen     = FastqOpener()
        listFastqForward = InstFileOpen.OpenFastqForward(splited_fq) # [(readID, sequence, quality_score)]
        splited_tag = os.path.basename(splited_fq).replace('.fastq', '')

        # IndelSearchParser를 불러온다. 원래 코드에서 template을 만드는 부분을 삭제하고, init에 넣었음. 
        InstIndelSearch = IndelSearchParser(self.df_info, self.options, self.strEDNAFULL)
        dict_Result = InstIndelSearch.SearchIndel(listFastqForward)

        # Make pickle output forward
        # ToDo: option으로 pickle 만드는 것을 지정하지 않으면 임시파일 없이 그대로 return
        # 바로 dataFrame으로 만들어서 결과 파일 만들기
        complete_id = self._make_result_pickle(dict_Result, splited_tag, self.options.pam_pos)
        
        return complete_id

        
    def _make_template(self, barcode:str) -> pd.DataFrame:

        # Load barcode file as DataFrame
        df_barcode = pd.read_csv(barcode)
        df_barcode.columns = ['Barcode', 'Target_region', 'Reference_sequence']

        list_info = []

        for i in df_barcode.index:
            
            data = df_barcode.loc[i] # debugging 0을 i로 바꿔야 함
            bc_seq = data['Barcode'].upper()
            target = data['Target_region'].upper()
            refseq = data['Reference_sequence'].upper()
            
            # 추가 info를 위해 필요한 인자들
            bc_pos = refseq.index(bc_seq)
            align_window = refseq[bc_pos + len(bc_seq):]

            try   : align_window_start = align_window.index(target)
            except: raise ValueError(f'\nalign_window: {align_window}\ntarget: {target}\n')

            list_info.append([
                # Reference info
                bc_seq, target,refseq,
                
                # align_window: Reference sequence after barcode
                align_window, align_window_start, align_window_start+len(target)-1,

                bc_pos + len(bc_seq) + align_window_start, 
                bc_pos + len(bc_seq) + align_window_start + len(target) - 1, 
                
                # Results를 담을 빈칸
                0,0,0,0,0,
                [],[],[],[],[],
                0,0,0,
            ])

        df_info = pd.DataFrame(list_info, columns=[
                # Reference info
                'Barcode', 'Target_region', 'Reference_sequence',

                # align_window: Reference sequence after barcode
                'align_window', 'align_window_start', 'align_window_end',
                
                'iIndel_start_pos', 'iIndel_end_pos',
                
                # Results를 담을 빈칸
                'intSwitching', 'intNumOfTotal', 'intNumOfIns', 'intNumOfDel', 'intNumofCom',
                'intTotalFastq', 'intInsFastq', 'intDelFastq', 'intComFastq', 'intIndelInfo',
                
                # Frame 정보를 담을 빈칸 
                'intFrame_0', 'intFrame_1', 'intFrame_2',
        ])

        return df_info
    

    def _make_result_pickle(self, 
                            dictResult:dict, 
                            # dictResultIndelFreq:dict, 
                            splited_tag:str, 
                            strBarcodePamPos:str=''):

        dict_output = {'dictResult'        : dictResult,
                    #   'dictResultIndelFreq': dictResultIndelFreq,
                      'strBarcodePamPos'   : strBarcodePamPos}

        with open(f'{str(self.DirTemp)}/aligned_{splited_tag}.pickle', 'wb') as Pickle:
            pickle.dump(dict_output, Pickle)

        return splited_tag


    def _make_output(self) -> pd.DataFrame:

        """
        dictResult: 
        {'TTTGTAGTCATACATCGCAATGTCAA': [0, 0, 0, 0, [], [], [], [], []]}

        dictResultIndelFreq: 
        {
            'TTTGTCGCGTATGAGTATG': 
            [
                [
                'AGCCGCCGCCATGGGGGCCTGCCTGGGAGCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAG',
                ['AGCCGCCGCCATGGGGTCTGCCTGGGAGCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAGTATT'],
                '18M1D',
                1.0,
                'AGCCGCCGCCATGGGGGCCTGCCTGGG',
                ['AGCCGCCGCCATGGGGGCCTGCCTGGGAGCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAG----'],
                ['AGCCGCCGCCATGGGGTC-TGCCTGGGAGCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAGTATT']
                ]],
            
            'TTTGCTCTCTCTAGACTAT': 
            [
                [
                    'CTCCATGAATCCAGCCCGCTCCTTCGGCCCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAG',
                    ['CTCCATGAATCCAGCCCGCTCTCTATGGAGTGTTCTGGGCCAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACCAGATCTTGAGACAAATGGCAGTATTA', 'CTCCATGAATCCCGCCCGCTCTCTATGGAGTGTTCTGGGCCAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACCAGATCTTGAGACAAATGGCAGTATTA'],
                    '25M14I',
                    0.5,
                    'CTCCATGAATCCAGCCCGCTCCTTCGG',
                    ['CTCCATGAATCCAGCCCGCTCCTTC--------------GGCCCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAG-----', 'CTCCATGAATCCAGCCCGCTCCTTC--------------GGCCCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAG-----'],
                    ['CTCCATGAATCCAGCCCGCTC--TCTATGGAGTGTTCTGGGCCAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACCAGATCTTGAGACAAATGGCAGTATTA', 'CTCCATGAATCCCGCCCGCTC--TCTATGGAGTGTTCTGGGCCAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACCAGATCTTGAGACAAATGGCAGTATTA']
                ],
                [
                    'CTCCATGAATCCAGCCCGCTCCTTCGGCCCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAG',
                    ['CTCCATGAATCCAGCCCGCTCTCTATGGAGTGTTCTGGGCCAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACCAGATCTTGAGACAAATGGCAGTATTA', 'CTCCATGAATCCCGCCCGCTCTCTATGGAGTGTTCTGGGCCAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACCAGATCTTGAGACAAATGGCAGTATTA'],
                    '21M2D',
                    0.5,
                    'CTCCATGAATCCAGCCCGCTCCTTCGG',
                    ['CTCCATGAATCCAGCCCGCTCCTTC--------------GGCCCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAG-----', 'CTCCATGAATCCAGCCCGCTCCTTC--------------GGCCCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAG-----'],
                    ['CTCCATGAATCCAGCCCGCTC--TCTATGGAGTGTTCTGGGCCAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACCAGATCTTGAGACAAATGGCAGTATTA', 'CTCCATGAATCCCGCCCGCTC--TCTATGGAGTGTTCTGGGCCAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCTAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACCAGATCTTGAGACAAATGGCAGTATTA']
                ]
                ],
        }
        
        strBarcodePamPos: 
        'Foward'
        """

        # Make dictionary for merging result values 
        dict_summary = self._make_template(self.barcode).set_index('Barcode').to_dict(orient='index')
        
        # Load all pickles
        # pickles = glob.glob(f'{self.strTempdir}/*.pickle') # 지울 예정
        pickles = self.DirTemp.glob('*.pickle')

        for binPickle in pickles:
            with open(binPickle, 'rb') as PickleResult:
                
                dictPickleResult    = pickle.load(PickleResult)
                dictResult          = dictPickleResult['dictResult']
                # dictResultIndelFreq = dictPickleResult['dictResultIndelFreq'] # Indel 정보 (e.g., 25M14I)들을 가져올 수 있음.

                for strBarcode, data in dictResult.items():

                    ds = dict_summary[strBarcode]

                    ds['intSwitching']  += data['intSwitching']
                    ds['intNumOfTotal'] += data['intNumOfTotal']
                    ds['intNumOfIns']   += data['intNumOfIns']
                    ds['intNumOfDel']   += data['intNumOfDel']
                    ds['intNumofCom']   += data['intNumofCom']
                    ds['intFrame_0']   += data['intFrame_0']
                    ds['intFrame_1']   += data['intFrame_1']
                    ds['intFrame_2']   += data['intFrame_2']

                    # FastqOut: _Classified_Indel_barcode.fastq
                    # 우선 memmory에 담아놓는데, 만약 memmory 문제가 있으면 각 pickle마다 dump 해서 저장하기?
                    # ToDo: 어차피 안 쓰게 될 기능인 것 같음. 그냥 오해의 소지 없이 지우는 것이 깔끔할듯
                    # 만약 쓰고 싶다면, 5000개 데이터 단위로 pickle에 넣고 갱신하도록 지정. 메모리 overuse 방지.
                    if self.options.save_classfied_FASTQ == True:
                        ds['intSwitching']  += data['intSwitching']
                        ds['intTotalFastq'] += data['intTotalFastq']
                        ds['intInsFastq']   += data['intInsFastq']
                        ds['intDelFastq']   += data['intDelFastq']
                        ds['intComFastq']   += data['intComFastq']
                        ds['intFrame_0']   += data['intFrame_0']
                        ds['intFrame_1']   += data['intFrame_1']
                        ds['intFrame_2']   += data['intFrame_2']

        # Temp file들을 삭제할지 결정하는 부분
        if self.options.save_pickle == False:
            self.logger.info('Delete tmp pickles')
            for f in self.DirTemp.glob('*.pickle'): 
                f.unlink()

        if self.options.save_split == False:
            self.logger.info('Delete splited input files')
            for f in self.DirTemp.glob('*.fastq'): 
                f.unlink()

        # convert dict to DataFrame
        df_summary = pd.DataFrame.from_dict(dict_summary, orient='index')
        df_summary['IndelFrequency'] = ((df_summary['intNumOfIns'] + df_summary['intNumOfDel'] + df_summary['intNumofCom']) / df_summary['intNumOfTotal']) * 100
        df_summary.index.name = 'Barcode'

        return df_summary

    #END:def

# END: cls InDelPatternAnalizer


class IndelSearchParser(object):

    def __init__(self, df_info, options, strEDNAFULL):

        # Setting: parameters and options
        self.options     = options
        self.strEDNAFULL = strEDNAFULL
        self.barcode_len = self._check_barcode_lengths(df_info)
        self.dict_info   = df_info.set_index('Barcode').to_dict(orient='index')


    def SearchIndel(self, lFASTQ:list, ):

        # lFASTQ : [(ID, seq, qual),(ID, seq, qual)]
        
        # Barcode length 추출
        intBarcodeLen = self.barcode_len
        InstGotoh = GotohAlignment(strEDNAFULL=self.strEDNAFULL, floOg=self.options.gap_open, floOe=self.options.gap_extend)

        # 각 NGS read 1개마다 진행되는 알고리즘
        for lCol_FASTQ in lFASTQ:
            
            # Step 1: NGS read info에 대한 검증
            sName = lCol_FASTQ[0]
            if self.options.pam_pos == 'Reverse':
                sSeq  = lCol_FASTQ[1][::-1]
                lQual = lCol_FASTQ[2][::-1]
            else:
                sSeq  = lCol_FASTQ[1] # NGS read sequence
                lQual = lCol_FASTQ[2] # NGS read quality

            assert isinstance(sName, str) and isinstance(sSeq, str) and isinstance(lQual, list)

            # Step 2: # NGS read에서 barcode 길이만큼 1bp씩 밀어가며 sequence 가져오기 (barcode candidates)
            listSeqWindow = HashBarcode.MakeHashList(sSeq, intBarcodeLen)

            iInsert_count  = 0
            iDelete_count  = 0
            iComplex_count = 0
            
            # Frame calculation
            indel_sum = 0
            iFrame_0  = 0
            iFrame_1  = 0
            iFrame_2  = 0

            for bc_cand in listSeqWindow:
                
                try:
                    # Barcode candidate이 barcode dictionary에 있는지 찾기
                    ref_info, sBarcode = HashBarcode.IndexHashList(self.dict_info, bc_cand)
                except KeyError:
                    continue
                
                sTarget_region     = ref_info['Target_region']
                sGuideN19_seq      = sTarget_region[5:24]
                align_window       = ref_info['align_window']
                align_window_start = ref_info['align_window_start']
                align_window_end   = ref_info['align_window_end']

                # Filtering Switching
                if sGuideN19_seq not in sSeq[15:50]:
                    self.dict_info[sBarcode]['intSwitching'] += 1
                    continue

                try:
                    if self.options.pam_type == 'CAS9':
                        iKbp_front_Indel_end = align_window_end - 6  ## cas9:-6, cpf1:-4
                    elif self.options.pam_type == 'CAF1':
                        iKbp_front_Indel_end = align_window_end - 4  ## NN(N)*NNN(N)*NNNN
                except Exception as e:
                    raise AssertionError(f'pam_type is not available: {self.options.pam_type}')


                (sSeq, sQuery_seq, lQuery_qual) = self._CheckBarcodePosAndRemove(sSeq, sBarcode, lQual)

                ## Alignment Seq to Ref
                npGapIncentive = InstGotoh.GapIncentive(align_window)

                try:
                    lResult = InstGotoh.RunCRISPResso2(sQuery_seq.upper(), align_window.upper(), npGapIncentive)

                except Exception as e:
                    logging.error(e, exc_info=True)
                    continue

                sQuery_needle_ori = lResult[0]
                sRef_needle_ori   = lResult[1]

                sRef_needle, sQuery_needle            = self._TrimRedundantSideAlignment(sRef_needle_ori, sQuery_needle_ori)
                lInsertion_in_read, lDeletion_in_read = self._MakeIndelPosInfo(sRef_needle, sQuery_needle)

                lTarget_indel_result = []  # ['20M2I', '23M3D' ...]

                iInsert_count = self._TakeInsertionFromAlignment(lInsertion_in_read, iKbp_front_Indel_end, lTarget_indel_result,
                                                                 align_window_end, iInsert_count)

                iDelete_count = self._TakeDeletionFromAlignment(lDeletion_in_read, iKbp_front_Indel_end, lTarget_indel_result,
                                                                align_window_end, iDelete_count)

                if iInsert_count == 1 and iDelete_count == 1:
                    iComplex_count = 1
                    iInsert_count = 0
                    iDelete_count = 0

                # Debugging: Memmory overuse
                # listResultFASTQ = self._MakeAndStoreQuality(sName, sSeq, lQual, self.dict_info, sBarcode)

                """
                iQual_end_pos + 1 is not correct, because the position is like this.
                *NNNN*(N)
                So, '+ 1' is removed.
                Howerver, seqeunce inspects until (N) position. indel is detected front of *(N).
                """

                if np.mean(lQuery_qual[align_window_start : align_window_end + 1]) >= self.options.base_quality: ## Quality cutoff

                    """
                    23M3I
                    23M is included junk_seq after barcode,

                    barcorde  junk   targetseq   others
                    *********ACCCT-------------ACACACACC
                    so should select target region.
                    If junk seq is removed by target region seq index pos.
                    """
                    # filter start,
                    iTarget_start_from_barcode   = align_window.index(sTarget_region)
                    lTrimmed_target_indel_result = self._FixPos(lTarget_indel_result, iTarget_start_from_barcode)

                    for indel_pattern in lTrimmed_target_indel_result:
                        indel_type = indel_pattern.split('M')[1]

                        if indel_type.endswith('I'):
                            indel_sum += int(indel_type.split('I')[0])
                        elif indel_type.endswith('D'):
                            indel_sum -= int(indel_type.split('D')[0])

                    if len(lTrimmed_target_indel_result) > 0:
                        indel_sum = indel_sum % 3

                        if   indel_sum == 0: iFrame_0 = 1
                        elif indel_sum == 1: iFrame_1 = 1
                        elif indel_sum == 2: iFrame_2 = 1
                    
                    # Debugging: Memmory overuse
                    # align_window, sQuery_seq = self._StoreToDictResult(align_window, sQuery_seq, iTarget_start_from_barcode, 
                    #                                                    self.dict_info, sBarcode, lTrimmed_target_indel_result, 
                    #                                                    sTarget_region, sRef_needle_ori, sQuery_needle_ori, 
                    #                                                    iInsert_count, iDelete_count, iComplex_count, listResultFASTQ)
                else:
                    iInsert_count  = 0
                    iDelete_count  = 0
                    iComplex_count = 0

                # total matched reads, insertion, deletion, complex
                self.dict_info[sBarcode]['intNumOfTotal'] += 1
                self.dict_info[sBarcode]['intNumOfIns'] += iInsert_count
                self.dict_info[sBarcode]['intNumOfDel'] += iDelete_count
                self.dict_info[sBarcode]['intNumofCom'] += iComplex_count
                self.dict_info[sBarcode]['intFrame_0']  += iFrame_0
                self.dict_info[sBarcode]['intFrame_1']  += iFrame_1
                self.dict_info[sBarcode]['intFrame_2']  += iFrame_2

                break

            #End:for
        #END:for
        return self.dict_info

    def _check_barcode_lengths(self, df_barcode:pd.DataFrame, barcode_column:str='Barcode') -> int:
        """Barcode 정보가 들어있는 DataFrame에서 barcode의 길이를 추출하는 함수.

        Args:
            df_barcode (pd.DataFrame): Barcode 정보
            barcode_column (str, optional): DataFrame에서 barcode 정보가 들어있는 column 이름. Defaults to 'Barcode'.

        Raises:
            ValueError: 만약 전체 barcode 중에서 길이가 다른 것이 발견되면 발생.

        Returns:
            int: 추출된 barcode 길이
        """        


        # 2. NaN 제거 + 문자열로 변환
        barcode_series = df_barcode[barcode_column].dropna().astype(str)

        # 3. 각 barcode의 길이 계산
        barcode_lengths = barcode_series.apply(len)

        # 4. 길이별로 몇 개씩 있는지 
        length_counts = barcode_lengths.value_counts().sort_index()
    
        # 길이 중 가장 많은 수 차지하는 길이를 expected length로 결정
        expected_length = int(length_counts.idxmax())

        # expected length가 아닌 barcode만 필터링
        invalid_barcodes = barcode_series[barcode_lengths != expected_length]

        # 그 barcode들의 잘못된 길이 목록 추출 (중복 제거 + 정렬) + np.int64 → int 변환
        invalid_lengths = sorted([int(x) for x in invalid_barcodes.apply(len).unique()])

        # 만약 잘못된 길이의 barcode가 하나라도 있다면 에러 발생
        if not invalid_barcodes.empty:
            invalid_sequences = invalid_barcodes.tolist()  # 문자열 리스트로 변환
            
            raise ValueError(
                f"Expected barcode length: {expected_length},"
                f"but found barcode(s) with length(s): {invalid_lengths}.\n"
                f"Invalid barcode sequences:\n{invalid_sequences}"
            )

        return expected_length

    def _CheckBarcodePosAndRemove(self, sSeq, sBarcode, lQual):
        '''Query: NGS read after barcode'''

        # Check the barcode pos and remove it.
        sSeq = sSeq.replace('\r', '')
        iBarcode_start_pos_FASTQ = sSeq.index(sBarcode)
        iBarcode_end_pos_FASTQ   = iBarcode_start_pos_FASTQ + len(sBarcode) - 1

        # Use this.
        sQuery_seq = sSeq[iBarcode_end_pos_FASTQ + 1:]
        lQuery_qual = lQual[iBarcode_end_pos_FASTQ:]

        return (sSeq, sQuery_seq, lQuery_qual)

    def _TrimRedundantSideAlignment(self, sRef_needle_ori, sQuery_needle_ori):

        # detach forward ---, backward ---
        # e.g.    ref   ------AAAGGCTACGATCTGCG------
        #         query AAAAAAAAATCGCTCTCGCTCTCCGATCT
        # trimmed ref         AAAGGCTACGATCTGCG
        # trimmed qeury       AAATCGCTCTCGCTCTC
        iReal_ref_needle_start = 0
        iReal_ref_needle_end = len(sRef_needle_ori)
        iRef_needle_len = len(sRef_needle_ori)

        for i, sRef_nucle in enumerate(sRef_needle_ori):
            if sRef_nucle in ['A', 'C', 'G', 'T']:
                iReal_ref_needle_start = i
                break

        for i, sRef_nucle in enumerate(sRef_needle_ori[::-1]):
            if sRef_nucle in ['A', 'C', 'G', 'T']:
                iReal_ref_needle_end = iRef_needle_len - (i + 1)
                # forward 0 1 2  len : 3
                # reverse 2 1 0,  len - (2 + 1) = 0
                break

        sRef_needle = sRef_needle_ori[iReal_ref_needle_start:iReal_ref_needle_end + 1]
        if iReal_ref_needle_start:
            sQuery_needle = sQuery_needle_ori[:iReal_ref_needle_end]
        sQuery_needle = sQuery_needle_ori[:len(sRef_needle)]
        # detaching completion
        return (sRef_needle, sQuery_needle)

    def _MakeIndelPosInfo(self, sRef_needle, sQuery_needle):

        # indel info making.
        iNeedle_match_pos_ref   = 0
        iNeedle_match_pos_query = 0
        iNeedle_insertion       = 0
        iNeedle_deletion        = 0

        lInsertion_in_read = []  # insertion result [[100, 1], [119, 13]]
        lDeletion_in_read  = []  # deletion result  [[97, 1], [102, 3]]

        for i, (sRef_nucle, sQuery_nucle) in enumerate(zip(sRef_needle, sQuery_needle)):

            if sRef_nucle == '-':
                iNeedle_insertion += 1

            if sQuery_nucle == '-':
                iNeedle_deletion += 1

            if sRef_nucle in ['A', 'C', 'G', 'T']:
                if iNeedle_insertion:
                    lInsertion_in_read.append([iNeedle_match_pos_ref, iNeedle_insertion])
                    iNeedle_insertion = 0
                iNeedle_match_pos_ref += 1

            if sQuery_nucle in ['A', 'C', 'G', 'T']:
                if iNeedle_deletion:
                    lDeletion_in_read.append([iNeedle_match_pos_query, iNeedle_deletion])
                    iNeedle_match_pos_query += iNeedle_deletion
                    iNeedle_deletion = 0
                iNeedle_match_pos_query += 1

        return (lInsertion_in_read, lDeletion_in_read)


    def _TakeInsertionFromAlignment(self, lInsertion_in_read, iKbp_front_Indel_end, lTarget_indel_result,
                                    iIndel_end_from_barcode_pos, iInsert_count):
        """
        ins case
        ...............................NNNNNNNNNNNNNN....NNNNNNNNNNNNNNNNNNN*NNNNNAGCTT
        """
        for iMatch_pos, iInsertion_pos in lInsertion_in_read:
            if self.options.pam_type == 'CAS9':
                # if i5bp_front_Indel_end == iMatch_pos -1 or iIndel_end_from_barcode_pos == iMatch_pos -1: # iMatch_pos is one base # original ver
                if iKbp_front_Indel_end - self.options.insertion_window <= iMatch_pos - 1 <= iKbp_front_Indel_end + self.options.insertion_window:  # iMatch_pos is one base
                    iInsert_count = 1
                    lTarget_indel_result.append(str(iMatch_pos) + 'M' + str(iInsertion_pos) + 'I')

            elif self.options.pam_type == 'CPF1':
                if iKbp_front_Indel_end - self.options.insertion_window <= iMatch_pos - 1 <= iKbp_front_Indel_end + self.options.insertion_window or \
                        iIndel_end_from_barcode_pos - self.options.insertion_window <= iMatch_pos - 1 <= iIndel_end_from_barcode_pos + self.options.insertion_window:  # iMatch_pos is one base
                    iInsert_count = 1
                    lTarget_indel_result.append(str(iMatch_pos) + 'M' + str(iInsertion_pos) + 'I')

        return iInsert_count

    def _TakeDeletionFromAlignment(self, lDeletion_in_read, iKbp_front_Indel_end, lTarget_indel_result,
                                   iIndel_end_from_barcode_pos, iDelete_count):

        """
        del case 1
        ...............................NNNNNNNNNNNNNN....NNNNNNNNNNNNNNNNNNNNN**NNNAGCTT
        del case 2
        ...............................NNNNNNNNNNNNNN....NNNNNNNNNNNNNNNNNNNNN**NNNNNCTT
        """
        for iMatch_pos, iDeletion_pos in lDeletion_in_read:
            """
            Insertion: 30M3I
                   ^
            ACGT---ACGT
            ACGTTTTACGT -> check this seq
            Insertion just check two position

            Deletion: 30M3D
                 ^
            ACGTTTTACGT
            ACGT---ACGT -> check this seq
            But deletion has to includes overlap deletion.
            """
            if self.options.pam_type == 'CAS9':
                if (iMatch_pos - self.options.deletion_window - 1 <= iKbp_front_Indel_end and iKbp_front_Indel_end < (iMatch_pos + iDeletion_pos + self.options.deletion_window - 1)):
                    iDelete_count = 1
                    lTarget_indel_result.append(str(iMatch_pos) + 'M' + str(iDeletion_pos) + 'D')
            elif self.options.pam_type == 'CPF1':
                if (iMatch_pos - self.options.deletion_window - 1 <= iKbp_front_Indel_end and iKbp_front_Indel_end < (iMatch_pos + iDeletion_pos + self.options.deletion_window - 1)) or \
                   (iMatch_pos - self.options.deletion_window - 1 <= iIndel_end_from_barcode_pos and iIndel_end_from_barcode_pos < (iMatch_pos + iDeletion_pos + self.options.deletion_window - 1)):
                    iDelete_count = 1
                    lTarget_indel_result.append(str(iMatch_pos) + 'M' + str(iDeletion_pos) + 'D')

        return iDelete_count

    def _MakeAndStoreQuality(self, sName, sSeq, lQual, dict_info, sBarcode):
        listResultFASTQ = [sName, sSeq, '+', ''.join(chr(i + 33) for i in lQual)]
        dict_info[sBarcode]['intTotalFastq'].append(listResultFASTQ)
        return listResultFASTQ

    def _FixPos(self, lTarget_indel_result, iTarget_start_from_barcode):

        lTrimmed_target_indel_result = []

        for sINDEL in lTarget_indel_result:
            # B - A is not included B position, so +1
            iMatch_target_start = int(sINDEL.split('M')[0]) - iTarget_start_from_barcode
            """ This part determines a deletion range.
                                      ^ current match pos                                           
            AGCTACGATCAGCATCTGACTTACTTC[barcode]


                           ^ fix the match start at here. (target region)                                           
            AGCTACGATCAGCATC TGACTTACTTC[barcode]

            if iMatch_target_start < 0:
                sContinue = 1

            But, this method has some problems.

                           ^ barcode start
            AGCTACGATCAGCAT*********C[barcode]
            Like this pattern doesn't seleted. because, deletion checking is begun the target region start position. 
            Thus, I have fixed this problem.
            """

            if iMatch_target_start <= -(iTarget_start_from_barcode):
                # print(iMatch_target_start, iTarget_start_from_barcode)
                continue

            lTrimmed_target_indel_result.append(str(iMatch_target_start) + 'M' + sINDEL.split('M')[1])
        # filter end
        return lTrimmed_target_indel_result

    def _StoreToDictResult(self, align_window, sQuery_seq, iTarget_start_from_barcode,
                           dict_info, sBarcode, lTrimmed_target_indel_result, sTarget_region, sRef_needle_ori, sQuery_needle_ori,
                           iInsert_count, iDelete_count, iComplex_count, listResultFASTQ):

        align_window   = align_window[iTarget_start_from_barcode:]
        sQuery_seq = sQuery_seq[iTarget_start_from_barcode:]

        dict_info[sBarcode]['intIndelInfo'].append([align_window, sQuery_seq, lTrimmed_target_indel_result,
                                                     sTarget_region, sRef_needle_ori, sQuery_needle_ori])
        if iInsert_count:
            dict_info[sBarcode]['intInsFastq'].append(listResultFASTQ)
        elif iDelete_count:
            dict_info[sBarcode]['intDelFastq'].append(listResultFASTQ)
        elif iComplex_count:
            dict_info[sBarcode]['intComFastq'].append(listResultFASTQ)

        return (align_window, sQuery_seq)

    def CalculateIndelFrequency(self, dict_info):
        dict_info_INDEL_freq = {}
        
        
        for sBarcode, lValue in dict_info.items():
            # lValue[gINDEL_info] : [[align_window, sQuery_seq_after_barcode, lTarget_indel_result, sTarget_region], ..])

            sRef_seq_loop = ''
            llINDEL_store = []  # ['ACAGACAGA', ['20M2I', '23M3D']]
            dINDEL_freq   = {}

            if lValue['intIndelInfo']:
                for sRef_seq_loop, sQuery_seq, lINDEL, sTarget_region, sRef_needle, sQuery_needle in lValue['intIndelInfo']: # llINDEL : [['20M2I', '23M3D'], ...]
                    # print 'lINDEL', lINDEL
                    for sINDEL in lINDEL:
                        llINDEL_store.append([sQuery_seq, sINDEL, sRef_needle, sQuery_needle])

                iTotal = len([lINDEL for sQuery_seq, lINDEL, sRef_needle, sQuery_needle in llINDEL_store])

                for sQuery_seq, sINDEL, sRef_needle, sQuery_needle in llINDEL_store:
                    dINDEL_freq[sINDEL] = [[], 0, [], []]

                for sQuery_seq, sINDEL, sRef_needle, sQuery_needle in llINDEL_store:
                    dINDEL_freq[sINDEL][1] += 1
                    dINDEL_freq[sINDEL][0].append(sQuery_seq)
                    dINDEL_freq[sINDEL][2].append(sRef_needle)
                    dINDEL_freq[sINDEL][3].append(sQuery_needle)

                for sINDEL in dINDEL_freq:
                    lQuery        = dINDEL_freq[sINDEL][0]
                    iFreq         = dINDEL_freq[sINDEL][1]
                    lRef_needle   = dINDEL_freq[sINDEL][2]
                    lQuery_needle = dINDEL_freq[sINDEL][3]

                    try:
                        dict_info_INDEL_freq[sBarcode].append([sRef_seq_loop, lQuery, sINDEL, float(iFreq) / iTotal,
                                                             sTarget_region, lRef_needle, lQuery_needle])
                    except (KeyError, TypeError, AttributeError) as e:
                        dict_info_INDEL_freq[sBarcode] = []
                        dict_info_INDEL_freq[sBarcode].append([sRef_seq_loop, lQuery, sINDEL, float(iFreq) / iTotal,
                                                             sTarget_region, lRef_needle, lQuery_needle])
            # end: if lValue[gINDEL_info]
        # end: for sBarcode, lValue
        return dict_info_INDEL_freq
        # end1: return
    # end: def
#END:class



class HashBarcode(object):

    @staticmethod
    def MakeHashList(strSeq, intBarcodeLen):
        listSeqWindow = [strSeq[i:i + intBarcodeLen] for i in range(len(strSeq))[:-intBarcodeLen - 1]]
        return listSeqWindow

    @staticmethod
    def IndexHashList(dictRef, strSeqWindow):
        lCol_ref = dictRef[strSeqWindow]
        strBarcode = strSeqWindow

        return (lCol_ref, strBarcode)
    

class GotohAlignment(object):

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

