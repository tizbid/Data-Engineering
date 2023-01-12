import configparser
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


# Import credentials
config = configparser.ConfigParser()
#Read configuration
config.read('config.ini')
language_key = config['language']['key']
language_endpoint = config['language']['endpoint']



def sentiment_analysis_df(csv_path:str):
    
    # Initialize the client with an API key
    credential = AzureKeyCredential(language_key)
    client = TextAnalyticsClient(endpoint=language_endpoint,credential=credential)

    # Read dataframe
    df = pd.read_csv(csv_path)
    # Create a new column to store the sentiment scores
    df["sentiment_score"] = None

    # Iterate over the rows of the DataFrame#
    for i, row in df.iterrows():  
        text = [row['twit']]
        # Perform sentiment analysis
        response = client.analyze_sentiment(text)

        # Extract the sentiment score and store it in the new column
        sentiment_score = response[0].sentiment
        df.at[i, "sentiment_score"] = sentiment_score
    
    df.to_csv('Sentiment-Analysis/SA_df.csv',index=False)
    
    return 



