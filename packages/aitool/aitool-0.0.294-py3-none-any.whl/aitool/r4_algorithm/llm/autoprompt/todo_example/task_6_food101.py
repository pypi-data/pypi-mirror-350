# -*- coding: UTF-8 -*-
"""
Created on
"""
from tqdm import tqdm
from json import loads
from aitool import (timestamp, dump_excel, AutoPrompt, get_file, make_dir, get_doubao_img_base64, dump_pickle,
                    load_pickle, InputIdx, OutputIdx, LabelIdx, CommentIdx, send_file2tos, send_text2tos)
from random import sample, shuffle
from pandas import read_parquet
from collections import defaultdict
from PIL import Image
import io
from os import path

def get_dataset():
    # 开源数据来源：https://huggingface.co/datasets/ethz/food101
    # 一共有类别101个、数据101000条
    # 每个类别保留最先遇到的3条
    name2id = {
        "apple_pie": 0,
        "baby_back_ribs": 1,
        "baklava": 2,
        "beef_carpaccio": 3,
        "beef_tartare": 4,
        "beet_salad": 5,
        "beignets": 6,
        "bibimbap": 7,
        "bread_pudding": 8,
        "breakfast_burrito": 9,
        "bruschetta": 10,
        "caesar_salad": 11,
        "cannoli": 12,
        "caprese_salad": 13,
        "carrot_cake": 14,
        "ceviche": 15,
        "cheesecake": 16,
        "cheese_plate": 17,
        "chicken_curry": 18,
        "chicken_quesadilla": 19,
        "chicken_wings": 20,
        "chocolate_cake": 21,
        "chocolate_mousse": 22,
        "churros": 23,
        "clam_chowder": 24,
        "club_sandwich": 25,
        "crab_cakes": 26,
        "creme_brulee": 27,
        "croque_madame": 28,
        "cup_cakes": 29,
        "deviled_eggs": 30,
        "donuts": 31,
        "dumplings": 32,
        "edamame": 33,
        "eggs_benedict": 34,
        "escargots": 35,
        "falafel": 36,
        "filet_mignon": 37,
        "fish_and_chips": 38,
        "foie_gras": 39,
        "french_fries": 40,
        "french_onion_soup": 41,
        "french_toast": 42,
        "fried_calamari": 43,
        "fried_rice": 44,
        "frozen_yogurt": 45,
        "garlic_bread": 46,
        "gnocchi": 47,
        "greek_salad": 48,
        "grilled_cheese_sandwich": 49,
        "grilled_salmon": 50,
        "guacamole": 51,
        "gyoza": 52,
        "hamburger": 53,
        "hot_and_sour_soup": 54,
        "hot_dog": 55,
        "huevos_rancheros": 56,
        "hummus": 57,
        "ice_cream": 58,
        "lasagna": 59,
        "lobster_bisque": 60,
        "lobster_roll_sandwich": 61,
        "macaroni_and_cheese": 62,
        "macarons": 63,
        "miso_soup": 64,
        "mussels": 65,
        "nachos": 66,
        "omelette": 67,
        "onion_rings": 68,
        "oysters": 69,
        "pad_thai": 70,
        "paella": 71,
        "pancakes": 72,
        "panna_cotta": 73,
        "peking_duck": 74,
        "pho": 75,
        "pizza": 76,
        "pork_chop": 77,
        "poutine": 78,
        "prime_rib": 79,
        "pulled_pork_sandwich": 80,
        "ramen": 81,
        "ravioli": 82,
        "red_velvet_cake": 83,
        "risotto": 84,
        "samosa": 85,
        "sashimi": 86,
        "scallops": 87,
        "seaweed_salad": 88,
        "shrimp_and_grits": 89,
        "spaghetti_bolognese": 90,
        "spaghetti_carbonara": 91,
        "spring_rolls": 92,
        "steak": 93,
        "strawberry_shortcake": 94,
        "sushi": 95,
        "tacos": 96,
        "takoyaki": 97,
        "tiramisu": 98,
        "tuna_tartare": 99,
        "waffles": 100
    }
    id2name = {}
    for name, nid in name2id.items():
        id2name[nid] = name
    max_cnt = 10
    all_data = []
    format_data = []
    label2cnt = defaultdict(int)
    out_dir = 'r4_algorithm/llm/autoprompt/example/food101/' + 'sample_{}'.format(timestamp(style='sec'))
    make_dir(out_dir)
    idx = 1
    for file in get_file('food101/data'):
        data = read_parquet(file)
        for pil, lid in data.values.tolist():

            label = id2name[lid]
            if label2cnt[label] >= max_cnt:
                continue
            try:
                file_name = path.join(out_dir, pil['path'])
                image = Image.open(io.BytesIO(pil['bytes']))
                image.save(file_name)

                pic_base64 = get_doubao_img_base64(file_name)
                pic_name = path.join(out_dir, pic_base64)
                label2cnt[label] += 1
                format_data.append([file_name, label])
                all_data.append((label, 'good', {'text': '', 'pic_list': [pic_base64], 'pic_type': 'base64'}, ''))
                idx += 1
            except Exception as e:
                print(e)

    shuffle(all_data)
    train_data = all_data[:int(len(all_data)*0.1)][:50]
    test_data = all_data[int(len(all_data)*0.1):][:500]
    shuffle(format_data)
    train_data_format = all_data[:int(len(format_data) * 0.1)][:50]
    test_data_format = all_data[int(len(format_data) * 0.1):][:500]
    dump_excel(train_data_format, './task6_food101_train_format.xlsx')
    dump_excel(test_data_format, './task6_food101_test_format.xlsx')
    return train_data, test_data


