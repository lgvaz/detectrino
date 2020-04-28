import detectron2, cv2

from fastcore.all import *
from detectron2.config import CfgNode
from detectron2 import model_zoo
from detectron2.engine import SimpleTrainer, DefaultTrainer, DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, build_detection_test_loader
from detectron2.structures import BoxMode
from detectron2.structures.masks import mask_utils
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.evaluation import COCOEvaluator, inference_on_dataset

from detectron2.utils.logger import setup_logger
setup_logger()
