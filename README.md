# AInvoice

<div align=center><img height=115 width=360 src="https://github.com/turtlehuang/AInvoice/blob/master/ainvoice.png"/></div>

## Background

Here is the AInvoice, a Taiwan receipt lottery checking application, using computer vision with deep learning model to achieve digit number recognition.

## Install
Please check these library and their version had been installed:

| Library | Version |
|:-:|:-:|
|tensorflow-gpu | 1.13.1|
|keras_retinanet |0.5.1 |
|imutils | 0.5.2|

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
Lauch the whole process takes seconds, then the UI will pop up.<br>

<center>
  
| Winning | No winning | Miss |
|:-:|:-:|:-:|
| <img height=350 width=200 src="https://github.com/turtlehuang/AInvoice/blob/master/winning.JPG"/> | <img height=350 width=200 src="https://github.com/turtlehuang/AInvoice/blob/master/no.JPG"/> | <img height=350 width=200 src="https://github.com/turtlehuang/AInvoice/blob/master/miss.JPG"/> |

</center>
<br>
The info displayed below the frame are digits recognition result、winning status and detail selected months' winning info respectively.
You can select others month's winning info by selecting the item in list and pressing "apply" buttom to update the table.

## Contributing

YuLong Huang<br>
LongYing Lin<br>
ChiaChe Sa<br>
HsuanHuai Wong

## History
v5.0 
- Import EAST model, Classifier model, filter module to detect whole frame
- Optimize inpot source of mobile camera

v4.3
- Improved wining info display
- Add 5.6/2019 wining table

v4.2
- Add threading
