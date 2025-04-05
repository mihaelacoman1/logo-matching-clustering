import tensorflow as tf
import numpy as np
import requests
from io import BytesIO
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.cluster import KMeans

__all__ = ["Clusterer"]

class Clusterer:

  def __init__(self):
    self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    self.downloaded_logos_rate = 0
    self.clustered_logos = {} 

  def get_embedding(self, img_url, name):
    """
    Get the embedding for a given image.
        
    Args:
      img_url (string): The url to the image.
      name (string): The name of the image.
    
    Returns:
      embedding (numpy array): The embedding for the image.
    """
    response = requests.get(img_url)
    if response.status_code != 200:
      raise Exception("Invalid URL.")
    img = image.load_img(BytesIO(response.content), target_size=(224, 224))
    if img == None:
      raise Exception("Failed to download logo.")
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    embedding = self.model.predict(img_array)

    return name, embedding.flatten()

  def cluster_logos(self, logos):
    """
    Cluster the logos in the clustered_logos field of this object.
        
    Args:
      logos (list): A list of tuples of form (website url, logo url).
    """
    downloaded_logos = 0
    names = []
    embeddings = []
    image_urls = []

    for name, img_url in logos:
      try:
        name, embedding = self.get_embedding(img_url, name)
        names.append(name)
        embeddings.append(embedding)
        image_urls.append(img_url)
        downloaded_logos += 1
      except:
        pass

    self.downloaded_logos_rate = downloaded_logos / len(logos)

    embeddings = np.array(embeddings)

    kmeans = KMeans(n_clusters=int(len(logos)/4 + 1))
    labels = kmeans.fit_predict(embeddings)

    for label, name, image_url in zip(labels, names, image_urls):
        if label not in self.clustered_logos:
            self.clustered_logos[label] = []
        self.clustered_logos[label].append((name, image_url))

  def print_clusters(self):
      output = []
      for cluster, logo_data in self.clustered_logos.items():
          output.append(f"Cluster {cluster}:")
          for name, image_url in logo_data:
              output.append(f"  - {name} - {image_url}")
          output.append("=" * 20)
      print("\n".join(output))
