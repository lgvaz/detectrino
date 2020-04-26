# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_data.core.ipynb (unless otherwise specified).

__all__ = ['DsetLoader', 'register_dset', 'draw_labels']

# Cell
from ..basics import *
from fastai2.vision.all import *

# Cell
class DsetLoader:
    def __init__(self, source, name, create_dset):
        self.source,self.name,self.create_dset = Path(source),name,create_dset

    def __call__(self, force):
        path = self.source/f'dsets/{self.name}.pkl'
        path.parent.mkdir(exist_ok=True)
        if not force:
            try:
                with open(str(path), 'rb') as f: return pickle.load(f)
            except FileNotFoundError: pass
        dset = self.create_dset()
        with open(str(path), 'wb') as f: pickle.dump(dset, f)
        return dset

# Cell
DatasetCatalog.force = False

# Cell
def _get(name):
    try: f = DatasetCatalog._REGISTERED[name]
    except KeyError:
        msg = "Dataset '{}' is not registered! Available datasets are: {}"
        raise KeyError(msg.format(name, ", ".join(DatasetCatalog._REGISTERED.keys())))
    return f(DatasetCatalog.force) if isinstance(f, DsetLoader) else f()
DatasetCatalog.get = _get

# Cell
def register_dset(name, f, meta=None, path=None):
    path, meta = path or storage_path, meta or {}
    DatasetCatalog.register(name, DsetLoader(path, name, f))
    MetadataCatalog.get(name).set(**meta)

# Cell
@delegates(Visualizer)
def draw_labels(d, meta, **kwargs):
    im = PILImage.create(d['file_name'])
    v = Visualizer(im.numpy(), meta).draw_dataset_dict(d)
    return PILImage.create(v.get_image())