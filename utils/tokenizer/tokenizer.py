from konlpy.tag import Okt
from collections import Counter

class tokenizer:
    def __init__(self):
        self.okt = Okt()
        # 불용어 리스트 (필요시 계속 추가 가능)
        self.stopwords = set(
            [
                "있다",
                "되다",
                "하다",
                "위해",
                "대한",
                "그리고",
                "그러나",
                "등",
                "것",
                "수",
                "더",
                "자",
                "등의",
                "및",
                "로",
                "도",
                "은",
                "는",
                "이",
                "가",
                "을",
                "를",
                "에",
                "와",
                "과",
                "에서",
            ]
        )

    # 단어 추출 함수
    def extract_keywords(self, texts):
        def clean_nouns(text):
            nouns = self.okt.nouns(text)
            return [word for word in nouns if len(word) > 1 and word not in self.stopwords]

        if isinstance(texts, str):
            return clean_nouns(texts)

        elif isinstance(texts, list):
            return [clean_nouns(text) for text in texts]

        else:
            raise TypeError("입력은 str 또는 list[str] 타입이어야 합니다.")
    
    
    def top_five_keywords(self, texts):
        keywords = self.extract_keywords(texts)
        counter = Counter(keywords)
        top_5 = counter.most_common(5)
        return [keyword for keyword, _ in top_5]
