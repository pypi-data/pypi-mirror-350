[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# bowtie2QC

A python bowtie2 QC ploter

![image](https://github.com/user-attachments/assets/fd1b697a-a9fa-4494-9569-8f83d38fd376)

# Getting Start

## install from pip

```
pip install bowtie2QC
```

# Usage

```
from  bowtie2QC import bowtie2QC


log_files = ["bowtie2.log", "bowtie2.log","bowtie3.log"]
bowtie2QC.procress_logs_with_pdf(log_files)
```
