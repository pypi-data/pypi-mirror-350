import vizy
import torch
import numpy as np

from PIL import Image

test_image = Image.open("test_image.jpg")
img = np.array(test_image)[np.newaxis, :, :, :]  # Convert to (1, H, W, C) and then to (C, B, H, W)
img = img.transpose(3, 0, 1, 2)  # Convert to CBHW format
img = torch.from_numpy(img).float()  # Convert to torch tensor and cast to float

# Create a batch of 4 images by duplicating and adding some noise
img = torch.cat([
    img, 
    img + torch.randn_like(img)*10,
    img + torch.randn_like(img)*5,
    img + torch.randn_like(img)*15
], dim=1)
img = torch.clip(img, 0, 255)  # Ensure values stay in valid range

print(img.shape)  # Should be (C, 4, H, W)
print(img.min())
print(img.max())

vizy.save('a.png', img)
