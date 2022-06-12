# sys.path.insert(1, '/home/bogdan_alexandru_bercean/ranger/Ranger-Deep-Learning-Optimizer/')
# from pytorch_ranger import Ranger

# from fastai.vision.models.cadene_models import inceptionv4

# # models for cnn_learner
# from torchvision.models import ResNet,resnet18,resnet34,resnet50,resnet101,resnet152
# from torchvision.models import SqueezeNet,squeezenet1_0,squeezenet1_1
# from torchvision.models import densenet121,densenet169,densenet201,densenet161
# from torchvision.models import vgg11_bn,vgg13_bn,vgg16_bn,vgg19_bn,alexnet

from PIL import Image
from PIL import ImageFile
from fastai.vision import open_image
from fastai.vision import Image as FastaiImage

from skimage import io, img_as_ubyte
from skimage.color import gray2rgb

ImageFile.LOAD_TRUNCATED_IMAGES = True
# from fastai.vision import Image
import logging

# logging.basicConfig(level=logging.DEBUG)

try:
    from .attention.models import attention_densenet121
    from .attention.heatmaps import calculate_attention
    from xfastai.simple_densenet121 import simple_densenet121
    # from .attention.bogdan_heatmap import calculate_attention
    from .utils import *
except ImportError:
    from xfastai.utils import *
    from xfastai.attention.models import attention_densenet121
    # from xfastai.attention.bogdan_heatmap import calculate_attention
    from xfastai.attention.heatmaps import calculate_attention

from torchvision.models import densenet201

import time

# not all dockers require this
try:
    from efficientnet_pytorch import EfficientNet
except ImportError:
    pass

def efficientnet(model_name, num_classes):
    return EfficientNet.from_name(model_name=model_name, num_classes=num_classes)

class AttentionHeatmapHandler:
    def __init__(self, model_path, classes, xtype, target_size=(256, 256), use_clahe=False, tile_grid_size = [8, 8], image_read_type='open_image', model_type='attention_densenet121'):
        if model_type == 'simple_densenet121':
            self.model = simple_densenet121(False, num_classes=len(classes))
        elif model_type == 'attention_densenet121':
            self.model = attention_densenet121(True, num_classes=len(classes), aggregation_mode='ft')
        elif model_type == 'densenet201':
            self.model = densenet201(False, num_classes=len(classes))
            self.model.to('cpu')
        elif 'efficientnet' in model_type:
            self.model = efficientnet(model_type, num_classes=len(classes))

        self.model = pretrain_model_from_path(self.model, model_path)

        self.model.eval()

        if use_clahe:
            self.valid_tfms = get_clahe_transform(tile_grid_size=tile_grid_size)
        else:
            self.valid_tfms = None

        self.target_size = target_size
        self.xtype = xtype
        self.classes = classes
        self.use_clahe = use_clahe
        self.image_read_type = image_read_type

    def predict(self, image_data):
        return self.model(image_data)

    def predict_and_generate_heatmap(self, img_path, attention=True):
        # load and normalize image
        original_im = Image.open(img_path)
        original_im = np.array(original_im)

        # logging.info(open_image(img_path).shape)

        # a = time.time()

        if self.image_read_type == 'open_image':
            model_input = open_image(img_path, convert_mode='RGB')
        elif self.image_read_type == 'skimage':
            img = gray2rgb(img_as_ubyte(io.imread(img_path)))
            
            model_input = FastaiImage(pil2tensor(img, np.float32 ).div(255))
        else:
            raise ValueError(f'Unknown image_read_type {self.image_read_type}')
        
        model_input = model_input.apply_tfms(self.valid_tfms, size=self.target_size[0])

        model_input = normalize(model_input.data, imagenet_mean, imagenet_std)

        model_input = model_input.cpu().unsqueeze(0)

        if attention:
            # generate predictions and save features we will later use for our heatmap
            predictions, heatmap, attentions = calculate_attention(self.model, model_input, original_im, len(self.classes),
                                                                self.xtype)

            return predictions, heatmap, original_im, attentions
        else:
            predictions = torch.sigmoid(self.model(model_input))

            return predictions

    def process_image_attention(self, input_path, save_path):
        predictions, heatmap, original_img, attentions = self.predict_and_generate_heatmap(input_path)

        heatmap.save(save_path)

        if isinstance(predictions, torch.Tensor):
            predictions = predictions.detach().cpu().numpy()

        return predictions, attentions

    def process_image(self, input_path, save_path, attention=True):
        """ Take an image, overlay heatmap on it save to save_path; return predictions """

        if attention:
            predictions, heatmap, original_img, _ = self.predict_and_generate_heatmap(input_path, attention)

            heatmap.save(save_path)
        else:
            predictions = self.predict_and_generate_heatmap(input_path, attention)

        if isinstance(predictions, torch.Tensor):
            predictions = predictions.detach().cpu().numpy()

        return predictions
