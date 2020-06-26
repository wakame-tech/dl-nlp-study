import os
from pathlib import Path
from typing import *
# workaround for joblib error
# see: https://stackoverflow.com/questions/61893719/importerror-cannot-import-name-joblib-from-sklearn-externals
import joblib
from janome.tokenizer import Tokenizer
import hydra
from omegaconf import DictConfig
import pandas as pd
import chariot.transformer as ct
from chariot.dataset_preprocessor import DatasetPreprocessor

from allennlp.data import Instance
from allennlp.data.token_indexers import TokenIndexer
from allennlp.data.tokenizers import Token
from allennlp.data.fields import TextField, LabelField
from allennlp.data.dataset_readers import DatasetReader
from allennlp.data.token_indexers import SingleIdTokenIndexer

MAX_SEQ_LEN = 100

class YoutubeTitleReader(DatasetReader):
    """
    - columns
        name,channel,video_id,title
    """
    def __init__(
        self, 
        tokenizer:Callable[[str], List[str]]=lambda x: x.split(),
        token_indexers:Dict[str, TokenIndexer]=None,
        max_seq_len:Optional[int]=MAX_SEQ_LEN
    ):
        super().__init__(lazy=False)
        self.tokenizer = tokenizer
        self.token_indexers = token_indexers or {'tokens':SingleIdTokenIndexer()}
        self.max_seq_len = max_seq_len

    def text_to_instance(self, question: List[Token], answer: List[Token]) -> Instance:
        # input
        question_field = TextField(question, self.token_indexers)
        # output
        answer_field = TextField(answer, self.token_indexers)
        fields = {
            'question': question_field,
            'answer': answer_field,
        }
        return Instance(fields)

    def _read(self, data_path:str) -> Iterator[Instance]:
        df = pd.read_csv(data_path)
        for i, row in df.iterrows():
            # question tokens
            q = [Token(x) for x in self.tokenizer(row['question'])]
            # ansewer tokens
            a = [Token(x) for x in self.tokenizer(row['answer'])]

            yield self.text_to_instance(q, a)

@hydra.main(config_path='config.yml')
def preprocess(cfg : DictConfig):
    print(cfg.pretty())

    # df = pd.read_csv(cfg.preprocess.csv_path, nrows=500)

    # print(df.head(5))

    # dp = DatasetPreprocessor()
    # # TODO: preprocess
    # dp.process('title')\
    #     .by(ct.text.UnicodeNormalizer())\
    #     .by(ct.Tokenizer('ja'))\
    #     .by(ct.token.StopwordFilter('ja'))\
    #     # .by(ct.Vocabulary(min_df=5, max_df=0.5))\
    #     # .by(Padding(length=pad_length))\

    # preprocessed = dp.preprocess(df)

    # print(preprocessed['title'])

    ter = Tokenizer()
    token_indexer = SingleIdTokenIndexer()
    def tokenizer(text: str):
        return [tok for tok in ter.tokenize(text, wakati=True)][:MAX_SEQ_LEN]

    print(tokenizer('今日は良い天気ですね。'))

    reader = YoutubeTitleReader(tokenizer=tokenizer)
    train_dataset = reader.read(Path(os.environ['ROOT']) / 'dataset/sample.tsv')

    print(train_dataset[0].fields['question'])


if __name__ == "__main__":
    preprocess()