import torch
import torch.nn as nn
from typing import Optional, Mapping, Union

from .base import Merger, Compose


class SegmentationTTAWrapper(nn.Module):
    def __init__(
        self,
        model: nn.Module,
        transforms: Compose,
        merge_mode: str = "mean",
        output_mask_key: Optional[str] = None,
    ):
        super().__init__()
        self.model = model
        self.transforms = transforms
        self.merge_mode = merge_mode
        self.output_mask_key = output_mask_key

    def forward(
        self, image: torch.Tensor, *args
    ) -> Union[torch.Tensor, Mapping[str, torch.Tensor]]:
        merger = Merger(type=self.merge_mode, n=len(self.transforms))

        for transformer in self.transforms:
            augmented_image = transformer.augment_image(image)
            augmented_output = self.model(augmented_image, *args)
            if self.output_key is not None:
                augmented_output = augmented_output[self.output_key]
            deaugmented_output = transformer.deaugment_mask(augmented_output)
            merger.append(deaugmented_output)

        result = merger.result
        if self.output_key is not None:
            result = {self.output_key: result}

        return result


class ClassificationTTAWrapper(nn.Module):
    def __init__(
        self,
        model: nn.Module,
        transforms: Compose,
        merge_mode: str = "mean",
        output_label_key: Optional[str] = None,
    ):
        super().__init__()
        self.model = model
        self.transforms = transforms
        self.merge_mode = merge_mode
        self.output_label_key = output_label_key

    def forward(
        self, image: torch.Tensor, *args
    ) -> Union[torch.Tensor, Mapping[str, torch.Tensor]]:
        merger = Merger(type=self.merge_mode, n=len(self.transforms))

        for transformer in self.transforms:
            augmented_image = transformer.augment_image(image)
            augmented_output = self.model(augmented_image, *args)
            if self.output_label_key is not None:
                augmented_output = augmented_output[self.output_label_key]
            deaugmented_output = transformer.deaugment_label(augmented_output)
            merger.append(deaugmented_output)

        result = merger.result
        if self.output_label_key is not None:
            result = {self.output_label_key: result}

        return result
