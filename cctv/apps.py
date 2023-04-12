from django.apps import AppConfig
from .segmentationCam import SegmentationModels

class CctvConfig(AppConfig):
    name = 'cctv'
    fcn_model = SegmentationModels("FCN")
    deeplab_model = SegmentationModels("DeepLab")
    unet_model = SegmentationModels("U_Net")
