# -*- coding: UTF-8 -*-
"""
Created on
"""
from aitool import dump_json, timestamp, AutoPrompt, infer_doubao

task = "生成口令，口令应属于赞美、祝福、励志、正能量主题。"

case_train = [
    ('你如秋菊淡雅', 'good', '', ''),
    ('您的聪慧如星', 'good', '', ''),
    ('你像璀璨星辰', 'good', '', ''),
    ('乐观拥抱新希望', 'good', '', ''),
    ('勇敢踏上新道路', 'good', '', ''),
    ('善良收获温暖回报', 'good', '', ''),
    ('坚定信念向前行', 'good', '', ''),
    ('拼搏奋进创佳绩', 'good', '', ''),
    ('努力拼搏铸辉煌', 'good', '', ''),
    ('积极向上永不言弃', 'good', '', ''),
    ('活力满满心愿达成', 'good', '', ''),
    ('心怀希望展宏图', 'good', '', ''),
]

ap = AutoPrompt(
    task,
    case_train,
    'good',
    'bad',
    target_size=50,
    name='token',
    show_print=True,
)

run_task_1 = False
if run_task_1:
    prompt_1 = """# 角色\n你是一个擅长创作口令的词人。\n\n# 目标\n创作独一无二的口令，这些口令需要韵律感和节奏感强烈，让人一看就能记住。这些口令需要包含主题，如赞美、祝福、励志、正能量，并且要有趣，能够吸引人们去搜索。\n\n# 技能\n## 技能 1: 创作赞美类口令\n1. 当用户请你创作赞美类口令时，首先需要了解用户需要赞美的对象。\n2. 根据赞美的对象，创作韵律感和节奏感强烈的口令。\n\n## 技能 2: 创作祝福类口令\n1. 当用户请你创作祝福类口令时，首先需要了解用户需要祝福的对象。\n2. 根据祝福的对象，创作韵律感和节奏感强烈的口令。\n\n## 技能 3: 创作励志类口令\n1. 当用户请你创作励志类口令时，首先需要了解用户需要励志的对象或者是场景。\n2. 根据励志的对象或者是场景，创作韵律感和节奏感强烈的口令。\n\n## 技能 4: 创作正能量类口令\n1. 当用户请你创作正能量类口令时，首先需要了解用户需要正能量的对象或者是场景。\n2. 根据正能量的对象或者是场景，创作韵律感和节奏感强烈的口令。\n\n# 限制\n- 只创作关于赞美、祝福、励志、正能量的口令，不创建关于诋毁、诅咒、消极、负能量的口令。\n- 所有创作的口令必须有韵律感和节奏感，一看就能记住，并且趣味性强，能引起用户检索的兴趣。"""
    ori_prompt_cases = ap.get_cases(
            prompt_1 + "\n用户输入：请直接生成1条数据。",
            50,
            [],
            # ['赞美', '祝福', '励志', '正能量']
            do_variety=False,
        )
    from aitool import dump_excel
    dump_excel(ori_prompt_cases, 'token_fornax.xlsx')

run_task_2 = False
if run_task_2:
    output_prompts, output_input, output_text = ap.work()
    dump_json({'prompts': output_prompts, 'cases': output_text}, './task_output/task_1_Token_{}.json'.format(timestamp(style='min')), formatting=True)

run_task_3 = True
if run_task_3:
    prompt_final_get = "任务背景：需要生成赞美、祝福、励志、正能量主题的简短口令。\n数据要求：生成表意明确、富有诗意与美感、高度凝练，能迅速传达核心意思且直接清晰表达赞美、祝福、励志、正能量主题的口令。多条数据之间用换行符分割。\n示例分析：例如“善良收获温暖回报”“心怀希望展宏图”“你如秋菊淡雅”“努力拼搏铸辉煌”“你像璀璨星辰”等都是符合要求的简短口令。\n输出格式：直接输出符合要求的口令，每条口令占一行。 "
    case_test = [''] * 20
    output_text = []
    for case in case_test:
        output_text.append(infer_doubao([prompt_final_get]))
    dump_excel(output_text, './task_output/task_1_Token_our_prompt_{}.xlsx'.format(timestamp(style='min')))
