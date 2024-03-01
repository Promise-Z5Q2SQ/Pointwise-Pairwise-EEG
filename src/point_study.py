from utilities import *
from trigger_test import send_trigger
from psychopy import core, visual, event


def main_test(win, image_arr, query):
    timer = core.Clock()
    point_info = []

    text_ui = visual.TextStim(win, text='+', pos=(0, IMAGE_BIAS_HEIGHT_1), height=WORD_HEIGHT, color=(1, 1, 1),
                              alignText='center')
    text_ui.draw()
    win.flip()
    send_trigger(TRIGGER_LIST['+'])
    core.wait(0.5)
    send_trigger(TRIGGER_LIST['+'])
    core.wait(0.5)

    wait_len = 1.5
    for idx, image_name in enumerate(image_arr):
        image_ui = visual.ImageStim(win, image=BASE_IMG_PATH + query + '/' + image_name, pos=(0, IMAGE_BIAS_HEIGHT_1),
                                    size=IMAGE_SIZE_1)
        image_ui.draw()
        win.flip()
        core.wait(0.010)  # 延迟10ms
        send_trigger(TRIGGER_LIST['image_base'] + 100 + idx)
        core.wait(wait_len)

        text_ui = visual.TextStim(win, text=split_text(["请打分1-5"]), pos=(0, TEXT_HEIGHT), height=WORD_HEIGHT,
                                  color=(1, 1, 1), alignText='center')
        text_ui.draw()
        win.flip()
        core.wait(0.010)  # 延迟10ms
        send_trigger(TRIGGER_LIST['preference_judgement'])
        timer.reset()
        keys = event.waitKeys(keyList=['1', '2', '3', '4', '5'])
        time_use = timer.getTime()
        point_info.append([keys[0], time_use])
        win.flip()
        send_trigger(int(keys[0]))
        core.wait(0.5)
    return point_info


def point_study(win, stu_list, fw, n=6):
    stu_list_all = split_arr(stu_list, n)
    fw.write("pilot_study\n")
    for idx, stu_list in enumerate(stu_list_all):
        if idx != 0:
            instruction_rest = visual.TextStim(win, text='实验一阶段' + str(idx) + '休息,\n按下空格继续实验', pos=(0, TEXT_HEIGHT),
                                               height=WORD_HEIGHT, color=(1, 1, 1), alignText='center')
            instruction_rest.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            core.wait(1.0)
        for stu in stu_list:
            query_intent = ['查询:' + stu['query'], '意图:' + stu['intent']]
            text_ui = visual.TextStim(win, text=split_text(query_intent), pos=(-TEXT_LEFT, TEXT_HEIGHT),
                                      height=WORD_HEIGHT, color=(1, 1, 1), alignText='center')
            text_ui.draw()
            win.flip()
            send_trigger(TRIGGER_LIST['query_intent'])
            event.waitKeys(keyList=['space'])
            pair_info = main_test(win, stu['image'], stu['query'])
            fw.write(str([stu, pair_info]) + '\n')
