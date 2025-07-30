# PKMB Package

A comprehensive Python package containing various NLP and Machine Learning implementations.

## Installation

```bash
pip install pkmb
```

## Usage

```python
from pkmb import print_program

# Print any program (1-5, 7, 9)
print_program(1)  # Basic NLP operations
print_program(2)  # Named Entity Recognition
print_program(3)  # TF-IDF implementation
print_program(4)  # N-grams analysis
print_program(5)  # Word Embeddings analysis
print_program(7)  # Text Generation with LSTM
print_program(9)  # Variational Autoencoder for MNIST
```

## Available Programs

1. **Program 1: Natural Language Processing (NLP) Text Analysis**
   - Basic NLP operations using NLTK
   - Includes: tokenization, stopword removal, stemming, and lemmatization
   - Demonstrates both sentence and word-level processing

2. **Program 2: Named Entity Recognition (NER)**
   - Uses NLTK for entity extraction
   - Identifies persons, organizations, locations
   - Includes BIO tagging and tree representation

3. **Program 3: TF-IDF Implementation**
   - Manual implementation of TF-IDF calculation
   - Comparison with scikit-learn's TfidfVectorizer
   - Document similarity analysis

4. **Program 4: N-grams Analysis**
   - Uses Pride and Prejudice as corpus
   - Generates unigrams, bigrams, and trigrams
   - Includes frequency analysis and visualization

5. **Program 5: Word Embeddings Analysis**
   - Uses GloVe embeddings (50d)
   - Word similarity computation
   - Semantic relationship analysis

7. **Program 7: Text Generation with LSTM**
   - Neural network-based text generation
   - Uses TensorFlow/Keras LSTM architecture
   - Includes training and text generation capabilities

9. **Program 9: Variational Autoencoder (VAE)**
   - Deep learning model for MNIST dataset
   - Implements both encoder and decoder networks
   - Generates new digit images from latent space

Note: Programs 6 and 8 are intentionally omitted from this collection.

## Dependencies

The package requires the following Python packages:
```bash
pip install nltk pandas scikit-learn requests gensim scipy==1.11.4 tensorflow matplotlib numpy
```

### Additional Setup

1. **NLTK Data**: Required for Programs 1-4
   - Downloads automatically when running the programs
   - Includes: punkt, stopwords, wordnet, averaged_perceptron_tagger, maxent_ne_chunker

2. **GloVe Embeddings**: Required for Program 5
   - Downloads automatically on first use (~66MB)
   - Uses the glove-wiki-gigaword-50 model

3. **MNIST Dataset**: Required for Program 9
   - Downloads automatically through TensorFlow
   - Used for training and testing the VAE

## Note on GPU Support

Programs 7 (LSTM) and 9 (VAE) can benefit from GPU acceleration if TensorFlow is installed with CUDA support.

## Error Handling

All programs include proper error handling and will display informative messages if:
- Required data is not available
- Words are not found in vocabulary
- Models fail to load or process 