import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from googleapiclient.discovery import build
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from deep_translator import GoogleTranslator 
import spacy
from tqdm import tqdm
from datetime import datetime
import torch
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
# ==========================================
# 1. CORE ARCHITECTURE
# =========================================
# This finds the folder where the script itself is sitting
basedir = os.path.abspath(os.path.dirname(__file__))
key_path = os.path.join(basedir, "key.env")

# Now it loads it from that specific folder
load_dotenv(key_path)
yt_key = os.getenv("yt_key")

# Initialize the YouTube API
if yt_key:
    youtube = build('youtube', 'v3', developerKey=yt_key)
else:
    print("ERROR: YOUTUBE_API_KEY not found in .env file.")

print("🚀 Deploying The Garrison v6.2 [Deep Harvest & Recovery]...")
nlp = spacy.load("en_core_web_md")
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
translator = GoogleTranslator(source='auto', target='en')

# WE KEEP THESE CONSISTENT TO FEED INTO YOUR ANALYTICS ENGINE
BACKUP_FILE = "INDIA_OVERNIGHT_RAW.csv"
FINAL_OUTPUT = "Master_Garrison_Thesis_Final.csv"

brand_pillars = {
    "Apple": "ecosystem seamless titanium intelligence privacy premium optimization",
    "Samsung": "galaxy ai ultra productivity display zoom multitasking innovative",
    "Vivo": "photography zeiss portrait camera battery speed aesthetic slim",
    "Xiaomi": "leica optics performance speed charging lofic pro-grade value",
    "Oppo": "rugged battery durability charging design find x ultra strength"
}

pillar_vectors = {b: nlp(p) for b, p in brand_pillars.items()}

# ==========================================
# 2. THE DEEP HARVESTER (Increased Depth)
# ==========================================
def deep_harvest(brand, env, fmt, query, seen_set):
    captured = []
    print(f" 🇮🇳 Deep Recovery [{env}]: '{query}'")
    try:
        search_res = youtube.search().list(
            q=query, part="id,snippet", 
            maxResults=12,          # DOUBLED: Searching for more videos per query
            type="video", 
            order="viewCount", 
            regionCode="IN"
        ).execute()

        for item in search_res['items']:
            v_id = item['id']['videoId']
            v_launch = item['snippet']['publishedAt']
            request = youtube.commentThreads().list(part="snippet", videoId=v_id, maxResults=100, textFormat="plainText")
            v_count = 0
            while request and v_count < 100: # INCREASED: Pulling more comments per video
                response = request.execute()
                for c in response['items']:
                    raw_text = c['snippet']['topLevelComment']['snippet']['textDisplay']
                    c_date = c['snippet']['topLevelComment']['snippet']['publishedAt']
                    if raw_text.strip().lower() not in seen_set:
                        seen_set.add(raw_text.strip().lower())
                        captured.append({
                            'Brand': brand, 'Text': raw_text, 'Env': env, 
                            'Format': fmt, 'Comment_Date': c_date, 'Video_Launch': v_launch
                        })
                        v_count += 1
                if 'nextPageToken' in response:
                    request = youtube.commentThreads().list_next(request, response)
                else: break
    except Exception: pass 
    return captured

# ==========================================
# 3. EXPANDED STRATEGIC HARVEST (Target: 24k+)
# ==========================================
all_samples = []
seen_comments = set()

# LOAD PREVIOUS DATA TO AVOID DUPLICATES
if os.path.exists(BACKUP_FILE):
    print(f" LOADING EXISTING DATA TO EXPAND SAMPLES...")
    old_df = pd.read_csv(BACKUP_FILE)
    all_samples = old_df.to_dict('records')
    seen_comments = set(old_df['Text'].str.strip().str.lower().tolist())
    print(f" Loaded {len(all_samples)} existing samples. Target: Add ~12,000 more.")

brands = ["Apple", "Samsung", "Vivo", "Xiaomi", "Oppo"]
for brand in brands:
    print(f"\n---  DEEP RECOVERY: {brand.upper()} ---")
    scenarios = [
        # TIER 1: AMPLIFIED
        {"env": "Amplified", "fmt": "Long-form", "q": f"{brand} India 2026 GeekyRanjit Trakin Tech"},
        # TIER 2: CONTROLLED
        {"env": "Controlled", "fmt": "Long-form", "q": f"{brand} India official features cinematic"},
        # TIER 3: GLOBAL
        {"env": "Global", "fmt": "Long-form", "q": f"{brand} India long term user problems 2026"},
        {"env": "Global", "fmt": "Shorts", "q": f"{brand} 2026 durability drop test India #shorts"},
        # TIER 4: COMPETITIVE (New Tier for extra 12k reach)
        {"env": "Global", "fmt": "Long-form", "q": f"{brand} vs OnePlus vs Nothing India comparison 2026"}
    ]
    for sc in scenarios:
        new_data = deep_harvest(brand, sc['env'], sc['fmt'], sc['q'], seen_comments)
        all_samples.extend(new_data)

df = pd.DataFrame(all_samples)
df.to_csv(BACKUP_FILE, index=False)
print(f" HARVEST COMPLETE. Total Dataset Size: {len(df)} samples.")

# ==========================================
# 4. BLITZKRIEG PARALLEL PROCESSING
# ==========================================
print(f"\n Processing Neural Matrix ({len(df)} samples)...")

def blitz_worker(row_data):
    idx, row = row_data
    # Skip if already processed in the CSV (check for 'Translated' column)
    if 'Translated' in row and pd.notna(row['Translated']):
        return idx, row['MPI'], row['Heat'], row['Translated']
    
    orig = str(row['Text'])
    try:
        time.sleep(0.1) 
        trans = translator.translate(orig) if len(orig) > 12 else orig
        comment_vec = nlp(trans)
        mpi = pillar_vectors[row['Brand']].similarity(comment_vec) if comment_vec.vector_norm else 0
        
        toks = tokenizer(trans, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            out = model(**toks)
        scores = softmax(out[0][0].detach().numpy())
        heat = scores[2] - scores[0]
        
        return idx, mpi, heat, trans
    except Exception:
        return idx, 0, 0, orig

results = [None] * len(df)
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(blitz_worker, (i, row)): i for i, row in df.iterrows()}
    for future in tqdm(as_completed(futures), total=len(df), desc="Blitzkrieg Analysis"):
        i, mpi, heat, trans = future.result()
        results[i] = (mpi, heat, trans)

df[['MPI', 'Heat', 'Translated']] = pd.DataFrame(results, index=df.index)
df.to_csv(FINAL_OUTPUT, index=False)
print(f"\n ALL DATA NEURAL-MAPPED. Ready for Analytics Engine.")