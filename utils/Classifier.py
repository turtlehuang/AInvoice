import os
import tensorflow as tf
from keras.models import load_model

class Classifier():
	def __init__(self): 
		self.model = load_model(os.path.join("model", "Classifier.h5"))
		self.classifier_graph = tf.get_default_graph()