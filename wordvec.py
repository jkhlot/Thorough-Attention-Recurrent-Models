from __future__ import absolute_import
from six.moves import cPickle
import numpy as np
import os
import pprint
from collections import defaultdict, OrderedDict

def get_wordvec(fname,vocab_path='imdb.dict.pkl'):
	vocab = cPickle.load(open(vocab_path,'rb'))
	w2v = load_bin_vec(fname, vocab)
	print "word2vec loaded!"
	print "num words already in word2vec: " + str(len(w2v))
	add_unknown_words(w2v, vocab)
	W, word_idx_map = get_W(w2v)
	return W, word_idx_map

def get_W(word_vecs, k=300):
	"""
	Get word matrix. W[i] is the vector for word indexed by i
	"""
	vocab_size = len(word_vecs)
	word_idx_map = dict()
	W = np.zeros(shape=(vocab_size+1, k))            
	W[0] = np.zeros(k)
	i = 1
	for word in word_vecs:
	    W[i] = word_vecs[word]
	    word_idx_map[word] = i
	    i += 1
	return W, word_idx_map

def load_bin_vec(fname, vocab):
	"""
	Loads 300x1 word vecs from Google (Mikolov) word2vec
	"""
	word_vecs = {}
	with open(fname, "rb") as f:
	    header = f.readline()
	    vocab_size, layer1_size = map(int, header.split())
	    binary_len = np.dtype('float32').itemsize * layer1_size
	    for line in xrange(vocab_size):
	        word = []
	        while True:
	            ch = f.read(1)
	            if ch == ' ':
	                word = ''.join(word)
	                break
	            if ch != '\n':
	                word.append(ch)   
	        if word in vocab:
	           word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')  
	        else:
	            f.read(binary_len)
	return word_vecs

def add_unknown_words(word_vecs, vocab, min_df=1, k=300):
	"""
	For words that occur in at least min_df documents, create a separate word vector.    
	0.25 is chosen so the unknown vectors have (approximately) same variance as pre-trained ones
	"""
	for word in vocab:
	    if word not in word_vecs and vocab[word] >= min_df:
	        word_vecs[word] = np.random.uniform(-0.25,0.25,k) 