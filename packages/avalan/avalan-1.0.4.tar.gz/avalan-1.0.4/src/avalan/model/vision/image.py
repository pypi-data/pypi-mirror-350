from ...model import TextGenerationVendor
from ...model.entities import ImageEntity, Input
from ...model.vision import BaseVisionModel
from ...model.transformer import TransformerModel
from PIL import Image
from torch import no_grad, Tensor
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    AutoModelForVision2Seq,
    PreTrainedModel,
)
from transformers.tokenization_utils_base import BatchEncoding
from typing import Literal

# model predicts one of the 1000 ImageNet classes
class ImageClassificationModel(BaseVisionModel):
    def _load_model(self) -> PreTrainedModel | TextGenerationVendor:
        self._processor = AutoImageProcessor.from_pretrained(
            self._model_id,
            # default behavior in transformers v4.48
            use_fast=True
        )
        model = AutoModelForImageClassification.from_pretrained(self._model_id)
        return model

    async def __call__(
        self,
        image_source: str | Image,
        tensor_format: Literal["pt"]="pt"
    ) -> ImageEntity:
        image = BaseVisionModel._get_image(image_source)
        inputs = self._processor(image, return_tensors=tensor_format)

        with no_grad():
            logits = self._model(**inputs).logits

        label_index = logits.argmax(dim=1).item()
        return ImageEntity(
            label=self._model.config.id2label[label_index]
        )

class ImageToTextModel(TransformerModel):
    def _load_model(self) -> PreTrainedModel | TextGenerationVendor:
        self._processor = AutoImageProcessor.from_pretrained(
            self._model_id,
            # default behavior in transformers v4.48
            use_fast=True
        )
        model = AutoModelForVision2Seq.from_pretrained(self._model_id)
        model.eval()
        return model

    def _tokenize_input(
        self,
        input: Input,
        context: str | None=None,
        tensor_format: Literal["pt"]="pt",
        **kwargs
    ) -> (
        dict[str,Tensor] | BatchEncoding | Tensor
    ):
        raise NotImplementedError()

    async def __call__(
        self,
        image_source: str | Image,
        skip_special_tokens: bool=True,
        tensor_format: Literal["pt"]="pt"
    ) -> str:
        image = BaseVisionModel._get_image(image_source)
        inputs = self._processor(images=image, return_tensors=tensor_format)
        output_ids = self._model.generate(**inputs)
        caption = self._tokenizer.decode(
            output_ids[0],
            skip_special_tokens=skip_special_tokens
        )
        return caption

