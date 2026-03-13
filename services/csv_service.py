import pandas as pd
from repositories.customer_repository import insert_customer

def import_csv(file):

    df = pd.read_csv(file)

    for i,row in df.iterrows():

        insert_customer(
            row["name"],
            row["city"]
        )