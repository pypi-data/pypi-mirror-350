import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import pandas as pd
import numpy as np
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from sklearn.feature_extraction.text import TfidfVectorizer

def p1():
    print('''
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import download

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
text = "Mumbai is the financial capital of India. It is known for Bollywood and its street food. I love going there"

sent = sent_tokenize(text)
print(sent)

tokens = word_tokenize(text)
print(f"Tokens: {tokens}")

stop_words = set(stopwords.words('english'))
len(stop_words)
filtered_words = []
for word in tokens:
    if word.lower() not in  stop_words:
        filtered_words.append(word)
        
print("Filtered Words i.e. No stop words: ",filtered_words)

stemmer = PorterStemmer()
stemmed_tokens = []
for word in filtered_words:
    stemmed_tokens.append(stemmer.stem(word))

print("Stemmed Words: ", stemmed_tokens)

lemmatizer = WordNetLemmatizer()
lemmatized_tokens = []
for word in filtered_words:
    lemmatized_tokens.append(lemmatizer.lemmatize(word))
print("Lemmatized : ", lemmatized_tokens)
    ''')

    

def p2():
    print('''
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

text = "NLTK is a powerful library for a natural language processing."

word = word_tokenize(text)
pos = pos_tag(word)

print("Original Text: ",text)
print("Pos Tagging: ")
for word, tag in pos:
print(word,":",tag)


from nltk.chunk import ne_chunk
text2 = "Apple Inc. is planning to open a new headquarters in Austin, Texas. CEO Tim Cook announced the plan along with Harry Potter"

word  = word_tokenize(text2)
pos = pos_tag(word)
chunk = ne_chunk(pos)

print("Original Text: ",text2)
print("Named Entity Recognition: ")
print(chunk)
''')

def p3():
    print(''' 
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

corpus=['data science is one of the most important fields of science','this is one of the best data science course',
        'data scientists analyze data']

model = TfidfVectorizer()
vector = model.fit_transform(corpus)
print(type(vector), vector.shape)
array_v = vector.toarray()
word_set = model.get_feature_names_out()
print(word_set)
df_tf_idf = pd.DataFrame(array_v, columns = word_set)
print(df_tf_idf)
''')
    
def p4():
    print(''' 
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
def gen_ngrms(text,n):
    tokens=word_tokenize(text.lower())
    return list(ngrams(tokens,n))

def main():
        text = "Artificial Intelligence and Machine Learning are revolutionizing many industries, including healthcare and finance."
        uni = gen_ngrms(text,1)
        bi = gen_ngrms(text,2)
        tri = gen_ngrms(text,3)
        print("\nUnigrams: ",uni)
        print("\nBigrams:",bi)
        print("\nTrigrams:",tri)

if __name__=="__main__":
    main()
        ''')
    
    
def p6():
    print('''
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
transform = transforms.ToTensor()
loader = DataLoader(datasets.MNIST('./data', train=True, download=True, transform=transform),
                    batch_size=128, shuffle=True)

class VAE(nn.Module):
    def __init__(self):
        super().__init__()
        self.enc = nn.Sequential(nn.Flatten(), nn.Linear(784, 256), nn.ReLU())
        self.mu = nn.Linear(256, 20)
        self.logvar = nn.Linear(256, 20)
        self.dec = nn.Sequential(nn.Linear(20, 256), nn.ReLU(), nn.Linear(256, 784), nn.Sigmoid())

    def forward(self, x):
        h = self.enc(x)
        mu, logvar = self.mu(h), self.logvar(h)
        z = mu + torch.exp(0.5 * logvar) * torch.randn_like(logvar)
        return self.dec(z), mu, logvar

def loss_fn(recon, x, mu, logvar):
    BCE = nn.functional.binary_cross_entropy(recon, x.view(-1, 784), reduction='sum')
    KLD = -0.5 * torch.sum(1 + logvar - mu**2 - logvar.exp())
    return BCE + KLD

model = VAE().to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(10):
    for x, _ in loader:
        x = x.to(device)
        recon, mu, logvar = model(x)
        loss = loss_fn(recon, x, mu, logvar)/100
        opt.zero_grad(); loss.backward(); opt.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item():.2f}')

with torch.no_grad():
    z = torch.randn(16, 20).to(device)
    samples = model.dec(z).view(-1, 1, 28, 28).cpu()

plt.figure(figsize=(12, 2))
grid = torch.cat([s.squeeze() for s in samples],dim=1)
plt.imshow(grid.numpy(), cmap='gray')
plt.axis('off')
plt.title("Generated Digits")
plt.show()
        ''')
    
    
