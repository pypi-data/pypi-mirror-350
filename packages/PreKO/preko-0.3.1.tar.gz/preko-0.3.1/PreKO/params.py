from pydantic import BaseModel
from typing import Literal


class AlinerOptions(BaseModel):
    base_quality: int     = 20
    gap_open: float       = -10
    gap_extend: float     = 1
    insertion_window: int = 4
    deletion_window: int  = 4


class InDelSearcherOptions(AlinerOptions):
    chunk_size: int                        = 100000
    pam_type: Literal['CAS9', 'CPF1']      = 'CAS9'
    pam_pos: Literal['Forward', 'Reverse'] = 'Forward'
    logger:str                             = 'InDelSearcher'
    save_pickle: bool                      = False
    save_split: bool                       = False
    save_classfied_FASTQ: bool             = False


class ParallelExecutorConfig(BaseModel):
    n_jobs: int        = 4
    use_threads: bool  = True # Thread 기반(default), False는 CPU 병렬 처리
    retry_failed: bool = True # 실패한 작업 재시도 여부
    max_retries: int   = 1    # 최대 재시도 횟수

