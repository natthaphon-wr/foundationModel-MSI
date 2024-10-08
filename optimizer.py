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


import json
from functools import partial
from torch import optim as optim

# def build_optimizer(config, model, logger, is_pretrain):
#   if is_pretrain:
#     return build_pretrain_optimizer(config, model, logger)


def build_pretrain_optimizer(config, model, logger):
  logger.info('>>>>>>>>>> Build Optimizer for Pre-training Stage')
  skip = {}
  skip_keywords = {}
  if hasattr(model, 'no_weight_decay'):
    skip = model.no_weight_decay()
    logger.info(f'No weight decay: {skip}')
  if hasattr(model, 'no_weight_decay_keywords'):
    skip_keywords = model.no_weight_decay_keywords()
    logger.info(f'No weight decay keywords: {skip_keywords}')

  parameters = get_pretrain_param_groups(model, logger, skip, skip_keywords)

  opt_lower = config.TRAIN.OPTIMIZER.NAME.lower()
  optimizer = None
  if opt_lower == 'sgd':
    optimizer = optim.SGD(parameters, momentum=config.TRAIN.OPTIMIZER.MOMENTUM, nesterov=True,
                          lr=config.TRAIN.BASE_LR, weight_decay=config.TRAIN.WEIGHT_DECAY)
  elif opt_lower == 'adamw':
    optimizer = optim.AdamW(parameters, eps=config.TRAIN.OPTIMIZER.EPS, betas=config.TRAIN.OPTIMIZER.BETAS,
                            lr=config.TRAIN.BASE_LR, weight_decay=config.TRAIN.WEIGHT_DECAY)

  logger.info(optimizer)
  return optimizer
    

def get_pretrain_param_groups(model, logger, skip_list=(), skip_keywords=()):
  has_decay = []
  no_decay = []
  has_decay_name = []
  no_decay_name = []
  
  for name, param in model.named_parameters():
    if not param.requires_grad:
      continue
    if len(param.shape) == 1 or name.endswith(".bias") or (name in skip_list) or \
        check_keywords_in_name(name, skip_keywords):
      no_decay.append(param)
      no_decay_name.append(name)
    else:
      has_decay.append(param)
      has_decay_name.append(name)
  logger.info(f'No decay params: {no_decay_name}')
  logger.info(f'Has decay params: {has_decay_name}')
  return [{'params': has_decay}, {'params': no_decay, 'weight_decay': 0.}]


# def get_vit_layer(name, num_layers):
#   if name in ("cls_token", "mask_token", "pos_embed"):
#     return 0
#   elif name.startswith("patch_embed"):
#     return 0
#   elif name.startswith("rel_pos_bias"):
#     return num_layers - 1
#   elif name.startswith("blocks"):
#     layer_id = int(name.split('.')[1])
#     return layer_id + 1
#   else:
#     return num_layers - 1


# def get_swin_layer(name, num_layers, depths):
#   if name in ("mask_token"):
#     return 0
#   elif name.startswith("patch_embed"):
#     return 0
#   elif name.startswith("layers"):
#     layer_id = int(name.split('.')[1])
#     block_id = name.split('.')[3]
#     if block_id == 'reduction' or block_id == 'norm':
#         return sum(depths[:layer_id + 1])
#     layer_id = sum(depths[:layer_id]) + int(block_id)
#     return layer_id + 1
#   else:
#     return num_layers - 1


def check_keywords_in_name(name, keywords=()):
  isin = False
  for keyword in keywords:
    if keyword in name:
      isin = True
  return isin