def p7():
    print('''
from transformers import (
    GPT2Tokenizer, GPT2LMHeadModel,
    Trainer, TrainingArguments,
    TextDataset, DataCollatorForLanguageModeling
)
import torch, os
from huggingface_hub import login

login("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")

os.environ["WANDB_DISABLED"] = "true"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token 
model.resize_token_embeddings(len(tokenizer))
model.config.pad_token_id = tokenizer.pad_token_id

def load_dataset(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        raise ValueError(f"Invalid or empty dataset: {path}")
    return TextDataset(tokenizer=tokenizer, file_path=path, block_size=64)

train_path = "/content/domain_train.txt"
eval_path = "/content/domain_eval.txt"

train_dataset = load_dataset(train_path)
try:
    eval_dataset = load_dataset(eval_path)
except:
    eval_dataset = None

collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="./gpt2-finetuned",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    logging_steps=10,
    save_steps=500,
    eval_strategy="epoch" if eval_dataset else "no",
    save_total_limit=2,
    fp16=torch.cuda.is_available()
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=collator,
)

trainer.train()
trainer.save_model("./gpt2-finetuned")

def generate_text(prompt, max_len=100):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(
        **inputs,
        max_length=max_len,
        do_sample=True,
        top_k=50,
        pad_token_id=tokenizer.pad_token_id
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)

print("Generated text:\n", generate_text("In quantum computing,"))

        ''')


def p8():
    print('''
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
import fitz

def load_text(path):
    try:
        with fitz.open(path) as doc:
            return "".join([page.get_text() for page in doc]).lower()
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return ""

text = load_text("Alice_in_Wonderland.pdf")

PAD = '<PAD>'
chars = [PAD] + sorted(set(text))
char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for ch, i in char_to_idx.items()}
vocab_size = len(chars)

seq_len = 40
step = 3
X, y = [], []

for i in range(0, len(text) - seq_len, step):
    X.append([char_to_idx.get(c, 0) for c in text[i:i+seq_len]])
    y.append(char_to_idx.get(text[i + seq_len], 0))

if X:
    X = np.array(X)
    y = to_categorical(y, num_classes=vocab_size)
else:
    print("Text too short to create training sequences.")
    exit()

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=50, input_length=seq_len),
    LSTM(128),
    Dense(vocab_size, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer=Adam(0.001))

model.fit(X, y, batch_size=64, epochs=10, validation_split=0.2)

def sample(preds, temp=1.0):
    preds = np.log(preds + 1e-8) / temp
    preds = np.exp(preds) / np.sum(np.exp(preds))
    return np.random.choice(len(preds), p=preds)

def generate(seed, length=300, temp=0.7):
    generated = seed
    input_seq = [char_to_idx.get(c, 0) for c in seed[-seq_len:]]
    input_seq = [0]*(seq_len - len(input_seq)) + input_seq

    for _ in range(length):
        x = np.array([input_seq])
        preds = model.predict(x, verbose=0)[0]
        next_idx = sample(preds, temp)
        next_char = idx_to_char[next_idx]
        generated += next_char
        input_seq.append(next_idx)
        input_seq = input_seq[-seq_len:]

    return generated

seed_text = "alice was beginning to get very tired"
print(generate(seed_text))

          ''')