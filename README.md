Indian Smartphone Market: Narrative Signal Erosion & The Garrison Model

This repository contains the data pipeline and analytical framework for quantifying marketing narrative decay across tiered markets in India. Using the **Garrison Model**, this project measures how brand messages fluctuate in penetration and sentiment as they move from controlled environments to organic consumer discourse.

Project Overview
In the highly competitive Indian smartphone sector, brand narratives often face "signal erosion"—a loss of message clarity and sentiment strength as information spreads. This project utilizes Python and Natural Language Processing (NLP) to audit thousands of data points across major brands including **Apple, Samsung, Vivo, Xiaomi, and Oppo.**

Key Metrics
Message Penetration Index (MPI):A quantitative measure of how effectively a specific brand narrative has reached the target audience.
Heat (Sentiment Analysis):Utilizing RoBERTa-based transformers to calculate the emotional intensity and polarity of consumer responses.
Environmental Tiers:Analysis is segmented into Controlled, Amplified, and Global environments to track decay.

Technical Stack
Language: Python 3.x
Data Acquisition: YouTube Data API v3
NLP Engine: Spacy & HuggingFace Transformers (RoBERTa)
Data Management: Pandas & NumPy
Visualization: Power BI (Integration via GitHub Raw Data)

Repository Structure
3 tier analysis od decay.py: The primary engine for harvesting and processing signal data.
analyse the stored data.py: Analytical script for calculating MPI and Heat distributions.
Master_Garrison_Thesis_Final.csv: The core dataset containing ~48,000 processed samples.
Garrison_Final_Intelligence_Package/: Segmented clean data for specific brand deep-dives.

Setup and Usage
1.  Clone the repository:
    bash
    git clone https://github.com/neeladrisanphui1234-cpu/Indian_Smartphone_Market_Signal_Erosion.git
    
2.  Install dependencies:
    bash
    pip install -r requirements.txt
    
3.  API Configuration:
    Create a `key.env` file in the root directory and add your YouTube API Key:
    text
    yt_key=your_api_key_here
    
4.  Run the Analysis:
    bash
    python "3 tier analysis od decay.py"
    

Research Context
This project is part of a Master of Business Analytics thesis focusing on the intersection of Big Data and Strategic Marketing in emerging economies.

Author:Neeladri Sanphui  
Specialization:Business Analytics  
Framework:The Garrison Model of Signal Erosion
