# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/08_learner.ipynb (unless otherwise specified).

__all__ = ['DetLearner']

# Cell
from .basics import *

# Cell
# Dsets is only train dataset for now
# TODO: Loading datset twice: Once for getting the len, other by detectron2 internals
# TODO: How to correctly hand max_iter and lr_schedule?
class DetLearner:
    def __init__(self, dset, mcfg, pretrained=True):
        self.dset = dset
        self.dset_len = self._dset_len()
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file(mcfg.mfile))
        cfg = mergedicts(cfg, mcfg.to_cfg())
        cfg.DATASETS.TRAIN,cfg.DATASETS.TEST = [dset],[]
        if pretrained: cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(mcfg.mfile)
        os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
        self.cfg = cfg

    def fit(self, n_epoch, lr, bs=None):
        cfg = self.cfg
        cfg.SOLVER.BASE_LR = lr
        cfg.SOLVER.IMS_PER_BATCH = bs
        trainer = DefaultTrainer(cfg)
        trainer.resume_or_load()
        trainer.max_iter = cfg.SOLVER.MAX_ITER = trainer.start_iter + int(n_epoch*(self.dset_len/bs))
        trainer.train()
        cfg.MODEL.WEIGHTS = str(Path(cfg.OUTPUT_DIR)/'model_final.pth')

    def load(self, name):
        cfg.MODEL.WEIGHTS = str(Path(cfg.OUTPUT_DIR)/name)
        trainer.resume_or_load()

    def _dset_len(self):
#         return len(self.trainer.data_loader.dataset.dataset._dataset._addr)
        return len(DatasetCatalog.get(self.dset))