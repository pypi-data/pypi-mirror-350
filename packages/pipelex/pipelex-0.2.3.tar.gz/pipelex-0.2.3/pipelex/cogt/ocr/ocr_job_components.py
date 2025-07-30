from pydantic import BaseModel

from pipelex.tools.config.models import ConfigModel


class OcrJobParams(BaseModel):
    should_include_images: bool
    should_caption_images: bool
    should_include_page_views: bool
    page_views_dpi: int

    @classmethod
    def make_default_ocr_job_params(cls) -> "OcrJobParams":
        return OcrJobParams(
            should_caption_images=False,
            should_include_page_views=False,
            should_include_images=True,
            page_views_dpi=300,
        )


class OcrJobConfig(ConfigModel):
    pass


########################################################################
### Outputs
########################################################################


class OcrJobReport(ConfigModel):
    pass
