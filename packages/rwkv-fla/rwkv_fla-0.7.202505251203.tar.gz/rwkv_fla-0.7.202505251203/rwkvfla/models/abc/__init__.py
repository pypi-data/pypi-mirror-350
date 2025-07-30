# -*- coding: utf-8 -*-

from transformers import AutoConfig, AutoModel, AutoModelForCausalLM

from rwkvfla.models.abc.configuration_abc import ABCConfig
from rwkvfla.models.abc.modeling_abc import ABCForCausalLM, ABCModel

AutoConfig.register(ABCConfig.model_type, ABCConfig)
AutoModel.register(ABCConfig, ABCModel)
AutoModelForCausalLM.register(ABCConfig, ABCForCausalLM)


__all__ = ['ABCConfig', 'ABCForCausalLM', 'ABCModel']
