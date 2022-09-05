import json
import os
import re
import random
import hashlib
import jieba
import pandas as pd
from transformers import AutoTokenizer

_clear_space_p = re.compile(r'\s+')

MODEL_DIR = os.path.dirname("D:\\graduation-project\\demo\\backend\\algorithm\\event_detection\\res"
                            "\\checkpoint-20000")
DATA_DIR = os.path.dirname("D:\\graduation-project\\demo\\backend\\algorithm\\event_detection\\data")
OUTPUT_NAME = 'test.jsonl'
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
labels = ['取消', '完成', '开始', '主动进行', '分析', '被动遭受', '合计', '各项占比', '破损', '质量', '操作', '烧损', '腐蚀', '接触', '久置', '错位', '开路',
          '变形', '脱落', '规定', '期望', '措施', '检查', '接入', '断开', '修改']

labels2ids = dict()
for i, label in enumerate(labels):
    labels2ids[label] = i


def get_title(id):
    return '[UNK]'


def get_hashid(strs):
    hashid = hashlib.md5()
    for s in strs:
        hashid.update(s.encode(encoding='utf8'))
    return hashid.hexdigest()


def clear_space(s):
    return _clear_space_p.sub('', s)


def get_offset(text_tokens, trigger_tokens):
    j, k = 0, 0
    while j < len(text_tokens) and k < len(trigger_tokens):
        if text_tokens[j] == trigger_tokens[k]:
            j += 1
            k += 1
        else:
            j -= (k - 1)
            k = 0
    if k == len(trigger_tokens):
        # print(j - k, j)
        return [j - k, j]
    else:
        return None


def gen_jsonl(text, title):
    text_tokens = tokenizer.tokenize(text)
    jsonl_res = {
        'id': get_hashid([title, text]),
        'title': '[UNK]',
        'content':
            [
                {
                    'sentence': text,
                    'tokens': text_tokens
                }
            ],
        'events': [],
        'candidates': []
    }
    try:
        segs = jieba.lcut(text)
        samples = list()
        for seg in segs:
            samples.append(seg)
        for candidate_sample in samples:
            id = get_hashid([title, text, candidate_sample])
            sent_id = 0
            offset = get_offset(text_tokens, tokenizer.tokenize(candidate_sample))
            if offset:
                candidate_trigger = {
                    'id': id,
                    'trigger_word': candidate_sample,
                    'sent_id': sent_id,
                    'offset': offset
                }
                jsonl_res['candidates'].append(candidate_trigger)
    except:
        print('generate candidate sample failed:\n\twith samples={}\n\ttext={}'.format(samples, text))
    return jsonl_res


def process(raw_input):
    # 将raw_input按句子切分开，然后找到每个句子中的谓语，并按照测试集的样式进行整理。得到模型输入json_input
    raw_inputs = str(raw_input).split('。')
    contents = list()
    for text in raw_inputs:
        if len(text) != 0:
            contents.append(json.dumps(gen_jsonl(text, get_title('')), ensure_ascii=False))
    with open("D:\\graduation-project\\demo\\backend\\algorithm\\event_detection\\data\\test.jsonl", 'w',
              encoding='utf8') as fout:
        fout.write('\n'.join(contents))


if __name__ == '__main__':
    process("故障情况下使用交流操作电源的设备不能操作导致停电范围扩大。")
