# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_data.config.ipynb (unless otherwise specified).

__all__ = ['RLE', 'DataCfg', 'Record', 'Info', 'Annotation', 'BBox', 'from_xyxy_abs', 'from_rle', 'Seg', 'from_polys',
           'from_rle']

# Cell
from ..basics import *

# Cell
class RLE:
    def __init__(self, v, h, w): store_attr(self, 'v,h,w')
    @classmethod
    def from_str(cls, s, h, w):
        v = np.array(s.split(), dtype=np.uint)
        return cls(v, h, w)
    def __repr__(self): return str({'shape':(self.h,self.w), 'points':self.v})

# Cell
@patch
def decode(self:RLE):
    'From https://www.kaggle.com/julienbeaulieu/imaterialist-detectron2'
    mask = np.full(self.h*self.w, 0, dtype=np.uint8)
    for i, start_pixel in enumerate(self.v[::2]):
        mask[start_pixel: start_pixel+self.v[2*i+1]] = 1
    mask = mask.reshape((self.h, self.w), order='F')
    return mask

# Cell
@patch
def to_bbox(self:RLE):
    'From https://www.kaggle.com/julienbeaulieu/imaterialist-detectron2'
    shape = (self.h,self.w)
    a = self.v
    a = a.reshape((-1, 2))  # an array of (start, length) pairs
    a[:,0] -= 1  # `start` is 1-indexed
    y0 = a[:,0] % shape[0]
    y1 = y0 + a[:,1]
    if np.any(y1 > shape[0]):
        # got `y` overrun, meaning that there are a pixels in mask on 0 and shape[0] position
        y0 = 0
        y1 = shape[0]
    else:
        y0 = np.min(y0)
        y1 = np.max(y1)
    x0 = a[:,0] // shape[0]
    x1 = (a[:,0] + a[:,1]) // shape[0]
    x0 = np.min(x0)
    x1 = np.max(x1)
    if x1 > shape[1]:
        # just went out of the image dimensions
        raise ValueError("invalid self or image dimensions: x1=%d > shape[1]=%d" % (
            x1, shape[1]
        ))
    return x0, y0, x1, y1

# Cell
class DataCfg:
    def to_cfg(self):   raise NotImplementedError
    def __repr__(self): return self.to_cfg().__repr__()

# Cell
class Record(DataCfg):
    def __init__(self, info, annons): self.info,self.annons = info,L(annons)
    def to_cfg(self): return {**self.info.to_cfg(),
                              'annotations':[o.to_cfg() for o in self.annons]}

# Cell
class Info(DataCfg):
    def __init__(self, id, fn, h, w): store_attr(self, 'fn,id,h,w')
    def to_cfg(self): return {'file_name':self.fn,'image_id':self.id,'height':self.h,'width':self.w}

# Cell
class Annotation(DataCfg):
    def __init__(self, id, bbox, seg, iscrowd=0): store_attr(self, 'id,bbox,seg,iscrowd')
    def to_cfg(self): return {**self.bbox.to_cfg(), **self.seg.to_cfg(),
                              'category_id':self.id, 'iscrowd':self.iscrowd}

# Cell
class BBox(DataCfg):
    def __init__(self, pts, mode): self.pts,self.mode = pts,mode
    def to_cfg(self): return {'bbox':self.pts, 'bbox_mode':self.mode}

# Cell
@patch_classmethod
def from_xyxy_abs(cls:BBox, pts): return cls(pts, BoxMode.XYXY_ABS)

# Cell
@patch_classmethod
def from_rle(cls:BBox, rle): return cls(rle.to_bbox(), BoxMode.XYXY_ABS)

# Cell
class Seg(DataCfg):
    def __init__(self, polys): self.polys = polys
    def to_cfg(self): return {'segmentation':self.polys}

# Cell
@patch_classmethod
def from_polys(cls:Seg, polys): return cls(polys)

# Cell
@patch_classmethod
def from_rle(cls:Seg, rle):
    mask = rle.decode()
    conts,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    seg = []
    for cont in conts:
        cont = cont.flatten().tolist()
        if len(cont) > 4: seg.append(cont)
    return cls(seg)