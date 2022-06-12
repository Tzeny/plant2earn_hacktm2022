from collections import OrderedDict

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.densenet import _DenseBlock, _Transition

try:
    from attention.grid_attention_layer import GridAttentionBlock2D_TORR as GridAttentionBlock2D
except ImportError:
    from .grid_attention_layer import GridAttentionBlock2D_TORR as GridAttentionBlock2D

class AttentionDensenet(nn.Module):

    def __init__(self, growth_rate=32, block_config=(6, 12, 24, 16),
                 num_init_features=64, bn_size=4, drop_rate=0, num_classes=1,
                 nonlocal_mode='concatenation_mean_flow', aggregation='mean', aggregation_mode='mean'
                 ):

        super(AttentionDensenet, self).__init__()

        self.features = nn.Sequential(OrderedDict([
            ('conv0', nn.Conv2d(3, num_init_features, kernel_size=7, stride=2,
                                padding=3, bias=False)),
            ('norm0', nn.BatchNorm2d(num_init_features)),
            ('relu0', nn.ReLU(inplace=True)),
            ('pool0', nn.MaxPool2d(kernel_size=3, stride=2, padding=1)),
        ]))

        self.feature_numbers = {}
        self.blocks = {}
        # frontal branch
        num_features = num_init_features
        for i, num_layers in enumerate(block_config):
            block = _DenseBlock(num_layers=num_layers, num_input_features=num_features,
                                bn_size=bn_size, growth_rate=growth_rate,
                                drop_rate=drop_rate)
            self.features.add_module('denseblock%d' % (i + 1), block)
            self.feature_numbers['denseblock%d' % (i + 1)] = num_features
            self.blocks['denseblock%d' % (i + 1)] = block

            num_features = num_features + num_layers * growth_rate

            if i != len(block_config) - 1:
                trans = _Transition(num_input_features=num_features,
                                    num_output_features=num_features // 2)
                self.features.add_module('transition%d' % (i + 1), trans)
                num_features = num_features // 2
                self.feature_numbers['denseblock%d' % (i + 1)] = num_features

        self.feature_numbers['norm5'] = num_features
        self.features.add_module('norm5', nn.BatchNorm2d(num_features))  # Final batch norm

        # self.classifier = nn.Linear(num_features, num_classes)
        #         print('denseblock2 ', self.feature_numbers['denseblock2'])
        #         print('denseblock3 ',self.feature_numbers['denseblock3'])
        #         print('denseblock4 ',self.feature_numbers['denseblock4'])
        #         print('norm5 ',self.feature_numbers['norm5'])
        self.compatibility_score1 = GridAttentionBlock2D(in_channels=self.feature_numbers['denseblock3'],
                                                         gating_channels=self.feature_numbers['norm5'],
                                                         inter_channels=self.feature_numbers['norm5'],
                                                         sub_sample_factor=(1, 1),
                                                         mode=nonlocal_mode, use_W=False, use_phi=True,
                                                         use_theta=True, use_psi=True, nonlinearity1='relu')

        self.compatibility_score2 = GridAttentionBlock2D(in_channels=self.feature_numbers['norm5'],
                                                         gating_channels=self.feature_numbers['norm5'],
                                                         inter_channels=self.feature_numbers['norm5'],
                                                         sub_sample_factor=(1, 1),
                                                         mode=nonlocal_mode, use_W=False, use_phi=True,
                                                         use_theta=True, use_psi=True, nonlinearity1='relu')

        # print(self.feature_numbers)
        # print(self.blocks)

        #########################
        # Aggreagation Strategies
        if aggregation_mode == 'concat':
            self.classifier = nn.Linear(filters[2] + filters[3] + filters[3], n_classes)
            self.aggregate = self.aggreagation_concat
        else:
            self.classifier1 = nn.Linear(self.feature_numbers['denseblock3'], num_classes)
            self.classifier2 = nn.Linear(self.feature_numbers['norm5'], num_classes)
            self.classifier3 = nn.Linear(self.feature_numbers['norm5'], num_classes)
            self.classifiers = [self.classifier1, self.classifier2, self.classifier3]

            if aggregation_mode == 'mean':
                self.aggregate = self.aggregation_sep

            elif aggregation_mode == 'ft':
                self.classifier = nn.Linear(num_classes*3, num_classes)

                # init weights so that it copies the mean function
                with torch.no_grad():
                    # init biases to 0
                    for i in range(num_classes):
                        self.classifier.bias[i] = 0.

                    # init weights
                    for i in range(num_classes): # 17 outputs
                        for j in range(num_classes*3): # 51 inputs
                            self.classifier.weight[i,j] = 0

                            if (j - i) % num_classes == 0:
                                self.classifier.weight[i,j] = 1/3

                #print(self.classifier.weight)

                self.aggregate = self.aggregation_ft
            else:
                raise NotImplementedError

        # Official init from torch repo.
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.constant_(m.bias, 0)

    def aggregation_sep(self, *attended_maps):
        return [clf(att) for clf, att in zip(self.classifiers, attended_maps)]

    def aggregation_ft(self, *attended_maps):
        preds = self.aggregation_sep(*attended_maps)
        return self.classifier(torch.cat(preds, dim=1))

    def forward(self, x):
        block2_out = None
        block3_out = None
        batch_size = x.shape[0]

        for idx, (name, l) in enumerate(self.features.named_children()):

            if name == 'conv0':
                features = l(x)
            else:
                features = l(features)

                if name == 'denseblock2':
                    block2_out = features
                elif name == 'denseblock3':
                    block3_out = features
        #         print(block2_out.shape)
        #         print(features.shape)
        g_conv1, att1 = self.compatibility_score1(block2_out, features)
        g_conv2, att2 = self.compatibility_score2(block3_out, features)

        #         features = self.features(x)
        #         out = F.relu(features, inplace=True)
        #         out = F.adaptive_avg_pool2d(out, (1, 1))
        #         out = torch.flatten(out, 1)
        #         out = self.classifier(out)
        #         return out
        pooled = F.adaptive_avg_pool2d(features, (1, 1)).view(batch_size, -1)

        g1 = torch.sum(g_conv1.view(batch_size, self.feature_numbers['denseblock3'], -1), dim=-1)
        g2 = torch.sum(g_conv2.view(batch_size, self.feature_numbers['norm5'], -1), dim=-1)

        return self.aggregate(g1, g2, pooled)


def _attention_densenet(arch, growth_rate, block_config, num_init_features, progress,
                        **kwargs):
    model = AttentionDensenet(growth_rate, **kwargs)
    return model


def attention_densenet121(pretrained=False, progress=True, **kwargs):
    r"""Densenet-121 model from
    `"Densely Connected Convolutional Networks" <https://arxiv.org/pdf/1608.06993.pdf>`_
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _attention_densenet('multi_input_densenet121', 32, (6, 12, 24, 16), 64, progress,
                               **kwargs)


def attention_densenet121_ft(pretrained=False, progress=True, **kwargs):
    r"""Densenet-121 model from
    `"Densely Connected Convolutional Networks" <https://arxiv.org/pdf/1608.06993.pdf>`_
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _attention_densenet('multi_input_densenet121', 32, (6, 12, 24, 16), 64, progress, aggregation_mode='ft'
                                                                                                              ** kwargs)




if __name__ == '__main__':
    from torchsummary import summary

    print('Initializing model')

    model = attention_densenet121(True, num_classes=14, aggregation_mode='ft')
    # model.load_state_dict(torch.load('/xvision-models/08.12.2019-01:27:05_ATTENTION_CHEXPERT_MIXUP_FOCAL_TOP_ONLY_stage1_19_state_dict.pt'))
    model.eval()

    print(summary(model, (3, 256, 256), device='cpu'))
