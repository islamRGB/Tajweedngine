# tajweed_engine.py
import re

class TajweedEngine:
    def __init__(self):
        self.sukun = '\u0652'
        self.shadda = '\u0651'
        self.nun = 'ن'
        self.ba = 'ب'
        self.ta = 'ت'
        self.tha = 'ث'
        self.dal = 'د'
        self.dha = 'ذ'
        self.sin = 'س'
        self.shin = 'ش'
        self.saad = 'ص'
        self.dad = 'ض'
        self.taa = 'ط'
        self.dhaa = 'ظ'
        self.zay = 'ز'
        self.qaf = 'ق'
        self.kaf = 'ك'
        self.jeem = 'ج'
        self.waw = 'و'
        self.ya = 'ي'

    def detect_iqlab(self, text):
        pattern = rf'({self.nun}{self.sukun})[^\u064B-\u0652]*{self.ba}'
        return [{'rule': 'Iqlab', 'ar': 'الإقلاب', 'desc': 'نون ساكنة تُقلب ميمًا قبل الباء', 'example': m.group()} for m in re.finditer(pattern, text)]

    def detect_idgham(self, text):
        letters = 'يرولمن'
        pattern = rf'({self.nun}{self.sukun})[^\u064B-\u0652]*[{letters}]'
        return [{'rule': 'Idgham', 'ar': 'الإدغام', 'desc': 'نون ساكنة تدخل في الحرف التالي', 'example': m.group()} for m in re.finditer(pattern, text)]

    def detect_ikhfa(self, text):
        letters = 'تثددذسشصضطظز'
        pattern = rf'({self.nun}{self.sukun})[^\u064B-\u0652]*[{letters}]'
        return [{'rule': 'Ikhfa', 'ar': 'الإخفاء', 'desc': 'نون ساكنة تُخفى بصوت الغنة', 'example': m.group()} for m in re.finditer(pattern, text)]

    def detect_madd(self, text):
        pattern = r'[اوي]\s+'
        return [{'rule': 'Madd', 'ar': 'المد', 'desc': 'إطالة الصوت', 'example': m.group().strip()} for m in re.finditer(pattern, text)]

    def analyze(self, text):
        rules = []
        rules += self.detect_iqlab(text)
        rules += self.detect_idgham(text)
        rules += self.detect_ikhfa(text)
        rules += self.detect_madd(text)
        return rules

    def compare(self, user_text, correct_text):
        user_words = user_text.strip().split()
        correct_words = correct_text.strip().split()
        mistakes = []
        correct = []

        max_len = max(len(user_words), len(correct_words))
        for i in range(max_len):
            u = user_words[i] if i < len(user_words) else ""
            c = correct_words[i] if i < len(correct_words) else ""
            if u == c:
                correct.append({"index": i, "word": u})
            else:
                mistakes.append({"index": i, "expected": c, "got": u or "(empty)"})
        return {"mistakes": mistakes, "correct": correct}

    def get_feedback(self, user_text, correct_text):
        ahkam = self.analyze(correct_text)
        comparison = self.compare(user_text, correct_text)
        mistake_count = len(comparison["mistakes"])
        total_words = len(correct_text.strip().split())
        accuracy = max(0, round((1 - (mistake_count / total_words)) * 100))
        status = "✅ تم بنجاح" if accuracy > 80 else "🔁 أعد المحاولة"

        return {
            "status": status,
            "accuracy": accuracy,
            "user_text": user_text,
            "correct_text": correct_text,
            "mistakes": comparison["mistakes"],
            "correct": comparison["correct"],
            "ahkam": ahkam
        }