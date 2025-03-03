from keras_cv_attention_models.cmt.cmt import CMT, CMTTiny, CMTXS, CMTSmall, CMTBig, light_mhsa_with_multi_head_relative_position_embedding

__head_doc__ = """
Keras implementation of CMT.
Paper [PDF 2107.06263 CMT: Convolutional Neural Networks Meet Vision Transformers](https://arxiv.org/pdf/2107.06263.pdf).
"""

__tail_doc__ = """  input_shape: it should have exactly 3 inputs channels, like `(224, 224, 3)`.
  num_classes: number of classes to classify images into. Set `0` to exclude top layers.
  activation: activation used in whole model, default `relu`.
  drop_connect_rate: is used for [Deep Networks with Stochastic Depth](https://arxiv.org/abs/1603.09382).
      Can be value like `0.2`, indicates the drop probability linearly changes from `0 --> 0.2` for `top --> bottom` layers.
      A higher value means a higher probability will drop the deep branch.
      or `0` to disable (default).
  classifier_activation: A `str` or callable. The activation function to use on the "top" layer if `num_classes > 0`.
      Set `classifier_activation=None` to return the logits of the "top" layer.
  dropout: dropout rate if top layers is included.
  pretrained: None or "imagenet". Only CMTTiny pretrained available.
  **kwargs: other parameters if available.

Returns:
    A `keras.Model` instance.
"""

CMT.__doc__ = __head_doc__ + """
Args:
  num_blocks: number of blocks in each stack.
  out_channels: output channels for each stack.
  stem_width: output dimension for stem block.
  num_heads: heads number for transformer block.
  sr_ratios: attenstion blocks key_value downsample rate.
  ffn_expansion: IRFFN blocks hidden expansion rate.
  model_name: string, model name.
""" + __tail_doc__ + """
Model architectures:
  | Model                              | Params | FLOPs | Input | Top1 Acc |
  | ---------------------------------- | ------ | ----- | ----- | -------- |
  | CMTTiny, (Self trained 105 epochs) | 9.5M   | 0.65G | 160   | 77.4     |
  | - 305 epochs                       | 9.5M   | 0.65G | 160   | 78.94    |
  | - fine-tuned 224 (69 epochs)       | 9.5M   | 1.32G | 224   | 80.73    |
  | CMTTiny, 1000 epochs               | 9.5M   | 0.65G | 160   | 79.2     |
  | CMTXS                              | 15.2M  | 1.58G | 192   | 81.8     |
  | CMTSmall                           | 25.1M  | 4.09G | 224   | 83.5     |
  | CMTBig                             | 45.7M  | 9.42G | 256   | 84.5     |
"""

CMTTiny.__doc__ = __head_doc__ + """
Args:
""" + __tail_doc__

CMTXS.__doc__ = CMTTiny.__doc__
CMTSmall.__doc__ = CMTTiny.__doc__
CMTBig.__doc__ = CMTTiny.__doc__

light_mhsa_with_multi_head_relative_position_embedding.__doc__ = __head_doc__ + """
Light multi head self attention with relative position embedding. Defined as function, not layer.
Downsample `key_value` with a `sr_ratio` using `DepthwiseConv2D` + `LayerNorm`.
Also adds `MultiHeadRelativePositionalEmbedding` to `attention_scores`.

Args:
  inputs: input tensor.
  num_heads: Number of attention heads.
  key_dim: Size of each attention head for query, key and value. Default `0` for `key_dim = inputs.shape[-1] // num_heads`.
  sr_ratio: `key_value` downsample rate.
  out_shape: The expected shape of an output tensor. If not specified, projects back to the input dim.
  out_weight: Boolean, whether use an ouput dense.
  out_bias: Boolean, whether the ouput dense layer use bias vectors/matrices.
  attn_dropout: Dropout probability for attention.

Examples:

>>> from keras_cv_attention_models import attention_layers
>>> inputs = keras.layers.Input([14, 16, 256])
>>> nn = attention_layers.light_mhsa_with_multi_head_relative_position_embedding(inputs, num_heads=4, sr_ratio=3, out_shape=512, name="attn_")
>>> print(f"{nn.shape = }")
# nn.shape = TensorShape([None, 14, 16, 512])

>>> mm = keras.models.Model(inputs, nn)
>>> mm.summary()
>>> print({ii.name: ii.shape for ii in mm.weights})
# {'attn_kv_sr_dw_conv/depthwise_kernel:0': TensorShape([3, 3, 256, 1]),
#  'attn_kv_sr_ln/gamma:0': TensorShape([256]),
#  'attn_kv_sr_ln/beta:0': TensorShape([256]),
#  'attn_query/kernel:0': TensorShape([256, 256]),
#  'attn_key_value/kernel:0': TensorShape([256, 512]),
#  'attn_pos_emb/positional_embedding:0': TensorShape([4, 837]),
#  'attn_output/kernel:0': TensorShape([256, 512])}
"""
