import datetime
import json

import typer

from app.core.config import Master
from app.core.invoke.generator_hive_reward_from_url import generator_hive_reward_pydantic_from_url
from app.core.invoke.io.reader import reader
from app.core.llm.data_structure.reward_data_json import hive_reward_pydantic
from app.core.validator.hive_reward_validator import validator

app = typer.Typer(
    name="hive-reward.json 生成器",
    no_args_is_help=True,
)


@app.command()
def generator(
        url: str = typer.Argument(..., help="静态文件的url(local file & http(s) static file)"),
        output_path: str = typer.Argument(f"tmp-{datetime.datetime.now().strftime('%Y%m%d')}.hive-reward.json",
                                          help="Output hive-reward.json path"),
        api_endpoint: str = typer.Option("https://www.gptapi.us/v1", help="Openai api endpoint"),
        api_key: str = typer.Option("sk-什么呢...", help="Openai api key"),
        default_model: str = typer.Option("o1-preview", help="Openai model"),

):
    """
    解析静态文章，生成hive-reward.json

    :param url: 静态文件的url(local file & http(s) static file)
    :param output_path: 输出的报告路径
    :param api_endpoint: openai api endpoint
    :param api_key: openai api key
    :param default_model: openai model
    :return:
    """
    Master['openai_api_endpoint'] = api_endpoint
    Master['openai_api_key'] = api_key
    Master['default_model'] = default_model
    result = generator_hive_reward_pydantic_from_url(url=url)
    json.dumps(result.json(), ensure_ascii=False, indent=4)


@app.command()
def validate(hive_reward_json_path: str, original_article_path: str) -> bool:
    """
    验证hive-reward.json的合法性

    :param original_article_path:
    :param hive_reward_json_path:
    :return:
    """
    body = reader(url=hive_reward_json_path)
    original_article = reader(url=original_article_path)
    return validator(original_article=original_article, hive_reward=hive_reward_pydantic(**json.loads(body)))


def main():
    app()


if __name__ == "__main__":
    main()
