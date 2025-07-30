p1='''
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
# Download required resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# Input text
text = "Natural language processing (NLP) is a field of computer science"
# Tokenize
word_tokens = word_tokenize(text)
print("Tokens:", word_tokens)
# Stopword removal (with lowercase)
stop_words = set(stopwords.words('english'))
filtered_sentence = [w for w in word_tokens if w.lower() not in stop_words]
print("Filtered (lowercase):", filtered_sentence)
# Stopword removal (without lowercase conversion)
filtered_sentence_no_lower = [w for w in word_tokens if w not in stop_words]
print("Filtered (no lowercase):", filtered_sentence_no_lower)
# Stemming
ps = PorterStemmer()
print("Stemming:")
for w in word_tokens:
    print(w, ":", ps.stem(w))
# Lemmatization
lemmatizer = WordNetLemmatizer()
print("Lemmatization:")
print("rocks :", lemmatizer.lemmatize("rocks"))
print("corpora :", lemmatizer.lemmatize("corpora"))
print("better (adj) :", lemmatizer.lemmatize("better", pos="a"))'''

p2='''
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
# Input sentence
sentence = "Apple is looking at buying U.K. startup for $1 billion."
# Tokenize and POS tagging
tokens = word_tokenize(sentence)
pos_tags = pos_tag(tokens)
print("POS Tags:", pos_tags)
# Named Entity Recognition (NER)
chunked = ne_chunk(pos_tags)
print("Named Entity Chunking:")
print(chunked)'''

p3='''
from sklearn.feature_extraction.text importTfidfVectorizer
import pandas as pd
import numpy as np
corpus = ['data science is one of the most important fields of science',
 'this is one of the best data science courses',
'data scientists analyze data' ]tr_idf_model = TfidfVectorizer()
tf_idf_vector = tr_idf_model.fit_transform(corpus)print(type(tf_idf_vector), tf_idf_vector.shape)tf_idf_array = tf_idf_vector.toarray()
# Use get_feature_names_out() instead of get_feature_names()
words_set = tr_idf_model.get_feature_names_out()print(words_set)
df_tf_idf = pd.DataFrame(tf_idf_array, columns = words_set)
df_tf_idf
'''

p4='''
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
# Download the necessary NLTK resources
nltk.download('punkt')
def generate_ngrams(text, n):
    """Generate n-grams from the given text."""
    tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    return list(ngrams(tokens, n))
def main():
    file_path = "/content/drive/MyDrive/Colab Notebooks/Brown_train.txt"  # Change this to your file path
    try:
        with open(file_path, 'r', encoding='utf8') as file:
            text = file.read()
        unigrams = generate_ngrams(text, 1)
        bigrams = generate_ngrams(text, 2)
        trigrams = generate_ngrams(text, 3)
        print("Unigrams:", unigrams)
        print("Bigrams:", bigrams)
        print("Trigrams:", trigrams)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
if __name__ == "__main__":
    main()'''
    
p6='''
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
    def __init__(self, latent_dim):
        super(VAE, self).__init__()
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

# Model and optimizer
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
    
    print(f'Epoch [{epoch+1}/{epochs}], Loss: {train_loss / len(train_loader.dataset):.4f}')

# Generate samples
model.eval()
with torch.no_grad():
    z = torch.randn(64, latent_dim).to(device)
    sample = model.decode(z).cpu()
    sample = sample.view(64, 1, 28, 28)

    # Plot generated samples
    grid_img = utils.make_grid(sample, nrow=8)
    plt.figure(figsize=(8, 8))
    plt.imshow(grid_img.permute(1, 2, 0))
    plt.axis('off')
    plt.title('Generated Images from VAE')
    plt.show()'''
    
p7='''
from transformers import (
 GPT2Tokenizer, GPT2LMHeadModel,
 Trainer, TrainingArguments,
 TextDataset, DataCollatorForLanguageModeling)
from huggingface_hub import login
import torch, os
# Login and disable wandb
login("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")os.environ["WANDB_DISABLED"] = "true"
# Load tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")tokenizer.pad_token = tokenizer.eos_tokenmodel.resize_token_embeddings(len(tokenizer))model.config.pad_token_id = tokenizer.pad_token_id# Load dataset utility
def load_dataset(path, tokenizer, block_size=64): if not os.path.exists(path) or
os.path.getsize(path) == 0:
 raise ValueError(f"Invalid dataset: {path}")
 return TextDataset(tokenizer=tokenizer, file_path=path, block_size=block_size)
# Load training and optional eval datasetstry:
 train_dataset =
load_dataset("/content/domain_train.txt", tokenizer)
except Exception as e:
 print(e); exit()
try:
 eval_dataset =
load_dataset("/content/domain_eval.txt", tokenizer)
except Exception as e:
 print(f"Eval warning: {e}")
 eval_dataset = None
# Data collator
collator =
DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
# Training arguments
args = TrainingArguments(
	output_dir="./gpt2-domain-finetuned", overwrite_output_dir=True,
 per_device_train_batch_size=2,
 per_device_eval_batch_size=2,
 num_train_epochs=3,
 logging_steps=10,
 save_steps=500,
 eval_strategy="epoch" if eval_dataset else"no",
 save_total_limit=2,
 fp16=torch.cuda.is_available()
)
# Trainer
trainer = Trainer(
 model=model,
 args=args,
 train_dataset=train_dataset,
 eval_dataset=eval_dataset,
 data_collator=collator,
)
print(f"Training on {len(train_dataset)}samples...")
trainer.train()
trainer.save_model()
# Text generation
def generate_text(prompt, max_len=100):
 inputs = tokenizer(prompt,
return_tensors="pt").to(model.device)
 output = model.generate(
 **inputs, max_length=max_len,
do_sample=True,
 top_k=50,
pad_token_id=tokenizer.eos_token_id
 )
	return tokenizer.decode(output[0],
skip_special_tokens=True)
# Example
print("Generated text:\n", generate_text("In quantum computing,"))'''

p8='''
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam 
!pip install pymupdf
import fitz  # PyMuPDF

# 1. Load and clean text from PDF
def load_text(pdf_path):
    with fitz.open(pdf_path) as doc:
        return "".join(page.get_text() for page in doc).lower()

text = load_text("Alice_in_Wonderland.pdf")

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
    Embedding(vocab_size, 50, input_length=seq_len),
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
print(generate_text("alice was beginning to get very tired", length=300, temp=0.7))'''