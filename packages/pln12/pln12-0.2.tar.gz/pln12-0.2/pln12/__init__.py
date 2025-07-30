p1='''import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')
text1 = "Mumbai is the financial capital of India. It is known for Bollywood and its street food. I love going there"
text2 = "The Taj Mahal is located in Agra. It was built by Emperor Shah Jahan in memory of his wife."
sentences1 = sent_tokenize(text1)
sentences2 = sent_tokenize(text2)
sentences1
words1 = word_tokenize(text1)
words2 = word_tokenize(text2)
words1
#stopword removal
stop_words = set(stopwords.words('english'))
len(stop_words)
filtered_words1 = []
for word in words1:
    if word.lower() not in stop_words:
        filtered_words1.append(word)
filtered_words1
#stemming
stemmer = PorterStemmer()
stemmed_words1 = []
for word in filtered_words1:
    stemmed_words1.append(stemmer.stem(word))
stemmed_words1
#lematization
lemmatizer = WordNetLemmatizer()
lemmatized_words1 = []
for word in filtered_words1:
    lemmatized_words1.append(lemmatizer.lemmatize(word))
lemmatized_words1'''

p2='''
!pip install svgling
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
text = """Apple Inc. is planning to open a new headquarters in Austin, Texas.
CEO Tim Cook announced the plan along with Harry Potter"""
text2 = "Harry Potter, goes to Hogwarts"
tokens = word_tokenize(text)
tokens
pos_tags = pos_tag(tokens)
pos_tags
ne_tree = ne_chunk(pos_tags)
ne_tree
bio_tags = tree2conlltags(ne_tree)
bio_tags
entities = []
current_entity = []
current_type = None
for word, pos, tag in bio_tags:
    if tag.startswith('B-'):  # Beginning of entity
        # First handle any existing entity we were building
        if current_entity:
            entities.append((' '.join(current_entity), current_type))
        # Start a new entity
        current_entity = [word]
        current_type = tag[2:]
    elif tag.startswith('I-'):  # Inside entity
        # Only append if we're already building an entity of matching type
        if current_entity and current_type == tag[2:]:
            current_entity.append(word)
        # If we get an I- without a preceding B-, it's an error in the tagging
        # But we can handle it by treating it as a B-
        elif not current_entity:
            current_entity = [word]
            current_type = tag[2:]
    else:  # Outside entity (O tag)
        # Finish any entity we were building
        if current_entity:
            entities.append((' '.join(current_entity), current_type))
            current_entity = []
            current_type = None

# Don't forget to add the last entity if we end on an entity
if current_entity:
    entities.append((' '.join(current_entity), current_type))

entities'''

p3='''
import math
from collections import Counter
import pandas as pd
from nltk.tokenize import word_tokenize
import nltknltk

# Download tokenizer models
nltk.download('punkt')

documents = [
    "This movie was fantastic and I loved every minute of it",
    "The acting was terrible and the plot made no sense",
    "Great special effects but the story was predictable",
    "I fell asleep during this boring movie",
    "The soundtrack was amazing and the cinematography stunning"
]

# Tokenize documents (lowercase)
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

# Calculate TF-IDF for each document
tfidf_docs = []
for i, tf in enumerate(term_freq):
    tfidf = {word: tf_val * idf[word] for word, tf_val in tf.items()}
    tfidf_docs.append(tfidf)

print("\nTF-IDF Scores:")
for i, tfidf in enumerate(tfidf_docs):
    print(f"Document {i+1}: {tfidf}")

# Compare with sklearn's TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

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
    print(present_words.sort_values(ascending=False))

'''

p4='''
import requests
import string
import re
import nltk
from nltk.util import ngrams
from collections import Counter
nltk.download('punkt_tab')
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

url = "https://www.gutenberg.org/files/1342/1342-0.txt"
response = requests.get(url)
text = response.text

main_text = text.lower()
tokens = nltk.word_tokenize(main_text)

cleaned_tokens = []
for token in tokens:
    cleaned_token = re.sub(r'[^\w\s]', '', token)
    if cleaned_token and not cleaned_token.isdigit():
        cleaned_tokens.append(cleaned_token)

unigrams = cleaned_tokens
bigrams = list(ngrams(cleaned_tokens, 2))
trigrams = list(ngrams(cleaned_tokens, 3))

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
    print(f"{item}: {count}")'''
    
