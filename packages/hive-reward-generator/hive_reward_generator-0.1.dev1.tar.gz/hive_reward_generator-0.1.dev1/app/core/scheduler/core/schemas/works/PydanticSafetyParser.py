import loguru
from langchain.output_parsers import OutputFixingParser
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.utils import Input
from pydantic import BaseModel


def ChatWithSafetyPydanticOutputParser(model: BaseChatModel, input_args: Input, promptTemplate: ChatPromptTemplate,
                                       schemas_model: BaseModel) -> BaseModel:
    """
    Chat with Safety Pydantic Output Parser
    :param model:
    :param input_args:
    :param promptTemplate:
    :param schemas_model:
    :return: Pydantic Model
    """
    parser = PydanticOutputParser(pydantic_object=schemas_model)
    chain = promptTemplate | model
    raw_output = chain.invoke(input_args)
    schemas_model_output = None
    try:
        str_content = str(raw_output.content)
        raw_output = str_content.split('</think>')[-1]
        schemas_model_output = parser.parse(raw_output)
    except OutputParserException as e:
        schemas_model_output = OutputFixingParser.from_llm(parser=parser, llm=model).parse(raw_output)
    return schemas_model_output
