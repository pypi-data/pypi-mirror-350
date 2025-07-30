import logging, traceback
from tqdm import tqdm
from pathlib import Path
from typing import Callable, List, Any, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from PreKO.params import ParallelExecutorConfig


def setup_logging(logger_id:str, logger_path:str, consol_level=logging.INFO):
    '''Usage
    
    setup_logging()  
    logging.info("콘솔과 파일에 동시에 출력됨")
    '''

    logfile = f"{logger_path}/{logger_id}.log"

    logger = logging.getLogger(logger_id)
    logger.setLevel(logging.DEBUG)

    # 중복 핸들러 방지
    if not logger.handlers:
        # 콘솔 핸들러
        ch = logging.StreamHandler()
        ch.setLevel(consol_level)

        # 파일 핸들러
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt = '%Y-%m-%d %H:%M:%S',
            )
        
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

def reverse_complement(sSeq):
    dict_sBases = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N', '.': '.', '*': '*',
                   'a': 't', 'c': 'g', 'g': 'c', 't': 'a'}
    list_sSeq   = list(sSeq)  # Turns the sequence in to a gigantic list
    list_sSeq   = [dict_sBases[sBase] for sBase in list_sSeq]
    return ''.join(list_sSeq)[::-1]
#def END: reverse_complement

# Legacy splitFASTQ
'''def splitFASTQ(fastq_file:str, output_dir:str, chunk_size:int=1000000, file_prefix="chunk") -> list:
    """FASTQ 파일을 정해진 reads 수마다 끊어서 chunked file로 만드는 함수.
    만들어진 파일은 InDelPatternAnalizer class에서 지정된 Temp 디렉토리에 저장된다.

    Args:
        fastq_file (str): 나누고 싶은 원본 FASTQ 파일.
        output_fir (str): splited file을 저장할 경로.
        chunk_size (int, optional): Chunk로 나눌 리드 수. Defaults to 1000000.
        file_prefix (str, optional): Chunked 파일의 접두어. Defaults to "chunk".

    Returns:
        list: Chunked file의 경로가 담긴 리스트.
    """
    
    # Setting
    chunk_idx = 1
    line_buffer = []
    list_files  = []
    lines_per_chunk = 4 * chunk_size
    output_prefix = f'{output_dir}/{file_prefix}'
    
    with open(fastq_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line_buffer.append(line)

            splited_file = f"{output_prefix}_{chunk_idx}.fastq"
            
            # when buffer has enough lines, write to new file
            if line_num % lines_per_chunk == 0:
                with open(splited_file, 'w') as out_f:
                    out_f.writelines(line_buffer)
                list_files.append(splited_file)
                chunk_idx += 1
                line_buffer = []

        # write remaining lines
        if line_buffer:
            with open(splited_file, 'w') as out_f:
                out_f.writelines(line_buffer)
            list_files.append(splited_file)

    return list_files'''


