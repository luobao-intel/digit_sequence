from create_digit_sequence import *
import argparse
from argparse import RawTextHelpFormatter

def args_parse():
    """
    Input the necessary parameters
    """
    description = """
    python create_digit_sequence.py --number="342500" --image_width 30 --image_height 30 \
     --min_spacing=5 --max_spacing=10 \
     --margin 4 --rotate 30 --rotate_step 1
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--data_dir', dest='data_dir',
                        default="data\mnist", required=False,
                        help='dir to save the MNIST dataset')
    parser.add_argument('--image_dir', dest='image_dir',
                        default="data\image", required=False,
                        help='dir to save the produced images')
    parser.add_argument('--number', type=str, dest='number',
                        default='123456', required=False,
                        help='A string representing the number')
    parser.add_argument('--image_width', dest='image_width',
                        default=170, required=False,
                        help='The image width')
    parser.add_argument('--image_height', dest='image_height',
                        default=28, required=False,
                        help='the image height')
    parser.add_argument('--min_spacing', dest='min_spacing',
                        default=1, required=False,
                        help='The minimum spacing between digits ')
    parser.add_argument('--max_spacing', dest='max_spacing',
                        default=10, required=False,
                        help='The maximum spacing between digits ')
    parser.add_argument('--need_crop', dest='need_crop',
                        default=True, required=False,
                        help='Cut out the redundant border', action='store_true')
    parser.add_argument('--margin', dest='margin',
                        default=3, required=False,
                        help='The padding width', )
    parser.add_argument('--rotate', dest='rotate',
                        default=40, required=False,
                        help='max rotate degree 0-45')
    parser.add_argument('--need_batch', dest='need_batch',
                        default=True, required=False,
                        help='need different digit sequences with same number input')
    parser.add_argument('--batch_num', dest='batch_num',
                        default=10, required=False,
                        help='the batch number if need different digit sequences')
    parser.add_argument('--need_aug', dest='need_aug',
                        default=True, required=False,
                        help='need data augmentation', action='store_true')
    args = parser.parse_args()
    return args

def main():
    opt = args_parse()
    Model = CreateImage(opt)
    Model.create_digit_sequence(opt.number, opt.image_width, opt.min_spacing, opt.max_spacing)

if __name__ == '__main__':
    main()


