with open("textqyandz.txt") as file:
    result = file.read()

length = len(result)
#去掉换行符
result = result.replace("\n","")

#实现两个list对应元素相加
def list_add(a,b):
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i])
    return c

#实现一个list的每个元素都乘一个相同的数
def list_multi_num(list,num):
    c = []
    for i in range(len(list)):
        c.append(list[i] * num)
    return c



#存放最后的字典类型
ans = {}
for i in range(10):
    ans[i] = []

#逐个batch进行读取
for i in range(length):
    #找到一个batch的y的开头和结尾
    batch_y_start = result.find("train_qy")
    batch_y_end = result.find("]]")
    #找不到train_qy就代表读到文件末尾，退出
    if batch_y_start == -1:
        break
    #将一个batch的y数据去掉前缀“train_qy[”和最后一个“]”后存放到batch_y_data中
    batch_y_data = result[batch_y_start + 9:batch_y_end + 1]
    #将result读过的y的数据从result中去掉
    result = result[batch_y_end + 2:]

    #存放标签
    cat = []
    #存放一个batch的y
    batch_y = []

    for j in range(batch_y_start, batch_y_end + 1):
        #找到一个图片对应的y的数据开头和结尾
        data_y_start = batch_y_data.find('[')
        data_y_end = batch_y_data.find(']')

        #当前batch_y_data中找不到]就说明读到batch_y_data最后
        if data_y_start == -1:
            break
        #将一个图片对应的数据去掉前缀'['和后缀‘]'之后存放到data_y中
        data_y = batch_y_data[data_y_start + 1:data_y_end]

        #处理读入的data_y
        data_y = data_y.split()
        for k in range(len(data_y)):
            data_y[k] = float(data_y[k])
        #将最大值对应的索引值作为标签存放到cat中
        cat.append(data_y.index(max(data_y)))
        batch_y.append(data_y)


        #若未读到末尾，就将batch_y_data中读过的数据删掉
        batch_y_data = batch_y_data[data_y_end + 1:]

    print(cat)
    print(batch_y)
    #找到一个batch的z的开头结尾
    batch_z_start = result.find('train_z_all')
    batch_z_end = result.find(']]]')

    # 将一个batch的z数据去掉前缀“train_z_all[”和最后一个“]”后存放到batch_z_data中
    batch_z_data = result[batch_z_start + 12:batch_z_end + 2]



    #存放一个batch的z，即n_y_active个[b,n_z]的z
    batch_z = []
    for j in range(batch_z_start,batch_z_end + 1):
        # 找到一个组件对应的数据开头和结尾
        data_z_start = batch_z_data.find('[[')
        data_z_end = batch_z_data.find(']]')

        #当前batch_z_data中找不到[[就代表这个batch结束，退出
        if data_z_start == -1:
            break
        # 存放一个组件生成的[b,n_z]的z
        z = []

        # 将一个组件对应的z去掉前缀'['和后缀‘]'知乎存放到data_z_comp中
        data_z_comp = batch_z_data[data_z_start + 1:data_z_end + 1]

        for k in range(data_z_start + 1,data_z_end + 1):
            #找到一个图片对应一行z
            pic_z_start = data_z_comp.find('[')
            pic_z_end = data_z_comp.find(']')

            if pic_z_start == -1:
                break

            #将一个图片对应的一行[1,n_z]的z放到pic_z中
            pic_z = data_z_comp[pic_z_start + 1: pic_z_end]
            #处理数据
            pic_z = pic_z.split()
            for l in range(len(pic_z)):
                pic_z[l] = float(pic_z[l])

            #将一个图片的一行[1,n_z]的z的添加到z中
            z.append(pic_z)

            #若未到当前组件对应的z的结尾，则将data_z_comp中读过的数据删掉
            data_z_comp = data_z_comp[pic_z_end + 1:]

        #将一个组件对应的z添加到batch_z中
        batch_z.append(z)

        batch_z_data = batch_z_data[data_z_end + 2:]

    print(z)
    # break


    #计算经过求期望的[b,n_z]的z
    #存放最终期望的z
    final_z = []
    for pos1 in range(len(batch_y)):
        #存放期望中每个图片对应的[1,n-z]的z
        final_pic_z = []
        for pos2 in range(len(batch_y[0])):
            temp = list_multi_num(batch_z[pos2][pos1],batch_y[pos1][pos2])
            final_pic_z = list_add(final_pic_z,temp)
        final_z.append(final_pic_z)

    #遍历当前batch中的每个图片对应的类别，按照类别分别将对应的[1,n_z]的一行z添加到最后的字典类型中
    for i in range(len(cat)):
        ans[cat[i]].append(final_z[i])



    #若未到达文件尾，则去掉读过的
    result = result[batch_z_end + 3:]
print(ans.items())