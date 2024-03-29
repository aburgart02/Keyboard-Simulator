import json
import os.path


class StatisticsRecorder:
    def __init__(self, text_id, text_language, speed_counter, accuracy_counter):
        self.text_id = text_id
        self.text_language = text_language
        self.speed_counter = int(speed_counter.text().split()[3])
        self.accuracy_counter = int(accuracy_counter.text().split()[1].replace('%', ''))

    def record_statistics(self):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            statistics = json.load(f)
        if self.text_id is not None:
            if self.text_language == 0:
                if self.speed_counter > statistics['rus_progress'][self.text_id][0]:
                    statistics['rus_progress'][self.text_id] = [self.speed_counter, self.accuracy_counter]
            else:
                if self.speed_counter > statistics['eng_progress'][self.text_id][0]:
                    statistics['eng_progress'][self.text_id] = [self.speed_counter, self.accuracy_counter]
        with open(os.path.join('progress', 'progress.txt'), 'w') as f:
            f.write(json.dumps(statistics))
