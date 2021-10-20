import json
import os.path


class StatisticsRecorder:
    def __init__(self, text_id, text_language, speed_counter):
        self.text_id = text_id
        self.text_language = text_language
        self.speed_counter = speed_counter

    def record_statistics(self):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            statistics = json.load(f)
        if self.text_id is not None and self.text_id < 10:
            if self.text_language == 0:
                statistics['rus_progress'][self.text_id] = int(self.speed_counter.text().split()[3])
            else:
                statistics['eng_progress'][self.text_id] = int(self.speed_counter.text().split()[3])
        with open(os.path.join('progress', 'progress.txt'), 'w') as f:
            f.write(json.dumps(statistics))
