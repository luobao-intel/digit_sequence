from create_digit_sequence import *
import argparse
from argparse import RawTextHelpFormatter

def args_parse():
    """
    Input the necessary parameters
    """
    description = """
    python create_digit_sequence.py -n 123456 -w 200 -ht 28 -min 5 -max 10 -c  -b -bn 100 -a -m 4 -r 30 
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-d', '--data_dir', type=str, default="data\mnist", required=False, help='dir to save the MNIST dataset')
    parser.add_argument('-s', '--image_dir', type=str, default="data\image", required=False, help='dir to save the produced images')
    parser.add_argument('-n', '--number', type=str, default='14543', required=True, help='A string representing the number')
    parser.add_argument('-w', '--image_width', type=int, default=170, required=False, help='The image width')
    parser.add_argument('-ht', '--image_height', type=int, default=28, required=False, help='the image height')
    parser.add_argument('-min', '--min_spacing', type=int, default=5, required=False, help='The minimum spacing between digits ')
    parser.add_argument('-max','--max_spacing', type=int, default=10, required=False, help='The maximum spacing between digits ')
    parser.add_argument('-c', '--need_crop', action='store_true', default=False, required=False, help='Cut out the redundant border')
    parser.add_argument('-a', '--need_aug', action='store_true', default=False, required=False, help='need data augmentation')
    parser.add_argument('-b', '--need_batch', action='store_true', default=False, required=False, help='need different digit sequences with same number input')
    parser.add_argument('-m', '--margin',type=int, default=0, required=False, help='The padding width', )
    parser.add_argument('-r', '--rotate',type=int, default=40, required=False, help='max rotate degree 0-45')
    parser.add_argument('-bn', '--batch_num', type=int, default=10, required=False, help='the batch number if need different digit sequences')

    args = parser.parse_args()
    return args

def main():
    opt = args_parse()
    Model = CreateImage(opt)
    Model.create_digit_sequence(opt.number, opt.image_width, opt.min_spacing, opt.max_spacing)

if __name__ == '__main__':
    main()


