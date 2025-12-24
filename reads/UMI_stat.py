# 2025.12.24
# pw
# 主要是统计sicelore之后相同umi在每个barcode中的占比情况;

import argparse

# 创建参数解析器
parser = argparse.ArgumentParser(description="Get unique reads!")
# 添加参数
parser.add_argument("-i", "--input", required=True, help="input spatial SAM file (sorted)!")
# parser.add_argument("-o", "--output", required=True, help="output SAM file!")

# 解析参数
args = parser.parse_args()

barcodeDict = {}
print("*** 1.读取文件每一行,  ! ", args.input," ***")
with open(args.input, "r") as infile:
    for line in infile:
        if line.startswith("@"):
            continue
        cols = line.rstrip("\n").split("\t")
        Flag = int(cols[1])
        now_U8 = ""
        now_BC = ""
        if ((Flag & 0x900) == 0):
            for each in cols[11:]:
                if each.startswith("BC:Z:"):
                    if each not in barcodeDict.keys():
                        barcodeDict[each] = {}
                    now_BC = each
                elif each.startswith("U8:Z:"):
                    now_U8 = each
                else:
                    if len(now_U8) > 0 and len(now_BC) > 0: break
                    continue
        
        if len(now_U8) > 0 and len(now_BC) > 0:
            if now_U8 not in barcodeDict[now_BC].keys():
                barcodeDict[now_BC][now_U8] = 1
            else:
                barcodeDict[now_BC][now_U8] += 1
print("*** 读取umi结束 ***")
print("*** ------------------- ***")

sumReads = 0
sumUMI = 0
sumBarcode = 0
umi_list = []
for i in barcodeDict.keys():
    # print(i, "个barcode, ", len(barcodeDict[i].keys()), "个umi;")
    sumUMI = sumUMI + len(barcodeDict[i])
    for j in barcodeDict[i].keys():
        # print(j, ": ", barcodeDict[i][j])
        sumReads = sumReads + barcodeDict[i][j]
        umi_list.append(barcodeDict[i][j])
print("sumBarcode: ", len(barcodeDict))
print("sumUMI: ", sumUMI)
print("sumReads: ", sumReads)
print("*** ------------------- ***")

count_1 = umi_list.count(1)
count_2 = umi_list.count(2)
count_3 = umi_list.count(3)
count_4 = umi_list.count(4)
count_5 = umi_list.count(5)

print(f"UMI只有1个read的数量: {count_1}", f"百分比: {count_1/len(umi_list)}")
print(f"UMI大于1个read的数量: {len(umi_list)-count_1}", f"百分比: {1-count_1/len(umi_list)}")
print()
print(f"UMI有2个read的数量: {count_2}", f"百分比: {count_2/len(umi_list)}")
print(f"UMI有3个read的数量: {count_3}", f"百分比: {count_3/len(umi_list)}")
print(f"UMI有4个read的数量: {count_4}", f"百分比: {count_4/len(umi_list)}")
print(f"UMI有5个read的数量: {count_5}", f"百分比: {count_5/len(umi_list)}")





