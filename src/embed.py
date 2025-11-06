from dotenv import load_dotenv
load_dotenv()
import requests
import json
import os
import numpy as np

def get_embeddings(texts: list[str]) -> np.array:
  models = [
     "qwen/qwen3-embedding-8b",
  ]
  response = requests.post(
    url="https://openrouter.ai/api/v1/embeddings",
    headers={
      "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
      "Content-Type": "application/json",
    },
    data=json.dumps({
      "model": models[0],
      "input": texts,
      "encoding_format": "float"
    })
  )
  if response.status_code != 200:
      raise ValueError(f"Error getting embeddings: {response.text}")
  obj = response.json()
  #print(obj)
  obj_arr = np.array([item["embedding"] for item in obj["data"]])
  return obj_arr
