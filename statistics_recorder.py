import json
import os.path


class StatisticsRecorder:
    def __init__(self, text_id, text_language, speed_counter):
        self.text_id = text_id
        self.text_language = text_language
        self.speed_counter = speed_counter

    def record_statistics(self):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            data = f.readlines()
        progress_rus = json.loads(data[0])
        progress_eng = json.loads(data[1])
        rus_max_speed = json.loads(data[2])
        eng_max_speed = json.loads(data[3])
        if self.text_id is not None and self.text_id < 10:
            if self.text_language == 0:
                progress_rus[self.text_id] = 1
            else:
                progress_eng[self.text_id] = 1
        if int(self.speed_counter.text().split()[3]) > rus_max_speed and self.text_language == 0:
            rus_max_speed = int(self.speed_counter.text().split()[3])
        if int(self.speed_counter.text().split()[3]) > eng_max_speed and self.text_language == 1:
            eng_max_speed = int(self.speed_counter.text().split()[3])
        with open(os.path.join('progress', 'progress.txt'), 'w') as f:
            f.write(json.dumps(progress_rus))
            f.write('\n')
            f.write(json.dumps(progress_eng))
            f.write('\n')
            f.write(json.dumps(rus_max_speed))
            f.write('\n')
            f.write(json.dumps(eng_max_speed))
