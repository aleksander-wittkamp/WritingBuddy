from typing import List, Tuple
import docx2txt
import re


class TextManager:

    def __init__(self, path: str) -> None:
        self.text = re.sub(r"\t", "", docx2txt.process(path))

    def get_paragraphs(self) -> List[str]:
        return [i for i in self.text.split("\n\n") if i]

    def get_sentences(self) -> List[str]:
        text = re.sub(r"[\n\t]", "", self.text)
        return [i for i in re.split(r"[.!?]\s?", text) if i]

    def get_average_sentence_length(self):
        total = 0
        count = 0
        for i in self.get_sentences():
            total += len(i)
            count += 1
        return total//count

    def get_average_paragraph_size(self):
        total = 0
        count = 0
        for i in self.get_paragraphs():
            total += len(i)
            count += 1
        return total // count

    def get_common_words(self, n: int) -> List[Tuple[int, int]]:
        pass

#
# if __name__ == "__main__":
#     manager = TextManager("C:\\Users\\awitt\\Desktop\\text.docx")
#     print(repr(manager.text))
#     print(manager.get_paragraphs())
#     print(manager.get_sentences())
#     print(manager.get_average_sentence_length())
