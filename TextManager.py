from typing import List, Tuple
import docx2txt
import re
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

"""
You could look at sentence structure, too. What % have conjunctions, look at sentences with 1 comma, but no 
conjunction and categorize them by whether there's more words before or after the comma, or sentences with more than 
one comma and no conjunction (those with a clause in the center). There'd be exceptions/false classifications, but it 
could pinpoint trouble areas. 

You could check sentence length within paragraphs (at least x% of sentences have y% more/less words than the average 
length).
 
Programs like the Hemingway app do some analysis, like identifying reading level and adverbs. I'm familiar with the 
Hemingway one in particular, but wish it grouped qualifiers separate from other adverbs.
"""


class TextManager:

    def __init__(self, path: str) -> None:
        self.text = re.sub(r"\t", "", docx2txt.process(path))
        self.nlp = spacy.load('en_core_web_sm')
        self.doc = self.nlp(self.text)

    def print_all_words(self):
        for token in self.doc:
            print(token)

    def show_wordcloud(self):
        wordcloud = WordCloud().generate(self.text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def get_paragraphs(self) -> List[str]:
        pass

    def get_sentences(self) -> List[str]:
        pass

    def get_average_sentence_length(self):
        pass

    def get_average_paragraph_size(self):
        pass

    def get_common_words(self, n: int) -> List[Tuple[int, int]]:
        pass


if __name__ == "__main__":
    manager = TextManager("C:\\Users\\awitt\\Desktop\\Spider Ears.docx")
    manager.show_wordcloud()
