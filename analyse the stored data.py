import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# 1. ARCHITECTURE SETUP
# ==========================================
base_folder = "Garrison_Final_Intelligence_Package"
os.makedirs(base_folder, exist_ok=True)

# LOAD THE FULL DATASET
print("🚀 Loading Master Dataset...")
df = pd.read_csv("Master_Garrison_Thesis_Final.csv")

# ==========================================
#  NEW: 2-TIER RE-CLASSIFICATION 
# ==========================================
# This is the "Controlled vs Uncontrolled" merger
# We map 'Amplified' and 'Global' into 'Uncontrolled'
tier_mapping = {
    'Controlled': 'Controlled',
    'Amplified': 'Uncontrolled',
    'Global': 'Uncontrolled'
}
df['Env'] = df['Env'].map(tier_mapping)
print(" Market re-classified: Controlled vs Uncontrolled")

# PRE-PROCESSING
df['Comment_Date'] = pd.to_datetime(df['Comment_Date'])
df['Video_Launch'] = pd.to_datetime(df['Video_Launch'])
df['Days_Since_Launch'] = (df['Comment_Date'] - df['Video_Launch']).dt.total_seconds() / 86400
df = df[df['Days_Since_Launch'] >= 0]

# ==========================================
# 2. CALCULATION ENGINE: λ (Day) & σ
# ==========================================
def get_metrics(data):
    if len(data) < 5: return 0, 0, 0, 0
    
    try:
        slope, _ = np.polyfit(data['Days_Since_Launch'], data['MPI'], 1)
        lam_day = abs(slope)
    except:
        lam_day = 0
        
    sigma = data['MPI'].std()
    avg_mpi = data['MPI'].mean()
    avg_heat = data['Heat'].mean()
    
    return lam_day, sigma, avg_mpi, avg_heat

# ==========================================
# 3. GLOBAL CONSOLIDATED REPORT
# ==========================================
print("📊 Generating Global Consolidated Report...")
with open(f"{base_folder}/GLOBAL_CONSOLIDATED_SUMMARY.txt", "w", encoding='utf-8') as f:
    f.write("=== GLOBAL MARKET DYNAMICS SUMMARY (2-TIER MODEL) ===\n\n")
    
    tier_stats = df.groupby('Env').agg({'MPI': ['mean', 'std'], 'Heat': 'mean'})
    f.write("--- CONTROLLED VS UNCONTROLLED PERFORMANCE ---\n")
    f.write(tier_stats.to_string() + "\n\n")
    
    format_stats = df.groupby(['Format', 'Env']).agg({'MPI': 'mean', 'Heat': 'mean'})
    f.write("--- FORMAT DYNAMICS: VIDEO VS SHORTS ---\n")
    f.write(format_stats.to_string() + "\n")

# ==========================================
# 4. BRAND-SPECIFIC PARTITIONING
# ==========================================
sns.set_theme(style="whitegrid")

for brand in df['Brand'].unique():
    print(f"🏗️ Architecting Folder: {brand.upper()}")
    brand_path = os.path.join(base_folder, brand)
    os.makedirs(brand_path, exist_ok=True)
    
    b_df = df[df['Brand'] == brand]
    
    b_df.to_csv(f"{brand_path}/{brand}_Clean_Data.csv", index=False)
    
    with open(f"{brand_path}/{brand}_Numeric_Report.txt", "w", encoding='utf-8') as f:
        f.write(f"=== {brand.upper()} BRAND INTELLIGENCE (2-TIER) ===\n")
        f.write(f"Total Samples: {len(b_df)}\n\n")
        
        for env in ['Controlled', 'Uncontrolled']:
            env_df = b_df[b_df['Env'] == env]
            if not env_df.empty:
                lam, sig, mpi, heat = get_metrics(env_df)
                
                f.write(f"Tier: {env:<12}\n")
                f.write(f"  - λ (Decay/Day):  {lam:.6f}\n")
                f.write(f"  - σ (Randomness): {sig:.4f}\n")
                f.write(f"  - Avg MPI:        {mpi:.4f}\n")
                f.write(f"  - Avg Heat:       {heat:.4f}\n")
                f.write(f"  - Sample Count:   {len(env_df)}\n\n")

    # C. Brand Visualization 1: Decay Path (Only 2 lines now)
    plt.figure(figsize=(10, 6))
    for env in ['Controlled', 'Uncontrolled']:
        subset = b_df[b_df['Env'] == env]
        if not subset.empty:
            sns.regplot(data=subset, x='Days_Since_Launch', y='MPI', scatter=False, label=f"{env} Decay")
    plt.title(f"{brand}: Signal Erosion Path (Controlled vs Uncontrolled)")
    plt.xlabel("Days Post-Launch")
    plt.ylabel("Message Penetration (MPI)")
    plt.legend()
    plt.savefig(f"{brand_path}/{brand}_Decay_Gradient.png")
    plt.close()

    # D. Brand Visualization 2: Market Map (Scatter)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=b_df, x='MPI', y='Heat', hue='Env', alpha=0.4, palette={'Controlled': 'red', 'Uncontrolled': 'blue'})
    plt.title(f"{brand}: Sentiment-Saliency Market Map")
    plt.axhline(0, color='black', linestyle='--', alpha=0.5)
    plt.savefig(f"{brand_path}/{brand}_Market_Map.png")
    plt.close()

print(f"\n ALL DATA PARTITIONED. Package ready in: {base_folder}")