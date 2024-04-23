# 读取列表
mv list > list.his 
find /mnt/e/09Nuget  -name "*nupkg*" > list

# 跟his比较 这个可以跟git版本比较

# 准备目录
rm -rf 20240423/ 
mkdir 20240423/

# 复制文件
for f in $(cat list)
do
echo "COPY" $f
cp $f 20240423/
done

# 打包
tar -zcvf dotnet_nupkgs_20240203.tart.gz 20240423/
rm -rf 20240423/


echo "finished"