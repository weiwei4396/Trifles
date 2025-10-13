# 2025.10.13
# pw
# 这一步主要是对mapping后的结果获取唯一的比对; 只保留每一条能mapping上的reads; 
# 方便后面统计各种reads所占的百分比;
# 脚本包括单细胞的脚本和bulk的, 使用一个参数决定是单细胞还是bulk;

import argparse

# 创建参数解析器
parser = argparse.ArgumentParser(description="Get unique reads!")
# 添加参数
parser.add_argument("-i", "--input", required=True, help="input SAM file (sorted)!")
parser.add_argument("-o", "--output", required=True, help="output SAM file!")
parser.add_argument("-m", "--mode", type=int, default=0, help="mode 1:single cell, 0:bulk")
# 解析参数
args = parser.parse_args()

if args.mode == 0 :
    UniqueReads = {}
    print("*** Bulk Mode ***")
    print("*** 1.Read the bulk sam ! ", args.input," ***")
    with open(args.input, "r") as infile:
        for line in infile:
            if line.startswith("@"):
                continue
            cols = line.rstrip("\n").split("\t")
            # 提取信息
            read_name = cols[0]
            flag = int(cols[1])
            chr_name = cols[2]
            position = int(cols[3])
            mapping_quality = int(cols[4])
        
            # 有mapping才会保留;
            if chr_name != '*':
                # 保存信息
                if read_name not in UniqueReads.keys():
                    UniqueReads[read_name] = [mapping_quality, chr_name, position, flag]
                else:
                    if mapping_quality > UniqueReads[read_name][0]:
                        UniqueReads[read_name] = [mapping_quality, chr_name, position, flag]
            else:
                continue
    print("Mapping 到 Reference 的 reads 有:", len(UniqueReads))
    print("*** The sam dictionary has been constructed. ! ***")

    count = 0
    read_name_set = set()
    print("*** 2.generate unique sam! ***")
    with open(args.input, "r") as infile, open(args.output, "w") as outfile:
        for line in infile:
            if line.startswith("@"):
                outfile.write(line)
            cols = line.rstrip("\n").split("\t")
            if cols[0] in UniqueReads.keys():
                if UniqueReads[cols[0]] == [int(cols[4]), cols[2], int(cols[3]), int(cols[1])]:
                    if cols[0] not in read_name_set:
                        outfile.write(line)
                        count = count + 1
                        read_name_set.add(cols[0])
                    else:
                        continue
    print("最终生成唯一的reads有:", count)
    print("*** Generated End ! ***")


else:
    # 对单细胞数据; unique; 需要barcode umi统一;
    UniqueBarcodeUMI = dict()
    print("*** Single cell Mode ***")
    print("*** 1.First Read the single cell sam ! ", args.input, " ***")
    with open(args.input, "r") as infile:
        for line in infile:
            if line.startswith("@"):
                continue
            cols = line.rstrip("\n").split("\t")
            # 提取信息
            barcode = [c for c in cols if c.startswith("BC:Z:")]
            barcode = barcode[0]
            umi = [c for c in cols if c.startswith("U8:Z:")]
            umi = umi[0]

            read_name = cols[0]
            flag = int(cols[1])
            chr_name = cols[2]
            position = int(cols[3])
            mapping_quality = int(cols[4])

            if barcode not in UniqueBarcodeUMI.keys():
                UniqueBarcodeUMI[barcode] = dict()
                UniqueBarcodeUMI[barcode][umi] = [flag, chr_name, position, mapping_quality, read_name]

            else:
                if umi not in UniqueBarcodeUMI[barcode]:
                    UniqueBarcodeUMI[barcode][umi] = [flag, chr_name, position, mapping_quality, read_name]
                else:
                    if UniqueBarcodeUMI[barcode][umi][3] < mapping_quality:
                        UniqueBarcodeUMI[barcode][umi] = [flag, chr_name, position, mapping_quality, read_name]

    Count = 0
    print("Barcode数量为:", len(UniqueBarcodeUMI))
    for eachBarcode in UniqueBarcodeUMI.keys():
        Count = Count + len(UniqueBarcodeUMI[eachBarcode])
    print("所有UMI数量为:", Count)
    print("*** The sam dictionary has been constructed. ! ***")


    Count = 0
    read_name_set = set()
    print("*** 2.generate unique sam! ***")
    with open(args.input, "r") as infile, open(args.output, "w") as outfile:
        for line in infile:
            if line.startswith("@"):
                outfile.write(line)
                continue
            cols = line.rstrip("\n").split("\t")
            # 提取信息
            barcode = [c for c in cols if c.startswith("BC:Z:")]
            barcode = barcode[0]
            umi = [c for c in cols if c.startswith("U8:Z:")]
            umi = umi[0]

            read_name = cols[0]
            flag = int(cols[1])
            chr_name = cols[2]
            position = int(cols[3])
            mapping_quality = int(cols[4]) 

            if barcode in UniqueBarcodeUMI.keys():
                if umi in UniqueBarcodeUMI[barcode].keys():
                    if UniqueBarcodeUMI[barcode][umi] == [flag, chr_name, position, mapping_quality, read_name]:
                        if read_name not in read_name_set:
                            outfile.write(line)
                            Count = Count + 1
                            read_name_set.add(read_name)
                        else:
                            continue
    print("最终生成唯一的reads有:", Count)
    print("*** Generated End ! ***")    






