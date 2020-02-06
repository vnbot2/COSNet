import os
import cv2
import argparse
import os.path as osp
import shutil
from glob import glob
from tqdm import tqdm
import tempfile
import re

def str_to_number(path):
    name = os.path.basename(path).split('.')[0]
    number = re.findall(r'\d+', name)[0]
    return number


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input','--i', )
    parser.add_argument('--output','--o',)
    parser.add_argument('--mode', choices=['v2i', 'i2v'])

    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)    
    if args.mode == 'v2i':
        file_name = os.path.basename(args.input).split('.')[0]
        vidcap = cv2.VideoCapture(args.input)
        def getFrame(sec):
            vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
            hasFrames,image = vidcap.read()
            if hasFrames:
                out_file = os.path.join(args.output_dir, f'{count}_{file_name}.jpg')
                print(out_file)
                cv2.imwrite(out_file, image)     # save frame as JPG file
            return hasFrames

        sec = 0
        fps = 30
        frameRate = 1/fps #//it will capture image in each 0.5 second
        count=1
        success = getFrame(sec)
        while success:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec)

    elif args.mode == 'i2v':
        all_img_paths= glob(os.path.join(args.input,'*'))#'./images/testing/'
        pathOut = args.output
        fps = 30
        video_dict = {}
        for img_path in all_img_paths:
            name = os.path.basename(img_path).split('.')[0]
            index = name.split('_')[0]
            vid_name = ''.join(name.split('_')[1:])
            if not vid_name in video_dict:
                video_dict[vid_name] = [img_path]
            else:    
                video_dict[vid_name].append(img_path)            
        # files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
        #for sorting the file names properly
        # files.sort(key = lambda x: x[5:-4])
        for video_name, files in video_dict.items():
            # ld = lambda path
            files = list(sorted(files, key=str_to_number, reverse=False))
            frame_array = []
            for i in range(len(files)):
                # import ipdb; ipdb.set_trace()
                img = cv2.imread(files[i])
                height, width, layers = img.shape
                size = (width,height)
                #inserting the frames into an image array
                frame_array.append(img)

            pathOut = os.path.join(args.output, video_name+'.mp4')

            out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
            for i in tqdm(range(len(frame_array))):
                # writing to a image array
                out.write(frame_array[i])
            out.release()
            print('--> VIDEO OUT:', pathOut)
