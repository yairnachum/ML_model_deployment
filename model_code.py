import torch
from torchvision import transforms, models
from PIL import Image
import numpy as np


def process_image_and_predict(file_path: str) -> Image.Image:
    model = models.segmentation.deeplabv3_resnet101(pretrained=True)
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((223, 223)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image = Image.open(file_path).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)

    with torch.no_grad():
        output = model(image)["out"]

    mask = torch.argmax(output.squeeze(), dim=0).detach().cpu().numpy()
    rng = np.random.default_rng(12345)
    values = np.unique(mask)
    color_map = {value: rng.integers(0, 256, size=3) for value in values}
    colored_mask = np.zeros((*mask.shape, 3), dtype=np.uint8)
    for value, color in color_map.items(): colored_mask[mask == value] = color

    return Image.fromarray(colored_mask)