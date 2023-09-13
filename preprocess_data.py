import pandas as pd

#this function removes '�' from the dataset and replaces it with an empty string
def remove_unknown_chars(data):
    data = data.map(lambda text: str(text).replace('�', ''))
    data = data.map(lambda text : str(text).strip())
    print(data.head(20))

    return data

df = pd.read_csv('shakespeare_and_translation_original_data.csv')
print(df.head(20))
print("HELLO WORLD \n\n")
df = remove_unknown_chars(df)