if __name__ == '__main__':
    re_sample = True
    if True:
        data_train, data_test = get_dataset()
        dump_pickle(data_train, './task6_food101_train.pkl')
        dump_pickle(data_test, './task6_food101_test.pkl')
    else:
        data_train = load_pickle('./task6_food101_train.pkl')
        data_test = load_pickle('./task6_food101_test.pkl')


    task = """对输入的食物图片判断其类别，每个图片只属于一个类别。所有可能类别有101种，包括：apple_pie、baby_back_ribs、baklava、beef_carpaccio、beef_tartare、beet_salad、beignets、bibimbap、bread_pudding、breakfast_burrito、bruschetta、caesar_salad、cannoli、caprese_salad、carrot_cake、ceviche、cheesecake、cheese_plate、chicken_curry、chicken_quesadilla、chicken_wings、chocolate_cake、chocolate_mousse、churros、clam_chowder、club_sandwich、crab_cakes、creme_brulee、croque_madame、cup_cakes、deviled_eggs、donuts、dumplings、edamame、eggs_benedict、escargots、falafel、filet_mignon、fish_and_chips、foie_gras、french_fries、french_onion_soup、french_toast、fried_calamari、fried_rice、frozen_yogurt、garlic_bread、gnocchi、greek_salad、grilled_cheese_sandwich、grilled_salmon、guacamole、gyoza、hamburger、hot_and_sour_soup、hot_dog、huevos_rancheros、hummus、ice_cream、lasagna、lobster_bisque、lobster_roll_sandwich、macaroni_and_cheese、macarons、miso_soup、mussels、nachos、omelette、onion_rings、oysters、pad_thai、paella、pancakes、panna_cotta、peking_duck、pho、pizza、pork_chop、poutine、prime_rib、pulled_pork_sandwich、ramen、ravioli、red_velvet_cake、risotto、samosa、sashimi、scallops、seaweed_salad、shrimp_and_grits、spaghetti_bolognese、spaghetti_carbonara、spring_rolls、steak、strawberry_shortcake、sushi、tacos、takoyaki、tiramisu、tuna_tartare、waffles"""

    ap = AutoPrompt(
        task,
        data_train,
        'good',
        'bad',
        window_size=10,
        beam_size=2,
        derive_time=2,
        iteration=2,
        target_inputs=[case[InputIdx] for case in data_test],
        target_size=len(data_test),
        split_subtask=False,
        skip_old_data=True,
        name='Food101',
        no_example_in_prompt=True,
        show_print=True,
    )

    run_task_1 = False
    if run_task_1:
        # 仅用任务描述作为基线prompt
        ori_prompt_cases = ap.get_cases(
            task,
            len(data_test),
            [case[2] for case in data_test],
            do_variety=False,
            num_consistent=True,
        )
        ap.record.note(('仅用任务描述作为基线prompt的准确率', ap.get_precision(ori_prompt_cases, data_test)))

    run_task_2 = False
    if run_task_2:
        # 将全部训练集数据作为示例的基线prompt
        examples = '\n'.join(['输入：\n{}\n输出：\n{}\n'.format(case[2], case[0]) for case in data_train])

        ori_prompt = """【判例】\n{}\n对输入的案例输出其标签，标签包括：无期徒刑、死刑，以及具体的罪名。""".format(examples)
        fix_prompt_cases = ap.get_cases(
            ori_prompt,
            len(data_test),
            [case[2] for case in data_test],
            do_variety=False,
            num_consistent=True,
        )
        ap.record.note(('将全部训练集数据作为示例的基线prompt的准确率', ap.get_precision(fix_prompt_cases, data_test)))

    run_task_3 = False
    if run_task_3:
        # AutoPrompt输出的prompt
        output_prompts, output_input, output_text = ap.work()
        output_cases = [(ot, '', oi, '') for oi, ot in zip(output_input, output_text)]
        ap.record.note(('优化后的prompt的准确率', ap.get_precision(output_cases, data_test)))
        ap.record.finish()
        dump_excel(output_cases, './Food101/test_rst_{}.xlsx'.format(timestamp(style='min')))
