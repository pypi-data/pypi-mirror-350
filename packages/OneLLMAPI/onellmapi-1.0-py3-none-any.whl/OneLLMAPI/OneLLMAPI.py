import copy
import hashlib
import time
import requests
import json
from dashscope import Generation
from openai import OpenAI
from baidubce.auth import bce_credentials
from baidubce import bce_base_client, bce_client_configuration


# 一个用于处理聊天消息的基类
class OneLLM:
    url = ''  # 用于API请求的URL
    messages = []  # 存储对话消息的列表

    def clean_history(self, keep_num: int = 5):
        """
                清理聊天历史记录，保留最新的若干条消息。
                参数:
                    keep_num (int): 要保留的消息数量，默认为5。

                返回:
                    str: 清除历史记录的状态消息。
                        - 如果历史记录长度大于保留数量的两倍加一，则返回“已完成历史清除！”。
                        - 否则返回“无需清除！”。
                """
        if len(self.messages) > keep_num * 2 + 1:
            self.messages = self.messages[0] + self.messages[-keep_num * 2:]
            return "已完成历史清除！"
        else:
            return "无需清除！"


# zhipu api
class Zhipu(OneLLM):
    """
       一个与Zhipu AI模型进行API交互的类。
       属性：
           url (str): 聊天补全的API端点。
           request_id (str): 每个请求的唯一标识符。
           messages (list): 存储对话消息的列表。
           api_key (str): 用于身份验证的API密钥。
           model (str): 用于补全的模型。
           system_msg (str): 可选的系统消息，用于上下文。
           stream (bool): 是否使用流式响应。
           do_sample (bool): 是否对响应进行采样。
           temperature (float): 控制响应的随机性。
           top_p (float): 通过核采样控制多样性。
           max_tokens (int): 响应中生成的最大令牌数。
           response_format (str): 响应的期望格式（例如，文本）。
           stop (list): 停止响应生成的标准。
           tools (list): 可用于交互的工具。
           type (str): 交互类型。
           tool_choice: 选中的工具。
           user_id (str): 用户的唯一标识符。
       """
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    request_id = None
    messages = []

    def __init__(self, api_key, model, system_msg=None, stream=False, do_sample=True, temperature=None, top_p=None,
                 max_tokens=None, response_format=None, stop=None, tools=None, type=None, tool_choice=None,
                 user_id=None):
        """
               使用必需参数初始化Zhipu实例。
               参数：
                   api_key (str): 访问模型的API密钥。
                   model (str): 要用于生成补全的模型。
                   system_msg (str, 可选): 可选的系统消息，用于设置上下文。
                   stream (bool, 可选): 是否启用流式响应。
                   do_sample (bool, 可选): 控制是否执行采样。
                   temperature (float, 可选): 采样温度。
                   top_p (float, 可选): 核采样参数。
                   max_tokens (int, 可选): 响应中的最大令牌数。
                   response_format (str, 可选): 响应的格式。
                   stop (list, 可选): 停止序列的列表。
                   tools (list, 可选): 可用于助理的工具列表。
                   type (str, 可选): 交互类型。
                   tool_choice: 选中的工具。
                   user_id (str, 可选): 制作请求的用户标识符。
               """
        self.api_key = api_key
        self.model = model
        self.system_msg = system_msg
        self.stream = stream
        self.dosome_sample = do_sample
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.response_format = response_format
        self.stop = stop
        self.tools = tools
        self.type = type
        self.tool_choice = tool_choice
        self.user_id = user_id
        if self.system_msg:
            self.messages.append({'role': 'system', 'content': self.system_msg})

    def getHistory(self):
        return self.messages

    def getAPiKey(self):
        return self.api_key

    def setAPiKey(self, value):
        self.api_key = value

    def getModel(self):
        return self.model

    def setModel(self, model):
        self.model = model

    def getSystemMsg(self):
        return self.system_msg

    def setSystemMsg(self, value):
        self.system_msg = value
        if value:
            self.messages.append({'role': 'system', 'content': value})

    def getStream(self):
        return self.stream

    def setStream(self, value):
        self.stream = value

    def getDoSample(self):
        return self.dosome_sample

    def setDoSample(self, value):
        self.dosome_sample = value

    def getTemperature(self):
        return self.temperature

    def setTemperature(self, value):
        self.temperature = value

    def getTopP(self):
        return self.top_p

    def setTopP(self, value):
        self.top_p = value

    def getMaxTokens(self):
        return self.max_tokens

    def setMaxTokens(self, value):
        self.max_tokens = value

    def getStop(self):
        return self.stop

    def setStop(self, value):
        self.stop = value

    def getTools(self):
        return self.tools

    def setTools(self, value):
        self.tools = value

    def getType(self):
        return self.type

    def setType(self, value):
        self.type = value

    def getToolChoice(self):
        return self.tool_choice

    def setToolChoice(self, value):
        self.tool_choice = value

    def getUserId(self):
        return self.user_id

    def setUserId(self, value):
        self.user_id = value

    def getRequestId(self):
        return self.request_id

    def get_resp(self, completion):
        """
                从补全输出中提取响应内容。
                参数：
                    completion (dict): 从API返回的补全响应。
                返回：
                    str: 响应消息的内容。
        """
        return completion['choices'][0]['message'].get('content', "")

    def get_request(self, messages):
        """
        准备并发送POST请求到API。
        参数：
            messages (list): 要发送的消息列表。
        返回：
            dict: 来自API的JSON响应或错误时返回None。
        """
        payload_base = {
            "model": self.model,
            "messages": self.messages
        }

        # 添加可选参数到有效负载中
        if self.type != None:
            payload_base['type'] = self.type
        if self.max_tokens != None:
            payload_base['max_tokens'] = self.max_tokens
        if self.tool_choice != None:
            payload_base['tool_choice'] = self.tool_choice
        if self.user_id != None:
            payload_base['user_id'] = self.user_id
        if self.request_id:
            payload_base['request_id'] = self.request_id
        if self.stop:
            payload_base['stop'] = self.stop
        if self.tools:
            payload_base['tools'] = self.tools
        if self.response_format:
            payload_base['response_format'] = self.response_format
        if self.temperature:
            payload_base['temperature'] = self.temperature
        if self.top_p:
            payload_base['top_p'] = self.top_p
        if self.max_tokens:
            payload_base['max_tokens'] = self.max_tokens
        if self.stream:
            payload_base['stream'] = self.stream
        if self.dosome_sample:
            payload_base['dosome_sample'] = self.dosome_sample

        payload = json.dumps(payload_base)
        headers = {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json'
        }

        response = requests.post(self.url, headers=headers, data=payload)

        # response = requests.request("POST", self.url, headers=headers, data=payload)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        else:
            response_json = json.loads(response.text)
            self.request_id = response_json['request_id']
            return response_json

    def send(self, msg):
        """
        发送用户消息并获取AI的响应。
        参数：
            msg (str): 用户发送的消息。
        返回：
            str: AI的响应消息。
        """

        self.messages.append({'role': 'user', 'content': msg})

        completion = self.get_request(self.messages)

        if completion:
            resp = self.get_resp(completion)
            self.messages.append({'role': 'assistant', 'content': resp})
            return resp
        else:
            return None

    def send_debug(self, msg, get_history: bool = True):
        """
        发送调试消息，可以选择获取历史。
        参数：
            msg (str): 用户发送的调试消息。
            get_history (bool, 可选): 指示是否获取消息历史。
        返回：
            dict: API的响应或调试请求的响应。
        """
        if get_history:
            self.messages.append({'role': 'user', 'content': msg})
            completion = self.get_request(messages=self.messages)
            if completion:
                resp = self.get_resp(completion)
                self.messages.append({'role': 'assistant', 'content': resp})
            return completion
        else:
            messages_debug = [{'role': 'user', 'content': msg}]
            return self.get_request(messages=messages_debug)


