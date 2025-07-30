# Dictionary to store all program texts
program_texts = {
    1: """Program 1: Natural Language Processing Text Analysis

# Required imports
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Sample texts
text1 = "Mumbai is the financial capital of India. It is known for Bollywood and its street food. I love going there"
text2 = "The Taj Mahal is located in Agra. It was built by Emperor Shah Jahan in memory of his wife."

# Sentence tokenization
sentences1 = sent_tokenize(text1)
sentences2 = sent_tokenize(text2)
print("Sentences from text1:", sentences1)

# Word tokenization
words1 = word_tokenize(text1)
words2 = word_tokenize(text2)
print("Words from text1:", words1)

# Stopword removal
stop_words = set(stopwords.words('english'))
print("Number of stopwords:", len(stop_words))

filtered_words1 = []
for word in words1:
    if word.lower() not in stop_words:
        filtered_words1.append(word)
print("Filtered words:", filtered_words1)

# Stemming
stemmer = PorterStemmer()
stemmed_words1 = []
for word in filtered_words1:
    stemmed_words1.append(stemmer.stem(word))
print("Stemmed words:", stemmed_words1)

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_words1 = []
for word in filtered_words1:
    lemmatized_words1.append(lemmatizer.lemmatize(word))
print("Lemmatized words:", lemmatized_words1)""",
    
    2: """Program 2: Named Entity Recognition with NLTK

nltk.download('averaged_perceptron_tagger')

import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags
import pandas as pd
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('maxent_ne_chunker')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('words')
nltk.download('maxent_ne_chunker_tab')

sample_text = '''Apple Inc. is planning to open a new headquarters
in Austin, Texas.
CEO Tim Cook announced the plan along with Harry Potter'''
text2 = "Harry Potter, goes to Hogwarts"

tokens = word_tokenize(sample_text)
print("Tokens:", tokens)

pos_tags = pos_tag(tokens)
print("POS Tags:", pos_tags)

ne_tree = ne_chunk(pos_tags)
print("Named Entity Tree:", ne_tree)

bio_tags = tree2conlltags(ne_tree)
print("BIO Tags:", bio_tags)

entities = []
current_entity = []
current_type = None

for word, pos, tag in bio_tags:
    if tag.startswith('B-'):  
        if current_entity:
            entities.append((' '.join(current_entity), current_type))
        current_entity = [word]
        current_type = tag[2:]
    elif tag.startswith('I-'):  
        if current_entity and current_type == tag[2:]:
            current_entity.append(word)
        elif not current_entity:
            current_entity = [word]
            current_type = tag[2:]
    else:  
        if current_entity:
            entities.append((' '.join(current_entity), current_type))
            current_entity = []
            current_type = None

if current_entity:
    entities.append((' '.join(current_entity), current_type))

print("Extracted Entities:", entities)""",
    
    3: """Program 3: TF-IDF Implementation

import math
from collections import Counter
import pandas as pd
from nltk.tokenize import word_tokenize
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')

documents = [
    "This movie was fantastic and I loved every minute of it",
    "The acting was terrible and the plot made no sense",
    "Great special effects but the story was predictable",
    "I fell asleep during this boring movie",
    "The soundtrack was amazing and the cinematography stunning"
]

# Tokenize documents
tokenized_docs = [word_tokenize(doc.lower()) for doc in documents]

# Calculate Term Frequency (TF)
term_freq = []
for doc in tokenized_docs:
    total_words = len(doc)
    word_counts = Counter(doc)
    tf = {word: count / total_words for word, count in word_counts.items()}
    term_freq.append(tf)

print("Term Frequency (TF):")
for i, tf in enumerate(term_freq):
    print(f"Document {i+1}: {tf}")

# Calculate Document Frequency (DF)
document_freq = {}
total_docs = len(tokenized_docs)

for doc in tokenized_docs:
    unique_words = set(doc)
    for word in unique_words:
        document_freq[word] = document_freq.get(word, 0) + 1

print("\nDocument Frequency (DF):")
print(document_freq)

# Calculate Inverse Document Frequency (IDF)
idf = {word: math.log(total_docs / freq) for word, freq in document_freq.items()}

print("\nInverse Document Frequency (IDF):")
print(idf)

# Calculate TF-IDF
tfidf_docs = []
for i, tf in enumerate(term_freq):
    tfidf = {word: tf_val * idf[word] for word, tf_val in tf.items()}
    tfidf_docs.append(tfidf)

print("\nTF-IDF Scores:")
for i, tfidf in enumerate(tfidf_docs):
    print(f"Document {i+1}: {tfidf}")

# Using scikit-learn's TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

df_sklearn = pd.DataFrame(X.toarray(), columns=feature_names)
df_sklearn.index = [f"Doc {i+1}" for i in range(len(documents))]

for i in range(len(documents)):
    doc_name = f"Doc {i+1}"
    doc_features = df_sklearn.loc[doc_name]
    present_words = doc_features[doc_features > 0]

    print(f"\n{doc_name} - Words present with TF-IDF scores (sklearn):")
    print(present_words.sort_values(ascending=False))""",
    
    4: """Program 4: N-grams Analysis with Pride and Prejudice Text

import requests
import string
import re
import nltk
from nltk.util import ngrams
from collections import Counter

nltk.download('punkt_tab')

# Example with sample data
sample_data = "This is an example corpus to find ngrams from text"
words = sample_data.split()
unigrams_eg = words
bigrams_eg = list(ngrams(words, 2))
trigrams_eg = list(ngrams(words, 3))

print("Unigrams:")
for unigram in unigrams_eg:
    print(unigram)

print("\nBigrams:")
for bigram in bigrams_eg:
    print(bigram)

print("\nTrigrams:")
for trigram in bigrams_eg:
    print(trigram)

# Analyze Pride and Prejudice
url = "https://www.gutenberg.org/files/1342/1342-0.txt"
response = requests.get(url)
text = response.text

main_text = text.lower()
tokens = nltk.word_tokenize(main_text)

# Clean tokens
cleaned_tokens = []
for token in tokens:
    cleaned_token = re.sub(r'[^\w\s]', '', token)
    if cleaned_token and not cleaned_token.isdigit():
        cleaned_tokens.append(cleaned_token)

# Generate n-grams
unigrams = cleaned_tokens
bigrams = list(ngrams(cleaned_tokens, 2))
trigrams = list(ngrams(cleaned_tokens, 3))

# Calculate frequencies
unigram_freq = Counter(unigrams)
bigram_freq = Counter(bigrams)
trigram_freq = Counter(trigrams)

top_unigrams = unigram_freq.most_common(20)
top_bigrams = bigram_freq.most_common(20)
top_trigrams = trigram_freq.most_common(20)

print(f"Total tokens: {len(cleaned_tokens)}")
print(f"Unique unigrams: {len(unigram_freq)}")
print(f"Unique bigrams: {len(bigram_freq)}")
print(f"Unique trigrams: {len(trigram_freq)}")

print("\nTop 20 Unigrams:")
for item, count in top_unigrams:
    print(f"{item}: {count}")

print("\nTop 20 Bigrams:")
for item, count in top_bigrams:
    print(f"{item}: {count}")

print("\nTop 20 Trigrams:")
for item, count in top_trigrams:
    print(f"{item}: {count}")""",
    
    5: """Program 5: Word Embeddings and Similarity Analysis

# Install required packages
%pip install scipy==1.11.4
from gensim.models import KeyedVectors
from gensim.downloader import load
from scipy.spatial.distance import cosine

# Load a lighter pre-trained GloVe model (50 dimensions)
print("Loading model...")
model = load('glove-wiki-gigaword-50')  # ~66MB, fast and compatible

# Function to compute cosine similarity
def cosine_similarity(word1, word2):
    if word1 in model and word2 in model:
        sim = 1 - cosine(model[word1], model[word2])
        return sim
    else:
        return "One or both words not in vocabulary."

# Define word pairs
word_pairs = [
    ("king", "queen"),
    ("king", "car"),
    ("cat", "dog"),
    ("sun", "moon"),
    ("apple", "banana"),
]

# Print cosine similarities
print("\n--- Cosine Similarity Between Word Pairs ---")
for w1, w2 in word_pairs:
    similarity = cosine_similarity(w1, w2)
    print(f"Similarity({w1}, {w2}) = {similarity}")

# Retrieve Top N similar words
target_word = "computer"
top_n = 10

print(f"\n--- Top {top_n} words similar to '{target_word}' ---")
if target_word in model:
    similar_words = model.most_similar(target_word, topn=top_n)
    for word, score in similar_words:
        print(f"{word}: {score}")
else:
    print(f"'{target_word}' not found in vocabulary.")""",
    
    6: """# program 6

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms, utils
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyperparameters
batch_size = 128
learning_rate = 1e-3
epochs = 10
latent_dim = 20

# MNIST dataset
transform = transforms.Compose([
    transforms.ToTensor(),
])

train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

# VAE Model
class VAE(nn.Module):
    def _init_(self, latent_dim):
        super(VAE, self)._init_()
        self.fc1 = nn.Linear(28*28, 400)
        self.fc21 = nn.Linear(400, latent_dim)  # Mean
        self.fc22 = nn.Linear(400, latent_dim)  # Log variance
        self.fc3 = nn.Linear(latent_dim, 400)
        self.fc4 = nn.Linear(400, 28*28)

    def encode(self, x):
        h1 = F.relu(self.fc1(x))
        return self.fc21(h1), self.fc22(h1)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        h3 = F.relu(self.fc3(z))
        return torch.sigmoid(self.fc4(h3))

    def forward(self, x):
        mu, logvar = self.encode(x.view(-1, 28*28))
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar

# Loss function
def loss_function(recon_x, x, mu, logvar):
    BCE = F.binary_cross_entropy(recon_x, x.view(-1, 28*28), reduction='sum')
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return BCE + KLD

# Model, optimizer
model = VAE(latent_dim).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
model.train()
for epoch in range(epochs):
    train_loss = 0
    for batch_idx, (data, _) in enumerate(train_loader):
        data = data.to(device)
        optimizer.zero_grad()
        recon_batch, mu, logvar = model(data)
        loss = loss_function(recon_batch, data, mu, logvar)
        loss.backward()
        train_loss += loss.item()
        optimizer.step()
    print(f'Epoch [{epoch+1}/{epochs}], Loss: {train_loss/len(train_loader.dataset):.4f}')

# Generate samples
model.eval()
with torch.no_grad():
    z = torch.randn(64, latent_dim).to(device)
    sample = model.decode(z).cpu()
    sample = sample.view(64, 1, 28, 28)
    grid_img = utils.make_grid(sample, nrow=8)
    plt.figure(figsize=(8, 8))
    plt.imshow(grid_img.permute(1, 2, 0))
    plt.axis('off')
    plt.title('Generated Images from VAE')
    plt.show()""",
    
    7: """Program 7: Text Generation with LSTM Neural Network

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Sample text for training
text = ("Machine learning is a field of artificial intelligence that uses statistical techniques "
        "to give computer systems the ability to learn from data, without being explicitly programmed. "
        "Deep Learning is a subset of machine learning concerned with algorithms inspired by the structure "
        "and function of the brain called artificial neural networks. These techniques are widely used in "
        "computer vision, natural language processing, and speech recognition.")
text = text.lower()

# Tokenize the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])
total_words = len(tokenizer.word_index) + 1

# Create input sequences
input_sequences = []
token_list = tokenizer.texts_to_sequences([text])[0]
for i in range(1, len(token_list)):
    n_gram_sequence = token_list[:i+1]
    input_sequences.append(n_gram_sequence)

# Pad sequences
max_seq_len = max(len(seq) for seq in input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_seq_len, padding='pre')

# Create training data
X = input_sequences[:, :-1]  
y = input_sequences[:, -1]  
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

# Build the model
model = Sequential()
model.add(Embedding(total_words, 64, input_length=max_seq_len - 1))
model.add(LSTM(100))
model.add(Dense(total_words, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=200, verbose=0)

# Function to generate text
def generate_text(seed_text, next_words=20):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_seq_len - 1, padding='pre')
        predicted_probs = model.predict(token_list, verbose=0)
        predicted_index = np.argmax(predicted_probs, axis=1)[0]
        output_word = tokenizer.index_word.get(predicted_index, "")
        if output_word == "":
            break
        seed_text += " " + output_word
    return seed_text

# Test the model
generated = generate_text("machine learning", next_words=15)
print("Generated text:\n", generated)""",
    
    8: """# program 8

!pip install PyMuPDF


import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
import fitz  # PyMuPDF
# !pip install PyMuPDF

# 1. Load and clean text from PDF
def load_text(pdf_path):
    with fitz.open(pdf_path) as doc:
        return "".join(page.get_text() for page in doc).lower()

text = load_text("/content/Algorithmic_Fairness_High_School_Dropout_Prediction_PPT.pptx")

# 2. Create vocabulary
PAD = '<PAD>'
chars = [PAD] + sorted(set(text))
char_to_idx = {c: i for i, c in enumerate(chars)}
idx_to_char = {i: c for c, i in char_to_idx.items()}
vocab_size = len(chars)

# 3. Prepare sequences
seq_len, step = 40, 3
X = [[char_to_idx[c] for c in text[i:i+seq_len]]
     for i in range(0, len(text) - seq_len, step)]
y = [char_to_idx[text[i + seq_len]] for i in range(0, len(text) - seq_len, step)]

X = np.array(X)
y = to_categorical(y, num_classes=vocab_size)

# 4. Build and train model
model = Sequential([
    Embedding(vocab_size, 50, input_length=seq_len),
    LSTM(128),
    Dense(vocab_size, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer=Adam(0.001))

model.fit(X, y, batch_size=64, epochs=10, validation_split=0.2)

# 5. Sampling function
def sample(preds, temp=1.0):
    preds = np.log(np.asarray(preds) + 1e-8) / temp
    preds = np.exp(preds) / np.sum(np.exp(preds))
    return np.random.choice(len(preds), p=preds)

# 6. Text generation function
def generate_text(seed, length=200, temp=1.0):
    generated = seed
    seq = [char_to_idx.get(c, 0) for c in seed[-seq_len:]]
    seq = ([0] * (seq_len - len(seq))) + seq  # pad if needed

    for _ in range(length):
        pred = model.predict(np.array([seq]), verbose=0)[0]
        next_idx = sample(pred, temp)
        generated += idx_to_char[next_idx]
        seq = seq[1:] + [next_idx]

    return generated

# 7. Example text generation
print(generate_text("alice was beginning to get very tired", length=300, temp=0.7))""",
    
    9: """Program 9: Variational Autoencoder (VAE) for MNIST

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

def build_encoder(latent_dim):
    inputs = keras.Input(shape=(28, 28, 1))
    x = layers.Flatten()(inputs)
    x = layers.Dense(400, activation="relu")(x)
    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)

    def sampling(args):
        z_mean, z_log_var = args
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

    z = layers.Lambda(sampling)([z_mean, z_log_var])
    return keras.Model(inputs, [z_mean, z_log_var, z], name="encoder")

def build_decoder(latent_dim):
    latent_inputs = keras.Input(shape=(latent_dim,))
    x = layers.Dense(400, activation="relu")(latent_inputs)
    x = layers.Dense(28 * 28, activation="sigmoid")(x)
    outputs = layers.Reshape((28, 28, 1))(x)
    return keras.Model(latent_inputs, outputs, name="decoder")

class VAE(keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def call(self, inputs):
        z_mean, z_log_var, z = self.encoder(inputs)
        reconstructed = self.decoder(z)
        return reconstructed, z_mean, z_log_var

def vae_loss(inputs, outputs, z_mean, z_log_var):
    reconstruction_loss = tf.reduce_mean(
        keras.losses.binary_crossentropy(inputs, outputs)
    ) * 28 * 28
    kl_loss = -0.5 * tf.reduce_mean(
        1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var)
    )
    return reconstruction_loss + kl_loss

# Training parameters
latent_dim = 20
batch_size = 128
epochs = 10

# Load and preprocess MNIST dataset
(x_train, _), _ = keras.datasets.mnist.load_data()
x_train = x_train.astype("float32") / 255.0
x_train = np.expand_dims(x_train, -1)

# Build and compile the VAE model
encoder = build_encoder(latent_dim)
decoder = build_decoder(latent_dim)
vae = VAE(encoder, decoder)
optimizer = keras.optimizers.Adam()

@tf.function
def train_step(images):
    with tf.GradientTape() as tape:
        reconstructed, z_mean, z_log_var = vae(images)
        loss = vae_loss(images, reconstructed, z_mean, z_log_var)
    gradients = tape.gradient(loss, vae.trainable_variables)
    optimizer.apply_gradients(zip(gradients, vae.trainable_variables))
    return loss

# Prepare the training dataset
train_dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(60000).batch(batch_size)

# Training loop
for epoch in range(epochs):
    total_loss = 0
    for batch in train_dataset:
        total_loss += train_step(batch)
    print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_dataset):.4f}")

# Generate new images
z_samples = np.random.normal(size=(16, latent_dim))
generated_images = decoder.predict(z_samples)

# Display generated images
fig, axes = plt.subplots(4, 4, figsize=(5, 5))
for i, ax in enumerate(axes.flat):
    ax.imshow(generated_images[i].squeeze(), cmap='gray')
    ax.axis('off')
plt.show()"""
}

def print_program(program_number):
    """
    Print the text of the specified program number
    
    Args:
        program_number (int): The number of the program to display
    """
    if program_number in program_texts:
        print(program_texts[program_number])
    else:
        print(f"Program {program_number} not found!")
