# 移除或注释掉原来的导入
#: code: utf-8

from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from agentcp.agentcp import AgentCP, AgentID

__version__ = "0.1.57"

__all__ = ["VERSION", "AgentCP", "AgentID"]