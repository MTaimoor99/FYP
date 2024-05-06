from django.apps import AppConfig
import html
from pathlib import Path
import os
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification #importing distilbert tokenizer+model
import torch
import os

from .helper_classes import DistilBERTClass

#from fastbert.prediction import BertClassificationPredictor


class WebScraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_scraper'
    MODEL_PATH =Path("web_scraper/model")
    #Load the model from the saved path
    predictor = torch.load(MODEL_PATH/"pytorch_model.bin", map_location="cpu")
    #Load the tokenizer
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    #The model is now in prediction mode
    predictor.eval()  