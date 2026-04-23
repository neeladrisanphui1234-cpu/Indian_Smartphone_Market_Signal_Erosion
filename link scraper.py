import pandas as pd
from googleapiclient.discovery import build

# Setup
yt_key = "AIzaSyBnzyQVkttz4qO-mBWWu6e7EiuStForfkg" 
youtube = build('youtube', 'v3', developerKey=yt_key)
brands = ["Apple", "Samsung", "Vivo", "Xiaomi", "Oppo"]

print("🔗 Extracting Video Evidence Registry for April 2026...")

evidence_data = []

for brand in brands:
    # This matches the search logic in your main script
    query = f"{brand} India 2026 GeekyRanjit Trakin Tech official honest review"
    search_res = youtube.search().list(q=query, part="id,snippet", maxResults=10, type="video", order="viewCount", regionCode="IN").execute()
    
    for item in search_res['items']:
        evidence_data.append({
            'Brand': brand,
            'Video_Title': item['snippet']['title'],
            'Video_Link': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            'Channel': item['snippet']['channelTitle'],
            'Launch_Date': item['snippet']['publishedAt']
        })

# Save as a separate file for your Thesis Appendix
evidence_df = pd.DataFrame(evidence_data)
evidence_df.to_csv("Garrison_Video_Source_Appendix.csv", index=False)
print("\n✅ Evidence Appendix created: Garrison_Video_Source_Appendix.csv")