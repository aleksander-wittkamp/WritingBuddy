import re
import os
import spacy
import docx2txt
import matplotlib.pyplot as plt
from spacy_syllables import SpacySyllables
from wordcloud import WordCloud, STOPWORDS
from typing import List, Tuple
from collections import Counter
from pathlib import Path
from math import floor
from os import path

"""
Programs like the Hemingway app do some analysis, like identifying reading level and adverbs. This tool performs similar checks.
"""

class TextManager:
    """Stores and analyzes a file's text."""
    def __init__(self, path: str, encoding="UTF-8") -> None:
        self.path = path
        self.text = self.get_text(encoding)
        self.nlp = prep_spacy()
        self.word_count = 0
        self.sentence_count = 0
        self.dialogue_word_count = 0
        self.fog_index_reading_level = 0
        self.parag_count = 0
        self.lemmatized_words = []
        self.vocab_count = 0
        self.complex_sentences = []
        self.populate_attributes()

    def populate_attributes(self) -> None:
        """Analyzes the text."""
        chunks = self.partition_text()
        unique_words = set()
        for i, chunk in enumerate(chunks):
            doc = self.nlp(chunk)
            words, diag_words = self.count_words(doc)
            self.word_count += words
            self.dialogue_word_count += diag_words
            self.sentence_count += self.get_sentence_count(doc)
            self.parag_count += self.get_parag_count(doc)
            self.complex_sentences += self.get_complex_sentences(doc)
            if i == 0:
                self.fog_index_reading_level = determine_reading_level(doc)
            self.lemmatized_words = self.lemmatized_words + [i.lemma_ for i in doc if i.text.isalnum()]
            del doc
        self.vocab_count = self.get_vocab_count()
        
    def get_text(self, encoding) -> str:
        """Gets file text based on file type."""
        text = ""
        if self.path.endswith(".txt"):
            text = Path(self.path).read_text(encoding=encoding)
        elif self.path.endswith(".docx"):
            text = docx2txt.process(self.path)
        else:
            raise Exception("File type must be .txt or .docx")
        return text.replace("\t", "")
        
    def save_summary_stats(self):
        """Saves summary to text file."""
        with open(f"{self.get_filename()}_stats.txt", "w") as text_file:
            print(self.get_summary_stats(), file=text_file)
            
    def save_complex_sentences(self):
        """Saves complex sentences to text file."""
        with open(f"{self.get_filename()}_complex.txt", "w") as text_file:
            print(self.get_complex_sentence_string(), file=text_file)
        
    def print_summary_stats(self):
        """Prints summary to console."""
        print(self.get_summary_stats())
        
    def get_summary_stats(self):
        """Returns a formatted string of summary."""
        return f"Reading level: {self.get_reading_level()}\nWord count: {self.word_count}\n" +\
            f"Dialogue proportion: {self.get_dialogue_proportion()}\n" +\
            f"Vocabulary size: {self.vocab_count}\nCommon words and their frequency: {self.get_common_words()}"

    def get_vocab_count(self) -> int:
        """Returns a count of lemmatized unique words."""
        return len(set(self.lemmatized_words))

    def generate_word_cloud(self) -> None:
        """Opens a wordcloud in a new window."""
        wordcloud = WordCloud(max_words=50, stopwords=STOPWORDS, width=800, height=400)\
            .generate(" ".join(self.lemmatized_words))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
        
    def get_filename(self):
        """Returns the name of the text file without its type."""
        _, fn_with_extension = os.path.split(self.path)
        return fn_with_extension.split(".")[0]

    def count_words(self, doc) -> Tuple:
        """Takes a spacy doc and returns a 2-tuple of overall word count and dialogue word count.
        Currently breaks on novels that have multi-paragraph dialogue.
        """
        words_with_quotations = [
            token.text for token in doc if is_quote_mark(token.text) or not (token.is_punct or is_newline(token.text))
        ]
        word_count = 0
        diag_count = 0
        diag = False
        for i in words_with_quotations:
            if is_quote_mark(i):
                diag = not diag
                continue
            if diag:
                diag_count += 1
            word_count += 1
        return (word_count, diag_count)

    def partition_text(self) -> List:
        """Cuts text into substrings of max length 60k characters.
        Doesn't break sentences.
        """
        chunks = []
        while len(self.text) > 20000:
            split_at = 15000
            while self.text[split_at] != ".":
                split_at += 1
            chunks.append(self.text[0:split_at+1])
            self.text = self.text[split_at+1:]
        chunks.append(self.text)
        return chunks

    def get_parag_count(self, doc) -> int:
        """Counts paragraphs in a spacy doc."""
        parag_count = 0
        for i in [token.text for token in doc]:
            if i == "\n\n" or i == "\n":
                parag_count += 1
        return parag_count

    def get_sentence_count(self, doc) -> int:
        return len(list(doc.sents))
    
    def get_complex_sentences(self, doc) -> List:
        """Returns a list of complex sentences.
        Complexity is determined using a one-sentence version of the FOG index.
        """
        return [sentence.text for sentence in doc.sents if is_complex_sentence(sentence)]
    
    def get_complex_sentence_string(self):
        return "\n".join(self.complex_sentences)
        
    def get_common_words(self, n=5):
        """Prints the five most common lemmatized words in the text."""
        interesting_words = [word for word in self.lemmatized_words if word not in STOPWORDS]
        word_freq = Counter(interesting_words)
        return word_freq.most_common(n)
        
    def get_reading_level(self):
        read_lvl = self.fog_index_reading_level
        return get_fog_index_string(read_lvl)
    
    def get_dialogue_proportion(self):
        return self.dialogue_word_count / self.word_count

def is_complex_sentence(sentence):
    """If the sentence contains >14 words or >2 subject nouns, it is considered complex."""
    num_subj_nouns = sum([1 for token in sentence if token.dep_ == "nsubj"])
    num_words = len([token.text for token in sentence])
    return num_words > 14 or num_subj_nouns > 2

def determine_reading_level(doc) -> int:
    """Determines the Fog index reading level for a spacy doc.
    Equation is .4(num_words/num_sents + 100*num_complex_words/num_words)"""
    sentence_count = 0
    word_count = 0
    complex_word_count = 0
    for sent in doc.sents:
        sentence_count += 1
        sent_word_count = 0
        sent_complex_count = 0
        for token in sent:
            if not token.is_punct and not is_newline(token.text):
                word_count += 1
                if token._.syllables is not None and token._.syllables_count >= 3:
                    complex_word_count += 1
        if word_count > 125:
            break
    raw_level = floor(.4 * (word_count / sentence_count + 100 * complex_word_count / word_count))
    if raw_level < 6:
        raw_level = 6
    elif raw_level > 17:
        raw_level = 17
    return raw_level

def prep_spacy():
    """Prepares the spacy nlp object."""
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe("syllables", after="tagger")
    return nlp

def get_fog_index_string(index: int) -> str:
    index_levels = list(range(6, 18))
    index_strings = [
        "Sixth grade",
        "Seventh grade",
        "Eighth grade",
        "High school freshman",
        "High school sophomore",
        "High school junior",
        "High school senior",
        "College freshman",
        "College sophomore",
        "College junior",
        "College senior",
        "College graduate"
    ]
    fog_dict = {level: string for level, string in zip(index_levels, index_strings)}
    return fog_dict[index]

def is_quote_mark(text):
    """Checks if text is a quotation mark"""
    return text == '"' or text == "“" or text == "”"

def is_newline(text):
    return text == "\n" or text == "\n\n"
    
if __name__ == "__main__":
    manager = TextManager("sample.txt")
    print(manager.get_common_words())
