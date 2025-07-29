import time
import pandas as pd
from sklearn.model_selection import train_test_split
from xplainable.core.models import XClassifier
import numpy as np
from xplainable_client import Client


np.set_printoptions(edgeitems=30, linewidth=1000)

print("connecting to client")
client = Client(
    # hostname="https://xplainable-api-uat-itdcj.ondigitalocean.app/",
    hostname="http://127.0.0.1:8000",
    api_key="55a506e7-07cd-4bc5-9a2c-5cb6d27b1c05"
)
print("connected to client")



df = pd.read_csv('telco_customer_churn.csv')

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna()


x, y = df.drop('Churn', axis=1), df['Churn']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

model = XClassifier(
    ignore_nan=False
    # **params
)
start = time.time()
model.fit(X_train, y_train, id_columns=["customerID"])
# print(model.evaluate(X_test, y_test))
print(time.time() - start)



# eval_dict = model.evaluate(X_test, y_test)
# model.explain()
# print(eval_dict["classification_report"]['0'])
# print(eval_dict["classification_report"]['1'])

# Saving the model goes here, this following is the old way to do it, not sure if thats still correct
content = client.create_model(
    model_name="CleintTestGonnaNek",
    model_description="Testing",
    model=model,
    x=X_train,
    y=y_train
)
print(content)

# model_id = client.create_model_id(model, model_name="RickTestAPI", model_description="Testing")
# version_id = client.create_model_version(model, model_id, X_train, y_train)
# print(model_id, version_id)
