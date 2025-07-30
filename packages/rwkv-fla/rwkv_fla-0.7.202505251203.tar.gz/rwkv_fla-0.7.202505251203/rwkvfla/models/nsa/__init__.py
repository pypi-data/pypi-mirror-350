# -*- coding: utf-8 -*-

from transformers import AutoConfig, AutoModel, AutoModelForCausalLM

from rwkvfla.models.nsa.configuration_nsa import NSAConfig
from rwkvfla.models.nsa.modeling_nsa import NSAForCausalLM, NSAModel

AutoConfig.register(NSAConfig.model_type, NSAConfig)
AutoModel.register(NSAConfig, NSAModel)
AutoModelForCausalLM.register(NSAConfig, NSAForCausalLM)


__all__ = [
    'NSAConfig', 'NSAModel', 'NSAForCausalLM',
]
