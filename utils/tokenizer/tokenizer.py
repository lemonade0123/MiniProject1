from konlpy.tag import Okt


class tokenizer:
    def __init__(self, module):
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
        results = []
        for text in texts:
            # 명사만 추출
            nouns = self.okt.nouns(text)
            # 1글자 제거 + 불용어 제거
            keywords = [
                word for word in nouns if len(word) > 1 and word not in stopwords
            ]
            results.append(keywords)
        return results
