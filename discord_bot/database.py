import os
from pymongo import MongoClient
from dotenv.main import load_dotenv


def get_database():
    load_dotenv('discord_bot\secrets.env')
    TOKEN = os.environ["MONGO_DB_PWD"]

    uri = f"mongodb+srv://alex:{TOKEN}@shakespearesvocabualry.qrdewhn.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client["vocab_database"]
    

if __name__ == "__main__":
    dbname = get_database()