def splitFASTQ(fastq_file: str, output_dir: str, chunk_size: int = 1_000_000, file_prefix: str = "chunk") -> List[str]:
    """FASTQ 파일을 정해진 read 수마다 끊어서 chunked 파일로 저장합니다.

    Args:
        fastq_file (str): 나눌 원본 FASTQ 파일 경로.
        output_dir (str): chunk 파일 저장 경로.
        chunk_size (int): 각 chunk 파일에 들어갈 read 수. (default=1,000,000)
        file_prefix (str): chunk 파일 접두어 (default="chunk")

    Returns:
        List[str]: 생성된 chunk 파일 경로 리스트.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = output_dir / file_prefix

    lines_per_chunk = 4 * chunk_size
    chunk_files = []
    buffer = []
    chunk_idx = 1

    # 전체 라인 수 확인 (progress bar 용)
    with open(fastq_file, 'r') as f:
        total_lines = sum(1 for _ in f)

    with open(fastq_file, 'r') as f, tqdm(total=total_lines, desc="Splitting FASTQ", unit="lines", ncols=150, ascii=' =') as pbar:
        for line_num, line in enumerate(f, 1):
            buffer.append(line)
            pbar.update(1)

            if line_num % lines_per_chunk == 0:
                chunk_path = output_prefix.with_name(f"{output_prefix.name}_{chunk_idx}.fastq")
                with open(chunk_path, 'w') as out_f:
                    out_f.writelines(buffer)
                chunk_files.append(str(chunk_path))
                chunk_idx += 1
                buffer = []

        # 남은 라인 쓰기
        if buffer:
            chunk_path = output_prefix.with_name(f"{output_prefix.name}_{chunk_idx}.fastq")
            with open(chunk_path, 'w') as out_f:
                out_f.writelines(buffer)
            chunk_files.append(str(chunk_path))

    return chunk_files


class FastqOpener(object):

    def OpenFastqForward(self, strForwardFqPath):

        listFastqForward = []
        listStore        = []

        with open(strForwardFqPath) as Fastq1:

            for i, strRow in enumerate(Fastq1):

                i = i + 1
                strRow = strRow.replace('\n', '').upper()

                if i % 4 == 1 or i % 4 == 2:
                    listStore.append(strRow)
                elif i % 4 == 0:
                    listQual = [ord(i) - 33 for i in strRow]
                    listStore.append(listQual)
                    listFastqForward.append(tuple(listStore))
                    listStore = []

        return listFastqForward

    def OpenFastqReverse(self, strReverseFqPath):

        listFastqReverse = []
        listStore        = []

        dictRev = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}

        with open(strReverseFqPath) as Fastq2:

            for i, strRow in enumerate(Fastq2):
                i = i + 1
                strRow = strRow.replace('\n', '').upper()

                if i % 4 == 1:
                    listStore.append(strRow)
                elif i % 4 == 2:
                    listStore.append(''.join([dictRev[strNucle] for strNucle in strRow[::-1]]))
                elif i % 4 == 0:
                    listQual = [ord(i) - 33 for i in strRow][::-1]
                    listStore.append(listQual)
                    listFastqReverse.append(tuple(listStore))
                    listStore = []

        return listFastqReverse
        #end1: return
    #end: def

class ParallelExecutor:
    def __init__(self, config: Optional[ParallelExecutorConfig] = None, logger: Optional[str] = None):
        
        self.config = config or ParallelExecutorConfig()
        
        if logger != None:
            self.logger = logging.getLogger(logger)

    def run(self, 
            tasks: List[Any], 
            func: Callable[[Any], Any],
            next_func: Optional[Callable[[Any], Any]] = None,
            desc: str = "Processing"
           ) -> Tuple[List[Any], List[Tuple[Any, str]]]:
        """병렬 처리 함수

        Args:
            tasks (List[Any]): 처리할 데이터 리스트
            func (Callable[[Any], Any]): 각 데이터에 적용할 함수
            next_func (Optional[Callable[[Any], Any]], optional): 성공한 결과에만 적용할 다음 함수. Defaults to None.
            desc (str, optional): tqdm progress bar 설명. Defaults to "Processing".

        Returns:
            Tuple[List[Any], List[Tuple[Any, str]]]: _description_
        """        


        ExecutorClass = ThreadPoolExecutor if self.config.use_threads else ProcessPoolExecutor

        success_results = []
        error_results = []

        with ExecutorClass(max_workers=self.config.n_jobs) as executor:
            futures = {executor.submit(self._safe_wrapper(func), task): task for task in tasks}

            for future in tqdm(as_completed(futures), total=len(futures), desc=desc, ncols=150, ascii=' ='):
                try:
                    ok, result = future.result()
                    if ok:
                        if next_func:
                            try:
                                result = next_func(result)  # 다음 단계 함수 실행
                            except Exception as e:
                                tb = traceback.format_exc()
                                error_results.append(("next_func_error", tb))
                                continue
                        success_results.append(result)
                    else:
                        error_results.append(result)

                except Exception as e:
                    tb = traceback.format_exc()
                    error_results.append(("unknown_task", tb))

        # 실패한 작업 재시도
        if self.config.retry_failed and error_results and self.config.max_retries > 0:
            failed_tasks = [task for task, _ in error_results]
            self.logger.info(f"재시도 {len(failed_tasks)}개 작업 (최대 {self.config.max_retries}회)")
            self.config.max_retries -= 1  # 재시도 횟수 차감
            retry_success, retry_error = self.run(failed_tasks, func, next_func, desc="Retrying")
            success_results.extend(retry_success)
            error_results = retry_error  # 마지막 에러 결과로 갱신

        return success_results, error_results

    @staticmethod
    def _safe_wrapper(func: Callable[[Any], Any]) -> Callable[[Any], Tuple[bool, Any]]:
        """
        에러 발생 시에도 안전하게 실행하는 함수
        """
        def wrapped(task: Any) -> Tuple[bool, Any]:
            try:
                result = func(task)
                return (True, result)
            except Exception:
                tb = traceback.format_exc()
                return (False, (task, tb))
        return wrapped


