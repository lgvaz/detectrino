# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/05_model.external.ipynb (unless otherwise specified).

__all__ = ['ModelCatalog']

# Cell
from fastai2.basics import *

# Cell
from ..basics import *
import pkg_resources

# Cell
class _ModelCatalog:
    def register(self, name, value): setattr(self, name, value)
ModelCatalog = _ModelCatalog()

# Cell
def _populate_model_catalog():
    cfg_file = Path(pkg_resources.resource_filename("detectron2.model_zoo", "configs"))
    fns = get_files(cfg_file, extensions='.yaml')
    fns = fns.map(lambda o: str(o.relative_to(cfg_file)))
    for fn in fns:
        name = fn.replace('-','_').replace('/','__').replace('.yaml','')
        ModelCatalog.register(name, fn)
_populate_model_catalog()