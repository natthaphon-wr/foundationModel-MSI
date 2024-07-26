# --------------------------------------------------------
# MIT License
#
# Copyright (c) 2024 Natthaphon Rotechanathamcharoen
# Licensed under The MIT License [see LICENSE for details]
#
# Contain functions that adapted from SimMIM by microsoft
# Available at: https://github.com/microsoft/SimMIM
#
# --------------------------------------------------------


from .swin_transformer import build_swin
from .vision_transformer import build_vit
from .simmim import build_simmim


def build_model(config, is_pretrain=True):
  if is_pretrain:
    model = build_simmim(config)
  else:
    model_type = config.MODEL.TYPE
    if model_type == 'swin':
      model = build_swin(config)
    elif model_type == 'vit':
      model = build_vit(config)
    else:
        raise NotImplementedError(f"Unknown fine-tune model: {model_type}")

  return model
