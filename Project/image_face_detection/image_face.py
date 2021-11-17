import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


img = cv.imread("../../cv-master/essential/assets/people.jpg")

# image dimension
h, w = img.shape[:2]

# load model
model = cv.dnn.readNetFromCaffe('../../cv-master/samples/data/deploy.prototxt',
                              '../../cv-master/samples/data/res10_300x300_ssd_iter_140000_fp16.caffemodel')

# preprocessing
# image resize to 300x300 by substraction mean vlaues [104., 117., 123.]
blob = cv.dnn.blobFromImage(img, 1.0, (300, 300), [
                            104., 117., 123.], False, False)

# set blob asinput and detect face
model.setInput(blob)
detections = model.forward()

faceCounter = 0
# draw detections above limit confidence > 0.7
for i in range(0, detections.shape[2]):
    # confidence
    confidence = detections[0, 0, i, 2]
    #
    if confidence > 0.7:
        # face counter
        faceCounter += 1
        # get coordinates of the current detection
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x1, y1, x2, y2) = box.astype("int")

        # Draw the detection and the confidence:
        cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
        text = "{:.3f}%".format(confidence * 100)
        y = y1 - 10 if y1 - 10 > 10 else y1 + 10
        cv.putText(img, text, (x1, y), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)

# show
fig = plt.figure(figsize=(20, 15))

# Plot the images:
imgRGB = img[:,:,::-1]
plt.imshow(imgRGB)

plt.show()
