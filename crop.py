from PIL import Image
import os
'''
A script to set a fixed ratio in country flags images dimensions
 - Each flag has a different ratio, and equal ratios/card sizes matters.
'''
def crop_image(img, ratio):
    width, height = img.size
    current_ratio = width /height

    if current_ratio > ratio:
        new_width = int(height * ratio)
        left = (width-new_width) //2
        box = (left, 0, left+new_width, height)
    else:
        new_height = int(width/ratio)
        top = (height-new_height) //2
        box = (0, top, width, top + new_height)
    return img.crop(box)

def main():
    input_folder = './flags'
    output_folder = './flags1.1'

    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        with Image.open(file_path)as f:
            f =f.convert('RGB')
            cropped= crop_image(f, 3/2)

            output_path = os.path.join(output_folder, file_name)
            cropped.save(output_path)

if __name__ == '__main__':
    main()