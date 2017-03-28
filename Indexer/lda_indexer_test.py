from Indexer.utils import *
from gensim import corpora, models
from gensim.models.ldamulticore import  LdaMulticore
import operator
path="/mnt/results/results_wordids.txt.bz2"
path2="/mnt/lda/lda.model"
id2word = corpora.Dictionary.load_from_text(path)
lda=models.LdaModel.load(path2)
new_doc=id2word.doc2bow(["i'm", "playing", "football"])
sorted_probs=sorted(lda[new_doc],key=lambda x: x[1])
top_topics, _ = [list(c) for c in zip(*sorted_probs[:5])]



