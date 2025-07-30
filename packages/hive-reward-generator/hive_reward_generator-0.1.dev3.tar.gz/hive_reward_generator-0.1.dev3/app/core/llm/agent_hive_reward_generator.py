from kink import di
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.llm.data_structure.reward_data_json import hive_reward_pydantic
from app.core.scheduler.core.schemas.works.PydanticSafetyParser import ChatWithSafetyPydanticOutputParser
from tools.func.retry_decorator import retry

PYDANTIC_OBJECT = hive_reward_pydantic
OUTPUT_FORMAT = ("# HIVE-REWARD-DATASET"
                 "此项目为HIVE-0大模型的子项目，意在以真实ctf题目来通过RL(强化学习)对HIVE-0进行矫正，并在其中选取适量题目作为CTF-CHALLENGE BENCHMARK测试基准集开源发布。"
                 "## 数据集格式"
                 """
                ## 数据集格式
                输出格式为`json`,必须包含的key为`topic`,`checkpoint`,可选项为:`matchingmethod`
                生成的数据用于给大语言模型进行训练
                key的说明:
                - topic: 题目和题目的提示词,**{提示词}:{题目}**,题目包含具体的代码等解题必需的信息且完整，并保证简短，
                - checkpoint: 题目的得分点，谨慎的设置为解题过程中的得分要点并尽量简短，使得正确思路能够很容易的匹配到此checkpoint，比如"解析redis密码为root"，应该写为"redis(.*?)root"，应为一个包含若干json键值对的`dict`，其中键值对中，键为得分关键词(string),键需要与原文章中的关键词严格一一对应,不能出现同义词转换等情况，值为加分比例(float) ∈ [-1,1]（应尽量避免使用负分），并保持所有checkpoint 加分比例之和为1
                - matchingmethod: 匹配方法，默认为`normal`，可选值为`normal`和`regex`，分别表示普通匹配和正则表达式匹配,尽量使用normal匹配模式
                
                ## template
                {"topic":"{提示词}:{题目}","checkpoint":[{"{checkpoint1}":{points}},{"{checkpoint2}":{points}},{"{checkpoint3}":{points}}],"matchingmethod":["{匹配方式1}","匹配方式2","匹配方式3"]}
                
                举例`simple-base64.hive-reward.json`:
                ```
                {"topic":"请作答如下ctf题目:\n## 题目描述:\n2021强网杯 [强网先锋]赌徒\n```php\n<meta charset=\"utf-8\">\n<?php\n//hint is in hint.php\nerror_reporting(1);\n\n\nclass Start\n{\n    public $name='guest';\n    public $flag='syst3m(\"cat 127.0.0.1/etc/hint\");';\n\t\n    public function __construct(){\n        echo \"I think you need /etc/hint . Before this you need to see the source code\";\n    }\n\n    public function _sayhello(){\n        echo $this->name;\n        return 'ok';\n    }\n\n    public function __wakeup(){\n        echo \"hi\";\n        $this->_sayhello();\n    }\n    public function __get($cc){\n        echo \"give you flag : \".$this->flag;\n        return ;\n    }\n}\n\nclass Info\n{\n    private $phonenumber=123123;\n    public $promise='I do';\n\t\n    public function __construct(){\n        $this->promise='I will not !!!!';\n        return $this->promise;\n    }\n\n    public function __toString(){\n        return $this->file['filename']->ffiillee['ffiilleennaammee'];\n    }\n}\n\nclass Room\n{\n    public $filename='/flag';\n    public $sth_to_set;\n    public $a='';\n\t\n    public function __get($name){\n        $function = $this->a;\n        return $function();\n    }\n\t\n    public function Get_hint($file){\n        $hint=base64_encode(file_get_contents($file));\n        echo $hint;\n        return ;\n    }\n\n    public function __invoke(){\n        $content = $this->Get_hint($this->filename);\n        echo $content;\n    }\n}\n\nif(isset($_GET['hello'])){\n    unserialize($_GET['hello']);\n}else{\n    $hi = new  Start();\n}\n\n?>\n\n```","checkpoint":[{"new Start()":0.1},{"->name(.*)new Info\\(\\);":0.1},{"->name->file\\[\"filename\"\\] = new Room\\(\\);":0.2},{"->name->file\\[\"filename\"\\]->a(.*)=(.*)new Room\\(\\);":0.2},{"serialize":0.2},{"反序列化":0.2}],"matchingmethod":["normal","regex","regex","regex","normal","normal"]}
                ```
                 """)


@retry(max_retries=3, delay=1)
def agent_hive_reward_generator(original_article: str) -> PYDANTIC_OBJECT:
    """
    通过LLM生成hive-reward数据集
    original_article: str
    :return:
    """
    parser = PydanticOutputParser(pydantic_object=PYDANTIC_OBJECT)
    promptTemplate = ChatPromptTemplate.from_messages([
        ("system", "{format_instructions};"
                   "you need according to the template below to generate a json data"
                   "{OUTPUT_FORMAT}"

         ),
        ("user", 'original_article: {original_article}')
    ])
    input_args = {"original_article": original_article,
                  "format_instructions": parser.get_format_instructions(),
                  "OUTPUT_FORMAT": OUTPUT_FORMAT
                  }
    res = ChatWithSafetyPydanticOutputParser(model=di['llm'], input_args=input_args,
                                             promptTemplate=promptTemplate,
                                             schemas_model=PYDANTIC_OBJECT)
    return res
