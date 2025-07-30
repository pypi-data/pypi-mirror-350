import numpy as np
from PIL import Image
import os

class Augementation:
    def hotEncodeLabels(self, allLabels, numClasses):
        labels = np.zeros((len(allLabels), numClasses))
        for i in range(len(allLabels)):
            labels[i][allLabels[i]] = 1
        return labels

    def getImagePaths(self, folderPath, extensions = ['.jpg', '.png', '.jpeg']):
        imagePaths = []
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                if(any(file.lower().endswith(ext) for ext in extensions)):
                    fullPath = os.path.join(root, file)
                    imagePaths.append(fullPath)
        return imagePaths

    def preprocessImages(self, imagePaths, targetSize = (128, 128)):
        images = []
        for path in imagePaths:
            img = Image.open(path).convert('RGB')
            resized = img.resize(targetSize)
            normalised = np.array(resized) / 255.0
            images.append(normalised)
        return np.array(images)

    def dataAugmentation(self, images):
        allImages = []
        for img in images:
            allImages.append(img)
            allImages.append(np.fliplr(img))
            allImages.append(np.flipud(img))
            allImages.append(np.flipud(np.fliplr(img)))
        return np.array(allImages)