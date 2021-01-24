# coding=utf-8
# 本实验使用版本为的python3.9

def trace_back(best_path, left, right, root, index=0):
    node = best_path[left][right][root]
    if node['path']['split'] is not None:  # 判断是否存在分裂点，值为下标
        print('\t' * index, (root, node['prob']))
        # 递归调用
        if len(node['path']['rule']) == 2:  # 如果规则为二元，递归调用左子树、右子树，如 NP-->NP NP
            trace_back(best_path, left, node['path']['split'], node['path']['rule'][0], index + 1)  # 左子树
            trace_back(best_path, node['path']['split'] + 1, right, node['path']['rule'][1], index + 1)  # 右子树
        else:  # 否则，只递归左子树,如 NP-->N
            trace_back(best_path, left, node['path']['split'], node['path']['rule'][0], index + 1)
    else:
        print('\t' * index, (root, node['prob']))
        print('--->', node['path']['rule'])


def main():
    sentence = 'fish people fish tanks'
    non_terminal = {'S', 'NP', 'VP', 'N', 'V', 'PP', 'P', '@VP_V'}
    start_symbol = 'S'
    # terminal = {'people', 'fish', 'tanks', 'rods', 'with'}
    rules_prob = {'S': {('NP', 'VP'): 0.9, 'VP': 0.1},
                  'VP': {('V', 'NP'): 0.5, 'V': 0.1, ('V', 'PP'): 0.1, ('V', '@VP_V'): 0.3},
                  '@VP_V': {('NP', 'PP'): 1.0},
                  'NP': {('NP', 'NP'): 0.1, 'N': 0.7, ('NP', 'PP'): 0.2},
                  'PP': {('P', 'NP'): 1.0},
                  'P': {'with': 1.0},
                  'V': {'fish': 0.6, 'people': 0.1, 'tanks': 0.3},
                  'N': {'people': 0.5, 'fish': 0.2, 'tanks': 0.2, 'rods': 0.1},
                  }

    words = sentence.split()
    best_match = [[dict() for _ in range(len(words))] for _ in range(len(words))]

    # 初始化
    for i in range(len(words)):
        for j in range(len(words)):
            for nt in non_terminal:
                # 初始化每个字典，每个语法规则概率及路径为None，避免溢出和空指针
                best_match[i][j][nt] = {'prob': 0.0, 'path': {'split': None, 'rule': None}}

    # 填叶结点，计算得到每个单词所有语法组成的概率
    for i in range(len(words)):
        for nt1 in non_terminal:
            # 遍历非终端符，找到并计算此条非终端-终端语法的概率
            if words[i] in rules_prob[nt1].keys():
                best_match[i][i][nt1]['prob'] = rules_prob[nt1][words[i]]  # 保存概率
                best_match[i][i][nt1]['path'] = {'split': None, 'rule': words[i]}  # 保存路径

                # 生成新的语法需要加入
                for nt2 in non_terminal:
                    if nt1 in rules_prob[nt2].keys():
                        best_match[i][i][nt2]['prob'] = rules_prob[nt1][words[i]] * rules_prob[nt2][nt1]
                        best_match[i][i][nt2]['path'] = {'split': i, 'rule': nt1}

    # 填非叶结点，计算得到每个单词所有语法组成的概率
    for layer_number in range(1, len(words)):
        # 该层节点个数
        for i in range(len(words) - layer_number):  # 第一层
            j = i + layer_number  # 处理第二层结点
            for nt in non_terminal:  # 获取每个非终结符
                temp_best_nt = {'prob': 0, 'path': None}

                for key, value in rules_prob[nt].items():  # 遍历该非终端符所有语法规则
                    if key[0] not in non_terminal:
                        break
                    # 计算产生的分裂点概率，保留最大概率
                    for split in range(i, j):
                        if len(key) == 2:
                            temp_prob = value * best_match[i][split][key[0]]['prob'] * \
                                        best_match[split + 1][j][key[1]][
                                'prob']
                        else:
                            temp_prob = value * best_match[i][split][key[0]]['prob'] * 0
                        if temp_prob > temp_best_nt['prob']:
                            # 保存分裂点和生成的可用规则
                            temp_best_nt['prob'] = temp_prob
                            temp_best_nt['path'] = {'split': split, 'rule': key}

                best_match[i][j][nt] = temp_best_nt  # 得到一个规则中最大概率

    # 调用回溯函数，寻找概率最大路径
    trace_back(best_match, 0, len(words) - 1, start_symbol)


if __name__ == '__main__':
    main()

'''
目前问题是所生成表格的内容不大对，需要重新检查生成表格的代码
具体发现的地方是在trace_back函数中的if判断中发现的，
正常的情况下是一开始就要进if的循环
目前不需要再开另外一个项目，直接在本项目内检查即可
使用的python版本为3.9
'''