p6='''
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

(x_train, _), _ = keras.datasets.mnist.load_data()
x_train = x_train.astype("float32") / 255.0
x_train = np.expand_dims(x_train, -1)

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

train_dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(60000).batch(batch_size)

for epoch in range(epochs):
    total_loss = 0
    for batch in train_dataset:
        total_loss += train_step(batch)
    print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_dataset):.4f}")

# Generate new images
z_samples = np.random.normal(size=(16, latent_dim))
generated_images = decoder.predict(z_samples)

fig, axes = plt.subplots(4, 4, figsize=(5, 5))
for i, ax in enumerate(axes.flat):
    ax.imshow(generated_images[i].squeeze(), cmap='gray')
    ax.axis('off')
plt.show()
'''
p7='''
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
import torch
import os
from huggingface_hub import login
login("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")
import os
os.environ["WANDB_DISABLED"] = "true"


# 1. Load tokenizer and model
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Resize embeddings if tokenizer was updated (optional)
model.resize_token_embeddings(len(tokenizer))

# 2. Load and preprocess domain-specific dataset
def load_dataset(file_path, tokenizer, block_size=64):
    # Add a check for file existence and content
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The dataset file was not found at: {file_path}")
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"The dataset file is empty: {file_path}")

    # TextDataset loads the file and processes it.
    # Its __len__ method will return the number of samples (tokenized blocks).
    # It expects the tokenizer to have an eos_token or pad_token defined.
    # Let's ensure the tokenizer has one of these before creating the dataset.
    if tokenizer.eos_token is None and tokenizer.pad_token is None:
        # Set eos_token if not present, as TextDataset often relies on it.
        # GPT2 tokenizer usually has eos_token_id = 50256
        tokenizer.eos_token = tokenizer.convert_ids_to_tokens(tokenizer.eos_token_id)
        model.config.eos_token_id = tokenizer.eos_token_id # Ensure model config is aligned


    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size
    )

# Sample domain-specific dataset (plain text file)
train_path = "/content/domain_train.txt"  # Replace with your file
eval_path = "/content/domain_eval.txt"    # Replace with your file

# Ensure the training file exists and is not empty before loading
train_dataset = None # Initialize train_dataset
try:
    train_dataset = load_dataset(train_path, tokenizer)
    # Debugging: Print the size of the loaded dataset
    print(f"Training dataset size after loading: {len(train_dataset)}")
except (FileNotFoundError, ValueError) as e:
    print(f"Error loading training dataset: {e}")
    # You might want to exit or handle this case appropriately
    exit() # Exit the script if the training data is not valid

# Add a check here to ensure the dataset is not empty before proceeding
if train_dataset is None or len(train_dataset) == 0:
    print("Error: Training dataset is empty or failed to load. Please check the content of your training file and ensure it has enough text for at least one block (approx 128 tokens).")
    exit()


eval_dataset = None # Initialize eval_dataset
try:
    eval_dataset = load_dataset(eval_path, tokenizer)
    # Debugging: Print the size of the loaded dataset
    print(f"Evaluation dataset size after loading: {len(eval_dataset)}")
except (FileNotFoundError, ValueError) as e:
    print(f"Warning: Error loading evaluation dataset: {e}")
    # Continue if eval data is not essential for your current run
    eval_dataset = None # Ensure eval_dataset is None if loading failed


# 3. Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # Set True for BERT-style masked LM
)

# 4. Training configuration
training_args = TrainingArguments(
    output_dir="./gpt2-domain-finetuned",
    overwrite_output_dir=True,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    logging_steps=10,
    save_steps=500,
    eval_strategy="epoch" if eval_dataset else "no", # Set eval_strategy based on if eval_dataset was loaded
    save_total_limit=2,
    fp16=torch.cuda.is_available()
)

# 5. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset, # eval_dataset can be None if you skip evaluation
    data_collator=data_collator,
)

# Add one more print statement before training to confirm dataset size
print(f"Training dataset size just before trainer.train(): {len(train_dataset)}")

# 6. Fine-tune the model
# This will now run if train_dataset has a positive size
trainer.train()

# 7. Save the fine-tuned model
trainer.save_model("./gpt2-domain-finetuned")

# 8. Generate text to evaluate
def generate_text(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    # You might need to set pad_token_id for generation with some models/tokenizers
    if tokenizer.pad_token_id is None:
         tokenizer.pad_token_id = tokenizer.eos_token_id
         model.config.pad_token_id = model.config.eos_token_id

    output = model.generate(**inputs, max_length=max_length, do_sample=True, top_k=50)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Example use
prompt = "In quantum computing,"
print("Generated text:\n", generate_text(prompt))

'''

p8='''
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
import fitz  # PyMuPDF

# 1. Load and clean text from PDF
def load_text(pdf_path):
    with fitz.open(pdf_path) as doc:
        return "".join(page.get_text() for page in doc).lower()

text = load_text("/content/Alice_in_Wonderland.pdf")

# 2. Create vocabulary
PAD = '<PAD>'
chars = [PAD] + sorted(set(text))
char_to_idx = {c: i for i, c in enumerate(chars)}
idx_to_char = {i: c for c, i in char_to_idx.items()}
vocab_size = len(chars)

# 3. Prepare sequences
seq_len, step = 40, 3
X = [[char_to_idx[c] for c in text[i:i+seq_len]] for i in range(0, len(text) - seq_len, step)]
y = [char_to_idx[text[i + seq_len]] for i in range(0, len(text) - seq_len, step)]
X, y = np.array(X), to_categorical(y, num_classes=vocab_size)

# 4. Build and train model
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=50, input_length=seq_len),
    LSTM(128),
    Dense(vocab_size, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer=Adam(0.001))

model.fit(X, y, batch_size=64, epochs=10, validation_split=0.2)

# 5. Sample and generate text
def sample(preds, temp=1.0):
    preds = np.log(np.asarray(preds) + 1e-8) / temp
    preds = np.exp(preds) / np.sum(np.exp(preds))
    return np.random.choice(len(preds), p=preds)

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

# 6. Example generation
print(generate_text("alice was beginning to get very tired", length=300, temp=0.7))
'''