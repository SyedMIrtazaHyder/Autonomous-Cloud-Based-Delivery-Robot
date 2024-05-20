import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from unet import UNet
import time

# Preprocess the image


def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])
    return transform(image).unsqueeze(0)


def capture_image():
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    cap.set(3, 480)
    cap.set(4, 480)
    if not cap.isOpened():
        print("Error: Failed to open camera")
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Error: Failed to capture frame")
        return None
    return frame


# Load the model
model = UNet()
model.load_state_dict(torch.load(
    r'segmentation_model2.pth'))
model.eval()

# Capture an image
image = capture_image()
if image is None:
    exit()

image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


input_image = preprocess_image(image_pil)


with torch.no_grad():
    output = model(input_image)


threshold = 0.40
binary_output = torch.where(
    output > threshold, torch.tensor(1), torch.tensor(0))


binary_output_np = binary_output.squeeze().cpu().numpy()


test_image = cv2.resize(image, (256, 256))


three_channel_out = np.zeros((*binary_output_np.shape, 3), dtype=np.uint8)
three_channel_out[binary_output_np == 1] = [255, 0, 0]

highlighted_image = cv2.addWeighted(test_image, 1, three_channel_out, 0.5, 0)

# Plot the results
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(binary_output_np, cmap='gray')
plt.title('Binary Output')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(test_image)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(highlighted_image, cv2.COLOR_BGR2RGB))
plt.title('Highlighted Image')
plt.axis('off')

plt.show()
