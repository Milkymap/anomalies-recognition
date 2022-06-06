import click 

import pickle, json 

import cv2 
import numpy as np 
import operator as op 
import itertools as it, functools as ft

from glob import glob 
from os import path 
from loguru import logger 

from time import sleep 
from rich.progress import track
from torch import tensor 

from strategies import * 

@click.group(chain=False, invoke_without_command=True)
@click.option('--debug/--no-debug', help='debug mode flag', default=True)
@click.pass_context
def router_command(ctx, debug):
    ctx.ensure_object(dict)
    invoked_subcommand = ctx.invoked_subcommand 
    if invoked_subcommand is not None:
        logger.debug(f'{invoked_subcommand} was called')
    else:
        logger.debug('add --help option in order to see availables subcommands')

@router_command.command()
@click.option('--path2videos', type=click.Path(True), required=True)
@click.option('--extension', help='video file extension', default='mp4')
@click.option('--window_size', help='size of frames_memory', default=7, type=int)
@click.option('--stride', help='value of the stride', default=3)
@click.option('--path2data', type=click.Path(False), required=True)
@click.option('--path2vectorizer', help='path to resnetnet(backbone)', type=click.Path(False))
def annotation(path2videos, extension, window_size, stride, path2data, path2vectorizer):
    video_paths = sorted(glob(path.join(path2videos, f'*.{extension}')))
    logger.debug(f'nb video files : {len(video_paths):03d}')
    try:
        vectorizer = load_vectorizer(path2vectorizer)
        logger.debug('vectorizer is ready')
    except Exception as e:
        logger.error(e)
        exit(1)

    accumulator = []
    for v_path in track(video_paths[1:2], 'video annotation'):
        logger.debug(f'annotation of the video : {v_path}')
        capture = cv2.VideoCapture(v_path)
        keep_reading = True 
        frames_memory = []
        while keep_reading:
            key_code = cv2.waitKey(25) & 0xFF 
            capture_status, bgr_frame = capture.read()
            keep_reading = key_code != 27  # hit the [ESCAPE] button tu quit the loop 
            if keep_reading and capture_status:
                bgr_frame = cv2.resize(bgr_frame, (512, 512))
                cv2.imshow('000', bgr_frame)
                character = chr(key_code)
                if character in 'an':
                    logger.debug(f'key_code : {key_code:03d}')
                    tensor_ = cv2th(bgr_frame)
                    single_batch = tensor_[None, ...]
                    out_features = th.flatten(vectorizer(single_batch))  # 512 
                    frames_memory.append(out_features.numpy())
                    if len(frames_memory) == window_size:
                        label = 1 if character == 'a' else 0
                        stacked_embedding = np.vstack(frames_memory)  # 7x512   
                        accumulator.append((stacked_embedding, label))
                        frames_memory = frames_memory[stride:]  # ignore 0 .. stride - 1
            # end if ...!
        # end while loop 
        capture.release()
        cv2.destroyAllWindows()
    
    with open(path2data, 'wb') as file_pointer:
        pickle.dump(accumulator, file_pointer)
        logger.success('the dataset was created')
        
if __name__ == '__main__':
    router_command(obj={})