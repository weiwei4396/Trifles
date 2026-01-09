# 2026.1.9
# pw
# 统计提取的barcode对不对, 在不在列表中;
# 依据的文件是 ${st_path}/out/${sample}_reformat_R1.fastq.gz
# 200T的py310环境;

import argparse
import pyfastx

# 创建参数解析器
parser = argparse.ArgumentParser(description="Get each read barcode!")

# 添加参数
parser.add_argument("-i", "--input", required=True, help="input read R1 file!")
parser.add_argument("-b", "--barcode", required=True, help="barcode whitelist!")
parser.add_argument("-m", "--mode", type=int, default=2, help="mode 2:barcode XY, 3:barcode XYZ")
parser.add_argument("-o", "--output", default="output_result.txt", help="output file!")

# 解析参数
args = parser.parse_args()
MODE_LEN = args.mode*8

white_set = set()
with open(args.barcode, "r") as infile:
    for line in infile:
        cols = line.rstrip("\n")
        white_set.add(cols)

with open(args.output, "w", buffering=8192*1024) as f_out:
    fastq = pyfastx.Fastq(args.input)
    for read in fastq:
        name = read.name
        seq = read.seq
        barcode = seq[:MODE_LEN]
        is_match = barcode in white_set
        f_out.write(f"{name}\t{barcode}\t{is_match}\n")







