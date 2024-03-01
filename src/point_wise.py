import random
from datetime import datetime
import argparse
from point_study import *


def main_function(stu_list, fw):
    fw.write(str(stu_list) + '\n')

    win = visual.Window(size=MIN_SIZE, fullscr=False, screen=0, winType='pyglet', allowGUI=False, allowStencil=False,
                        monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb', blendMode='avg', useFBO=True,
                        units='pix')

    instruction_train = visual.TextStim(win, text='请仔细阅读实验说明,\n按下空格开始实验训练', pos=(0, 0), height=WORD_HEIGHT,
                                        color=(1, 1, 1), alignText='center')
    instruction_end = visual.TextStim(win, text='实验结束,请联系主试', pos=(0, TEXT_HEIGHT), height=WORD_HEIGHT, color=(1, 1, 1),
                                      alignText='center')
    instruction_test = visual.TextStim(win, text='按空格键，开始正式实验', pos=(0, TEXT_HEIGHT), height=WORD_HEIGHT,
                                       color=(1, 1, 1), alignText='center')

    # 1 准备训练
    instruction_train.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    # 1 训练
    point_study(win, stu_list[:1], fw)

    # 1 准备正式实验
    instruction_test.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    # 1 正式实验
    point_study(win, stu_list[1:], fw)

    # end
    instruction_end.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    win.close()
    core.quit()
    fw.close()


def load_question_info(info_file_name):
    total_arr = []
    with open(info_file_name, encoding='UTF-8') as f:
        for line in f.readlines():
            line_list = line.strip().split()
            tmp_dic = {
                "query": line_list[0],
                "intent": line_list[1],
                "image": line_list[2:]
            }
            # 打乱图片顺序
            random.shuffle(tmp_dic['image'])
            total_arr.append(tmp_dic)
    # 随机化所有问题的顺序
    random.shuffle(total_arr)
    return total_arr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='point-wise preference research with eeg')
    parser.add_argument('-s', '--seed', type=int, default=54321, help='random seed')
    args = parser.parse_args()
    random.seed(args.seed)

    total_arr = load_question_info('./data/query_info.txt')
    main_function(total_arr, open('./record/point/' + datetime.now().strftime('%Y%m%d') + '_' + str(args.seed), 'w',
                                  encoding='utf8'))
