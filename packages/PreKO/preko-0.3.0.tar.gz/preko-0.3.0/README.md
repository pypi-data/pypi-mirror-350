# PreKO: Precise KO system
Analysis pipeline for PreKO project

### Installation
PreKO에 대한 분석 프로그램은 아래와 같이 설치할 수 있습니다. 

```
pip install PreKO
```


### InDelSearcher: Cas9 nuclease indel analyzer
InDelSearcher는 target sequence에서 indel frequency를 분석하고 계산해주는 파이프라인이다. 특히, high-throughput screening 데이터에서 barcode에 따른 indel frequency를 분석하는 것에 특화되어 있다. 

분석을 위해서, 아래와 같이 barcode와 target sequence 정보가 담긴 csv 파일이 필요하다. 


| Barcode             | Target_region               | Reference_sequence                                            |
| ------------------- | --------------------------- | ------------------------------------------------------------- |
| TTTGCTGTGAGCACTGCTG | TTGTGAACATAGATCCATTTTTCTTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGCTGTGAGCACTGCTGT |
| TTTGGACGTCATAGTGAGA | TCCAGATAGTCATCAACTTTTTGTTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGGACGTCATAGTGAGAT |
| TTTGGCTATCTGCACGTGC | GTGGGGGGCCTGGGGCCTGGAGCCTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGGCTATCTGCACGTGCG |
| TTTGATGCGCATCTCTACG | CCCAGGCAAAACTGCAGTTTTACCTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGATGCGCATCTCTACGC |
| TTTGACTCGAGTCTCTCAC | ACGAGGTGGCCCTGGGGGGCCCCCTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGACTCGAGTCTCTCACA |


barcode 파일과 분석할 FASTQ 파일이 있다면, InDelSearcher를 이용한 분석을 할 수 있다. 

```python
import pandas as pd
from PreKO.indel import InDelSearcher

# Setting: required information
DIR_FASTQ   = f'NGS_data/Cas9_FASTQ_combined/'
barcode     = f'ref_Small_Cas9_KO_Lib.csv'

sample_name = f'HCT_Cas9_R1_Day7'
fastq_file  = f'{DIR_FASTQ}/{sample_name}.fastq'

ids = InDelSearcher()

# Run and show summary
df_summary = ids.run(strFq=fastq_file, barcode=barcode, sample_name=sample_name, thread=25)
df_summary.to_csv(f'InDel_Summary_{sample_name}.csv')
```

InDelSearcher.run의 output (pd.DataFrame)은 아래와 같이 나온다.

| Barcode      | Target_region               | intSwitching | intNumOfTotal | intNumOfIns | intNumOfDel | intNumofCom | IndelFrequency |
| ------------ | --------------------------- | ------------ | ------------- | ----------- | ----------- | ----------- | -------------- |
| ATGTGATCATGC | CAGGAAAAAATATGTGCTATGGAGGGG | 477          | 9425          | 771         | 4997        | 145         | 62.7374        |
| GACTCTCGTCGA | TTTTAGAGAATATTCACCGTGTCACGG | 1034         | 10495         | 726         | 5355        | 9           | 58.02763       |
| GACTGATACTGT | ACAAAGTCAACTGCCTTCAAACAAGGG | 3630         | 13708         | 2968        | 7268        | 176         | 75.95565       |
| GCTGCGCGCACT | CTTCTATAACAAGAAATCTGATGTGGG | 726          | 10402         | 451         | 5919        | 50          | 61.7189        |
| TCGCTGTGACTC | CCGCGCCGCGCGTTACCTTCCGCGGGG | 479          | 9150          | 1225        | 4749        | 44          | 65.77049       |

이를 `to_csv()` 등의 함수로 저장해서 이후 분석에 사용한다.

# Environments
These codes were tested in Ubuntu 22.04 LTS environments.

# Requirements
- Python >= 3.8
- biopython
- pandas
- numpy
- pydantic
- tqdm