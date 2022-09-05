import os
import json
from backend.algorithm.preprocess import process

RUN_DEMO_PATH = 'D:\\graduation-project\\demo\\backend\\algorithm\\event_detection\\baselines\\DMBERT\\run_ee_double2_7028.py'
RUN_GET_PATH = 'D:\\graduation-project\\demo\\backend\\algorithm\\event_detection\\baselines\\DMBERT\\get_submission.py'
RESULTS_PATH = 'D:\\graduation-project\\demo\\backend\\algorithm\\event_detection\\upload_res\\results.jsonl'


def eventDetection(raw_input):
    if len(raw_input) == 0:
        return json.dumps({'code': 3001, 'message': "请输入检测文本"})
    # 数据预处理:
    process(raw_input)
    # 调用模型、进行预测
    os.system(f"python3.6 {RUN_DEMO_PATH} --data_dir D:\\graduation-project\\demo\\backend\\algorithm\\MAVEN-dataset"
              f"-lmx-test-zh-1\\data --model_type bert --model_name_or_path "
              f"D:\\graduation-project\\demo\\backend\\algorithm\\event_detection\\res\\checkpoint-20000 "
              f"--task_name zh_infer --output_dir "
              f"D:\\graduation-project\\demo\\backend\\algorithm\\event_detection\\res "
              f"--max_seq_length 128 --do_lower_case --per_gpu_train_batch_size 4 --per_gpu_eval_batch_size 4 "
              f"--gradient_accumulation_steps 1 --learning_rate 5e-5 --num_train_epochs 20 --save_steps 500 "
              f"--logging_steps 500 --seed 42 --do_test --evaluate_during_training --overwrite_output_dir "
              f"--overwrite_cache")
    # 处理预测结果，返回json数据
    os.system(f"python3.6 {RUN_GET_PATH}")
    result_file = open(RESULTS_PATH, "r", encoding='gbk')
    lines = result_file.readlines()
    tableData = []
    Cnt = 0
    for line in lines:
        data = json.loads(line)
        text = data['sentence']
        for pred in data['predictions']:
            if pred['type_id'] != '无':
                Cnt += 1
                trigger_word = pred['trigger_word']
                eventType = pred['type_id']
                tableData.append({'ID': Cnt, "缺陷文本": text, "缺陷触发词": trigger_word, "缺陷分类": eventType})
    result = json.dumps({"code": 3000, "tableData": tableData}, ensure_ascii=False)
    return result


if __name__ == '__main__':
    print(eventDetection("故障情况下使用交流操作电源的设备不能操作导致停电范围扩大。"))
