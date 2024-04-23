# coding:utf-8
# author:杜亚宁
# Time:2024/4/23 9:13
#设置规则库，识别虎、金钱豹、斑马、长颈鹿、鸵鸟、企鹅、信天翁、大象
txt_rule = '''有毛发，是哺乳类
有母乳，是哺乳类
有羽毛，是鸟类
会飞，是鸟类
会下蛋，是卵生类
食肉，是食肉动物
有犬齿，有爪子，是食肉动物
主食为植物，是食草动物
有蹄，是蹄类动物
是哺乳类，有咀嚼反刍行为，是蹄类动物
是哺乳类，是食肉动物，毛发黄褐色，身上有暗斑点，金钱豹
是哺乳类，是食肉动物，毛发黄褐色，身上有黑色条纹，虎
是哺乳类，是食草动物，有长鼻子，有大耳朵，大象
是哺乳类，是食草动物，是蹄类动物，有长脖子，有长腿，身上有暗斑点，长颈鹿
是哺乳类，是食草动物，是蹄类动物，身上有黑色条纹，斑马
是鸟类，有长脖子，有长腿，不会飞，有黑白二色，鸵鸟
是鸟类，会游泳，不会飞，有黑白二色，企鹅
是鸟类，会下蛋，会飞，飞得又快又远，信天翁'''

#设置特征字典
character_dict = {
                  '1':'有毛发','2':'有母乳','3':'有羽毛','4':'会飞','5':'会下蛋',
                  '6':'食肉','7':'有犬齿','8':'有爪子','9':'主食为植物','10':'有蹄',
                  '11':'有咀嚼反刍行为','12':'毛发黄褐色','13':'身上有暗斑点','14':'身上有黑色条纹','15':'有长鼻子',
                  '16':'有大耳朵','17':'有长脖子','18':'有长腿','19':'不会飞','20':'有黑白二色',
                  '21':'会游泳','22':'飞得又快又远','23':'是哺乳类','24':'是鸟类','25':'是卵生类','26':'是食肉动物','27':'是食草动物',
                  '28':'是蹄类动物',
                 }

#设置结论字典
result_dict = {'29':'虎','30':'金钱豹','31':'斑马','32':'长颈鹿',
               '33':'鸵鸟','34':'企鹅','35':'信天翁','36':'大象',
              }

#设置对比数据库，整合特征和结论字典
dataset = {**character_dict,**result_dict}

#预处理数据，将规则库转换为列表
def data2list():
    # 存储过程数据
    data_process_list = []
    #存储结果数据
    data_result_list = []
    #预处理规则库数据，按照回车分割成不同字符串
    data_str = txt_rule.split('\n')
    for data in data_str:
        data = data.split('，') #按照逗号分割字符串
        data_process_list.append(data[:-1])# 添加从0到倒数第二个数据
        data_result_list.append(data[-1].replace('\n','')) #添加最后一个数据，删去回车
    #print(data_str)
    return data_process_list,data_result_list

data_process_list,data_result_list = data2list()
print(data_process_list,data_result_list)

#特征值字典转为提示词函数
def character_to_callword():
    # 获取字典的键值及其索引 enumerate()
    index_data = list(enumerate(character_dict.items()))
    result_str = '' #定义存储结果空字符串
    #遍历键值，每五个元素输出一行
    for i in range(0,len(index_data),5):
        line = ''
        for j in range(5):
            if i+j < len(index_data):
                line +=str(index_data[i+j][1][0] + ':' +index_data[i+j][1][1])
                pass
            pass
        #测试输出
        # print(line)
        result_str += line + '\n'
        pass
    return result_str

#查询结果函数
def find_result(process_list,dict_output):
    #循环查找并对过程排序
    for index,process in enumerate(data_process_list):
        #判断过程是否成立
        num = 0
        for i in process_list:
            if i in process:
                num += 1
        #判断过程是否统一，统一数值应相同
        if num == len(process):
            #判断是否为最终结果，不是将此过程结果放入过程中
            if data_result_list[index] not in result_dict.values():
                #弹出过程和过程结果，因为过程已经进行过，结果存入需要查找的过程中
                result = data_result_list.pop(index)
                process = data_process_list.pop(index)
                #判断结果是否已在过程中，存在则重新寻找，不在则加入过程，并存入最终结果
                if result not in process_list:
                    dict_output[','.join(process)] = result #dict_output中添加进程和对应的结果
                    final_result = find_result(process_list + [result],dict_output)
                    if final_result :
                        return True
                    else :
                        return False
                    pass
                #存在则直接进行寻找
                else :
                    final_result = find_result(process_list,dict_output)
                    if final_result :
                        return True
                    else:
                        return False
                    pass
                pass
            else:
                process = data_process_list.pop(index)
                dict_output[','.join(process)] = data_result_list[index]
                return True
            pass

#快速排序函数 从左到右从小到大
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2] #取出列表最中间的元素
    left  = [x for x in arr if x <  pivot] #将小于中间元素的放在左侧数组
    mid   = [x for x in arr if x == pivot] #将等于中间元素的放在中间数组
    right = [x for x in arr if x >  pivot] #将大于中间元素的放在右侧数组
    return quicksort(left) + mid + quicksort(right) #采用递归的方式进行排序

#主函数
if __name__ == '__main__' :
    #规则库转换为列表
    data_temp_list, data_result_list = data2list()
    print_start = '''             请输入对应条件前的数字编号：
-----------------------------------------------------------------
'''
    print_end = '''-----------------------输入数字0程序结束---------------------------'''
    #将特征值转换为提示词
    character_str = character_to_callword()
    character_all_str = print_start + character_str +print_end #全部提示词
    print(character_all_str) #打印提示词
    #存储查询数据列表
    list_data = []
    #循环输入，直到输入0结束
    while 1 :
        input_num = input('请输入数字编号：')
        while int(input_num) >28 or int(input_num)< 0 :
            print('输入错误，请重输！')
            input_num = input('请输入数字编号：')

        if input_num == '0' :
            break
        #如果编号不在列表中，则加入
        if input_num not in list_data :
            list_data.append(input_num)
            pass
        #将查询的编号快速排序
    sort_list_data = quicksort([int(i) for i in list_data])
    #打印查询条件
    list_data_str =[character_dict[str(i)] for i in sort_list_data]
    print('查询条件为：' + ' '.join(list_data_str) + '\n')
    #存储输出结果
    dict_output = {}
    #递归查找最终结果，如果返回1，则说明找到了结果
    final_result = find_result(list_data_str,dict_output)
    #判断是否查找成功
    if final_result == 1 :
        print('查询成功！推理过程如下：')
        #打印结果
        for data in dict_output.keys():
            print(f'{data}-->{dict_output[data]}')
            #输出判断出来的结果
            if dict_output[data] in result_dict.values():
                print(f'所识别的动物为：{dict_output[data]}！')
                pass
            pass
        pass
    else: #查询识别返回0
        print('无法匹配，查询失败！')



