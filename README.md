# AInvoice

<div align=center><img height=360 width=115 src="https://github.com/turtlehuang/AInvoice/blob/master/ainvoice.png"/></div>

This is an example file with default selections.

## Background

Here is the AInvoice, a Taiwan receipt lottery checking application, using computer vision with deep learning model to achieve digit number recognition.

## Install
tensorflow == 1.12.0 <br>
keras_retinanet <br>
imutils<br>
cv2、numpy、tkinter、PIL


```
```

## Usage
Please specify the camera source in main.py file<br>

```python=18
video_source = 1
```
If you are using the webcam embedded in the laptop, the source should be 0 as default.<br>
Then execute the command as below:

```
python main.py
```

## Contributing

YuLong Huang<br>
LongYing Lin<br>
ChiaChe Sa<br>
HsuanHuai Wong



v5.0 
- Import EAST model, Classifier model, filter module to detect whole frame
- Optimize inpot source of mobile camera

v4.3
- Improved wining info display
- Add 5.6/2019 wining table
- 
v4.2
- Add threading