# ali_qwen api
class Qwen(OneLLM):
    """
    Qwen类，继承自OneLLM，负责与千问模型进行API交互。
    属性：
        messages (list): 存储对话消息的列表。
    """
    messages = []

    def __init__(self, api_key, model, system_msg=None, temperature: float = None, top_p: float = None):
        """
                初始化Qwen实例。
                参数：
                    api_key (str): 访问模型的API密钥。
                    model (str): 使用的模型名称。
                    system_msg (str, 可选): 可选的系统消息，用于设置上下文。
                    temperature (float, 可选): 控制响应的随机性。
                    top_p (float, 可选): 控制采样的多样性。
                """
        self.api_key = api_key
        self.model = model
        self.system_msg = system_msg
        self.temperature = temperature
        self.top_p = top_p

        if self.system_msg:
            self.messages.append({'role': 'system', 'content': self.system_msg})

    def getHistory(self):
        return self.messages

    def getApiKey(self):
        return self.api_key

    def setApiKey(self, value):
        self.api_key = value

    def getModel(self):
        return self.model

    def setModel(self, value):
        self.model = value

    def getSystemMsg(self):
        return self.system_msg

    def setSystemMsg(self, value):
        self.system_msg = value
        if value:
            self.messages.append({'role': 'system', 'content': value})

    def get_request(self, messages):
        """
               发送请求到模型API并返回响应。
               参数：
                   messages (list): 要发送的消息列表。
               返回：
                   response.output或None：若请求成功则返回输出，失败则返回None。
         """
        response = Generation.call(
            api_key=self.api_key,
            model=self.model,
            messages=self.messages,
            result_format="message",
            temperature=self.temperature,
            top_p=self.top_p
        )

        if response.status_code == 200:
            return response.output
        else:
            print(f"HTTP返回码：{response.status_code}")
            print(f"错误码：{response.code}")
            print(f"错误信息：{response.message}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
            return None

    def get_resp(self, completion):
        """
         从API响应中提取内容。
         参数：
             completion: API返回的完整响应。
         返回：
             str: 提取的响应消息内容。
         """
        return completion.choices[0].message.content

    def send(self, msg):
        """
        发送用户消息并获取模型的响应。
        参数：
            msg (str): 用户发送的消息。
        返回：
            str或None: 模型的响应消息，或在请求失败时返回None。
        """
        self.messages.append({'role': 'user', 'content': msg})

        completion = self.get_request(self.messages)
        if completion:
            resp = self.get_resp(completion)
            self.messages.append({'role': 'assistant', 'content': resp})
            return resp
        else:
            return None

    def send_debug(self, msg, get_history: bool = True):
        """
        发送调试消息，可以选择获取历史记录。
        参数：
            msg (str): 用户发送的调试消息。
            get_history (bool, 可选): 指示是否提取消息历史，默认为True。
        返回：
            completion或None: API的响应或在请求失败时返回None。
        """
        if get_history:
            self.messages.append({'role': 'user', 'content': msg})
            completion = self.get_request(messages=self.messages)
            if completion:
                resp = self.get_resp(completion)
                self.messages.append({'role': 'assistant', 'content': resp})
            return completion

        else:
            messages_debug = [{'role': 'user', 'content': msg}]
            return self.get_request(messages=messages_debug)


class Moonshot(OneLLM):
    """
    Moonshot类，继承自OneLLM，负责与Moonshot API进行交互。
    属性：
        url (str): API请求的基础URL。
        messages (list): 存储对话消息的列表。
    """
    url = "https://api.moonshot.cn/v1"
    messages = []

    def __init__(self, api_key, model, system_msg=None, temperature=None, max_tokens=None, top_p=None, n=None,
                 presence_penalty=None, frequency_penalty=None, response_format=None, stop=None, stream=None):
        """
        初始化Moonshot实例。
        参数：
            api_key (str): 访问API的API密钥。
            model (str): 使用的模型名称。
            system_msg (str, 可选): 可选的系统消息，用于设置上下文。
            temperature (float, 可选): 控制响应的随机性。
            max_tokens (int, 可选): 生成响应的最大令牌数。
            top_p (float, 可选): 控制采样的多样性。
            n (int, 可选): 要生成的响应数量。
            presence_penalty (float, 可选): 对于新概念的生成处罚。
            frequency_penalty (float, 可选): 对于重复概念的生成处罚。
            response_format (str, 可选): 响应格式。
            stop (list, 可选): 停止序列。
            stream (bool, 可选): 是否使用流式响应。
        """
        self.api_key = api_key
        self.model = model
        self.system_msg = system_msg
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.n = n
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.response_format = response_format
        self.stop = stop
        self.stream = stream
        # 创建客户端以连接到API
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.url,
        )
        # 如果提供了系统消息，则将其添加到消息列表中
        if self.system_msg:
            self.messages.append({'role': 'system', 'content': self.system_msg})

    def getHistory(self):
        return self.messages

    def getApiKey(self):
        return self.api_key

    def setApiKey(self, value):
        self.api_key = value

    def getModel(self):
        return self.model

    def setModel(self, value):
        self.model = value

    def getSystemMsg(self):
        return self.system_msg

    def setSystemMsg(self, value):
        self.system_msg = value
        if value:
            self.messages.append({'role': 'system', 'content': value})

    def getTemperature(self):
        return self.temperature

    def setTemperature(self, value):
        self.temperature = value

    def getMaxTokens(self):
        return self.max_tokens

    def setMaxTokens(self, value):
        self.max_tokens = value

    def getTopP(self):
        return self.top_p

    def setTopP(self, value):
        self.top_p = value

    def getN(self):
        return self.n

    def setN(self, value):
        self.n = value

    def getPresencePenalty(self):
        return self.presence_penalty

    def setPresencePenalty(self, value):
        self.presence_penalty = value

    def getFrequencyPenalty(self):
        return self.frequency_penalty

    def setFrequencyPenalty(self, value):
        self.frequency_penalty = value

    def getResponseFormat(self):
        return self.response_format

    def setResponseFormat(self, value):
        self.response_format = value

    def getStop(self):
        return self.stop

    def setStop(self, value):
        self.stop = value

    def getStream(self):
        return self.stream

    def setStream(self, value):
        self.stream = value

    def get_resp(self, completion):
        """
        从API响应中提取消息内容。
        参数：
            completion: API返回的完整响应。
        返回：
            str: 提取的回应内容。
        """
        return completion.choices[0].message.content

    def get_request(self):
        """
        向Moonshot API发送请求并返回响应。
        返回：
            completion: API的响应对象。
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            n=self.n,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            stop=self.stop,
            stream=self.stream
        )
        return completion

    def send(self, msg):
        """
        发送用户消息并获取模型的响应。
        参数：
            msg (str): 用户发送的消息。
        返回：
            str或None: 模型的响应消息，或在请求失败时返回None。
        """
        self.messages.append({'role': 'user', 'content': msg})

        completion = self.get_request(self.messages)

        if completion:
            resp = self.get_resp(completion)
            self.messages.append({'role': 'assistant', 'content': resp})
            return resp
        else:
            return None

    def send_debug(self, msg, get_history: bool = True):
        """
        发送调试消息，可以选择获取历史记录。
        参数：
            msg (str): 用户发送的调试消息。
            get_history (bool, 可选): 指示是否提取消息历史，默认为True。
        返回：
            completion或None: API的响应或在请求失败时返回None。
        """
        if get_history:
            self.messages.append({'role': 'user', 'content': msg})
            completion = self.get_request(messages=self.messages)
            if completion:
                resp = self.get_resp(completion)
                self.messages.append({'role': 'assistant', 'content': resp})
            return completion
        else:
            messages_debug = [{'role': 'user', 'content': msg}]
            return self.get_request(messages=messages_debug)


class Doubao(OneLLM):
    """
    Doubao类，继承自OneLLM，负责与指定API进行交互。
    属性：
        url (str): API请求的完整URL。
        messages (list): 存储对话消息的列表。
    """
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    messages = []

    def __init__(self, api_key, model, system_msg=None, stream=False, stream_options=None, max_tokens=None, stop=None,
                 frequency_penalty=None, presence_penalty=None, temperature=None, top_p=None, logprobs=None,
                 top_logprobs=None, logit_bias=None, tools=None):
        """
        初始化Doubao实例。
        参数：
            api_key (str): 访问API的API密钥。
            model (str): 使用的模型名称。
            system_msg (str, 可选): 可选的系统消息，用于设置上下文。
            stream (bool, 可选): 是否使用流式响应，默认为False。
            stream_options (dict, 可选): 流式响应的选项。
            max_tokens (int, 可选): 生成响应的最大令牌数。
            stop (list, 可选): 停止序列。
            frequency_penalty (float, 可选): 对于重复概念的生成处罚。
            presence_penalty (float, 可选): 对于新概念的生成处罚。
            temperature (float, 可选): 控制响应的随机性。
            top_p (float, 可选): 控制采样的多样性。
            logprobs (int, 可选): 返回的log概率。
            top_logprobs (dict, 可选): 返回的每个token的top log概率。
            logit_bias (dict, 可选): 对特定token的生成偏置。
            tools (list, 可选): 可用于响应的工具。
        """
        self.api_key = api_key
        self.model = model
        self.system_msg = system_msg
        self.stream = stream
        self.stream_options = stream_options
        self.max_tokens = max_tokens
        self.stop = stop
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.temperature = temperature
        self.top_p = top_p
        self.logprobs = logprobs
        self.top_logprobs = top_logprobs
        self.logit_bias = logit_bias
        self.tools = tools
        if self.system_msg:
            self.messages.append({'role': 'system', 'content': self.system_msg})

        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=self.api_key
        )

    def getHistory(self):
        return self.messages

    def getApiKey(self):
        return self.api_key

    def setApiKey(self, value):
        self.api_key = value

    def getModel(self):
        return self.model

    def setModel(self, value):
        self.model = value

    def getSystemMsg(self):
        return self.system_msg

    def setSystemMsg(self, value):
        self.system_msg = value
        if value:
            self.messages.append({'role': 'system', 'content': value})

    def getStream(self):
        return self.stream

    def setStream(self, value):
        self.stream = value

    def getStreamOptions(self):
        return self.stream_options

    def setStreamOptions(self, value):
        self.stream_options = value

    def getMaxTokens(self):
        return self.max_tokens

    def setMaxTokens(self, value):
        self.max_tokens = value

    def getStop(self):
        return self.stop

    def setStop(self, value):
        self.stop = value

    def getFrequencyPenalty(self):
        return self.frequency_penalty

    def setFrequencyPenalty(self, value):
        self.frequency_penalty = value

    def getPresencePenalty(self):
        return self.presence_penalty

    def setPresencePenalty(self, value):
        self.presence_penalty = value

    def getTemperature(self):
        return self.temperature

    def setTemperature(self, value):
        self.temperature = value

    def getTopP(self):
        return self.top_p

    def setTopP(self, value):
        self.top_p = value

    def getLogprobs(self):
        return self.logprobs

    def setLogprobs(self, value):
        self.logprobs = value

    def getTopLogprobs(self):
        return self.top_logprobs

    def setTopLogprobs(self, value):
        self.top_logprobs = value

    def getLogitBias(self):
        return self.logit_bias

    def setLogitBias(self, value):
        self.logit_bias = value

    def getTools(self):
        return self.tools

    def setTools(self, value):
        self.tools = value

    def getId(self):
        return self.id

    def getCompletion(self):
        return self.completion

    def get_resp(self, completion):
        """
        从API响应中提取消息内容。
        参数：
            completion: API返回的完整响应。
        返回：
            str: 提取的回应内容。
        """
        return completion.choices[0].message.content

    def get_request(self):
        """
        向API发送请求并返回响应。
        返回：
            completion: API的响应对象。
        """
        completion = self.client.chat.completions.create(
            model=self.model,  # your model endpoint ID
            messages=self.messages,
            stream=self.stream,
            max_tokens=self.max_tokens,
            stop=self.stop,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            temperature=self.temperature,
            top_p=self.top_p,
            logprobs=self.logprobs,
            top_logprobs=self.top_logprobs,
            logit_bias=self.logit_bias,
            tools=self.tools

        )
        self.completion = completion
        self.id = completion.id
        return completion

    def send(self, msg):
        """
        发送用户消息并获取模型的响应。
        参数：
            msg (str): 用户发送的消息。
        返回：
            str或None: 模型的响应消息，或在请求失败时返回None。
        """
        self.messages.append({'role': 'user', 'content': msg})

        completion = self.get_request(self.messages)

        # print(completion)
        # print(completion.choices[0].message.content)
        if completion:
            resp = self.get_resp(completion)
            self.messages.append({'role': 'assistant', 'content': resp})
            return resp
        else:
            return None

    def send_debug(self, msg, get_history: bool = True):
        """
        发送调试消息，可以选择获取历史记录。
        参数：
            msg (str): 用户发送的调试消息。
            get_history (bool, 可选): 指示是否提取消息历史，默认为True。
        返回：
            completion或None: API的响应或在请求失败时返回None。
        """
        if get_history:
            self.messages.append({'role': 'user', 'content': msg})
            completion = self.get_request(messages=self.messages)
            if completion:
                resp = self.get_resp(completion)
                self.messages.append({'role': 'assistant', 'content': resp})
            return completion
        else:
            messages_debug = [{'role': 'user', 'content': msg}]
            return self.get_request(messages=messages_debug)

    def send2(self, msg):
        """
        使用特定的POST请求格式发送消息。
        参数：
            msg (str): 用户发送的消息。
        """
        self.messages.append({'role': 'user', 'content': msg})

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        data_base = {
            'model': self.model,
            'messages': self.messages,
        }
        if self.stream:
            data_base['stream'] = self.stream
        if self.stream_options:
            data_base['stream_options'] = self.stream_options
        if self.max_tokens:
            data_base['max_tokens'] = self.max_tokens
        if self.stop:
            data_base['stop'] = self.stop
        if self.frequency_penalty:
            data_base['frequency_penalty'] = self.frequency_penalty
        if self.presence_penalty:
            data_base['presence_penalty'] = self.presence_penalty
        if self.temperature:
            data_base['temperature'] = self.temperature
        if self.top_p:
            data_base['top_p'] = self.top_p
        if self.logprobs:
            data_base['logprobs'] = self.logprobs
        if self.top_logprobs:
            data_base['top_logprobs'] = self.top_logprobs
        if self.logit_bias:
            data_base['logit_bias'] = self.logit_bias
        if self.tools:
            data_base['tools'] = self.tools

        data = json.dumps(data_base)

        response = requests.post(self.url, headers=headers, data=data)
        print(response.status_code)
        print(response.json())


class Spark(OneLLM):

    """
    Spark类，继承自OneLLM，负责与指定的API进行交互。
    属性：
        url (str): API请求的完整URL。
        messages (list): 存储对话消息的列表。
    """

    url = 'https://spark-api-open.xf-yun.com/v1/chat/completions'
    messages=[]

    """
        初始化Spark实例。
        参数：
            APIPassword (str): API的访问密码。
            model (str): 使用的模型名称。
            system_msg (str, 可选): 可选的系统消息用于设定上下文。
            user (str, 可选): 用户信息。
            temperature (float, 可选): 控制响应的随机性。
            top_p (float, 可选): 控制采样的多样性。
            top_k (int, 可选): 选择top_k个token进行生成。
            presence_penalty (float, 可选): 对于新概念的生成处罚。
            frequency_penalty (float, 可选): 对于重复概念的生成处罚。
            stream (bool, 可选): 是否使用流式响应，默认为False。
            max_tokens (int, 可选): 生成响应的最大令牌数。
            response_format (object, 可选): 响应格式。
            tools (list, 可选): 可用于响应的工具。
        
    """
    def __init__(self,APIPassword,model,system_msg:str=None,user:str=None,temperature:float=None,top_p:float=None,top_k:int=None,presence_penalty:float=None,frequency_penalty:float=None,stream:bool=False,max_tokens:int=None,response_format:object=None,tools:list=None):
        self.api_key=APIPassword
        self.model=model
        self.system_msg=system_msg
        self.user=user
        self.temperature=temperature
        self.top_p=top_p
        self.top_k=top_k
        self.presence_penalty=presence_penalty
        self.frequency_penalty=frequency_penalty
        self.stream=stream
        self.max_tokens=max_tokens
        self.response_format=response_format
        self.tools=tools

        if self.system_msg:
            self.messages.append({'role':'system', 'content': self.system_msg})

    def getHistory(self):
        return self.messages

    def getApiKey(self):
        return self.api_key

    def setApiKey(self, value):
        self.api_key = value

    def getModel(self):
        return self.model

    def setModel(self, value):
        self.model = value

    def getSystemMsg(self):
        return self.system_msg

    def setSystemMsg(self, value):
        self.system_msg = value
        if value:
            self.messages.append({'role': 'system', 'content': value})
    def getUser(self):
        return self.user

    def setUser(self,value):
        self.user = value

    def getTemperature(self):
        return self.temperature
    def setTemperature(self,value):
        self.temperature = value

    def getTopP(self):
        return self.top_p

    def setTopP(self, value):
        self.top_p = value
    def getTopK(self):
        return self.top_k
    def setTopK(self,value):
        self.top_k = value
    def getPresencePenalty(self):
        return self.presence_penalty

    def setPresencePenalty(self, value):
        self.presence_penalty = value

    def getFrequencyPenalty(self):
        return self.frequency_penalty

    def setFrequencyPenalty(self, value):
        self.frequency_penalty = value
    def getStream(self):
        return self.stream
    def setStream(self,value):
        self.stream = value
    def getMaxTokens(self):
        return self.max_tokens
    def setMaxTokens(self,value):
        self.max_tokens = value
    def getResponseFormat(self):
        return self.response_format
    def setResponseFormat(self,value):
        self.response_format = value
    def getTools(self):
        return self.tools
    def setTools(self,value):
        self.tools = value

    def get_resp(self,completion):
         
        """
        从API响应中提取消息内容。
        参数：
            completion (dict): API返回的完整响应。
        返回：
            str: 提取的回应内容，若没有内容则返回空字符串。
        """
         
        return completion['choices'][0]['message'].get('content', "")
    
    def get_request(self):
        """
        向API发送请求并返回响应。
        返回：
            dict或None: API的响应对象，成功时返回字典，失败时返回None。
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": self.model,
            "messages": self.messages,
            "stream": self.stream
        }
        if self.user:
            data['user'] = self.user
        if self.temperature:
            data['temperature'] = self.temperature
        if self.top_p:
            data['top_p'] = self.top_p
        if self.top_k:
            data['top_k'] = self.top_k
        if self.presence_penalty:
            data['presence_penalty'] = self.presence_penalty
        if self.frequency_penalty:
            data['frequency_penalty'] = self.frequency_penalty
        if self.max_tokens:
            data['max_tokens'] = self.max_tokens
        if self.response_format:
            data['response_format'] = self.response_format
        if self.tools:
            data['tools'] = self.tools

        response = requests.post(self.url, headers=headers, json=data, verify=False)
        
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None


    def send(self,msg):
        """
        发送用户消息并获取模型的响应。
        参数：
            msg (str): 用户发送的消息。
        返回：
            str或None: 模型的响应消息，或在请求失败时返回None。
        """
        self.messages.append({'role': 'user', 'content': msg})
       
        completion=self.get_request()
        if completion:
            resp=self.get_resp(completion)
            self.messages.append({'role':'assistant', 'content': resp})
            return resp
        else:
            return None
    
    def send_debug(self,msg,get_history:bool=True):
        """
        发送调试消息，可以选择获取历史记录。
        参数：
            msg (str): 用户发送的调试消息。
            get_history (bool, 可选): 指示是否提取消息历史，默认为True。
        返回：
            dict或None: API的响应或在请求失败时返回None。
        """
        if get_history:
            self.messages.append({'role':'user','content':msg})
            completion=self.get_request()
            if completion:
                resp=self.get_resp(completion)
                self.messages.append({'role':'assistant', 'content': resp})
            return completion
        else:
            messages_debug=[{'role':'user','content':msg}]
            return self.get_request(messages=messages_debug)


