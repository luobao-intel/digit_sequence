from src.data_download import *
from src.data_augment import *
import matplotlib.pyplot as plt

class CreateImage(object):
    def __init__(self, opt):
        self.opt = opt

    def show(self, image):
        """
        Render a given numpy.uint8 2D array of pixel data.
        """
        plt.imshow(image, cmap='gray')
        plt.show()

    def create_digit_sequence(self, number, image_width, min_spacing, max_spacing):
        DataLib = DatasetAccess(self.opt.data_dir, self.opt.image_dir, number)
        dataset = DataLib.get_mnist_dataset()

        batch = self.opt.batch_num if self.opt.need_batch else 1
        for count in range(batch):
            image_list = []
            for digit in number:
                if digit < '0' or digit > '9':
                    logging.error('Invalid number!')
                    os._exit(0)
                index = int(digit)
                rand_seed = int(random.uniform(0, len(dataset[index])))
                sample = dataset[index][rand_seed]
                image_list.append(sample)

            if self.opt.need_crop:
                image = []
                model = Digit2Image(sample.shape[0], sample.shape[1], self.opt.image_height,  self.opt.margin)
                for pic in image_list:
                    trans_image = model.do(pic)
                    image.append(trans_image)
                image_list = image

            if self.opt.need_aug:
                data_aug = DataAugmentation(self.opt.rotate)
                image_list = data_aug.do(image_list)

            index = 1
            for _ in range(len(number) - 1):
                space = int(random.uniform(min_spacing, max_spacing))
                if space:
                    space_grid = np.zeros((self.opt.image_height, space))
                    image_list.insert(index, space_grid)
                    index = index + 2
                else:
                    index = index + 1

            res_img = np.concatenate(image_list, axis=1)
            if image_width < res_img.shape[1]:
                logging.warning("The image width is too small to meet the requirement! Here resize the image instead!")
                res_img = cv2.resize(res_img, (image_width, self.opt.image_height))
            else:
                margin = int((image_width - res_img.shape[1]) / 2)
                res_img = cv2.copyMakeBorder(res_img, 0, 0, margin, image_width - res_img.shape[1] - margin,
                                             cv2.BORDER_CONSTANT, value=0)
            image_path = os.path.join(self.opt.image_dir, number)
            save_path = os.path.join(image_path, number + "_{0}.jpg".format(count))
            save = cv2.imwrite(save_path, res_img)
            if save:
                logging.info("successfully save image {0}_{1}.jpg".format(number,count))
            else:
                logging.error("fail to save image {0}_{1}.jpg".format(number, count))

        self.show(res_img)
