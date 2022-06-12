import PIL
import cv2
import numpy as np
from PIL import ImageFile
from skimage.transform import resize
from torch.autograd import Variable

ImageFile.LOAD_TRUNCATED_IMAGES = True
import torch

from .utils import HookBasedFeatureExtractor

from matplotlib.colors import ListedColormap

N = 256
vals = np.ones((N, 4))
vals[:, 0] = np.linspace(4. / 255., 237. / 255., N)
vals[:, 1] = np.linspace(39. / 255., 27. / 255., N)
vals[:, 2] = np.linspace(59. / 255., 36. / 255., N)
vals[:, 3] = np.linspace(0., 0.75, N)
xvision_cmap = ListedColormap(vals, name='xvision')


def return_cam(feature_conv, weight_softmax, class_idx):
    # generate the class activation maps upsample to 256x256
    size_upsample = (256, 256)
    bz, nc, h, w = feature_conv.shape
    output_cam = []
    for idx in class_idx:
        cam = weight_softmax[idx].dot(feature_conv.reshape((nc, h * w)).cpu())
        cam = cam.reshape(h, w)
        cam = cam - np.min(cam)
        cam_img = cam / np.max(cam)
        # cam_img = np.uint8(255 * cam_img)
        output_cam.append(cv2.resize(cam_img, size_upsample))

    return output_cam


def blend_images(original, attention, shape=(1024, 1024)):
    original = cv2.resize(original, shape)
    attention = cv2.resize(attention, shape)

    attention_pil = PIL.Image.fromarray(np.uint8(xvision_cmap(attention) * 255))
    orig = PIL.Image.fromarray(original).convert('RGBA')

    # im = PIL.Image.blend(orig, attention_pil, alpha=0.5).convert('RGB')

    orig.paste(attention_pil, (0, 0), attention_pil)

    orig = orig.convert('RGB')

    return orig


def get_feature_maps(model_to_use, layer_name, upscale, input_image):
    feature_extractor = HookBasedFeatureExtractor(model_to_use, layer_name, upscale)
    return feature_extractor.forward(Variable(input_image))


def calculate_attention(model, normalized_image, image, num_classes, xtype):
    input_img = image
    # input_img = np.expand_dims(input_img, axis=2)
    # print(f'Input img size: {input_img.shape}')

    params = list(model.parameters())

    mean = 0
    model_in = normalized_image
    # print(f'---Normalized sum: ', model_in.sum())
    # print(f'---Normalized mean: ', model_in.mean())
    # print(f'---Normalized min: ', model_in.min())
    # print(f'---Normalized max: ', model_in.max())
    # print(f'---Normalized shape: ', model_in.shape)
    # print(f'---Normalized hash: ', hash(normalized_image))
    model_out = model(model_in)
    # print(f'---Normalized sum: ', normalized_image.data.unsqueeze(0).cpu().sum())
    # print(f'---Normalized mean: ', normalized_image.data.unsqueeze(0).cpu().mean())
    # print(f'---Normalized hash: ', hash(normalized_image))
    # with open('/tmp/img.pkl', 'wb') as f:
    #     pickle.dump(normalized_image.data, f)   
    # print(model_out)
    # for output in model_out:
    #     mean += output
    # predicted = mean / len(model_out)
    # predicted = torch.sigmoid(predicted)
    predicted = torch.sigmoid(model_out)

    print(f'---Predicted: ', predicted)

    attentions = []
    first_layer_attentions_class = []
    second_layer_attentions_class = []
    third_layer_attentions_class = []

    fmaps = []
    CAM_feature = None

    for i in [1, 2]:
        inputs, fmap, final_feature = get_feature_maps(model,
                                                       'compatibility_score%d' % i,
                                                       upscale=False,
                                                       #    input_image=normalized_image.data.unsqueeze(0).cpu()
                                                       input_image=normalized_image
                                                       )  # .cuda())
        CAM_feature = final_feature

        if not fmap:
            continue

        # Output of the attention block
        fmap_0 = fmap[0].squeeze().permute(1, 2, 0).cpu().numpy()
        fmap_size = fmap_0.shape

        fmaps.append(fmap[0])
        # Attention coefficient (b x c x w x h x s)
        attention = fmap[1].squeeze().cpu().numpy()
        attention = attention[:, :]

        attention = attention - np.min(attention)
        attention = attention / np.max(attention)
        # attn_img = np.uint8(255 * attn_img)

        # attention = numpy.expand_dims(resize(attention, (fmap_size[0], fmap_size[1]), mode='constant', preserve_range=True), axis=2)
        attention = np.expand_dims(
            resize(
                attention,
                (normalized_image.shape[2], normalized_image.shape[3]),
                mode='constant',
                preserve_range=True),
            axis=2
        )

        attentions.append(attention)

        # blended_attention = blend_images(input_img, attention)

        if i == 1:
            weight_softmax = params[-8].data.cpu().numpy()
        elif i == 2:
            weight_softmax = params[-6].data.cpu().numpy()
        else:
            print('ERROR - undefined case')
            return

        # for j in range(num_classes):
        #    CAM = np.expand_dims(return_cam(fmap[0], weight_softmax, [j])[0], axis = 2)
        #    class_attention = np.mean([attention, CAM], 0)
        #    class_attention_blended = blend_images(input_img, class_attention)

        #    if i == 1:
        #        first_layer_attentions_class.append(class_attention_blended)
        #    elif i == 2:
        #        second_layer_attentions_class.append(class_attention_blended)
        #    else:
        #        print('ERROR - undefined case')
        #        return

    weight_softmax = params[-4].data.cpu().numpy()

    # print(attentions[0].shape)

    # return predicted, blend_images(input_img, np.random.rand(8,8,1), shape=(input_img.shape[1], input_img.shape[0]))
    if xtype == 'debugging':
        class_attentions = []
        for j in range(num_classes):
            CAM = np.expand_dims(return_cam(CAM_feature, weight_softmax, [j])[0], axis=2)
            # class_attention = np.mean([attentions[1], CAM], 0)
            class_attentions.append(CAM)
            # class_attention_blended = blend_images(input_img, class_attention, shape=(input_img.shape[1], input_img.shape[0]))

            # third_layer_attentions_class.append(class_attention_blended)
        return predicted, blend_images(input_img, np.mean(attentions, axis=0),
                                       shape=(input_img.shape[1], input_img.shape[0])), (attentions, class_attentions)
    elif xtype == 'chest_diag':
        # zero out first & last couple of rows / columns
        bordered_attn = np.mean(attentions, axis=0)

        # val = bordered_attn.min()

        # bordered_attn[:10, :] = val
        # bordered_attn[-10:, :] = val
        # bordered_attn[:, :10] = val
        # bordered_attn[:, -10:] = val

        return predicted, blend_images(input_img, bordered_attn,
                                       shape=(input_img.shape[1], input_img.shape[0])), attentions
    elif xtype == 'chest_screen':
        return predicted, blend_images(input_img, attentions[0],
                                       shape=(input_img.shape[1], input_img.shape[0])), attentions
    elif xtype == 'mura':
        return predicted, blend_images(input_img, np.mean(np.array(attentions), axis=0),
                                       shape=(input_img.shape[1], input_img.shape[0])), attentions
    elif xtype == 'covid':
        return predicted, blend_images(input_img, attentions[0],
                                       shape=(input_img.shape[1], input_img.shape[0])), attentions
    else:
        raise ValueError(f'Unknown xtype {xtype}')