class Ernie(OneLLM):

    """
    Ernie类，继承自OneLLM，负责与指定的API进行交互。
    属性：
        url (str): API请求的完整URL。
        ENDPOINT (str): SDK访问的身份验证端点。
        messages (list): 存储对话消息的列表。
    """

    url = "https://qianfan.baidubce.com/v2/chat/completions"
    ENDPOINT = "https://iam.bj.baidubce.com"
    messages=[]

    def __init__(self,model:str,ak:str=None,sk:str=None,api_key:str=None,app_id:str=None,system_msg=None,temperature:float=None,top_p:float=None,penalty_score:float=None,functions:list=None,stop:str=None,disable_search:bool=False,enable_citation:bool=False,max_completion_tokens:int=None):
        """
        初始化Ernie实例。
        参数：
            model (str): 使用的模型名称。
            ak (str, 可选): 访问密钥（Access Key）。
            sk (str, 可选): 秘密密钥（Secret Key）。
            api_key (str, 可选): API密钥。
            app_id (str, 可选): 应用ID。
            system_msg (str, 可选): 系统消息，用于设定上下文。
            temperature (float, 可选): 控制响应的随机性。
            top_p (float, 可选): 控制采样的多样性。
            penalty_score (float, 可选): 惩罚分数。
            functions (list, 可选): 功能列表。
            stop (str, 可选): 停止序列。
            disable_search (bool, 可选): 是否禁用搜索。
            enable_citation (bool, 可选): 是否启用引用功能。
            max_completion_tokens (int, 可选): 最大完成令牌数。
        """
        self.api_key=api_key
        self.ak=ak
        self.sk=sk
        self.model=model
        self.system_msg=system_msg
        self.temperature=temperature
        self.top_p=top_p
        self.penalty_score=penalty_score
        self.functions=functions
        self.stop=stop
        self.disable_search=disable_search
        self.enable_citation=enable_citation
        self.max_completion_tokens=max_completion_tokens
        self.app_id=app_id

        config = bce_client_configuration.BceClientConfiguration(credentials=bce_credentials.BceCredentials(AK, SK),
                                                                endpoint=self.ENDPOINT)
        self.config = copy.deepcopy(bce_client_configuration.DEFAULT_CONFIG)
        self.config.merge_non_none_values(config)

        if self.system_msg:
            self.messages.append({'role':'system', 'content': self.system_msg})
    def run(self):
        """
        获取BCE Bearer Token。
        返回：
            str: 获取到的令牌。
        """
        path = b'/v1/BCE-BEARER/token'
        headers = {
            b'Content-Type': 'application/json'
        }
        

        params = {"expireInSeconds":""}
        payload = json.dumps("", ensure_ascii=False)

        return self._send_request(b'GET', path, headers, params, payload.encode('utf-8'))
    
    def getBearToken(self):
        """
        获取Bearer Token。
        返回：
            str: Bearer Token。
        """
        token=self.run()
        self.token=token
        return token

    def getHistory(self):
        return self.messages

    def getApiKey(self):
        return self.api_key
    def setApiKey(self,value):
        self.api_key = value
    def getModel(self):
        return self.model
    def setModel(self,value):
        self.model = value

    def getSystemMsg(self):
        return self.system_msg

    def setSystemMsg(self, value):
        self.system_msg = value
        if value:
            self.messages.append({'role': 'system', 'content': value})
    def getTemperature(self):
        return self.temperature
    def setTemperature(self,value):
        self.temperature = value

    def getTopP(self):
        return self.top_p

    def setTopP(self, value):
        self.top_p = value

    def getPenaltyScore(self):
        return self.penalty_score
    def setPenaltyScore(self,value):
        self.penalty_score = value
    def getFunctions(self):
        return self.functions
    def setFunctions(self,value):
        self.functions = value
    def getStop(self):
        return self.stop
    def setStop(self,value):
        self.stop = value
    def getDisableSearch(self):
        return self.disable_search
    def setDisableSearch(self,value):
        self.disable_search = value
    def getEnableCitation(self):
        return self.enable_citation
    def setEnableCitation(self,value):
        self.enable_citation = value

    def getMaxCompletionTokens(self):
        return self.max_completion_tokens
    def setMaxCompletionTokens(self,value):
        self.MaxCompletionTokens = value

    def getAppId(self):
        return self.app_id

    def setAppId(self, value):
        self.app_id = value

    def get_resp(self,completion):
        """
        从 API 响应中提取并返回模型生成的内容。
        参数：
            completion (dict): API 返回的完整响应对象。
        返回：
            str: 模型生成的回复内容。
        """
        return completion['choices'][0]['message']['content']
        

    def get_request(self):
        """
        构建并发送 API 请求，返回 API 的响应。
        返回：
            dict或None: API 响应的 JSON 对象，成功时返回字典，失败时返回 None。
        """
        payload_json={
            "model": self.model,
            "messages": self.messages,
            "disable_search": False,
            "enable_citation": False
        }         
        if self.temperature:
            payload_json['temperature'] = self.temperature
        if self.top_p:
            payload_json['top_p'] = self.top_p
        if self.penalty_score:
            payload_json['penalty_score'] = self.penalty_score
        if self.functions:
            payload_json['functions'] = self.functions
        if self.stop:
            payload_json['stop'] = self.stop
        if self.disable_search:
            payload_json['disable_search'] = self.disable_search
        if self.enable_citation:
            payload_json['enable_citation'] = self.enable_citation
        if self.max_completion_tokens:
            payload_json['max_completion_tokens'] = self.max_completion_tokens

        payload = json.dumps(payload_json, ensure_ascii=False)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        if self.app_id:
            headers['app_id']=self.app_id
        
        response = requests.request("POST", self.url, headers=headers, data=payload.encode("utf-8"))
        if response.status_code >= 200 and response.status_code < 300:
            print(response.text)
            response_json=json.loads(response.text)
            return response_json
        else:
            return None

    def send(self,msg):
        """
        发送用户消息，并获取模型的响应。
        参数：
            msg (str): 用户发送的消息内容。
        返回：
            str或None: 模型的响应内容，成功时返回字符串，失败时返回 None。
        """
        self.messages.append({'role': 'user', 'content': msg})   
        
        completion=self.get_request()
        if completion:
            resp=self.get_resp(completion)
            self.messages.append({'role':'assistant', 'content': resp})
            return resp
        else:
            return None
        
    def send_debug(self,msg,get_history:bool=True):
        """
        发送调试消息，可以选择获取历史记录。
        参数：
            msg (str): 用户发送的调试消息。
            get_history (bool, 可选): 指示是否获取消息历史，默认为 True。
        返回：
            dict或None: API 的响应对象，成功时返回字典，失败时返回 None。
        """
        if get_history:
            self.messages.append({'role':'user','content':msg})
            completion=self.get_request()
            if completion:
                resp=self.get_resp(completion)
                self.messages.append({'role':'assistant', 'content': resp})
            return completion
        else:
            messages_debug=[{'role':'user','content':msg}]
            return self.get_request(messages=messages_debug)


