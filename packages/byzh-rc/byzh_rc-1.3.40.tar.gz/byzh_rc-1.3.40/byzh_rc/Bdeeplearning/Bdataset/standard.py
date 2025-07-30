import numpy as np
import torch
def b_data_standard1d(source_data, target_datas: list):

    if type(source_data) == torch.Tensor:
        mean = torch.mean(source_data, dim=(0, 2), keepdim=True)
        std = torch.std(source_data, dim=(0, 2), keepdim=True) + 1e-8
    # elif type(source_data) == np.ndarray:
    else:
        mean = np.mean(source_data, axis=(0, 2), keepdims=True)
        std = np.std(source_data, axis=(0, 2), keepdims=True) + 1e-8

    results = []
    for target_data in target_datas:
        target_data = (target_data - mean) / std
        results.append(target_data)

    return results