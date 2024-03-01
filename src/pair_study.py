from utilities import *
from trigger_test import send_trigger
from psychopy import core, visual, event


def main_test(win, image_pair, query):
    timer = core.Clock()
    pair_info = []

    text_ui = visual.TextStim(win, text='+', pos=(0, IMAGE_BIAS_HEIGHT_1), height=WORD_HEIGHT, color=(1, 1, 1),
                              alignText='center')
    text_ui.draw()
    win.flip()
    send_trigger(TRIGGER_LIST['+'])
    core.wait(0.5)
    send_trigger(TRIGGER_LIST['+'])
    core.wait(0.5)

    wait_len = 1.5
    for idx, image_name in enumerate(image_pair):
        image_ui = visual.ImageStim(win, image=BASE_IMG_PATH + query + '/' + image_name, pos=(0, IMAGE_BIAS_HEIGHT_1),
                                    size=IMAGE_SIZE_1)
        image_ui.draw()
        win.flip()
        core.wait(0.010)  # 延迟10ms
        send_trigger(TRIGGER_LIST['image_base'] + idx)
        core.wait(wait_len)

    text_ui = visual.TextStim(win, text=split_text(["第一张图好：A", "相差无几：F", "第二张图好：J"]), pos=(0, TEXT_HEIGHT),
                              height=WORD_HEIGHT,
                              color=(1, 1, 1), alignText='center')
    text_ui.draw()
    win.flip()
    core.wait(0.010)  # 延迟10ms
    send_trigger(TRIGGER_LIST['preference_judgement'])
    timer.reset()
    keys = event.waitKeys(keyList=[FIRST_KEY, FAIR_KEY, NEXT_KEY])
    time_use = timer.getTime()
    pair_info.append([keys[0], time_use])
    win.flip()
    core.wait(0.1)

    # validate
    img1 = visual.ImageStim(win, image=BASE_IMG_PATH + query + '/' + image_pair[0], pos=POS_LIST_2[0],
                            size=IMAGE_SIZE_2)
    img2 = visual.ImageStim(win, image=BASE_IMG_PATH + query + '/' + image_pair[1], pos=POS_LIST_2[1],
                            size=IMAGE_SIZE_2)
    txt1 = visual.TextStim(win, text=split_text(["第一张图好：A", "相差无几：F", "第二张图好：J"]), pos=TEXT_POS_LIST_2[0],
                           height=WORD_HEIGHT / 2, color=(1, 1, 1), alignText='center')
    txt1.draw()
    img1.draw()
    img2.draw()
    win.flip()
    core.wait(0.010)  # 延迟10ms
    send_trigger(TRIGGER_LIST['validation_preference_judgement'])
    timer.reset()
    keys = event.waitKeys(keyList=[FIRST_KEY, FAIR_KEY, NEXT_KEY])
    time_use = timer.getTime()
    pair_info.append([keys[0], time_use])
    if keys[0] == pair_info[0][0]:
        if keys[0] == 'a':
            send_trigger(TRIGGER_LIST['a_trigger'])
        elif keys[0] == 'f':
            send_trigger(TRIGGER_LIST['f_trigger'])
        else:
            send_trigger(TRIGGER_LIST['j_trigger'])
    core.wait(1.0)
    return pair_info


def pair_study(win, stu_list, fw, n=48):
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
