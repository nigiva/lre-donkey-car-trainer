from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import json
from tqdm import tqdm
import os
from loguru import logger

class ESLRExtractor:
  def __init__(self, eslr_path):
    self.eslr_path = eslr_path
    if not os.path.exists(self.eslr_path):
      logger.error("ESLR File not found !")
      raise Exception("ESLR File not found !")
  
  def extract(self, label_path, images_path, image_ext = ".jpeg"):
    if os.path.exists(images_path):
        logger.info(".eslr is already extracted !")
        return
    # Créer le dossier qui contiendra toutes les images extraites du .eslr s'il n'existe pas
    os.makedirs(images_path, exist_ok=True)

    # Ouvrir le fichier label.csv
    label_file = open(label_path, "w")

    # Pour définir les en-têtes du fichier label, il faut lire au moins la première ligne
    # du fichier *.eslr
    label_head_is_defined = False

    # Lire le fichier eslr
    with open(self.eslr_path, "r") as dataset_file:
      for i, line in enumerate(tqdm(dataset_file)):
        data_line = json.loads(line)
        if (data_line["msg_type"] == "telemetry"):
          # Si le header n'a pas encore initialisé
          if not label_head_is_defined:
            label_head_list = list(data_line.keys())
            label_head_list.remove("msg_type")
            label_head_list.remove("image")
            label_head_list = ['path'] + label_head_list
            label_head_str = ",".join(label_head_list)
            # Écrire le header dans le CSV
            label_file.write(label_head_str + "\n")
            label_head_is_defined = True
          # Définir le path de l'image à enregistrer
          image_focused_path = os.path.join(images_path, str(i) + image_ext)
          data_line['path'] = image_focused_path
          # Lire, décoder et enregistrer l'image
          Image.open(BytesIO(base64.b64decode(data_line["image"]))).save(image_focused_path)
          # Ajouter toutes les données de la ligne lue dans un le CSV
          # Mettre 0 comme valeur par défaut si la valeur n'est pas trouvée dans data_line
          data_list_to_write = [str(data_line.get(k, 0)) for k in label_head_list]
          label_file.write(",".join(data_list_to_write) + "\n")
    label_file.close()
    logger.info("Extraction is done !")
  
  @staticmethod
  def read_csv(images_path):
    return pd.read_csv(images_path)