import torch.nn.functional as F
from PIL import Image
from PIL import ImageFile
from matplotlib.colors import ListedColormap
from skimage.transform import resize

ImageFile.LOAD_TRUNCATED_IMAGES = True

from xfastai.utils import *

N = 256
vals = np.ones((N, 4))
vals[:, 0] = np.linspace(4. / 255., 237. / 255., N)
vals[:, 1] = np.linspace(39. / 255., 27. / 255., N)
vals[:, 2] = np.linspace(59. / 255., 36. / 255., N)
xvision_cmap = ListedColormap(vals, name='xvision')


class SaveFeatures():
    features = None

    def __init__(self, m): self.hook = m.register_forward_hook(self.hook_fn)

    def hook_fn(self, module, input, output): self.features = output

    def remove(self): self.hook.remove()


class DenseNet121HeatmapHandler:
    def __init__(self, model_path, target_size=(512, 512), heatmap_features_size=None, final_activation=F.sigmoid):
        self.model = torch.load(model_path, map_location='cpu')
        # if we are loading a DataParallelObject we are interested in the module, which is
        # the actual model
        if isinstance(self.model, dict) and 'model' in self.model:
            self.model = self.model['model']

        if isinstance(self.model, torch.nn.parallel.DataParallel):
            self.model = self.model.module

        self.model.eval().float().cpu()

        self.target_size = target_size
        if heatmap_features_size is None:
            self.heatmap_features_size = (1024, self.target_size[0] // 32, self.target_size[1] // 32)
        else:
            self.heatmap_features_size = heatmap_features_size

        self.final_activation = final_activation

        try:
            self.last_conv = self.model[-2][-1][-1]
        except TypeError:
            self.last_conv = list(self.model.children())[0][-1]

        print(self.last_conv)

    def predict_and_generate_heatmap(self, img_path):
        # load and normalize image
        original_im = Image.open(img_path)
        # print(f'Opened image {img_path}, size: {original_im.size}')
        im = original_im.resize(self.target_size)

        # remove transparency from image
        if im.mode == 'RGBA':
            rgb_im = Image.new("RGB", im.size, (255, 255, 255))
            rgb_im.paste(im, mask=im.split()[3])  # 3 is the alpha channel
            im = rgb_im

        im = normalize(toTensor(im), imagenet_mean, imagenet_std)

        # generate predictions and save features we will later use for our heatmap
        sfs = SaveFeatures(self.last_conv)
        predictions = self.final_activation((self.model(im.unsqueeze(0)))).cpu().detach().numpy()[0]
        sfs.remove()

        # generate a heatmap from the features
        heatmap_features = sfs.features.reshape(self.heatmap_features_size)
        values, indices = heatmap_features.max(0)

        heatmap = values.cpu().detach().numpy()
        heatmap = resize(heatmap, (original_im.height, original_im.width), anti_aliasing=True)

        return predictions, heatmap, original_im

    def process_image(self, input_path, save_path, alpha=0.5):
        """ Take an image, overlay heatmap on it save to save_path; return predictions """
        predictions, heatmap, original_img = self.predict_and_generate_heatmap(input_path)

        # generate heatmap from heatmap values
        heat_interp = np.interp(heatmap, (heatmap.min(), heatmap.max()), (0, 1))
        heat_interp = xvision_cmap(heat_interp)[:, :, 0:3]
        heat_interp = np.uint8(heat_interp * 255)
        heatmap_pil = Image.fromarray(heat_interp)

        Image.blend(original_img.convert('RGB'), heatmap_pil, alpha=0.5).save(save_path)

        return predictions
