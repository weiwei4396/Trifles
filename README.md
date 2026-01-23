# Trifles
unappetizing and yet not bad enough to be thrown away


1.**UniqueSam_bulk_sc.py**
<details>
<summary> </summary>
输入给定的bulk或者single cell的sam文件, 输出一个每条reads唯一的sam文件, 其中每条reads是它mapping quality最大的mapping结果;

-i:输入sam文件路径;

-o:输出的sam文件路径;

-m:默认为0, 是bulk的文件, 其他数字是single cell的文件;

</details>


2.**concat_me.py**
<details>
<summary> </summary>
这个代码是用来替代MAGIC-seq流程中合并seqkit concat两个文件的功能; 因为seqkit的concat后名称中出现"|", 跟read的R2匹配不上，因此只是将fastq的第二行reads和第四行测序质量合并，其他两行不变。

-a:输入的1-8的barcode, 这里就是barcodeX;

-b:输入的27-46位置的barcodeY和UMI;

-o:输出的合并的结果, 也还是fastq.gz;

</details>



3.**stat_Barcode.py**
<details>
<summary> </summary>

这个脚本是针对MAGIC-seq的二代数据，提取出固定的barcode, XY或者XYZ，看看固定的barcode是否在所有给定的白名单范围内，然后计算出barcode正确率;

-i:输入的是提取好了的R1的fastq.gz文件, 就是那个reformat.R1;

-b:输入的是barcode的白名单文件;

-m:表示是XY的2个barcode模式还是XYZ的3个barcode的模式, 默认是2, 或者输入3;

-o:输出的txt文件, 具体的每个reads的barcode的信息;

</details>



4.**.py**
<details>
<summary> </summary>


</details>





5.**.py**
<details>
<summary> </summary>


</details>













