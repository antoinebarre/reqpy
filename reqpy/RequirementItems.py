from pydantic import BaseModel, Field


class AdvancedText(str):
    
    def __new__(cls, content: str):
        return super().__new__(cls, content)

    # class Config:
    #     """Configuration class for the AdvancedText class.

    #     Attributes:
    #         allow_mutation (bool): Whether mutation is allowed for
    #         the class GenericFolder.
    #         validate_assignment (bool): Whether to activate validation
    #         for assignment.
    #         extra (str): How to handle unknown fields.

    #     """
    #     allow_mutation = False
    #     validate_assignment = True
    #     extra = 'forbid'

    def test(self):
        print("aller le sco")
        return self.center(20)




class RequirementDetail(AdvancedText):
    pass


class RequirementRationale(AdvancedText):
    # content: str = Field(
    #     min_length=0,
    #     max_length=40,
    # )

    def __new__(cls, content: str):
        return super().__new__(cls, content)


class RequirementComment(AdvancedText):
    pass
