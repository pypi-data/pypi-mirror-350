# -*- coding: UTF-8 -*-
import math
from collections import defaultdict, Counter
from random import sample, randint, shuffle
from time import sleep, gmtime, strftime
from typing import List, Tuple, Dict, Callable, Any
import os
from tqdm import tqdm

from aitool import (AUTOPROMPT_PATH, ngram_sim, split_punctuation, is_punctuation, infer_doubao, Record, get_batch,
                    load_json, infer_doubao_vision)

InputPics = List[str]   # 是用豆包特定的base64格式
Input = Dict[str, Any]
Output = str
Label = str
Comment = str
InputIdx = 2
OutputIdx = 0
LabelIdx = 1
CommentIdx = 3
Prompt = str

LabeledCase = Tuple[Output, Label, Input, Comment]
Generation = 'generation'
Classification = 'classification'
CLSAnalysis = 'cls_analysis'


class UndefinedTask(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return '未定义的任务类型'


class AutoPrompt:
    def __init__(
            self,
            task: str,
            dataset: List[LabeledCase] = None,
            label_good: str = None,
            label_bad: str = None,
            window_size: int = 5,
            beam_size: int = 2,
            derive_time: int = 2,
            iteration: int = 2,
            target_inputs: List[Input] = None,
            target_size: int = 100,
            split_subtask: bool = False,  # split_subtask = True 还需要多实验各种极端情况, 默认还是设置False
            auto_task_kind: bool = True,  # task_kind is None 时有效
            task_kind: str = None,
            name: str = '',
            llm_interface: Callable = infer_doubao,     #
            vllm_interface: Callable = infer_doubao_vision,     #
            llm_teacher_interface: Callable = infer_doubao,     # 用来评估prompt->文本优劣的llm
            vllm_teacher_interface: Callable = infer_doubao_vision,     #
            skip_old_data: bool = False,
            ratio_fixed: float = 0.1,
            ratio_new: float = 0.7,
            ratio_hard: float = 0.2,
            bad_cases_num: int = 7,
            good_cases_num: int = 3,
            no_example_in_prompt: bool = False,
            show_print: bool = False,
            use_all_propose: bool = False,
            has_pic: bool = False,
            has_video: bool = False,
    ):
        """
        自动优化prompt
        :param task: 任务描述
        :param dataset: 已标注数据
        :param label_good: 优质数据的标签
        :param label_bad: 低质数据的标签
        :param window_size: 迭代过程中数据集里的case数量
        :param beam_size: 寻找举报最优解的窗口
        :param derive_time: 求梯度的次数
        :param iteration: 迭代轮次
        :param target_inputs: case级别的输入信息
        :param target_size: 生成数据的量
        :param split_subtask: 是否划分子任务
        :param auto_task_kind: 自动判断任务类型
        :param task_kind: 任务类型
        :param name: 任务名
        :param llm_interface: 用来生成文本的llm接口
        :param vllm_interface: 用来理解图片的llm接口
        :param llm_teacher_interface: 用来评估prompt->文本优劣的llm接口
        :param vllm_teacher_interface: 用来评估prompt->图片理解优劣的llm接口
        :param skip_old_data: 验证集上不使用旧的数据
        :param ratio_fixed: 固定的验证数据占比
        :param ratio_new: 新的验证数据占比
        :param ratio_hard: 困难的验证数据占比
        :param no_example_in_prompt: prompt里面不带example以免图片携带问题
        :param show_print: note是否print
        :param use_all_propose: 是否使用全部的propose
        :param has_pic: 输入里面是否包含图片
        :param has_video: 输入里面是否包含视频
        """
        self.task = task
        self.dataset = dataset if dataset is not None else []
        self.label_good = label_good if label_good is not None else 'good'
        self.label_bad = label_bad if label_bad is not None else 'bad'
        self.window_size = window_size
        self.beam_size = beam_size
        self.derive_time = derive_time
        self.iteration = iteration
        self.target_inputs = target_inputs if target_inputs is not None else ['']
        self.target_size = target_size
        self.split_subtask = split_subtask
        self.auto_task_kind = auto_task_kind
        self.task_kind = task_kind
        self.task_name = name
        self.llm_interface = llm_interface
        self.vllm_interface = vllm_interface
        self.llm_teacher_interface = llm_teacher_interface
        self.vllm_teacher_interface = vllm_teacher_interface
        self.use_all_propose = use_all_propose
        self.has_pic = has_pic
        self.has_video = has_video

        self.templates = load_json(os.path.join(AUTOPROMPT_PATH, 'templates.json'))

        self.skip_old_data = skip_old_data
        self.ratio_fixed = ratio_fixed
        self.ratio_new = ratio_new
        self.ratio_hard = ratio_hard

        # 如果不跳过历史轮次评测数据就需要将测试集的改为固定参数
        if not self.skip_old_data:
            self.ratio_fixed = 1.0
            self.ratio_new = 0.0
            self.ratio_hard = 0.0

        self.output_limited = False
        self.all_allowed_outputs = []
        self.good_cases = []
        self.inspector_prompt = None
        self.subtasks = []
        self.subdatasets = []
        self.prompt2idx = defaultdict(str)
        self.all_final_prompts = []
        self.prompt2case = {}
        self.prompt_score = []
        self.prompt2gradient = defaultdict(list)
        self.output_prompts = []
        self.output_case_texts = []
        self.output_case_inputs = []

        # 分类任务专属
        self.is_multi_label = False
        self.split_punctuation = ','  # 多分类任务用来拼接label的符号
        self.validate_new_idx = 0
        self.window_size_fixed = int(self.window_size * self.ratio_fixed)
        self.window_size_new = int(self.window_size * self.ratio_new)
        self.window_size_hard = int(self.window_size * self.ratio_hard)
        self.validate_cases = []
        self.validate_cases_fixed = []
        self.validate_cases_new = []
        self.validate_cases_hard = []
        self.validate_cases_hard_next = []
        self.prompt2precision = {}
        self.prompt2wrong_cases_str = {}

        # 分类解析任务专属
        self.bad_cases_num = bad_cases_num
        self.good_cases_num = good_cases_num
        self.label2tips = defaultdict(list)
        self.label2fitips = {}

        # 视觉任务专属
        self.no_example_in_prompt = no_example_in_prompt
        self.show_print = show_print

        self.record = Record(name=self.task_name, show=show_print)
        self.note_params()

        # 兼容历史版本的输入LabeledCase=Tuple[Output, Label, Input, Comment]
        self.update_dataset()

    def update_input(self, the_input):
        if the_input is None:
            return {'text': '', 'pic_list': [], 'pic_type': ''}
        if isinstance(the_input, str):
            return {'text': the_input, 'pic_list': [], 'pic_type': ''}
        return the_input

    def update_dataset(self):
        # 兼容历史版本的数据输入格式
        new_dataset = []
        for case in self.dataset:
            if isinstance(case[InputIdx], str):
                new_input = self.update_input(case[InputIdx])
                new_dataset.append(('{}'.format(case[OutputIdx]), case[LabelIdx], new_input, case[CommentIdx]))
            elif isinstance(case[InputIdx], Dict):
                if 'text' not in case[InputIdx]:
                    case[InputIdx]['text'] = ''
                if 'pic_list' not in case[InputIdx]:
                    case[InputIdx]['pic_list'] = []
                if 'pic_type' not in case[InputIdx]:
                    case[InputIdx]['pic_type'] = ''
                new_dataset.append(case)
            else:
                raise ValueError('未知的历史版本数据输入格式')
        self.dataset = new_dataset

    def get_prompts(self) -> List[Prompt]:
        # 迭代prompt
        for subtask, subdataset in zip(self.subtasks, self.subdatasets):
            prompt_init = self.task2prompt(subtask, subdataset)
            for idx, prompt in enumerate(prompt_init):
                self.prompt2idx[prompt] = 'init_{}'.format(idx)
            self.record.note(('subtask', subtask))
            self.record.note(('subdataset', subdataset))
            self.record.note(('prompt_init', prompt_init))
            self.all_final_prompts.append(self.beam_search(subtask, prompt_init, subdataset, self.iteration))

        self.record.note(('output_prompts', self.all_final_prompts))
        return self.all_final_prompts

    def get_outputs(self, prompts: List[str] = None) -> Tuple[List[Input], List[Output]]:
        # 批量生成数据
        self.infer_inputs(prompts)
        self.record.note(('output_case_inputs', self.output_case_inputs))
        self.record.note(('output_case_texts', self.output_case_texts))
        self.record.finish()
        return self.output_case_inputs, self.output_case_texts

    def get_tip_str(self):
        rst = ''
        for label, tips in self.label2tips.items():
            rst += '{}: {}\n'.format(label, '。'.join(tips))
        return rst

    def get_tip(self, all_wrong_cases, all_wrong_outputs, all_right_cases, prompt, label):
        wrong_cases_str, pic_lists, pic_type = self.get_wrong_cases_str(all_wrong_cases, all_wrong_outputs)
        all_predict_cases = [(output, case[LabelIdx], case[InputIdx], case[CommentIdx]) for case, output
                             in zip(all_right_cases, all_wrong_outputs)]
        propose = self.analysis_case2good(all_predict_cases, all_right_cases, prompt,
                                          wrong_cases_str=wrong_cases_str, label=label)
        self.label2tips[label].append(propose)

    def get_tips(self):
        label2case = defaultdict(list)
        for case in self.good_cases:
            label2case[case[OutputIdx]].append(case)
        prompt_init = self.task2prompt(self.subtasks[0], self.subdatasets[0])
        prompt = prompt_init[0]

        iteration = 0
        while iteration < self.iteration:
            iteration += 1
            prompt = self.merge_prompt(prompt, self.get_tip_str())

            for label in label2case:
                all_right_cases = []
                all_wrong_cases = []
                all_wrong_outputs = []
                for case_golden in tqdm(get_batch(label2case[label][:self.target_size], self.window_size), label):
                    case_inputs = [case[InputIdx] for case in case_golden]
                    case_predicted = self.get_cases(prompt, len(case_inputs), case_inputs, do_variety=False)
                    right_cases, wrong_cases, wrong_outputs = self.check_response(case_predicted, case_golden)
                    all_right_cases.extend(right_cases)
                    all_wrong_cases.extend(wrong_cases)
                    all_wrong_outputs.extend(wrong_outputs)
                    if (len(all_right_cases) >= self.good_cases_num) and (len(all_wrong_cases) >= self.bad_cases_num):
                        self.get_tip(all_wrong_cases, all_wrong_outputs, all_right_cases, prompt, label)
                        all_right_cases = []
                        all_wrong_cases = []
                        all_wrong_outputs = []
                if len(all_right_cases) > 0:
                    self.get_tip(all_wrong_cases, all_wrong_outputs, all_right_cases, prompt, label)

        for label in self.label2tips:
            self.label2fitips[label] = self.get_final_tips(label)

    def work(self):
        if self.task_kind is not None:
            self.auto_task_kind = False
        if self.auto_task_kind:
            self.get_task_kind()

        self.get_output_limitation()
        self.get_classification_type()

        if self.split_subtask:
            self.get_subtasks()
            self.get_subdatasets()
        else:
            self.subtasks = [self.task]
            self.subdatasets = [self.dataset]
        self.time_estimate()

        self.good_cases = self.pick_dataset(self.dataset, self.label_good, len(self.dataset))
        shuffle(self.good_cases)

        if self.task_kind == Generation:
            # 检查器（用于分类和修正），在全部数据上获取，不针对子任务
            self.inspector_prompt = self.get_inspector_prompt()
            self.record.note(('inspector_prompt_init', self.inspector_prompt))
            self.rewrite_inspector_prompt()
            self.record.note(('inspector_prompt_rewrite', self.inspector_prompt))
        elif self.task_kind == Classification:
            # 分类任务不支持 subtask
            assert self.split_subtask is False
            # 分类任务从全量数据中筛选出一个评测集。TODO 优先保证正负样本均衡，然后在案input占比分配case
            self.validate_cases_fixed, _ = self.split_dataset(self.good_cases, self.window_size_fixed,
                                                              balance_idx=OutputIdx)
            self.record.note(('validate_cases_fixed', self.validate_cases_fixed))
        elif self.task_kind == CLSAnalysis:
            # 分类分析任务不支持 subtask
            assert self.split_subtask is False
        else:
            raise UndefinedTask

        if self.task_kind in (Generation, Classification):
            self.get_prompts()
            self.get_outputs()
            return self.output_prompts, self.output_case_inputs, self.output_case_texts
        elif self.task_kind == CLSAnalysis:
            self.get_tips()
            return self.label2fitips

    def get_task_kind(self):
        records = [
            [
                """请判断下列【任务】的任务类型是生成任务还是分类任务。直接输出“是生成任务。”或“是分类任务。”，不要输出分析过程，直接输出任务类型即可。\n\n【任务：】\n{}\n\n【任务类型：】""",
                [self.task], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        template2 = self.templates['get_task_kind'][-1]['text'].format(self.task)
        rst = self.call_llm(template)
        if '分类任务' in rst:
            self.task_kind = Classification
        elif '生成任务' in rst:
            self.task_kind = Generation
        else:
            self.task_kind = Generation
        self.record.note(('get_task_kind', rst))
        self.record.note(('get_task_kind', self.task_kind))

    def get_output_limitation(self):
        output_cases_str = '\n'.join([case[OutputIdx] for case in self.dataset][:10])
        template = """请结合【任务输出示例】判断【任务】的输出是否为有限的集合。如果是，则写出该任务所有可能输出的集合，集合中的元素用“,”分隔。如果不是或难以判断，则写出一个空集。\n以下是一些示例：\n【示例任务：】\n生成一句打招呼的话\n【所有可能输出的集合：】\n{}\n\n【示例任务：】\n依据输入数据输出它的类别标签\n【所有可能输出的集合：】\n{}\n\n【示例任务：】\n处罚力度按月来计算，最小的月数是3，最大是7。请判断应该处以几个月的处罚最合适。\n【所有可能输出的集合：】\n{3, 4, 5, 6, 7}\n\n【示例任务：】\n请判断输入的类别。类别分为：A1、A5、C2、None。 \n【所有可能输出的集合：】\n{A1, A5, C2, None}\n\n【示例任务：】\n对于用户的输入需要回答“对”或“不对”，并给出理由。\n【所有可能输出的集合：】\n{}\n\n【示例任务：】\n判断分析过程是否正确，生成判断的结果，仅输出“对”、“不对”、“不知道”，不要输出原因。\n【所有可能输出的集合：】\n{对, 不对, 不知道}\n\n【示例任务：】\n对文章进行分类，如果文章体现出作者高兴的情绪就输出高兴，如果体现出愤怒的情绪就输出愤怒，其他情况输出平静。\n【所有可能输出的集合：】\n{高兴, 愤怒, 平静}\n\n【示例任务：】\n对文章进行分类，如果文章体现出作者高兴的情绪就输出高兴，如果体现出愤怒的情绪就输出愤怒。如果不属于这两种情况，就输出最匹配的一个情绪词。\n【所有可能输出的集合：】\n{}\n\n请输出下述【任务】的【所有可能输出的集合】\n【任务：】\n""" + self.task + """\n\n【所有可能输出的集合：】"""
        rst = self.call_llm(template)
        task_output_set = [_.strip() for _ in rst.replace('{', '').replace('}', '').split(',')]
        dataset_output_set = set([case[OutputIdx] for case in self.dataset])

        self.output_limited = False
        self.all_allowed_outputs = {}
        if len(task_output_set) > 0:
            is_all_contain = True
            # 处理多分类的包含情况。 TODO 目前只支持符号分割的拼接方式
            for case_output in dataset_output_set:
                if case_output in task_output_set:
                    continue
                for item in [_.strip() for _ in split_punctuation(case_output)]:
                    if len(item) > 0 and item not in task_output_set:
                        is_all_contain = False
                        break
                if not is_all_contain:
                    break
            if is_all_contain:
                self.output_limited = True
                self.all_allowed_outputs = task_output_set
        self.record.note(('output_limited', self.output_limited))
        self.record.note(('all_allowed_outputs', self.all_allowed_outputs))

    def get_output_limitation_str(self):
        if not self.output_limited:
            return ''
        allowed_outputs_str = '、'.join(self.all_allowed_outputs)
        text = '不允许输出额外的推理过程，输出的必须为这些内容中的一个或多个：{}。即使是缺少信息无法判断或与所有可选的输出内容都无关，也只能输出这些内容中的一个或多个：{}。'.format(
            allowed_outputs_str, allowed_outputs_str)
        return text

    def get_classification_type(self):
        if self.task_kind != Classification:
            self.is_multi_label = False
            return

        output_cases_str = '\n'.join([case[OutputIdx] for case in self.dataset][:10])
        records = [
            [
                """请基于下列【任务描述】和【样例输出数据】判断该任务是否是多标签分类任务，即一个样例的输出里可以包含1个或多个类别标签。判断结果直接输出“是多标签分类任务。”或“不是。”，不要输出分析过程。\n\n【任务描述：】\n{}\n\n【样例输出数据（每行为1个样例的输出）：】\n{}\n\n【判断结果：】""",
                [self.task, output_cases_str], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        if '不是' in rst:
            self.is_multi_label = False
        elif '是多标签分类任务' in rst:
            self.is_multi_label = True
            self.get_split_punctuation()
        else:
            self.is_multi_label = False
        self.record.note(('is_multi_label', self.is_multi_label))

    def get_split_punctuation(self):
        all_output_str = ''.join([case[OutputIdx] for case in self.dataset])
        punctuations = Counter([_ for _ in all_output_str if is_punctuation(_)])
        most_common = punctuations.most_common()
        if len(most_common) > 0:
            self.split_punctuation = most_common[0][0]

    def infer_inputs(self, prompts: str = None):
        # 批量生成数据
        if prompts is None:
            prompts = [final_prompts[0] for final_prompts in self.all_final_prompts]
        task_size = math.ceil(self.target_size / len(self.subtasks))  # 平分要生成的数据量
        for prompt, subdataset in zip(prompts, self.subdatasets):
            self.output_prompts.append(prompt)
            if self.task_kind == Generation:
                cases = self.get_cases(
                    prompt,
                    task_size,
                    self.target_inputs,
                    dataset=subdataset,
                    use_inspector_rewrite=True,
                    use_allowed_outputs=True,
                )
            elif self.task_kind == Classification:
                cases = self.get_cases(
                    prompt,
                    task_size,
                    self.target_inputs,
                    do_variety=False,
                    num_consistent=True,
                    use_allowed_outputs=True,
                )
            else:
                raise UndefinedTask
            for case in cases:
                self.output_case_inputs.append(case[2])
                self.output_case_texts.append(case[0])

    @staticmethod
    def description():
        description = """AutoPrompt包括2个模块，支持多模块生成/分类任务：
1、自动优化prompt：模拟人工调优prompt的过程，得到一个较好的prompt。
2、批量生成物料：LLM批量调用模块 + 多样性增强模块 + 低质数据清洗/改写模块”。
        """
        return description

    def rewrite_inspector_prompt(self):
        if self.inspector_prompt is None:
            return
        if self.has_pic:
            records = [
                [
                    """修改分类任务的【原prompt】,要求保持原本的信息不缺失，并将其输出格式修改为：“\n【分类结果】\n（该分类prompt原本的结果，即是否符合要求）。\n【修正后的输入】\n（如果不合符要求就额外输出修正后的输入，使其符合要求。如果已经符合要求，则输出“无需修正”）”。prompt里的图片数量不应该多余10张，可以是0张即不含任务图片。如果原prompt里有双括号包裹的变量{{变量名}}，则输出的prompt里也应该包含所有双括号包裹的变量，不要丢失变量。\n\n【原prompt:】\n{}\n\n【修改输出格式后的prompt:】\n""",
                    [self.inspector_prompt], """第一版"""],
            ]
        else:
            records = [
                [
                    """修改分类任务的【原prompt】,要求保持原本的信息不缺失，并将其输出格式修改为：“\n【分类结果】\n（该分类prompt原本的结果，即是否符合要求）。\n【修正后的输入】\n（如果不合符要求就额外输出修正后的输入，使其符合要求。如果已经符合要求，则输出“无需修正”）”。\n\n【原prompt:】\n{}\n\n【修改输出格式后的prompt:】\n""",
                    [self.inspector_prompt], """第一版"""],
            ]
        template = records[-1][0].format(*records[-1][1])
        self.inspector_prompt = self.call_llm(template)

    def get_inspector_prompt(self) -> str:
        case_good = self.pick_dataset(self.dataset, self.label_good, len(self.dataset))
        case_bad = self.pick_dataset(self.dataset, self.label_bad, len(self.dataset))
        task = self.generation2classification_task(self.task, self.label_good, self.label_bad)
        dataset = self.generation2classification_dataset(case_good + case_bad)
        inspector_prompt = None
        if len(case_good) >= 5 and len(case_bad) >= 5:
            ap = AutoPrompt(
                task,
                dataset,
                self.label_good,
                self.label_bad,
                window_size=20,
                beam_size=2,
                derive_time=1,
                iteration=2,
                target_inputs=[],
                target_size=0,
                split_subtask=False,
                task_kind='classification',
            )
            output_prompts, output_input, output_text = ap.work()
            inspector_prompt = output_prompts[0]
        return inspector_prompt

    @staticmethod
    def generation2classification_dataset(dataset: List[LabeledCase]) -> List[LabeledCase]:
        dataset_new = []
        for case in dataset:
            c_output, c_label, c_input, c_comment = case
            if len(c_input) > 0:
                new_input = 'input: ' + '{}'.format(c_input) + '\noutput: ' + c_output
            else:
                new_input = c_output
            dataset_new.append((c_label, 'good', new_input, c_comment))
        return dataset_new

    @staticmethod
    def generation2classification_task(task: str, label_good: str, label_bad: str) -> str:
        records = [
            [
                """依据生成任务的【任务描述:】\n{}\n\n已生成了一些数据，请判定生成的数据是否符合上述生成任务的要求。如果符合要求就输出“{}”,如果不符合要求就输出“{}”""",
                [task, label_good, label_bad], """第一版"""],
        ]
        task = records[-1][0].format(*records[-1][1])
        return task

    @staticmethod
    def aggregate_dataset(dataset: List[LabeledCase], target_idx: int = InputIdx) -> Dict:
        # 按target_id列汇总数据
        target2cases = defaultdict(list)
        for labeled_case in dataset:
            target = labeled_case[target_idx]['text']
            target2cases[target].append(labeled_case)
        return target2cases

    def time_estimate(self):
        """预估耗时。不包含已用于做子任务划分的时间"""
        second_per_call = 4.95  # 平均调用一次大模型的时间(秒)
        case_per_call = 1.17  # 平均调用一次大模型获得的case数量

        # 生成新的prompt调用llm的次数。每个都先算梯度，再生产，再清洗
        time_propose = 3 * self.beam_size * self.derive_time * self.iteration
        # 计算每个prompt的样例数据调用llm的次数。初始有 self.beam_size 个 prompt。每轮迭代新获得self.beam_size * self.derive_time 个 prompt
        # 每份样例数据要包含 self.window_size 个数据，生成数据后额外需要清洗一次格式
        time_get_cases = (self.beam_size * self.derive_time * self.iteration + self.beam_size) * (
                    self.window_size / case_per_call + 1)
        # 两两对比计算分数调用llm的次数
        if self.task_kind == Generation:
            time_rank_score = (self.beam_size * self.derive_time + self.beam_size) ^ 2
        elif self.task_kind == Classification:
            time_rank_score = 0
        elif self.task_kind == CLSAnalysis:
            time_rank_score = 0
        else:
            raise UndefinedTask
        # 推理过程调用llm的次数。
        time_inference = self.target_size / case_per_call
        # 总的调用llm的次数。
        time_whole = time_propose + time_get_cases + time_rank_score + time_inference
        # 总耗时（小时）
        hour_estimated = time_whole * second_per_call * len(self.subtasks)
        self.record.note(('预估耗时', '{}'.format(strftime("%H:%M:%S", gmtime(hour_estimated)))))

    def note_params(self):
        members = dir(self)
        filtered_members = [m for m in members if not m.startswith('__')]
        for member in filtered_members:
            value = getattr(self, member)
            if callable(value):
                continue
            self.record.note(('参数 :: {}'.format(member), value))

    def call_llm(self, the_input: Input, llm: str = 'doubao') -> str:
        """
        调用大模型生成结果，依据Input情况调用不同模型
        :param the_input:
        :param llm:
        :return:
        """
        try_time = 1
        sleep_second = [0, 1, 1, 1]
        if len(sleep_second) <= try_time:
            raise ValueError('len sleep_second is less than or equal try_time')

        the_input = self.update_input(the_input)
        prompt = the_input['text']
        pics = the_input['pic_list'] if 'pic_list' in the_input else []
        pic_type = the_input['pic_type'] if 'pic_type' in the_input else ''
        while try_time > 0:
            try:
                if len(pics) == 0:
                    self.record.note(('>>> call_llm', prompt))
                    if llm == 'doubao':
                        rst = self.llm_interface([prompt])
                    else:
                        raise ValueError('llm:'.format(llm))
                    self.record.note(('>>> rst_llm', rst))
                    return rst
                else:
                    self.record.note(('>>> call_vllm', prompt))
                    if pic_type in ('base64', 'url'):
                        if pic_type == 'url':
                            self.record.note(('>>> call_inputs', the_input))
                        if llm == 'doubao':
                            rst = self.vllm_interface(prompt, pics, pic_type)
                        else:
                            raise ValueError('llm:'.format(llm))
                        self.record.note(('>>> rst_llm', rst))
                        return rst
                    else:
                        raise ValueError(pic_type)
            except Exception as e:
                print(e)
                sleep(sleep_second[try_time])
                try_time -= 1
        return ''

    def merge_rst(self, llm_rsts: List[str]) -> str:
        """
        汇总多个大模型的结果 TODO
        """
        self.record.note(('>>> call_llm', llm_rsts))
        return ''

    def variety_prompt(
            self,
            prompt: str,
            dataset: List[LabeledCase],
            use_example: bool = True,
            multi_gen: bool = False,
    ) -> str:
        """基于规则对prompt进行多样性修饰"""
        additional_prompt = ''

        # 用good_dataset做多样性
        if use_example:
            good_dataset = self.pick_dataset(dataset, self.label_good, self.window_size)

            if len(good_dataset) > 0:
                example_str, data_pics, pic_type = self.get_example_str(good_dataset, min_num=2)
                additional_prompt += example_str

        # 一次调用生成多个case
        if multi_gen:
            additional_prompt += '请生成{}条数据，不同数据之间用换行符进行分割。'.format(randint(5, 10))

        # 寻找合适的插入位置
        if len(additional_prompt) > 0:
            splits = prompt.rsplit('【', maxsplit=1)
            if len(splits) == 2:
                spl, spr = splits
            else:
                spl, spr = '', prompt
            new_prompt = spl + additional_prompt + spr
        else:
            new_prompt = prompt
        return new_prompt

    def task2subtask(self, task: str) -> List[str]:
        records = [
            [
                """请判断【任务描述】是否包含多个并列的目标或领域，如果有请拆分出多个子任务，并用换行符分割不同的子任务。每个子任务都需要保留【任务描述】的其他所有任务要求、限制条件、格式要求等信息。\n【任务描述:】\n{}\n【子任务:】\n""",
                [task, ], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)

        subtask = []
        for raw_subtask in rst.split('\n'):
            raw_subtask = raw_subtask.strip()
            sim = ngram_sim(raw_subtask, task, 3)
            if sim < 0.5:
                continue
            subtask.append(raw_subtask)

        if len(subtask) == 0:
            subtask = [task]
        return subtask

    def get_subdataset(self, task: str, clean_space: bool = True) -> List[LabeledCase]:
        string2case = {}
        all_string = []
        for case in self.dataset:
            c_str = case[0]
            if clean_space:
                c_str = c_str.replace(' ', '')
            string2case[c_str] = case
            all_string.append(c_str)

        records = [
            [
                """请判断【数据集】中的哪些任务属于【子任务】，并用换行符分割不同的数据。\n【数据集:】\n{}\n【子任务:】\n{}\n【属于该子任务的数据:】\n""",
                [all_string, task], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        substring = []
        for r in rst.split('\n'):
            r = r.strip()
            r = r.replace(' ', '')
            substring.append(r)
        subdataset = []
        for c_str in substring:
            if c_str in string2case:
                subdataset.append(string2case[c_str])
            else:
                print('c_str not in string2case', c_str)
                sim_rank = []
                for p_str in all_string:
                    sim = ngram_sim(c_str, p_str, 3)
                    sim_rank.append([p_str, sim])
                sim_rank = sorted(sim_rank, key=lambda x: x[1], reverse=True)
                if sim_rank[0][1] > 0.92:
                    subdataset.append(string2case[sim_rank[0][0]])
        return subdataset

    def task2prompt(
            self,
            task: str,
            dataset: List[LabeledCase],
            use_rule: bool = True,
            use_llm: bool = True,
            use_example: bool = True,
    ) -> List[str]:
        """
        将用户自然语言的任务描述转写为prompt
        :param task:
        :param dataset:
        :param use_rule:
        :param use_llm:
        :param use_example:
        :return:
        """
        raw_prompt = []

        example_str = ''
        output_format_str = ''
        output_limitation_str = self.get_output_limitation_str()

        if use_example:
            # 附加少量（3~4个）示例
            if self.task_kind == Generation:
                example_cases, _ = self.split_dataset(self.good_cases, randint(3, 4), balance_idx=InputIdx)
            elif self.task_kind in (Classification, CLSAnalysis):
                example_cases, _ = self.split_dataset(self.good_cases, randint(3, 4), balance_idx=OutputIdx)
            else:
                raise UndefinedTask
            shuffle(example_cases)
            example_str, data_pics, pic_type = self.get_example_str(example_cases, min_num=len(example_cases), max_num=len(example_cases), use_all=True)
            example_str = self.fill_slot(example_str)
            output_format_str = self.get_output_format_str(task, example_str)

        if self.task_kind == Generation:
            if use_rule:
                if self.has_pic:
                    records = [
                        [[
                            """依据【任务描述】生成数据。包含图片数量不应该多余20张。$示例数据$\n$输出限制$\n$输出格式$\n【任务描述:】\n{}\n【生成的数据:】\n""",
                        ], [task], """第一版"""],
                    ]
                else:
                    records = [
                        [[
                            """依据【任务描述】生成数据。$示例数据$\n$输出限制$\n$输出格式$\n【任务描述:】\n{}\n【生成的数据:】\n""",
                        ], [task], """第一版"""],
                    ]
                for platform in records[-1][0]:
                    template = platform.format(*records[-1][1])
                    prompt = template.replace('$示例数据$', example_str).replace('$输出格式$',
                                                                                 output_format_str).replace(
                        '$输出限制$', output_limitation_str)
                    raw_prompt.append(prompt)
            if use_llm:
                if self.has_pic:
                    records = [
                        [[
                            """请基于以下【任务描述】生成一个数据生成任务的【prompt】。生成的【prompt】应包括：生成任务的背景、生成目标、限制条件、示例、输出格式。包含图片数量不应该多余20张。$示例数据$\n$输出限制$\n$输出格式$\n【任务描述:】\n{}\n【prompt:】\n""",
                        ], [task], """第一版"""],
                    ]
                else:
                    records = [
                        [[
                            """请将【任务描述】改写为数据生成任务的【prompt】。\n一个prompt需要精练地说明生成任务的背景、生成目标、限制条件、示例、输出格式。$示例数据$\n$输出限制$\n$输出格式$\n【任务描述:】\n{}\n【prompt:】\n""",
                            """请基于以下【任务描述】生成一个数据生成任务的【prompt】。生成的【prompt】应包括：生成任务的背景、生成目标、限制条件、示例、输出格式。$示例数据$\n$输出限制$\n$输出格式$\n【任务描述:】\n{}\n【prompt:】\n""",
                        ], [task], """第一版"""],
                    ]
                if self.no_example_in_prompt:
                    output_limitation_str += '生成出的prompt里面不应该包含任何具体的示例，而是应该用文字对示例数据里面能产生重要影响的要点进行概括性地描述。'
                for platform in records[-1][0]:
                    template = platform.format(*records[-1][1])
                    template = template.replace('$示例数据$', example_str).replace('$输出格式$',
                                                                                   output_format_str).replace(
                        '$输出限制$', output_limitation_str)
                    prompt = self.call_llm(template)
                    raw_prompt.append(prompt)
        elif self.task_kind in (Classification, CLSAnalysis):
            if use_rule:
                records = [
                    [[
                        """分类任务：\n{}\n。$示例数据$\n$输出限制$\n$输出格式$\n【以下是待分类的数据:】\n""",
                    ], [task], """第一版"""],
                ]
                for platform in records[-1][0]:
                    template = platform.format(*records[-1][1])
                    if self.no_example_in_prompt:
                        template = (template.replace('$输出格式$', output_format_str).
                        replace('$输出限制$', output_limitation_str))
                    else:
                        template = (template.replace('$示例数据$', example_str).
                        replace('$输出格式$', output_format_str).
                        replace('$输出限制$', output_limitation_str))
                    raw_prompt.append(template)
        else:
            raise UndefinedTask

        cleaned_prompt = []
        for prompt in raw_prompt:
            cleaned_prompt.append(self.clean_prompt(prompt))
        return cleaned_prompt

    def get_output_format_str(self, task, example_str):
        records = [
            [
                """请分析【任务】的【示例数据】，然后结出这个任务的【输出格式】，如果示例数据不包含中文语应在输出格式里明确要求输出的语言。\n\n【任务：】\n{}\n\n【示例数据：】\n{}\n\n【输出格式：】\n""",
                [task, example_str], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        return rst

    def get_final_tips(self, label):
        tips = self.label2tips[label]
        records = [
            [
                """请整理有关标签{}的所有分类要点，注意不要遗漏任何信息，直接输出整理后的所有分类要点。要点里不应该包含任何图片。\n\n【信息：】\n{}\n\n【所有分类要点：】\n""",
                [label, '\n'.join(tips)], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        return rst

    def get_example_str(
            self,
            dataset,
            min_num: int = 1,
            max_num: int = 10,
            add_header: bool = True,
            use_all: bool = False,
    ) -> str:
        if use_all:
            chosen_dataset = dataset
        else:
            min_num = min(min_num, len(dataset))
            max_num = min(max_num, len(dataset))
            chosen_dataset = sample(dataset, randint(min_num, max_num))

        example_case = ''
        data_pics = []
        pic_type = ''
        if len(chosen_dataset) >= 1:
            if add_header:
                example_case += '\n【示例数据:】\n'
            data_texts, data_pics, pic_type = self.get_texts(dataset)
            example_case += '\n'.join(data_texts)
        return example_case, data_pics, pic_type

    def get_output(self, prompt: str, target_input: Input) -> str:
        """
        用大模型基于prompt生成数据
        :param prompt:
        :param target_input:
        :return:
        """
        target_input = self.update_input(target_input)
        if target_input['text'] == '' and len(target_input['pic_list']) == 0:
            rst = self.call_llm(prompt)
        else:
            new_input = {
                'text': prompt + self.get_texts([('', '', target_input, '')])[0][0],
                'pic_list': target_input['pic_list'],
                'pic_type': target_input['pic_type'],
            }
            rst = self.call_llm(new_input)
        return rst

    def rewrite_output(self, input_info: str, output_info: str):
        one_str, pic_list, pic_type = self.get_text((output_info, '', input_info, ''))
        new_inputs = {'text': one_str, 'pic_list': pic_list, 'pic_type': pic_type}
        ans = self.get_cases(
            self.inspector_prompt,
            1,
            [new_inputs],
            do_variety=False,
        )
        rw = ''
        rst = ans[0][0].split('【修正后的输入】', 1)
        if len(rst) == 2:
            if '无需修正' not in rw:
                rw = rst[1]
        sim = ngram_sim(output_info, rw, 3)
        if sim >= 0.4:
            return rw
        self.record.note(('>>> rewrite_input', self.get_text((output_info, '', input_info, ''))))
        self.record.note(('>>> rewrite_output', ans))
        self.record.note(('>>> rewrite_text', output_info))
        return output_info

    def get_cases(
            self,
            prompt: str,
            size: int,
            inputs: List[str],
            dataset: List[LabeledCase] = None,
            do_variety=True,
            use_example: bool = True,  # do_variety=True时才有效
            multi_gen: bool = False,  # do_variety=True时才有效
            delete_same: bool = True,
            clean=False,
            num_consistent: bool = False,
            use_inspector_rewrite: bool = False,
            use_allowed_outputs: bool = False,  # 使用allowed_outputs纠正输出
    ) -> List[LabeledCase]:
        """
        批量生成case, 添加多样性（示例、输出数量等），并对结果去重
        如果是生成任务不允许delete_same、clean、multi_gen
        """
        if self.task_kind == Classification:
            multi_gen = False
            delete_same = False
            clean = False
            num_consistent = True

        if len(inputs) == 0:
            inputs = ['']
        distribute = self.average_split(size, len(inputs))

        cases = []
        all_try_times = 0
        for input_case, input_size in zip(inputs, distribute):
            rst = []
            try_times_max = input_size // 0.9 + 1
            try_times = 0
            while len(rst) < input_size:
                if try_times >= try_times_max:
                    break
                try_times += 1
                all_try_times += 1

                if do_variety:
                    if dataset is None:
                        raise ValueError('need provide dataset if do_variety ')
                    prompt_new = self.variety_prompt(prompt, dataset, use_example=use_example, multi_gen=multi_gen)
                else:
                    prompt_new = prompt

                output_ori = self.get_output(prompt_new, target_input=input_case)
                if multi_gen:
                    outputs = output_ori.split('\n')
                    for output in outputs:
                        output = output.strip()
                        if delete_same:
                            if output in rst:
                                continue
                        if len(output) == 0:
                            continue
                        rst.append(output)
                else:
                    rst.append(output_ori)

                if num_consistent:
                    # 分类任务必须严格生成input_size个结果，如果过多就截断，如果过少就补''
                    if len(rst) < input_size:
                        rst += [''] * (input_size - len(rst))
                    else:
                        rst = rst[:input_size]

                if clean:
                    if len(rst) >= input_size:  # 在积累了一定量级数据后才执行
                        # TODO 量太大时要分批处理, 没去没有启用这个流程
                        outputs_cleaned = self.clean_case(prompt, '\n'.join(rst))
                        rst = list(set(outputs_cleaned))

            for output in rst:
                if use_inspector_rewrite and self.inspector_prompt is not None:
                    output = self.rewrite_output(input_case, output)
                if use_allowed_outputs:
                    output = self.get_allowed_output(output)
                cases.append((output, '', input_case, ''))

            self.record.note(('[part] get cases try times', try_times))
            self.record.note(('[part] get case num', len(rst)))

        self.record.note(('[whole] get cases try times', all_try_times))
        self.record.note(('[whole] get case num', len(cases)))
        self.record.note(('inference_prompt', prompt))
        self.record.note(('inference_cases', cases))
        return cases

    @staticmethod
    def get_best_label(text, labels) -> Tuple[str, float]:
        label_score = []
        for label in labels:
            label_score.append([label, ngram_sim(text, label, 3)])
        shuffle(label_score)  # 在分值全一样时增加随机性
        label_score.sort(key=lambda x: x[1], reverse=True)
        return label_score[0][0], label_score[0][1]

    def get_allowed_output(self, ori_output: str) -> str:
        # 对于多标签分类任务，仅支持通过符号连接多个标签的情况
        # 如果标签本身含有标点符合，则会被错误识别为多个标签
        if not self.output_limited:
            return ori_output
        if ori_output in self.all_allowed_outputs:
            return ori_output

        if not self.is_multi_label:
            best_label, best_score = self.get_best_label(ori_output, self.all_allowed_outputs)
            return best_label
        else:
            # 找多标签分类任务用来拼接的符号
            punctuations = list(set([_ for _ in ori_output if is_punctuation(_)]))

            ori_output_parts = split_punctuation(ori_output)
            fix_output_parts = []
            for part in ori_output_parts:
                best_label, best_score = self.get_best_label(part, self.all_allowed_outputs)
                if best_score > 0.1:
                    fix_output_parts.append(best_label)
            if len(fix_output_parts) == 0:
                fix_output_parts = sample(self.all_allowed_outputs, 1)

            fix_output_parts = list(set(fix_output_parts))
            fix_output = self.split_punctuation.join(fix_output_parts)
            return fix_output

    @staticmethod
    def average_split(ball_num, box_num, size: List[int] = None):
        if box_num == 0:
            raise ValueError('box_num cannot be zero')
        if size is not None:
            assert len(size) == box_num

        if size is None or min(size) >= (ball_num // box_num + 1):
            # 如果box_size的最小值大于ball_num // box_num + 1
            base_num = ball_num // box_num
            distribute = [base_num] * box_num
            remainder = ball_num - base_num * box_num
            # 尽量均匀地采样：不重复
            fifo = [idx for idx in range(box_num)]
            shuffle(fifo)
            for idx in range(remainder):
                distribute[fifo[idx]] += 1
        else:
            fifo = []
            for idx, size in enumerate(size):
                fifo.extend([idx] * size)
            shuffle(fifo)
            distribute = [0] * box_num
            for idx in fifo[:ball_num]:
                distribute[idx] += 1
        return distribute

    def clean_case(self, prompt: str, cases: str) -> List[str]:
        """
        清洗大模型基于prompt生成的数据，去掉冗余的格式信息，用回车分割case
        TODO: 这个方案里不支持case中包含回车
        :param prompt:
        :param cases:
        :return:
        """
        if self.has_pic:
            records = [
                [
                    """下列【原始数据】中包含多条为【任务】生成的数据，请过滤掉冗余的格式信息和背景描述，包含图片数量不应该多余20张，然后输出其中生成的数据（每行一条数据）。\n【任务:】\n{}\n【原始数据:】\n{}\n【清洗后的数据:】\n""",
                    [prompt, cases], """第一版"""],
            ]
        else:
            records = [
                [
                    """下列【原始数据】中包含多条为【任务】生成的数据，请过滤掉冗余的格式信息和背景描述，然后输出其中生成的数据（每行一条数据）。\n【任务:】\n{}\n【原始数据:】\n{}\n【清洗后的数据:】\n""",
                    [prompt, cases], """第一版"""],
            ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        rst = [line for line in rst.split('\n') if len(line) > 0]
        return rst

    @staticmethod
    def pick_dataset(dataset: List[LabeledCase], sign: str, num: int, target_idx: int = LabelIdx) -> List[LabeledCase]:
        """
        基于结构化的标注数据dataset(输出，标签，输入，备注)，从target_idx例里选出和sign标签一样的数据里抽样num个
        TODO 目前只考虑good label
        :param dataset:
        :param sign:
        :param num:
        :param target_idx:
        :return:
        """
        matched_data = []
        for data in dataset:
            if data[target_idx] == sign:
                matched_data.append(data)

        if num is None:
            return matched_data

        # 全随机采样
        chosen_case = sample(matched_data, min(num, len(matched_data)))
        return chosen_case

    def split_dataset(self, dataset: List[LabeledCase], length: int, balance_idx=None) -> Tuple[
        List[LabeledCase], List[LabeledCase]]:
        # 将数据集切分成两份
        length = min(len(dataset), length)

        tag2cases = defaultdict(list)
        if balance_idx is None:
            tag2cases[''] = dataset
        else:
            for case in dataset:
                # TODO 仅使用了 'text'
                if isinstance(case[balance_idx], str):
                    tag2cases[case[balance_idx]].append(case)
                elif isinstance(case[balance_idx], dict) and 'text' in case[balance_idx]:
                    tag2cases[case[balance_idx]['text']].append(case)
                else:
                    tag2cases['{}'.format(case[balance_idx])].append(case)
        dataset_1 = []
        dataset_2 = []
        tags = list(tag2cases.keys())
        tag_size = [len(tag2cases[tag]) for tag in tags]
        tag2num = self.average_split(length, len(tags), size=tag_size)
        for tag, num in zip(tags, tag2num):
            sub_dataset = tag2cases[tag]
            if num == 0:
                selected_idx = []
            else:
                selected_idx = sample(list(range(len(sub_dataset))), num)
            sub_dataset_1 = []
            sub_dataset_2 = []
            for idx, case in enumerate(sub_dataset):
                if idx in selected_idx:
                    sub_dataset_1.append(case)
                else:
                    sub_dataset_2.append(case)
            dataset_1.extend(sub_dataset_1)
            dataset_2.extend(sub_dataset_2)
        return dataset_1, dataset_2

    def get_input_str(self, the_input):
        text = ''
        pic_list = []
        pic_type = ''
        if 'text' in the_input:
            text = the_input['text']
        if 'pic_list' in the_input and len(the_input['pic_list']) > 0:
            pic_list = the_input['pic_list']
            pic_type = the_input['pic_type']
            text = '$pic_note$'*len(pic_list) + text
        return text, pic_list, pic_type

    @staticmethod
    def get_text(case: LabeledCase) -> str:
        pic_list = []
        pic_type = ''
        if len(case[InputIdx]) == 0:
            one_str = case[OutputIdx]
        else:
            if 'text' in case[InputIdx]:
                text = case[InputIdx]['text']
            if 'pic_list' in case[InputIdx]:
                pic_list = case[InputIdx]['pic_list']
                pic_type = case[InputIdx]['pic_type']
                text = '$pic_note$'*len(pic_list) + text
            one_str = '输入：\n{}\n输出：\n{}\n'.format(text, case[OutputIdx])
        if case[CommentIdx] != '':
            one_str += '备注：\n{}\n'.format(case[CommentIdx])
        return one_str, pic_list, pic_type

    def fill_slot(self, text):
        idx = 1
        while '$pic_note$' in text:
            p = '（关联第{}张图）'.format(idx)
            text = text.replace('$pic_note$', p, 1)
            idx += 1
        return text

    def get_texts(self, cases: List[LabeledCase]) -> List[str]:
        texts = []
        pics = []

        for case in cases:
            one_str, pic_list, pic_type = self.get_text(case)
            pics.extend(pic_list)
            texts.append(one_str)
        return texts, pics, pic_type

    def analysis_case2good(
            self,
            case_new_ori: List[LabeledCase],
            case_good_ori: List[LabeledCase],
            task: str,
            wrong_cases_str: str = '',
            label: str = '',
    ) -> str:
        """
        分析旧的生成数据和人工标注的优质数据之间的差异，并总结出需要对旧生成数据做什么修改
        :param case_new_ori:
        :param case_good_ori:
        :param task:
        :param wrong_cases_str:
        :return:
        """
        whole_pic_list = []
        whole_pic_type = ''
        case_new, pics_new, pic_type_new = self.get_example_str(case_new_ori, add_header=False, use_all=True)
        case_good, pics_good, pic_type_good = self.get_example_str(case_good_ori, add_header=False, use_all=True)
        whole_pic_list.extend(pics_new)
        whole_pic_list.extend(pics_good)
        whole_pic_type = pic_type_good
        if len(case_new) == 0 and self.task_kind != CLSAnalysis:
            # CLSAnalysis 任务允许只对正确case做分析
            raise ValueError('cases is empty')
        if len(case_good) > 0:
            if self.task_kind == Generation:
                records = [
                    [
                        """请总结出【生成数据】和【优质数据】的差别，包括语言风格、用词风格、情绪特点、内容重心、其他角度等，并总结出需要对【生成数据】做什么【修改】才能使其更接近【优质数据】。【历史生成数据：】\n{}\n【优质数据：】\n{}\n【修改：】\n""",
                        [case_new, case_good],
                        """1、很容易受列出的细节点的影响，导致分析不了它们之外的项的特点和强行分析每个项的特点，2、不容易拆解出哪些是需要做的修改"""],
                    [
                        """请观察【生成数据】和【优质数据】，总结出【优质数据的特点】。【历史生成数据：】\n{}\n【优质数据：】\n{}\n【优质数据的特点：】\n""",
                        [case_new, case_good], """不做对比分析，只总结优质数据的特点，以及不限度分析角度"""],
                    [
                        """基于【数据生成任务:】{}\n请对比观察【当前数据】和【优质数据】，总结出【优质数据的特点】。\n【当前数据：】\n{}\n【优质数据：】\n{}\n【优质数据的特点：】\n""",
                        [task, case_new, case_good], """提供task做背景知识"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            elif self.task_kind == Classification:
                records = [
                    [
                        """基于分类任务的【任务描述:】{}\n请对比观察【当前分类结果】和【标准答案】，总结出需要补充的【分类判断标准】。\n【当前分类结果：】\n{}\n【标准答案：】\n{}\n$错误数据$总结出的【分类判断标准：】\n""",
                        [task, case_new, case_good], """提供task做背景知识"""],
                ]
                template = records[-1][0].format(*records[-1][1])
                if wrong_cases_str is not None and len(wrong_cases_str) > 0:
                    wrong_cases_str_text, wrong_cases_pic_lists, wrong_cases_pic_type = wrong_cases_str
                    whole_pic_list.extend(wrong_cases_pic_lists)
                    template = template.replace('$错误数据$', '【错误分析：】\n' + wrong_cases_str_text + '\n')
                else:
                    template = template.replace('$错误数据$', '')
            elif self.task_kind == CLSAnalysis:
                if len(case_new) > 0:
                    records = [
                        [
                            """基于分类任务的【任务描述:】{}\n请对比观察【当前分类结果】和【标准答案】，总结出{}类别的判断标准。\n【当前分类结果：】\n{}\n【标准答案：】\n{}\n$错误数据$总结出的【{}类别的判断标准：】\n""",
                            [task, label, case_new, case_good, label], """提供task做背景知识"""],
                    ]
                else:
                    # 无负例
                    records = [
                        [
                            """基于分类任务的【任务描述:】{}\n请对比观察【标准答案】，总结出{}类别的判断标准。\n【标准答案：】\n{}\n$错误数据$总结出的【{}类别的判断标准：】\n""",
                            [task, label, case_good, label], """提供task做背景知识"""],
                    ]
                template = records[-1][0].format(*records[-1][1])
                if wrong_cases_str is not None and len(wrong_cases_str) > 0:
                    wrong_cases_str_text, wrong_cases_pic_lists, wrong_cases_pic_type = wrong_cases_str
                    whole_pic_list.extend(wrong_cases_pic_lists)
                    template = template.replace('$错误数据$', '【错误分析：】\n' + wrong_cases_str_text + '\n')
                else:
                    template = template.replace('$错误数据$', '')
            else:
                raise UndefinedTask
        else:
            if self.task_kind == Generation:
                records = [
                    [
                        """基于【数据生成任务:】{}\n请观察【当前数据】，总结出【当前数据的待改进点】。\n【当前数据：】\n{}\n【当前数据的待改进点：】\n""",
                        [task, case_new], """提供task做背景知识"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            elif self.task_kind in (Classification, CLSAnalysis):
                records = [
                    [
                        """基于分类任务的【任务描述:】{}\n请观察【当前分类结果】，总结出需要补充的【分类判断标准】。\n【当前分类结果：】\n{}\n需要补充的【分类判断标准：】\n""",
                        [task, case_new], """提供task做背景知识"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            else:
                raise UndefinedTask
        template = self.fill_slot(template)
        rst = self.call_llm({'text': template, 'pic_list': whole_pic_list, 'pic_type': whole_pic_type})
        return rst

    def clean_prompt(self, prompt):
        """清洗prompt里面不合适的内容"""
        if self.task_kind == Generation:
            records = [
                [
                    """请对【原prompt】进行修改，并输出【修正后的prompt】。prompt里不应该出现“已有历史数据”、“相比优质数据”、“原prompt”等类似的表达，因为一个prompt应该是独立且完整的不依赖任何其他任务的结果。在保持【原prompt】的信息不遗漏的情况下整理其格式，不要遗漏原prompt里任何信息，按任务背景、数据要求、示例分析、输出格式的结构进行组织。直接输出修正后的prompt，不要输出修改过程。\n【原prompt：】\n{}\n【修正后的prompt：】\n""",
                    [prompt], """第一版"""],
            ]
        elif self.task_kind in (Classification, CLSAnalysis):
            records = [
                [
                    """请对【原prompt】进行修改，并输出【修正后的prompt】。prompt里不应该出现“已有历史数据”、“相比标准答案”、“原prompt”等类似的表达，因为一个prompt应该是独立且完整的不依赖任何其他任务的结果。在保持【原prompt】的信息不遗漏的情况下整理其格式，不要遗漏原prompt里任何信息，按任务的背景、分类标准、限制条件、示例数据、输出格式的结构进行组织。直接输出修正后的prompt，不要输出修改过程。\n【原prompt：】\n{}\n【修正后的prompt：】\n""",
                    [prompt], """第一版"""],
            ]
        else:
            raise UndefinedTask
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        return rst

    def merge_prompt(self, prompt, tips):
        """更新tips"""
        if self.task_kind in (CLSAnalysis, Classification, Generation):
            records = [
                [
                    """请对【原prompt】进行修改，将【要点】融合进去。融合进去后的prompt的格式要和原prompt一致。融合后不应该丢失任何原prompt里面的信息。要直接输出融合后的prompt，不要输出修改过程。\n【原prompt：】\n{}\n【要点：】\n{}\n【融合后的prompt：】\n""",
                    [prompt, tips], """第一版"""],
            ]
        else:
            raise UndefinedTask
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        return rst

    def update_prompt(
            self,
            prompt: str,
            propose: str,
            case_old: List[LabeledCase],
            case_good: List[LabeledCase],
            wrong_cases_str: str = None,
    ) -> str:
        """
        基于propose优化prompt
        :param prompt:
        :param propose:
        :param case_old:
        :param case_good:
        :param wrong_cases_str:
        :return:

        TODO 生成结果里的badcase，对于修改建议需要再清洗一下
        改写后的prompt：xxx
        背景：已生成一些关于赞美、祝福、励志、正能量主题的【历史数据】，但与【优质数据】相比存在不足。
        示例：【优质数据】中的“积极向上永不言弃”，简单直接地表达了励志主题，这就是我们想要达到的风格。
        """
        whole_pic_list = []
        whole_pic_type = ''
        case_old, pics_old, pic_type_old = self.get_example_str(case_old, add_header=False, use_all=True)
        case_good, pics_good, pic_type_good = self.get_example_str(case_good, add_header=False, use_all=True)
        whole_pic_list.extend(pics_old)
        whole_pic_list.extend(pics_good)
        whole_pic_type = pic_type_old

        if len(case_good) > 0:
            if self.task_kind == Generation:
                records = [
                    [
                        """请参考【修改意见】，对【prompt】进行改写。【改写后的prompt】需要基于【修改意见】进行修改，并精练地说明生成任务的背景、生成目标、限制条件、输出格式、示例数据。\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [propose, prompt], """第一版"""],
                    [
                        """【历史数据】是由【prompt】生成，和【优质数据】对比起来还有一些不足。为了生成和【优质数据】更接近的数据，需要参考【历史数据】、【优质数据】和【修改意见】对【prompt】进行改写，并输出【改写后的prompt】，注意改写后的prompt不应该包含文本“历史数据”，“优质数据”，注意改写后的prompt是一个独立且完整的任务描述。改写后的prompt应精练地说明生成任务的背景、生成目标、限制条件、示例数据、输出格式(如果示例数据不包含中文语应在输出格式里明确要求输出的语言)。如果原prompt里有双括号包裹的变量{{变量名}}，则输出的prompt里也应该包含所有双括号包裹的变量，不要丢失变量。\n【历史数据:】\n{}\n【优质数据:】\n{}\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [case_old, case_good, propose, prompt], """第一版"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            elif self.task_kind == Classification:
                if self.no_example_in_prompt:
                    records = [
                        [
                            """【历史分类结果：】是由用分类任务的【原prompt】生成的，和【标准答案】对比起来还有一些不足。为了让分类结果更加精准，需要参考【分类结果】、【标准答案】和【修改意见】对【原prompt】进行优化，并输出【优化后的prompt】，注意优化后的prompt不应该包含文本“历史分类结果”，“标准答案”等字样，优化后的prompt依然是一个独立且完整的任务描述。优化后的prompt应说明分类任务的背景、分类标准、限制条件、输出格式(如果示例数据不包含中文语应在输出格式里明确要求输出的语言)。优化后的prompt应尽量包含修改意见里的总结出的要点，只要原prompt里面没有对子任务分别做要求，那么就应尽量去掉修改意见里总结出的要点的适用范围限制，使这些要点能应用到整个任务的生成中。优化后的prompt必须包含对不同类别分类要求的分析（注意，生成出的prompt里面不应该包含任何具体的示例，而是应该用文字对示例数据里面能产生重要影响的要点进行概括性地描述。）。如果原prompt里有双括号包裹的变量{{变量名}}，则输出的prompt里也应该包含所有双括号包裹的变量，不要丢失变量。\n【历史分类结果:】\n{}\n【标准答案:】\n{}\n$错误数据$【修改意见:】\n{}\n【prompt:】\n{}\n【优化后的prompt:】\n""",
                            [case_old, case_good, propose, prompt], """"""],
                    ]
                else:
                    records = [
                        [
                            """【历史分类结果：】是由用分类任务的【原prompt】生成的，和【标准答案】对比起来还有一些不足。为了让分类结果更加精准，需要参考【分类结果】、【标准答案】和【修改意见】对【原prompt】进行优化，并输出【优化后的prompt】，注意优化后的prompt不应该包含文本“历史分类结果”，“标准答案”等字样，优化后的prompt依然是一个独立且完整的任务描述。优化后的prompt应说明分类任务的背景、分类标准、限制条件、示例数据、输出格式。优化后的prompt应尽量包含修改意见里的总结出的要点，只要原prompt里面没有对子任务分别做要求，那么就应尽量去掉修改意见里总结出的要点的适用范围限制，使这些要点能应用到增个任务的生成中。\n【历史分类结果:】\n{}\n【标准答案:】\n{}\n$错误数据$【修改意见:】\n{}\n【prompt:】\n{}\n【优化后的prompt:】\n""",
                            [case_old, case_good, propose, prompt], """第一版"""],
                        [
                            """【历史分类结果：】是由用分类任务的【原prompt】生成的，和【标准答案】对比起来还有一些不足。为了让分类结果更加精准，需要参考【分类结果】、【标准答案】和【修改意见】对【原prompt】进行优化，并输出【优化后的prompt】，注意优化后的prompt不应该包含文本“历史分类结果”，“标准答案”等字样，优化后的prompt依然是一个独立且完整的任务描述。优化后的prompt应说明分类任务的背景、分类标准、限制条件、示例数据（示例数据部分的字数不应超过1000个字。如果示例字数过多，尽量选择有代表性的示例，并通过凝练示例里的关键信息来减少字数）、输出格式。优化后的prompt应尽量包含修改意见里的总结出的要点，只要原prompt里面没有对子任务分别做要求，那么就应尽量去掉修改意见里总结出的要点的适用范围限制，使这些要点能应用到增个任务的生成中。\n【历史分类结果:】\n{}\n【标准答案:】\n{}\n$错误数据$【修改意见:】\n{}\n【prompt:】\n{}\n【优化后的prompt:】\n""",
                            [case_old, case_good, propose, prompt], """修正prompt里case数量过多"""],
                        [
                            """【历史分类结果：】是由用分类任务的【原prompt】生成的，和【标准答案】对比起来还有一些不足。为了让分类结果更加精准，需要参考【分类结果】、【标准答案】和【修改意见】对【原prompt】进行优化，并输出【优化后的prompt】，注意优化后的prompt不应该包含文本“历史分类结果”，“标准答案”等字样，优化后的prompt依然是一个独立且完整的任务描述。优化后的prompt应说明分类任务的背景、分类标准、限制条件、示例数据（示例数据部分的字数不应超过500个字。如果示例字数过多，尽量选择有代表性的示例，并通过凝练示例里的关键信息来减少字数）、输出格式(如果示例数据不包含中文语应在输出格式里明确要求输出的语言)。优化后的prompt应尽量包含修改意见里的总结出的要点，只要原prompt里面没有对子任务分别做要求，那么就应尽量去掉修改意见里总结出的要点的适用范围限制，使这些要点能应用到增个任务的生成中。优化后的prompt必须包含对不同类别分类要求的分析（字数不限）和示例（不超过500字）。如果原prompt里有双括号包裹的变量{{变量名}}，则输出的prompt里也应该包含所有双括号包裹的变量，不要丢失变量。\n【历史分类结果:】\n{}\n【标准答案:】\n{}\n$错误数据$【修改意见:】\n{}\n【prompt:】\n{}\n【优化后的prompt:】\n""",
                            [case_old, case_good, propose, prompt], """修正prompt里case数量过多"""],
                    ]
                template = records[-1][0].format(*records[-1][1])
                if wrong_cases_str is not None and len(wrong_cases_str) > 0:
                    wrong_cases_str_text, wrong_cases_pic_lists, wrong_cases_pic_type = wrong_cases_str
                    whole_pic_list.extend(wrong_cases_pic_lists)
                    template = template.replace('$错误数据$', '【错误分析：】\n' + wrong_cases_str_text + '\n')
                else:
                    template = template.replace('$错误数据$', '')
            else:
                raise UndefinedTask
        else:
            if self.task_kind == Generation:
                records = [
                    [
                        """【历史数据】是由【prompt】生成。为了生成质量更好的数据，需要参考【历史数据】和【修改意见】对【prompt】进行改写，并输出【改写后的prompt】。【改写后的prompt】应精练地说明生成任务的背景、生成目标、限制条件、示例数据、输出格式(如果示例数据不包含中文语应在输出格式里明确要求输出的语言)。如果原prompt里有双括号包裹的变量{{变量名}}，则输出的prompt里也应该包含所有双括号包裹的变量，不要丢失变量。\n【历史数据:】\n{}\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [case_old, propose, prompt], """第一版"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            elif self.task_kind == Classification:
                records = [
                    [
                        """【当前分类结果】是用分类任务的【prompt】生成的。为了生成质量更好的数据，需要参考【当前分类结果】和【修改意见】对【prompt】进行优化，并输出【优化后的prompt】。【优化后的prompt不应该包含文本“历史分类结果”，“标准答案”等字样，优化后的prompt依然是一个独立且完整的任务描述。【优化后的prompt】应说明分类任务的背景、分类标准、限制条件、示例数据、输出格式。\n【历史数据:】\n{}\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [case_old, propose, prompt], """第一版"""],
                    [
                        """【当前分类结果】是用分类任务的【prompt】生成的。为了生成质量更好的数据，需要参考【当前分类结果】和【修改意见】对【prompt】进行优化，并输出【优化后的prompt】。【优化后的prompt不应该包含文本“历史分类结果”，“标准答案”等字样，优化后的prompt依然是一个独立且完整的任务描述。【优化后的prompt】应说明分类任务的背景、分类标准、限制条件、示例数据、输出格式(如果示例数据不包含中文语应在输出格式里明确要求输出的语言)。优化后的prompt必须包含对不同类别分类要求的分析（字数不限）和示例（不超过500字）。如果原prompt里有双括号包裹的变量{{变量名}}，则输出的prompt里也应该包含所有双括号包裹的变量，不要丢失变量。\n【历史数据:】\n{}\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [case_old, propose, prompt], """第二版"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            else:
                raise UndefinedTask
        template = self.fill_slot(template)
        rst = self.call_llm({'text': template, 'pic_list': whole_pic_list, 'pic_type': whole_pic_type})
        rst = self.clean_prompt(rst)
        return rst

    def verify(self, case_old: List[str], case_new: List[str], case_good: List[str], task: str) -> Tuple[str, int]:
        """

        :param case_old:
        :param case_new:
        :param case_good:
        :param task:
        :return:
        """
        case_old = sample(case_old, min(len(case_old), self.window_size))
        case_new = sample(case_new, min(len(case_new), self.window_size))
        if len(case_good) > 0:
            case_good = sample(case_good, min(len(case_good), self.window_size))
            records = [
                [
                    """请判断【数据集1】和【数据集2】中哪个数据集和【优质数据集】里的数据风格更相似，给出【分析结论】回答“数据集1更相似”或“数据集2更相似”。\n【数据集1:】\n{}\n【数据集2:】\n{}\n【优质数据集:】\n{}\n【分析结论：】\n""",
                    [case_old, case_new, case_good], """第一版"""],
                [
                    """对于数据生成任务：\n{}\n请判断生成的【数据集1】和【数据集2】中哪个数据集和【优质数据集】里的数据风格更相似，给出【分析结论】回答“数据集1更相似”或“数据集2更相似”。\n【数据集1:】\n{}\n【数据集2:】\n{}\n【优质数据集:】\n{}\n【分析结论：】\n""",
                    [task, case_old, case_new, case_good], """第一版"""],
            ]
            template = records[-1][0].format(*records[-1][1])
        else:
            records = [
                [
                    """对于数据【生成任务】：\n{}\n请判断生成的【数据集1】和【数据集2】中哪个数据集更符合【生成任务】的要求。给出【分析结论】回答“数据集1更相似”或“数据集2更相似”。\n【数据集1:】\n{}\n【数据集2:】\n{}\n【分析结论：】\n""",
                    [task, case_old, case_new], """第一版"""],
            ]
            template = records[-1][0].format(*records[-1][1])

        rst = self.call_llm(template)
        rst = rst.replace(' ', '').replace('一', '1').replace('二', '2')
        if '数据集1更相似' in rst:
            rst_signal = 1
        elif '数据集2更相似' in rst:
            rst_signal = 2
        else:
            rst_signal = 0
        return rst, rst_signal

    def get_subtasks(self):
        self.subtasks = self.task2subtask(self.task)

    def get_subdatasets(self):  # TODO 分类容易出错，考虑多做基础之后取交集
        def intersection(dataset1, dataset2):
            rst = []
            str2case = {}
            for case in dataset1 + dataset2:
                str2case[case[0]] = case
            text1 = [case[0] for case in dataset1]
            text2 = [case[0] for case in dataset2]

            text_inter = list(set(text1) & set(text2))
            text_chosen = []
            if len(text_inter) == 0:
                if len(text1) > 0 or len(text2) > 0:
                    text_chosen = list(set(text1) | set(text2))
            else:
                text_chosen = text_inter

            for text in text_chosen:
                rst.append(str2case[text])
            return rst

        subdatasets = []
        for subtask in self.subtasks:
            # 计算2次子集，提高可性度。如果无法获取到有效的子集则用全量数据。
            rst_1 = self.get_subdataset(subtask)
            rst_2 = self.get_subdataset(subtask)
            rst_intersection = intersection(rst_1, rst_2)
            if len(rst_intersection) > 0:
                subdatasets.append(rst_intersection)
            else:
                subdatasets.append(subtask)
        self.subdatasets = subdatasets
        assert len(self.subtasks) == len(self.subdatasets)

    def verify_data(self, prompt: str, size: int, inputs: List[str]) -> None:
        # 基于prompt生成数据
        if prompt in self.prompt2case and not self.skip_old_data:
            return
        cases = self.get_cases(prompt, size, inputs, do_variety=False)

        self.record.note(('prompt', prompt))
        if len(cases) > 0:
            self.prompt2case[prompt] = cases
            self.record.note(('cases generated', cases))
        else:
            self.record.note(('cases generated Fail', ''))

    def gradient_and_update(self, prompt: str, validate: List[LabeledCase], task: str):
        # 计算梯度并更新prompt
        if prompt not in self.prompt2case:
            return []

        new_prompts = []
        for _ in range(self.derive_time):
            # 分析差异
            if self.task_kind == Classification:
                right_cases, wrong_cases, wrong_outputs = self.check_response(self.prompt2case[prompt], validate)
                self.prompt2wrong_cases_str[prompt] = self.get_wrong_cases_str(wrong_cases, wrong_outputs)
            wrong_cases_str = ''
            if prompt in self.prompt2wrong_cases_str:
                wrong_cases_str = self.prompt2wrong_cases_str[prompt]

            # 基于task做分析，以免受到错误迭代后的prompt的干扰
            propose = self.analysis_case2good(self.prompt2case[prompt], validate, task, wrong_cases_str=wrong_cases_str)
            self.prompt2gradient[prompt].append(propose)

            # 更新prompt
            prompt_updated = self.update_prompt(prompt, propose, self.prompt2case[prompt], validate,
                                                wrong_cases_str=wrong_cases_str)
            new_prompts.append(prompt_updated)
            self.record.note(('propose', propose))
            self.record.note(('prompt_updated', prompt_updated))
        return new_prompts

    def check_response(self, respond_cases, validate_cases):
        right_cases, wrong_cases, wrong_outputs = [], [], []
        for respond_case, validate_case in zip(respond_cases, validate_cases):
            if respond_case[InputIdx] != validate_case[InputIdx]:
                xxx = 1
            assert respond_case[InputIdx] == validate_case[InputIdx]
            respond_reformat = self.get_reformat_text(respond_case[OutputIdx])
            validate_reformat = self.get_reformat_text(validate_case[OutputIdx])
            if respond_reformat == validate_reformat:
                right_cases.append(validate_case)
            else:
                wrong_cases.append(validate_case)
                wrong_outputs.append(respond_case[OutputIdx])
        return right_cases, wrong_cases, wrong_outputs

    def get_wrong_cases_str(self, wrong_cases, wrong_outputs):
        texts = []
        pic_lists = []
        pic_type = ''
        for case, output in zip(wrong_cases, wrong_outputs):
            text, pic_list, pic_type = self.get_input_str(case[InputIdx])
            pic_lists.extend(pic_list)
            pic_type = pic_type
            one_str = '对于输入：\n{}\n正确输出是：\n{}\n但却给出了以下错误输出：\n{}\n'.format(text, case[OutputIdx], output)
            if case[CommentIdx] != '':
                one_str += '备注：\n{}\n'.format(case[CommentIdx])
            texts.append(one_str)
        return '\n'.join(texts), pic_lists, pic_type

    def get_rank_score(self, prompts: List[str], dataset: List[LabeledCase], task: str):
        checked_prompts = []
        for prompt in prompts:
            if prompt in self.prompt2case:
                checked_prompts.append(prompt)

        prompt2score = defaultdict(float)
        if self.task_kind == Generation:
            # 计算相对分数
            for prompt_1 in tqdm(checked_prompts, desc='get rank score'):
                for prompt_2 in checked_prompts:
                    if prompt_1 == prompt_2:
                        good, pics, pic_type = self.get_texts(self.pick_dataset(dataset, self.label_good, self.window_size))
                        self.record.note(('good', good))
                        verify_rst, verify_signal = self.verify(self.prompt2case[prompt_1], self.prompt2case[prompt_2],
                                                                good, task)
                        self.record.note(('verify_rst', verify_rst))
                        self.record.note(('verify_signal', verify_signal))
                        if verify_signal == 1:
                            prompt2score[prompt_1] += 1
                        elif verify_signal == 2:
                            prompt2score[prompt_2] += 1
                        else:
                            pass
        elif self.task_kind == Classification:
            # 计算绝对分数
            for prompt in tqdm(checked_prompts, desc='get rank score'):
                prompt2score[prompt] = self.get_prompt_precision(prompt)
        else:
            raise ValueError("unexpected task", self.task_kind)
        prompt_score = [[k, v] for k, v in prompt2score.items()]
        prompt_score.sort(key=lambda x: x[1], reverse=True)
        return prompt_score

    def get_prompt_precision(self, prompt, is_lenient=False) -> float:
        """is_lenient == True 时为宽松的统计模式，在分类结果不完全正确的情况下会酌情给分，以便做更精准的排序"""
        if prompt in self.prompt2precision and not self.skip_old_data:
            return self.prompt2precision[prompt]
        cand_cases = self.prompt2case[prompt]
        score = self.get_precision(cand_cases,
                                   self.validate_cases_fixed + self.validate_cases_new + self.validate_cases_hard,
                                   is_lenient=is_lenient)
        self.prompt2precision[prompt] = score
        return score

    @staticmethod
    def get_reformat_text(text):
        # 假设输出里的多分类的结果用标点符合分隔，且不重复
        return ''.join(sorted(split_punctuation(text)))

    def get_precision(self, cases1: List[LabeledCase], cases2: List[LabeledCase], is_lenient: bool = False) -> float:
        assert len(cases1) == len(cases2)
        right_count = 0
        for case1, case2 in zip(cases1, cases2):
            output1 = case1[OutputIdx]
            output2 = case2[OutputIdx]
            output1_reformat = self.get_reformat_text(output1)
            output2_reformat = self.get_reformat_text(output2)
            if output1_reformat == output2_reformat:
                right_count += 1
            else:
                # 记录hardcase
                if case2 not in (self.validate_cases_fixed + self.validate_cases_hard):
                    self.record.note(('hard_case', case2))
                    self.validate_cases_hard_next.append(case2)
                # 做宽松计分
                if is_lenient:
                    right_count += ngram_sim(output1_reformat, output2_reformat, 2)

        precision = right_count / len(cases1)
        return precision

    def beam_search(self, task: str, prompts: List[str], dataset: List[LabeledCase], iteration: int) -> List[str]:
        """
        beam_search 循环
        :param task: 任务表述
        :param prompts: beam_size个候选prompt
        :param dataset: 标注数据
        :param iteration: 剩余的迭代轮次
        :return:
        """
        self.record.note(('iteration', iteration))
        if iteration == 0:
            for prompt in prompts:
                self.record.note(('final_prompts', prompt))
                if prompt in self.prompt2case:
                    self.record.note(('final_case', self.prompt2case[prompt]))
            if self.use_all_propose:
                new_prompts = []
                all_proposes = []
                for gradients in self.prompt2gradient.values():
                    all_proposes.extend(gradients)
                all_proposes_text = '\n'.join(all_proposes)
                for prompt in prompts:
                    new_prompt = self.merge_prompt(prompt, all_proposes_text)
                    new_prompts.append(new_prompt)
                prompts = new_prompts
                self.record.note(('prompts with all propose', prompts), max_char=100000)
            return prompts

        explored_prompt = []  # 梯度更新后的prompt
        if self.task_kind == Generation:
            input2dataset = self.aggregate_dataset(dataset)
            inputs = list(input2dataset.keys())
            # 对于生成任务，每次求梯度时都随机采样一批数据作为验证集
            validate = self.pick_dataset(dataset, self.label_good, self.window_size)
        elif self.task_kind == Classification:
            # 分类任务按窗口大小遍历所有训练数据
            self.validate_cases_new = self.good_cases[
                                      self.validate_new_idx: self.validate_new_idx + self.window_size_new]
            self.validate_new_idx += self.window_size_new
            if self.validate_new_idx >= len(self.good_cases):
                self.validate_new_idx = 0
            validate = self.validate_cases_fixed + self.validate_cases_new + self.validate_cases_hard
        else:
            raise ValueError("unexpected task", self.task_kind)

        inputs = [case[InputIdx] for case in validate]
        window_size = len(inputs)
        for prompt in prompts:
            self.verify_data(prompt, window_size, inputs)  # 为prompt生成数据
            new_prompts = self.gradient_and_update(prompt, validate, task)  # 得到新的prompt
            explored_prompt.extend(new_prompts)
        for idx, prompt in enumerate(explored_prompt):
            self.prompt2idx[prompt] = 'iter_{}_{}'.format(iteration, idx)
            self.verify_data(prompt, window_size, inputs)

        prompt_score = self.get_rank_score(prompts + explored_prompt, dataset, task)
        prompt_selected = [prompt for prompt, score in prompt_score[:self.beam_size]]
        self.validate_cases_hard += self.validate_cases_hard_next
        self.validate_cases_hard = self.validate_cases_hard[
                                   max(len(self.validate_cases_hard) - self.window_size_hard, 0):]
        self.record.note(('explored_prompt', explored_prompt))
        for prompt, score in prompt_score:
            self.record.note(('Prompt', prompt))
            self.record.note(('Prompt Idx', self.prompt2idx[prompt]))
            self.record.note(('In Rank Score', score))
        self.record.note(('prompt_selected', prompt_selected))
        return self.beam_search(task, prompt_selected, dataset, iteration - 1)