# 暂时没用
class Skychat(OneLLM):
    """
    Skychat 类，继承自 OneLLM，负责与 Skychat API 进行交互。
    属性：
        url (str): API 请求的完整 URL。
        messages (list): 存储对话消息的列表。
    """
    url = 'https://api-maas.singularity-ai.com/sky-work/api/v1/chat'
    messages = []

    def __init__(self, app_key, app_secret, model, system_msg=None, sky_trace_id: str = None, stream: bool = False,
                 intent: str = None, mixed_image: bool = False):
        """
        初始化 Skychat 实例。
        参数：
            app_key (str): 应用的密钥。
            app_secret (str): 应用的秘密。
            model (str): 使用的模型名称。
            system_msg (str, 可选): 系统消息，用于设定上下文。
            sky_trace_id (str, 可选): 可选的跟踪 ID。
            stream (bool, 可选): 是否启用流式响应，默认为 False。
            intent (str, 可选): 强制指定意图，默认为 None。
            mixed_image (bool, 可选): 是否允许混合图像，默认为 False。
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.model = model
        self.system_msg = system_msg
        self.sky_trace_id = sky_trace_id
        self.stream = stream
        self.intent = intent
        self.mixed_image = mixed_image

        if self.system_msg:
            self.messages.append({'role': 'system', 'content': self.system_msg})

    def sign(self, app_key, app_secret, timestamp):
        """
        生成签名以用于 API 请求的身份验证。
        参数：
            app_key (str): 应用的密钥。
            app_secret (str): 应用的秘密。
            timestamp (str): 当前时间戳。
        返回：
            str: 生成的签名。
        """
        sign = hashlib.md5(app_key + app_secret + timestamp)
        return sign

    def send(self, msg):
        """
        发送用户消息并获取模型的响应。
        参数：
            msg (str): 用户发送的消息内容。
        返回：
            None: 该方法只处理响应，不返回值。
        """
        timestamp = str(int(time.time()))  # 获取当前时间戳
        sign_content = self.app_key + self.app_secret + timestamp
        sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()

        # 设置请求头，请求的数据格式为json
        headers = {
            "app_key": self.app_key,
            "timestamp": timestamp,
            "sign": sign_result,
            "Content-Type": "application/json",
            "stream": self.stream
        }

        # 设置请求URL和参数
        data = {
            "messages": self.messages,
            "intent": self.intent  # 用于强制指定意图，默认为空将进行意图识别判定是否搜索增强，取值 'chat'则不走搜索增强
        }

        # 发起请求并获取响应
        response = requests.post(self.url, headers=headers, json=data, stream=True)

        # 处理响应流
        for line in response.iter_lines():
            if line:
                # 处理接收到的数据
                print(line.decode('utf-8'))


        

