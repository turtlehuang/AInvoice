import numpy as np
import cv2

def Overlap(box1, box2, swap=False):
	if box1[0] < box2[0]:
		return Overlap(box2, box1, True)
	ymin1, xmin1, ymax1, xmax1 = box1
	ymin2, xmin2, ymax2, xmax2 = box2
	yUnion = ymax2 - ymin1
	if yUnion > 0:
		# print("No Union")
		return False
	yInter = ymax1 - ymin2 + 1e-5
	IoU = yUnion / yInter
	if IoU < 0.5:
		# print("y overlap too small")
		return False
	if not swap:
		if xmin2 >= xmax1:
			# print("x no overlap")
			return False
	else:
		if xmin1 >= xmax2:
			# print("swap, x no overlap")
			return False
	return True

def FindNumber(boxs, label):
	bb_cord = np.array(boxs)

	# Get the coordinates
	box_xmin = bb_cord[:,1]
	box_xmax = bb_cord[:,3]
	box_ymin = bb_cord[:,0]
	box_ymax = bb_cord[:,2]

	# Expand coordinates to matrixes
	box_xmin_matrix = np.tile(box_xmin, (len(box_xmin), 1))
	box_xmax_matrix = np.tile(box_xmax, (len(box_xmax), 1))
	box_ymin_matrix = np.tile(box_ymin, (len(box_ymin), 1))
	box_ymax_matrix = np.tile(box_ymax, (len(box_ymax), 1))

	# Calculate the distance of all pairs
	# norm_ij is the distance of box_i's TopRight to box_j's TopLeft
	norm = np.sqrt((box_xmin_matrix - box_xmax_matrix.T)**2 + (box_ymin_matrix - box_ymin_matrix.T)**2)
	
	# Offset a big number on the diagnal, so we won't choose itself as the nearest
	norm += np.identity(len(boxs)) * 99999

	# Get all nearest pairs
	index = np.argmin(norm, axis=1)
	neighbor = []
	for i in range(len(index)):
		neighbor.append((i, index[i]))
	
	# Calculate threshold
	diag = np.sqrt((box_xmax - box_xmin)**2 + (box_ymax - box_ymin)**2)
	threshold = diag * 0.35

	for i in range(len(neighbor)-1,-1,-1):
		# If the first box is at the right, just kill it
		if bb_cord[i][1] > bb_cord[index[i]][1]:
			del neighbor[i]
			continue

		# If the two boxes overplap, they should be neightbors
		if Overlap(bb_cord[i], bb_cord[index[i]]):
			# print("Overlap:", label[i], label[index[i]])
			continue

		# If the two boxes are aligned normally and do not overlap,
		# Check if they are within the range of threshold
		Threshold = (threshold[i] + threshold[index[i]]) / 2
		if norm[neighbor[i]] > Threshold:
			del neighbor[i]
			continue
	# print(neighbor)
	if len(neighbor) > 0:		
		return Domino(neighbor, label)
	else:
		return "Cannot find invoice number QwQ"

def FindTarget(List):
	for i in List:
		if len(i) == 8:
			return i
	return None

'''
Domino() runs the domino game.
Currently using some stupid brute force algorithm (O(n^2))
May be speed up, but since n is small, 
there won't be significant improve in time.
'''
def Domino(Neighbor, label):
	neighbor = list(np.copy(Neighbor))
	temp = [list(neighbor[0])]
	cur = 0
	del neighbor[0]
	while(len(neighbor) > 0):
		# print(neighbor)
		# print(temp)
		Left, Right = -1, -1
		CurLeft, CurRight = temp[cur][0], temp[cur][-1]
		for i in range(len(neighbor)):
			# print(CurLeft, CurRight)
			Next = neighbor[i]
			if CurLeft == Next[1]:
				# print("Add", Next[0], "to left")
				Left = i
			if CurRight == Next[0]:
				# print("Add", Next[1], "to right")
				Right = i
		if Left != -1:
			# print("KILL", neighbor[Left])
			temp[cur] = [neighbor[Left][0]] + temp[cur]
			del neighbor[Left]
		if Right != -1 and Left != Right:
			if Left < Right and Left != -1:
				Right -= 1
			temp[cur].append(neighbor[Right][1])
			# print("KILL", neighbor[Right])
			del neighbor[Right]
		if Left == -1 and Right == -1:
			if len(neighbor) == 0:
				break
			temp.append(list(neighbor[0]))
			del neighbor[0]
			cur +=1
	# print("Index:", temp)
	temp2 = [label[i] for sublist in temp for i in sublist]
	# print("Nums:", temp2)
	TargetSeq = FindTarget(temp)
	if TargetSeq is None:
		return "No Number Found OwQ"
	Numbers = [str(label[i]) for i in TargetSeq]
	Numbers = "".join(Numbers)
	return Numbers