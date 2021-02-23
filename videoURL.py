import pandas as pd
import random

#CSV ROWS = 11210

def videoURL():
    df = pd.read_csv("Youtube Video Dataset.csv")
    urls = df["Videourl"]
    url = urls[random.randint(0,11210)]
    return "https://www.youtube.com" + url
