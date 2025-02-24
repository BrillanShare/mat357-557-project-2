from gensim.models import KeyedVectors

# Load pretrained model (since intermediate data is not included, the model cannot be updated)
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

# Getting a word vector from the pretrained model
vector = model['fish']  # Use model[key] instead of model.wv[key] for pretrained models

# Finding similar words using the pretrained model
similar_words = model.most_similar('fish')

print(vector)
# Displaying the similar words
print(similar_words)