from pydantic import BaseModel


class AdvancedText(BaseModel):
    content: str


class RequirementDetail(AdvancedText):
    None


class RequirementRationale(AdvancedText):
    None


class RequirementComment(AdvancedText):
    None
