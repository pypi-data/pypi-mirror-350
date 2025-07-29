from core.llm.front_layer.slice import section

from core.scheduler.agent_scheduler_manager import agent_scheduler


def sec_report_writer(agent_name="网络安全领域的报告写手", **kwargs):
    """
    你是一名精通网络安全专家的报告写手，请根据输入的相关信息编写流量包的研判报告，编写过程中要注重主观、客观结合，并写出其攻击详情，并不要遗漏提供的任何一个材料。
    生成的报告请严格按照以上要求，且不要多说任何其他无关的话，包括询问问题、道歉等。
    """
    resp = agent_scheduler(agent_entry=sec_report_writer, agent_name=agent_name, **kwargs)
    return resp