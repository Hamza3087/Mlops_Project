import pandas as pd

def preprocess_data():
    df = pd.read_csv("raw_data.csv")
    
    # Handle missing values
    df.fillna(method="ffill", inplace=True)
    
    # Normalize numerical fields
    df["Temperature"] = (df["Temperature"] - df["Temperature"].min()) / (df["Temperature"].max() - df["Temperature"].min())
    df["Wind Speed"] = (df["Wind Speed"] - df["Wind Speed"].min()) / (df["Wind Speed"].max() - df["Wind Speed"].min())
    
    # Save preprocessed data
    df.to_csv("processed_data.csv", index=False)
    print("Preprocessed data saved to processed_data.csv")

if __name__ == "__main__":
    preprocess_data()
