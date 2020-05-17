with open("resultqyandx.txt") as file:
    result = file.read()

length = len(result)
#去掉换行符
result = result.replace("\n","")


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


        #若未读到末尾，就将batch_y_data中读过的数据删掉
        batch_y_data = batch_y_data[data_y_end + 1:]

    print(cat)

    #找到一个batch的x_bar的数据
    batch_x_bar_start = result.find('train_x_bar[[')
    batch_x_bar_end = result.find(']]')
    batch_x_bar_data = result[batch_x_bar_start + 12:batch_x_bar_end + 1]

    # 将result读过的y的数据从result中去掉
    result = result[batch_x_bar_end + 2:]

    #存放读到的x_bar数据
    x_bar = []

    for j in range(len(batch_x_bar_data)):
        #找到一个图片对应的向量的头和尾
        single_x_bar_start = batch_x_bar_data.find('[')
        single_x_bar_end = batch_x_bar_data.find(']')

        #找不到则代表找完，退出
        if single_x_bar_start == -1:
            break

        #存放一个图片的向量
        single_x_bar_data = batch_x_bar_data[single_x_bar_start + 1:single_x_bar_end]

        #处理数据
        single_x_bar_data = single_x_bar_data.split()
        for k in range(len(single_x_bar_data)):
            single_x_bar_data[k] = int(single_x_bar_data[k])

        #找到一个x_bar的数据就添加到x_bar中
        x_bar.append(single_x_bar_data)

        #若没有读到末尾，则将读过的部分去掉
        batch_x_bar_data = batch_x_bar_data[single_x_bar_end + 1:]

    print(x_bar)

    # 找到一个batch的x的数据
    batch_x_start = result.find('train_x[[')
    batch_x_end = result.find(']]')
    batch_x_data = result[batch_x_start + 8:batch_x_end + 1]

    # 将result读过的y的数据从result中去掉
    result = result[batch_x_end + 2:]

    #存放读到的x的数据
    x = []

    for j in range(len(batch_x_data)):

        #获取每个x的开头和结尾
        single_x_start = batch_x_data.find('[')
        single_x_end = batch_x_data.find(']')

        #找不到则代表找完了所有的x，退出
        if single_x_start == -1:
            break

        #存放单个x的数据
        single_x_data = batch_x_data[single_x_start + 1:single_x_end]

        #处理数据
        single_x_data = single_x_data.split()
        for k in range(len(single_x_data)):
            single_x_data[k] = int(single_x_data[k])

        #找到一个x的数据就存放到x中去
        x.append(single_x_data)

        # 若没有读到末尾，则将读过的部分去掉
        batch_x_data = batch_x_data[single_x_end + 1:]
    print(x)

    #根据标签，将x和x_ba存放到字典中
    for m in range(len(cat)):
        temp = []
        temp.append(x[m])
        temp.append(x_bar[m])
        ans[cat[m]].append(temp)
print(ans.items())