from PIL import Image
from pathlib import Path
from tqdm.auto import tqdm
import cv2


path = Path.home() / ("Downloads/Data/dataset/item_matching/img/img_/batch_0_to_999")
files = sorted([*path.glob("*.jpg")], key=lambda x: int(x.stem))

for idx, f in tqdm(enumerate(files), total=len(files)):
    img = Image.open(str(f)).convert('RGB')
    resized_img = img.resize((300, 200))
    resized_img.save(path.parent / f"{f.stem}.jpg")

for idx, f in tqdm(enumerate(files), total=len(files)):
    img = cv2.imread(str(f))
    resized_img = cv2.resize(img, (300, 200))
    cv2.imwrite(str(path.parent / f"{f.stem}_cv.jpg"), resized_img)
