import cv2
import numpy as np

def YOverlap(Box1, Box2):
	Ymin1, Ymax1 = Box1[1], Box1[3]
	Ymin2, Ymax2 = Box2[1], Box2[3]

	if Ymin1 < Ymin2:
		return YOverlap(Box2, Box1)

	if Ymin1 > Ymax2:
		return False
	else:
		Union = Ymax2 - Ymin1
		Inter = Ymax1 - Ymin2
		IoU = Union / Inter
		if IoU > 0.5:
			return True
		else:
			return False

	return False

def Domino(neighbor):
	temp = [neighbor[0]]
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

	return temp

def MergeBoxes(Boxes):
	Boxes = np.array(Boxes)
	Len = len(Boxes)

	# Get the coordinates
	Xmin = Boxes[:,0]
	Ymin = Boxes[:,1]
	Xmax = Boxes[:,2]
	Ymax = Boxes[:,3]

	# Expand coordinates to matrixes
	Xmin_matrix = np.tile(Xmin, (Len, 1))
	Xmax_matrix = np.tile(Xmax, (Len, 1))
	Ymin_matrix = np.tile(Ymin, (Len, 1))
	Ymax_matrix = np.tile(Ymax, (Len, 1))

	# Calculate the distance of all pairs
	# Distance_ij is the distance of box_i's TopRight to box_j's TopLeft
	Distance = np.sqrt((Xmin_matrix - Xmax_matrix.T)**2 + (Ymin_matrix - Ymin_matrix.T)**2)

	# Offset a big number on the diagnal, so we won't choose itself as the nearest
	Distance += np.identity(Len) * 99999

	# Get all nearest pairs
	index = np.argmin(Distance, axis=1)

	Neighbor = []
	for i in range(Len):
		BoxLeft, BoxRight = Boxes[i], Boxes[index[i]]
		if BoxLeft[0] > BoxRight[0]:
			# print("Wrong Order:", i, index[i])
			continue
		if not YOverlap(BoxLeft, BoxRight):
			# print("Not at same height:", i, index[i])
			continue
		if BoxLeft[2] > BoxRight[0] or Distance[i][index[i]] < abs(BoxLeft[3] - BoxLeft[1] + BoxRight[3] - BoxRight[1]) / 2:
			# print("Are neighbors:", i, index[i])
			Neighbor.append([i, index[i]])
			continue
	if len(Neighbor) <= 0:
		return Boxes

	Neighbor = Domino(Neighbor)
	Merging = [i for sublist in Neighbor for i in sublist]
	Going2Merge = Boxes[Merging]
	NewBoxes = np.delete(Boxes, Merging, axis=0)
	NewLen = len(NewBoxes) + len(Neighbor)

	Cur = 0
	for i in Neighbor:
		L = len(i)
		MergingBoxes = Boxes[i]
		xmin, ymin, xmax, ymax = MergingBoxes[:,0], MergingBoxes[:,1], MergingBoxes[:,2], MergingBoxes[:,3]
		NewBox = [min(xmin), min(ymin), max(xmax), max(ymax)]
		NewBoxes = np.append(NewBoxes, NewBox)
		Cur += L

	NewBoxes = np.reshape(NewBoxes, (NewLen, 4))

	return NewBoxes

def KillBoxes(Boxes):
	Xmin = Boxes[:,0]
	Ymin = Boxes[:,1]
	Xmax = Boxes[:,2]
	Ymax = Boxes[:,3]

	H, W = Ymax - Ymin, Xmax - Xmin
	R = W / H

	Kill = R < 3
	Kill = [i for i, x in enumerate(Kill) if x]
	
	Boxes = np.delete(Boxes, Kill, axis=0)

	return Boxes

def BoxFilter(Boxes):
	if len(Boxes) <= 0:
		return Boxes
	Boxes = MergeBoxes(Boxes)
	Boxes = KillBoxes(Boxes)
	return Boxes