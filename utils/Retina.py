# -*- coding: utf-8 -*-

from keras_retinanet import models
from keras_retinanet.utils.image import preprocess_image, resize_image

import cv2
import os
import numpy as np
import time
import tensorflow as tf

from utils.retina_utils import visualize_boxes
from utils.NumberFilter import *

class Retina():
	@staticmethod
	def pred_string(frame):
		global model
		image = frame
		# copy to draw on
		draw = image.copy()
		draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
		
		# preprocess image for network
		image = preprocess_image(image)
		image, _ = resize_image(image, 416, 448)
		
		# process image
		start = time.time()
		boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
		print("processing time: ", time.time() - start)

		#######################################
		h, w, _ = image.shape
		h2, w2, _ = draw.shape
		boxes[:, :, 0] = boxes[:, :, 0] / w * w2
		boxes[:, :, 2] = boxes[:, :, 2] / w * w2
		boxes[:, :, 1] = boxes[:, :, 1] / h * h2
		boxes[:, :, 3] = boxes[:, :, 3] / h * h2        
		#######################################
		
		labels = labels[0]
		scores = scores[0]
		boxes = boxes[0]
		out_image, pred_str, bb_cord = visualize_boxes(draw, boxes, labels, scores, class_labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
		pred_str_np = []
		#print("pred_str:",pred_str)
		#print("bb_cord:",bb_cord)

		for i,val in enumerate(pred_str):
			#print (val[0][0])
			pred_str_np.append(int(val[0][0]))
		pred_str_np = np.array(pred_str_np)[:,np.newaxis]

		if (pred_str_np != []):
			print("pred_str_np: ", pred_str_np)
		# cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(out_image, cv2.COLOR_RGB2BGR))
		labels = [int(i[0][0]) for i in pred_str]
		if len(bb_cord) > 0:
			return FindNumber(bb_cord, labels)
		else:
			return "Can't Find Invoice Number"

	def __init__(self):    
		global model, graph
		MODEL_PATH = os.path.join("model", "Retinanet.h5")
		model = models.load_model(MODEL_PATH, backbone_name='resnet50')
		model._make_predict_function()
		self.graph = tf.get_default_graph()
		model = models.convert_model(model)