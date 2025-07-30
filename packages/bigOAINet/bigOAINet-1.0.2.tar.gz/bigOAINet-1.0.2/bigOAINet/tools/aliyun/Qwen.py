import os
import copy
import json
from mxupy import ApiControl
# 需要安装的包
# from http import HTTPStatus
# from datetime import datetime

# from fastapi import FastAPI
# from sse_starlette.sse import EventSourceResponse
# pip install fastapi uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip install sse-starlette -i https://pypi.tuna.tsinghua.edu.cn/simple

class Qwen(ApiControl):
    """
        空间: bigOAINET.aliyun.Qwen
        名称：通义千问
        参考网址：https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api?spm=a2c4g.11186623.0.i6
        
        提供普通问答、流式问答、两者的异步问答、http事件请求等功能
        辅助功能：提供历史记录超出最大请求额度则按比例裁剪的功能

    """
    def __init__(self, history_tokens=0, history_percent=0.6, min_history_length=5, record_error_log=False, write_error_to_file=False, client_id=''):
        """ 初始化

        Args:
            history_tokens (int): 历史记录最大token数。小于等于0时, 则不传历史消息。
            history_percent (float): 当超过历史记录最大token数时, 则保留最新的历史百分比(为了消息的完整性, 这里指的是消息条数)。
            min_history_length (int): 历史保留最小条数
            record_error_log (bool): 是否记录错误日志
            write_error_to_file (bool): 是否把错误日志记录到文档
            clientId (str): 对话id, 一个用户一次与ai的完整对话可以看成 client, 
                根据 clientId 可自动保存其历史消息, 用于本次的对话, 辅助ai更好的理解用户对话的含义
        Returns:
            无
        """
        # setx ALIYUN_API_KEY 你的APIKey 设置后需要重启
        self.api_key = 'sk-879c45ea8b464c94a5fc4316652315e8'
        # self.api_key = os.getenv('ALIYUN_API_KEY')
        
        self.histories = []
        self.history_tokens = history_tokens
        self.history_percent = history_percent
        self.min_history_length = min_history_length
        
        self.record_error_log = record_error_log
        self.write_error_to_file = write_error_to_file
        self.error_logs = []
        
        self.client_id = client_id
    
    def handleParam(self, messages, tools, tool_choice, result_format, enable_search, incremental_output):
        """ 预处理参数

        Args:
            messages (list[dict]): 消息
            tools (array): 工具
            tool_choice (str|obj): 在使用tools参数时, 用于控制模型调用指定工具。有三种取值。
            result_format (str): 用户返回的内容类型, 默认为text, 当输入格式为messages时可配置为message。
            enable_search (bool): True:包含网络结果, False:不包含网络结果
            incremental_output (bool): 流返回方式
        Returns:
            response: 响应结果
            
        """
        
        if messages == '':
            messages = None
        elif isinstance(messages, str):
            messages = eval(messages)
            
        if tools == '':
            tools = None
        elif isinstance(tools, str):
            tools = eval(tools)
            
        if tools == None:
            # 当tools无值时, 默认值为'none'。
            tool_choice = 'none'
        else:
            # 当tools有值时, 返回类型只能为'message'
            result_format = 'message'
            
            if tool_choice == 'none':
                tool_choice = 'auto'
            
        enable_search = bool(enable_search)
        incremental_output = bool(incremental_output)
        
        return messages, tools, tool_choice, result_format, enable_search, incremental_output
    
    def judgePromptAndMessages(self, messages, prompt):
        """ 预处理参数

        Args:
            messages (list[dict]): 消息
            prompt (str): 用户当前输入的期望模型执行指令。
        Returns:
            response: 响应结果
        """
        if messages == None and prompt == None:
            return False, 'messages 与 prompt 必传一个。'
        
        return True, ''
        
    def tokenizer(self, messages, model='qwen-turbo'):
        """ 计算输入消息的 token 数

        Args:
            model (str): qwen-plus: 中, qwen-turbo: 弱, 注意不支持 qwen-max
            messages (list): 消息, 
                [ { 'role': 'system', 'content': 'You are a helpful assistant.' },
                { 'role': 'user', 'content': '百度网址' } ]
                # 保证角色的顺序为  system->user->assistant->user->assistant->user... 
                # 或者                     user->assistant->user->assistant->user...
                一定要按严格的角色顺序，否则会返回错误信息“无效的参数”
        Returns:
            input_tokens: 输入令牌数
            status_code: 响应码
            request_id: 会话id
            response: 响应结果
        """
        from dashscope import Tokenization
        
        response = Tokenization.call(
            api_key = self.api_key,
            model = model,
            messages = messages,
        )
        
        return response.usage['input_tokens'] if response.usage is not None else -1, response.status_code, response.request_id, response
        
    def appendToErrorLog(self, response):
        """ 添加到错误日志集

        Args:
            response (obj): 反馈的消息
        Returns:
        
        """
        if not self.record_error_log:
            return
        
        from http import HTTPStatus
        if response.status_code == HTTPStatus.OK:
            return
        
        self.error_logs.append(response)
    
    def getErrorLogs(self):
        """ 获取错误日志集

        Args:
            response (obj): 反馈的消息
        Returns:
        
        """        
        return self.error_logs
        
    def appendToHistory(self, response, content=''):
        """ 把消息添加到历史集中

        Args:
            response (obj): 反馈的消息
            content (int): 只有在流式问答，且incremental_output为true的情况下才启用
        Returns:
        
        """
        
        # 没有消息或历史记录没有限制，则直接返回
        # history_tokens 小于等于0 说明不需要记录历史
        if self.history_tokens <= 0:
            return
        
        answer = content if content != '' else response['output']['choices'][0]['message']['content']
        assistant = [{ 'role': 'assistant', 'content': answer }]
        self.histories.extend(assistant)
        
    def handleHistory(self, messages):
        """ 把用户的消息添加到历史消息，如果历史消息token超过阈值，则按比例去掉历史消息的一部分
            如果历史消息第一条role是system，历史消息则会一直保留这条消息

        Args:
            messages (list[dict]): 消息
        Returns:
        
        """
        msg = copy.copy(messages)
        
        # 没有消息或历史记录没有限制，则直接返回
        # history_tokens 小于等于0 说明不需要记录历史
        if msg == None or self.history_tokens <= 0:
            return msg
        
        # 第一次直接添加
        if self.histories == None or len(self.histories) == 0:
            self.histories = msg
            return msg
        
        hs = copy.copy(self.histories)
        hs.extend(msg)
        
        if len(hs) > self.min_history_length:
            tokens, _, _, _, = self.tokenizer(hs)
            # 如果超过最大限定token，则需按比例去掉历史信息
            if tokens > self.history_tokens:
                # print(hs)
                # 按比例保留历史信息，如果第一条 role 是 system，则保留第一条
                # 保证角色的顺序为  system->user->assistant->user->assistant->user... 
                # 或者                     user->assistant->user->assistant->user...
                l1 = int(len(hs) * (1 - self.history_percent))
                if hs[0]['role'] == 'system':
                    hhs = hs[:1] + hs[l1 + 1:]
                    # 去掉第二条role为assistant的那条
                    self.histories = hs[:1] + hs[l1 + 2:] if hhs[1]['role'] == 'assistant' else hhs
                else:
                    # 去掉第一条role为assistant的那条
                    self.histories = hs[l1 + 1:] if hs[l1:][0]['role'] == 'assistant' else hs[l1:]
                hs = copy.copy(self.histories)
            else:
                self.histories = copy.copy(hs)
        else:
            self.histories = copy.copy(hs)
            
        # 测试
        # if len(hs) > 3 and tokens > history_tokens:
        #     print(hs)
        # for m in hs:
        #     print(client_id + ': ' + m['role'] + ":" + m['content'])
        
        return hs

    def call(self, messages=None, prompt=None, tools=None, *, tool_choice='none', 
            model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
            seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None):
        """ 访问阿里云大模型

        Args:
            messages (list[dict]): 消息, 可包含历史消息
                [ { 'role': 'system', 'content': 'You are a helpful assistant.' },
                { 'role': 'user', 'content': '百度网址' } ]
              
                # 400：InvalidParameter，只有 system 角色的消息是无效的
                # 正确示例：messages = [ { 'role': 'system', 'content': '你是数学专家' }] 
            prompt (str): 用户当前输入的期望模型执行指令。
                messages和prompt任选一个参数使用即可, 二选其一
            tools (array): 用于指定可供模型调用的工具库, 一次function call流程模型会从中选择其中一个工具。
                tools中每一个tool的结构如下: 
                type, 类型为string, 表示tools的类型, 当前仅支持function。
                function, 类型为object, 键值包括name, description和parameters: 
                name: 类型为string, 表示工具函数的名称, 必须是字母、数字, 可以包含下划线和短划线, 最大长度为64。
                description: 类型为string, 表示工具函数的描述, 供模型选择何时以及如何调用工具函数。
                parameters: 类型为object, 表示工具的参数描述, 需要是一个合法的JSON Schema。JSON Schema的描述可以见链接。如果parameters参数为空, 表示function没有入参。
            tool_choice(str|obj): 在使用tools参数时, 用于控制模型调用指定工具。有三种取值: 
                "none"表示不调用工具。tools参数为空时, 默认值为"none"。
                "auto"表示模型判断是否调用工具, 可能调用也可能不调用。tools参数不为空时, 默认值为"auto"。
                object结构可以指定模型调用指定工具。例如
                tool_choice={"type": "function", "function": {"name": "user_function"}}。
                    type只支持指定为"function"。
                    function name 表示期望被调用的工具名称, 例如"get_current_time"。
            
            model (str): qwen-max: 强, qwen-plus: 中, qwen-turbo: 弱
            stop (str|array): 默认值None, 用于实现内容生成过程的精确控制, 在模型生成的内容即将包含指定的字符串或token_id时自动停止。array时, 字符串或token_id不可混用。
            enable_search (bool): True:包含网络结果, False:不包含网络结果
            result_format (str): 用户返回的内容类型, 默认为text, 当输入格式为messages时可配置为message。当tools有值时, 返回类型只能为message
            max_tokens (int): 指定模型可生成的最大token个数。
                qwen-turbo最大值和默认值为1500 tokens。
                qwen-max、qwen-max-1201、qwen-max-longcontext和qwen-plus模型, 最大值和默认值均为2000 tokens。
            
            seed (int): 生成时使用的随机数种子, 用于控制模型生成内容的随机性。seed支持无符号64位整数。
            top_p (float): 取值范围为(0, 1.0), 取值越大, 生成的随机性越高；取值越低, 生成的确定性越高。
            top_k (int): 生成时, 采样候选集的大小。例如, 取值为50时, 仅将单次生成中得分最高的50个token组成随机采样的候选集。
                取值越大, 生成的随机性越高；取值越小, 生成的确定性越高。取值为None或当top_k大于100时, 表示不启用top_k策略, 此时, 仅有top_p策略生效。
            repetition_penalty(float): 用于控制模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度, 1.0表示不做惩罚。没有严格的取值范围。
            presence_penalty(float): 提高presence_penalty时可以降低模型生成的重复度, 取值范围[-2.0, 2.0]。
            temperature(float): 取值范围:  [0, 2), 不建议取值为0, 无意义。
                较高的temperature值会降低概率分布的峰值, 使得更多的低概率词被选择, 生成结果更加多样化；
                而较低的temperature值则会增强概率分布的峰值, 使得高概率词更容易被选择, 生成结果更加确定。
            
            
        Returns:
            response: 响应结果
            
        """
        
        from http import HTTPStatus
        from dashscope import Generation
        
        messages, tools, tool_choice, result_format, enable_search, _ \
            = self.handleParam(messages, tools, tool_choice, result_format, enable_search, False)
        
        isSuccess, errorMsg = self.judgePromptAndMessages(messages, prompt)
        if not isSuccess:
            return errorMsg
        
        ms = self.handleHistory(messages)
        
        response = Generation.call(
            api_key = self.api_key,
            
            prompt = prompt,
            messages = ms,
            tools = tools,
            tool_choice = tool_choice,
            
            model = model,
            enable_search = enable_search,
            result_format = result_format,
            max_tokens = max_tokens,
            stop = stop,
            
            seed = seed,
            top_k = top_k,
            top_p = top_p,
            temperature = temperature,
            presence_penalty = presence_penalty,
            repetition_penalty = repetition_penalty,
            
            stream = False,
            stream_options = None
        )
        
        if response.status_code == HTTPStatus.OK:
            self.appendToHistory(response)
        else:
            self.appendToErrorLog(response)
            
        return response
    
    async def callAsync(self, messages=None, prompt=None, tools=None, *, tool_choice='none', 
            model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
            seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None):
        """ 访问阿里云大模型

        Args:
            messages (list[dict]): 消息, 可包含历史消息
                [ { 'role': 'system', 'content': 'You are a helpful assistant.' },
                { 'role': 'user', 'content': '百度网址' } ]
              
                # 400：InvalidParameter，只有 system 角色的消息是无效的
                # messages = [ { 'role': 'system', 'content': '你是数学专家' }]
            prompt (str): 用户当前输入的期望模型执行指令。
                messages和prompt任选一个参数使用即可, 二选其一
            tools (array): 用于指定可供模型调用的工具库, 一次function call流程模型会从中选择其中一个工具。
                tools中每一个tool的结构如下: 
                type, 类型为string, 表示tools的类型, 当前仅支持function。
                function, 类型为object, 键值包括name, description和parameters: 
                name: 类型为string, 表示工具函数的名称, 必须是字母、数字, 可以包含下划线和短划线, 最大长度为64。
                description: 类型为string, 表示工具函数的描述, 供模型选择何时以及如何调用工具函数。
                parameters: 类型为object, 表示工具的参数描述, 需要是一个合法的JSON Schema。JSON Schema的描述可以见链接。如果parameters参数为空, 表示function没有入参。
            tool_choice(str|obj): 在使用tools参数时, 用于控制模型调用指定工具。有三种取值: 
                "none"表示不调用工具。tools参数为空时, 默认值为"none"。
                "auto"表示模型判断是否调用工具, 可能调用也可能不调用。tools参数不为空时, 默认值为"auto"。
                object结构可以指定模型调用指定工具。例如
                tool_choice={"type": "function", "function": {"name": "user_function"}}。
                    type只支持指定为"function"。
                    function name 表示期望被调用的工具名称, 例如"get_current_time"。
            
            model (str): qwen-max: 强, qwen-plus: 中, qwen-turbo: 弱
            stop (str|array): 默认值None, 用于实现内容生成过程的精确控制, 在模型生成的内容即将包含指定的字符串或token_id时自动停止。array时, 字符串或token_id不可混用。
            enable_search (bool): True:包含网络结果, False:不包含网络结果
            result_format (str): 用户返回的内容类型, 默认为text, 当输入格式为messages时可配置为message。当tools有值时, 返回类型只能为message
            max_tokens (int): 指定模型可生成的最大token个数。
                qwen-turbo最大值和默认值为1500 tokens。
                qwen-max、qwen-max-1201、qwen-max-longcontext和qwen-plus模型, 最大值和默认值均为2000 tokens。
            
            seed (int): 生成时使用的随机数种子, 用于控制模型生成内容的随机性。seed支持无符号64位整数。
            top_p (float): 取值范围为(0, 1.0), 取值越大, 生成的随机性越高；取值越低, 生成的确定性越高。
            top_k (int): 生成时, 采样候选集的大小。例如, 取值为50时, 仅将单次生成中得分最高的50个token组成随机采样的候选集。
                取值越大, 生成的随机性越高；取值越小, 生成的确定性越高。取值为None或当top_k大于100时, 表示不启用top_k策略, 此时, 仅有top_p策略生效。
            repetition_penalty(float): 用于控制模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度, 1.0表示不做惩罚。没有严格的取值范围。
            presence_penalty(float): 提高presence_penalty时可以降低模型生成的重复度, 取值范围[-2.0, 2.0]。
            temperature(float): 取值范围:  [0, 2), 不建议取值为0, 无意义。
                较高的temperature值会降低概率分布的峰值, 使得更多的低概率词被选择, 生成结果更加多样化；
                而较低的temperature值则会增强概率分布的峰值, 使得高概率词更容易被选择, 生成结果更加确定。
            
            
        Returns:
            response: 响应结果
            
        """
        
        from http import HTTPStatus
        from dashscope.aigc.generation import AioGeneration
        
        messages, tools, tool_choice, result_format, enable_search, _ \
            = self.handleParam(messages, tools, tool_choice, result_format, enable_search, False)
            
        isSuccess, errorMsg = self.judgePromptAndMessages(messages, prompt)
        if not isSuccess:
            return errorMsg
        
        ms = self.handleHistory(messages)
        
        response = await AioGeneration.call(
            api_key = self.api_key,
            
            prompt = prompt,
            messages = ms,
            tools = tools,
            tool_choice = tool_choice,
            
            model = model,
            enable_search = enable_search,
            result_format = result_format,
            max_tokens = max_tokens,
            stop = stop,
            
            seed = seed,
            top_k = top_k,
            top_p = top_p,
            temperature = temperature,
            presence_penalty = presence_penalty,
            repetition_penalty = repetition_penalty,
            
            stream = False,
            stream_options = None
        )
        
        if response.status_code == HTTPStatus.OK:
            self.appendToHistory(response)
        else:
            self.appendToErrorLog(response)
        
        return response
    
    

    def stream(self, messages=None, prompt=None, tools=None, *, tool_choice='none', incremental_output=False,
            model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
            seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None):
        """ 流式访问阿里云大模型

        Args:
            messages (list[dict]): 消息, 可包含历史消息
            [ { 'role': 'system', 'content': 'You are a helpful assistant.' },
              { 'role': 'user', 'content': '百度网址' } ]
            prompt (str): 用户当前输入的期望模型执行指令。
                messages和prompt任选一个参数使用即可, 二选其一
            tools (array): 用于指定可供模型调用的工具库, 一次function call流程模型会从中选择其中一个工具。
                tools中每一个tool的结构如下: 
                type, 类型为string, 表示tools的类型, 当前仅支持function。
                function, 类型为object, 键值包括name, description和parameters: 
                name: 类型为string, 表示工具函数的名称, 必须是字母、数字, 可以包含下划线和短划线, 最大长度为64。
                description: 类型为string, 表示工具函数的描述, 供模型选择何时以及如何调用工具函数。
                parameters: 类型为object, 表示工具的参数描述, 需要是一个合法的JSON Schema。JSON Schema的描述可以见链接。如果parameters参数为空, 表示function没有入参。
            tool_choice(str|obj): 在使用tools参数时, 用于控制模型调用指定工具。有三种取值: 
                "none"表示不调用工具。tools参数为空时, 默认值为"none"。
                "auto"表示模型判断是否调用工具, 可能调用也可能不调用。tools参数不为空时, 默认值为"auto"。
                object结构可以指定模型调用指定工具。例如
                tool_choice={"type": "function", "function": {"name": "user_function"}}。
                    type只支持指定为"function"。
                    function name 表示期望被调用的工具名称, 例如"get_current_time"。
            
            incremental_output (bool): 控制在流式输出模式下是否开启增量输出, 即后续输出内容是否包含已输出的内容。
                设置为True时, 将开启增量输出模式, 后面输出不会包含已经输出的内容, 您需要自行拼接整体输出；设置为False则会包含已输出的内容。
                False: 
                    I
                    I like
                    I like apple
                True:
                    I
                    like
                    apple
                    该参数只能在stream为True时使用。
            clientId (str): 对话id, 一个用户一次与ai的完整对话可以看成 client, 
                根据 clientId 可自动保存其历史消息, 用于本次的对话, 辅助ai更好的理解用户对话的含义
            history_tokens (int): 历史记录最大token数。小于等于0时, 则不传历史消息。
            history_percent (float): 当超过历史记录最大token数时, 则保留最新的历史百分比(为了消息的完整性, 这里指的是消息条数)。
            
            model (str): qwen-max: 强, qwen-plus: 中, qwen-turbo: 弱
            stop (str|array): 默认值None, 用于实现内容生成过程的精确控制, 在模型生成的内容即将包含指定的字符串或token_id时自动停止。array时, 字符串或token_id不可混用。
            enable_search (bool): True:包含网络结果, False:不包含网络结果
            result_format (str): 用户返回的内容类型, 默认为text, 当输入格式为messages时可配置为message。当tools有值时, 返回类型只能为message
            max_tokens (int): 指定模型可生成的最大token个数。
                qwen-turbo最大值和默认值为1500 tokens。
                qwen-max、qwen-max-1201、qwen-max-longcontext和qwen-plus模型, 最大值和默认值均为2000 tokens。
            
            seed (int): 生成时使用的随机数种子, 用于控制模型生成内容的随机性。seed支持无符号64位整数。
            top_p (float): 取值范围为(0, 1.0), 取值越大, 生成的随机性越高；取值越低, 生成的确定性越高。
            top_k (int): 生成时, 采样候选集的大小。例如, 取值为50时, 仅将单次生成中得分最高的50个token组成随机采样的候选集。
                取值越大, 生成的随机性越高；取值越小, 生成的确定性越高。取值为None或当top_k大于100时, 表示不启用top_k策略, 此时, 仅有top_p策略生效。
            repetition_penalty(float): 用于控制模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度, 1.0表示不做惩罚。没有严格的取值范围。
            presence_penalty(float): 提高presence_penalty时可以降低模型生成的重复度, 取值范围[-2.0, 2.0]。
            temperature(float): 取值范围:  [0, 2), 不建议取值为0, 无意义。
                较高的temperature值会降低概率分布的峰值, 使得更多的低概率词被选择, 生成结果更加多样化；
                而较低的temperature值则会增强概率分布的峰值, 使得高概率词更容易被选择, 生成结果更加确定。
            
            
        Returns:
            response: 响应结果
            
        """
        
        from dashscope import Generation
        
        messages, tools, tool_choice, result_format, enable_search, incremental_output \
            = self.handleParam(messages, tools, tool_choice, result_format, enable_search, incremental_output)
        
        isSuccess, errorMsg = self.judgePromptAndMessages(messages, prompt)
        if not isSuccess:
            return errorMsg
        
        ms = qwen.handleHistory(messages)
        
        responses = Generation.call(
            api_key = self.api_key,
            
            prompt = prompt,
            messages = ms,
            tools = tools,
            tool_choice = tool_choice,
            
            model = model,
            enable_search = enable_search,
            result_format = result_format,
            max_tokens = max_tokens,
            stop = stop,
            
            seed = seed,
            top_k = top_k,
            top_p = top_p,
            temperature = temperature,
            presence_penalty = presence_penalty,
            repetition_penalty = repetition_penalty,
            
            stream = True,
            stream_options = { "include_usage": False },
            incremental_output = incremental_output
        )
       
        return responses
        
    async def streamWithHttp(self, messages=None, prompt=None, tools=None, *, tool_choice='none', incremental_output=False,
            model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
            seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None):
        """ 流式访问阿里云大模型

        Args:
            messages (list[dict]): 消息, 可包含历史消息
            [ { 'role': 'system', 'content': 'You are a helpful assistant.' },
              { 'role': 'user', 'content': '百度网址' } ]
            prompt (str): 用户当前输入的期望模型执行指令。
                messages和prompt任选一个参数使用即可, 二选其一
            tools (array): 用于指定可供模型调用的工具库, 一次function call流程模型会从中选择其中一个工具。
                tools中每一个tool的结构如下: 
                type, 类型为string, 表示tools的类型, 当前仅支持function。
                function, 类型为object, 键值包括name, description和parameters: 
                name: 类型为string, 表示工具函数的名称, 必须是字母、数字, 可以包含下划线和短划线, 最大长度为64。
                description: 类型为string, 表示工具函数的描述, 供模型选择何时以及如何调用工具函数。
                parameters: 类型为object, 表示工具的参数描述, 需要是一个合法的JSON Schema。JSON Schema的描述可以见链接。如果parameters参数为空, 表示function没有入参。
            tool_choice(str|obj): 在使用tools参数时, 用于控制模型调用指定工具。有三种取值: 
                "none"表示不调用工具。tools参数为空时, 默认值为"none"。
                "auto"表示模型判断是否调用工具, 可能调用也可能不调用。tools参数不为空时, 默认值为"auto"。
                object结构可以指定模型调用指定工具。例如
                tool_choice={"type": "function", "function": {"name": "user_function"}}。
                    type只支持指定为"function"。
                    function name 表示期望被调用的工具名称, 例如"get_current_time"。
            
            incremental_output (bool): 控制在流式输出模式下是否开启增量输出, 即后续输出内容是否包含已输出的内容。
                设置为True时, 将开启增量输出模式, 后面输出不会包含已经输出的内容, 您需要自行拼接整体输出；设置为False则会包含已输出的内容。
                False: 
                    I
                    I like
                    I like apple
                True:
                    I
                    like
                    apple
                    该参数只能在stream为True时使用。
            clientId (str): 对话id, 一个用户一次与ai的完整对话可以看成 client, 
                根据 clientId 可自动保存其历史消息, 用于本次的对话, 辅助ai更好的理解用户对话的含义
            history_tokens (int): 历史记录最大token数。小于等于0时, 则不传历史消息。
            history_percent (float): 当超过历史记录最大token数时, 则保留最新的历史百分比(为了消息的完整性, 这里指的是消息条数)。
            
            model (str): qwen-max: 强, qwen-plus: 中, qwen-turbo: 弱
            stop (str|array): 默认值None, 用于实现内容生成过程的精确控制, 在模型生成的内容即将包含指定的字符串或token_id时自动停止。array时, 字符串或token_id不可混用。
            enable_search (bool): True:包含网络结果, False:不包含网络结果
            result_format (str): 用户返回的内容类型, 默认为text, 当输入格式为messages时可配置为message。当tools有值时, 返回类型只能为message
            max_tokens (int): 指定模型可生成的最大token个数。
                qwen-turbo最大值和默认值为1500 tokens。
                qwen-max、qwen-max-1201、qwen-max-longcontext和qwen-plus模型, 最大值和默认值均为2000 tokens。
            
            seed (int): 生成时使用的随机数种子, 用于控制模型生成内容的随机性。seed支持无符号64位整数。
            top_p (float): 取值范围为(0, 1.0), 取值越大, 生成的随机性越高；取值越低, 生成的确定性越高。
            top_k (int): 生成时, 采样候选集的大小。例如, 取值为50时, 仅将单次生成中得分最高的50个token组成随机采样的候选集。
                取值越大, 生成的随机性越高；取值越小, 生成的确定性越高。取值为None或当top_k大于100时, 表示不启用top_k策略, 此时, 仅有top_p策略生效。
            repetition_penalty(float): 用于控制模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度, 1.0表示不做惩罚。没有严格的取值范围。
            presence_penalty(float): 提高presence_penalty时可以降低模型生成的重复度, 取值范围[-2.0, 2.0]。
            temperature(float): 取值范围:  [0, 2), 不建议取值为0, 无意义。
                较高的temperature值会降低概率分布的峰值, 使得更多的低概率词被选择, 生成结果更加多样化；
                而较低的temperature值则会增强概率分布的峰值, 使得高概率词更容易被选择, 生成结果更加确定。
            
            
        Returns:
            response: 响应结果
            
        """
        responses = self.stream(messages=messages, prompt=prompt, tools=tools, tool_choice=tool_choice, incremental_output=incremental_output,
            model=model, enable_search=enable_search, result_format=result_format, stop=stop, max_tokens=max_tokens, 
            seed=seed, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, presence_penalty=presence_penalty)

        from http import HTTPStatus
        
        answer = []
        for re in responses:
            if re.status_code == HTTPStatus.OK:
                finish = re['output']['choices'][0]['finish_reason']
                if incremental_output:
                    answer.append(re['output']['choices'][0]['message']['content'])
                    if finish != 'null':
                        Qwen.appendToHistory(re, ''.join(answer))
                else:
                    if finish != 'null':
                        Qwen.appendToHistory(re)
            
            yield json.dumps(re, ensure_ascii=False)
    
    async def streamAsync(self, messages=None, prompt=None, tools=None, *, tool_choice='none', incremental_output=False, 
            model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
            seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None):
        """ 流式访问阿里云大模型

        Args:
            messages (list[dict]): 消息, 可包含历史消息
            [ { 'role': 'system', 'content': 'You are a helpful assistant.' },
              { 'role': 'user', 'content': '百度网址' } ]
            prompt (str): 用户当前输入的期望模型执行指令。
                messages和prompt任选一个参数使用即可, 二选其一
            tools (array): 用于指定可供模型调用的工具库, 一次function call流程模型会从中选择其中一个工具。
                tools中每一个tool的结构如下: 
                type, 类型为string, 表示tools的类型, 当前仅支持function。
                function, 类型为object, 键值包括name, description和parameters: 
                name: 类型为string, 表示工具函数的名称, 必须是字母、数字, 可以包含下划线和短划线, 最大长度为64。
                description: 类型为string, 表示工具函数的描述, 供模型选择何时以及如何调用工具函数。
                parameters: 类型为object, 表示工具的参数描述, 需要是一个合法的JSON Schema。JSON Schema的描述可以见链接。如果parameters参数为空, 表示function没有入参。
            tool_choice(str|obj): 在使用tools参数时, 用于控制模型调用指定工具。有三种取值: 
                "none"表示不调用工具。tools参数为空时, 默认值为"none"。
                "auto"表示模型判断是否调用工具, 可能调用也可能不调用。tools参数不为空时, 默认值为"auto"。
                object结构可以指定模型调用指定工具。例如
                tool_choice={"type": "function", "function": {"name": "user_function"}}。
                    type只支持指定为"function"。
                    function name 表示期望被调用的工具名称, 例如"get_current_time"。
            incremental_output (bool): 控制在流式输出模式下是否开启增量输出, 即后续输出内容是否包含已输出的内容。
                设置为True时, 将开启增量输出模式, 后面输出不会包含已经输出的内容, 您需要自行拼接整体输出；设置为False则会包含已输出的内容。
                False: 
                    I
                    I like
                    I like apple
                True:
                    I
                    like
                    apple
                    该参数只能在stream为True时使用。
            
            
            model (str): qwen-max: 强, qwen-plus: 中, qwen-turbo: 弱
            stop (str|array): 默认值None, 用于实现内容生成过程的精确控制, 在模型生成的内容即将包含指定的字符串或token_id时自动停止。array时, 字符串或token_id不可混用。
            enable_search (bool): True:包含网络结果, False:不包含网络结果
            result_format (str): 用户返回的内容类型, 默认为text, 当输入格式为messages时可配置为message。当tools有值时, 返回类型只能为message
            max_tokens (int): 指定模型可生成的最大token个数。
                qwen-turbo最大值和默认值为1500 tokens。
                qwen-max、qwen-max-1201、qwen-max-longcontext和qwen-plus模型, 最大值和默认值均为2000 tokens。
            
            seed (int): 生成时使用的随机数种子, 用于控制模型生成内容的随机性。seed支持无符号64位整数。
            top_p (float): 取值范围为(0, 1.0), 取值越大, 生成的随机性越高；取值越低, 生成的确定性越高。
            top_k (int): 生成时, 采样候选集的大小。例如, 取值为50时, 仅将单次生成中得分最高的50个token组成随机采样的候选集。
                取值越大, 生成的随机性越高；取值越小, 生成的确定性越高。取值为None或当top_k大于100时, 表示不启用top_k策略, 此时, 仅有top_p策略生效。
            repetition_penalty(float): 用于控制模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度, 1.0表示不做惩罚。没有严格的取值范围。
            presence_penalty(float): 提高presence_penalty时可以降低模型生成的重复度, 取值范围[-2.0, 2.0]。
            temperature(float): 取值范围:  [0, 2), 不建议取值为0, 无意义。
                较高的temperature值会降低概率分布的峰值, 使得更多的低概率词被选择, 生成结果更加多样化；
                而较低的temperature值则会增强概率分布的峰值, 使得高概率词更容易被选择, 生成结果更加确定。
            
        Returns:
            response: 响应结果
        """
        
        from dashscope.aigc.generation import AioGeneration
        
        messages, tools, tool_choice, result_format, enable_search, incremental_output \
            = self.handleParam(messages, tools, tool_choice, result_format, enable_search, incremental_output)
        
        isSuccess, errorMsg = self.judgePromptAndMessages(messages, prompt)
        if not isSuccess:
            return errorMsg
        
        ms = self.handleHistory(messages)
        responses = await AioGeneration.call(
            api_key = self.api_key,
            
            prompt = prompt,
            messages = ms,
            tools = tools,
            tool_choice = tool_choice,
            
            model = model,
            enable_search = enable_search,
            result_format = result_format,
            max_tokens = max_tokens,
            stop = stop,
            
            seed = seed,
            top_k = top_k,
            top_p = top_p,
            temperature = temperature,
            presence_penalty = presence_penalty,
            repetition_penalty = repetition_penalty,
            
            stream = True,
            stream_options = { "include_usage": False },
            incremental_output = incremental_output
        )
        return responses

    async def streamAsyncWithHttp(self, messages=None, prompt=None, tools=None, *, tool_choice='none', incremental_output=False, 
            model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
            seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None, queue=None):
        """ 流式访问阿里云大模型

        Args:
            messages (list[dict]): 消息, 可包含历史消息
            [ { 'role': 'system', 'content': 'You are a helpful assistant.' },
              { 'role': 'user', 'content': '百度网址' } ]
            prompt (str): 用户当前输入的期望模型执行指令。
                messages和prompt任选一个参数使用即可, 二选其一
            tools (array): 用于指定可供模型调用的工具库, 一次function call流程模型会从中选择其中一个工具。
                tools中每一个tool的结构如下: 
                type, 类型为string, 表示tools的类型, 当前仅支持function。
                function, 类型为object, 键值包括name, description和parameters: 
                name: 类型为string, 表示工具函数的名称, 必须是字母、数字, 可以包含下划线和短划线, 最大长度为64。
                description: 类型为string, 表示工具函数的描述, 供模型选择何时以及如何调用工具函数。
                parameters: 类型为object, 表示工具的参数描述, 需要是一个合法的JSON Schema。JSON Schema的描述可以见链接。如果parameters参数为空, 表示function没有入参。
            tool_choice(str|obj): 在使用tools参数时, 用于控制模型调用指定工具。有三种取值: 
                "none"表示不调用工具。tools参数为空时, 默认值为"none"。
                "auto"表示模型判断是否调用工具, 可能调用也可能不调用。tools参数不为空时, 默认值为"auto"。
                object结构可以指定模型调用指定工具。例如
                tool_choice={"type": "function", "function": {"name": "user_function"}}。
                    type只支持指定为"function"。
                    function name 表示期望被调用的工具名称, 例如"get_current_time"。
            
            incremental_output (bool): 控制在流式输出模式下是否开启增量输出, 即后续输出内容是否包含已输出的内容。
                设置为True时, 将开启增量输出模式, 后面输出不会包含已经输出的内容, 您需要自行拼接整体输出；设置为False则会包含已输出的内容。
                False: 
                    I
                    I like
                    I like apple
                True:
                    I
                    like
                    apple
                    该参数只能在stream为True时使用。
            clientId (str): 对话id, 一个用户一次与ai的完整对话可以看成 client, 
                根据 clientId 可自动保存其历史消息, 用于本次的对话, 辅助ai更好的理解用户对话的含义
            history_tokens (int): 历史记录最大token数。小于等于0时, 则不传历史消息。
            history_percent (float): 当超过历史记录最大token数时, 则保留最新的历史百分比(为了消息的完整性, 这里指的是消息条数)。
            
            model (str): qwen-max: 强, qwen-plus: 中, qwen-turbo: 弱
            stop (str|array): 默认值None, 用于实现内容生成过程的精确控制, 在模型生成的内容即将包含指定的字符串或token_id时自动停止。array时, 字符串或token_id不可混用。
            enable_search (bool): True:包含网络结果, False:不包含网络结果
            result_format (str): 用户返回的内容类型, 默认为text, 当输入格式为messages时可配置为message。当tools有值时, 返回类型只能为message
            max_tokens (int): 指定模型可生成的最大token个数。
                qwen-turbo最大值和默认值为1500 tokens。
                qwen-max、qwen-max-1201、qwen-max-longcontext和qwen-plus模型, 最大值和默认值均为2000 tokens。
            
            seed (int): 生成时使用的随机数种子, 用于控制模型生成内容的随机性。seed支持无符号64位整数。
            top_p (float): 取值范围为(0, 1.0), 取值越大, 生成的随机性越高；取值越低, 生成的确定性越高。
            top_k (int): 生成时, 采样候选集的大小。例如, 取值为50时, 仅将单次生成中得分最高的50个token组成随机采样的候选集。
                取值越大, 生成的随机性越高；取值越小, 生成的确定性越高。取值为None或当top_k大于100时, 表示不启用top_k策略, 此时, 仅有top_p策略生效。
            repetition_penalty(float): 用于控制模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度, 1.0表示不做惩罚。没有严格的取值范围。
            presence_penalty(float): 提高presence_penalty时可以降低模型生成的重复度, 取值范围[-2.0, 2.0]。
            temperature(float): 取值范围:  [0, 2), 不建议取值为0, 无意义。
                较高的temperature值会降低概率分布的峰值, 使得更多的低概率词被选择, 生成结果更加多样化；
                而较低的temperature值则会增强概率分布的峰值, 使得高概率词更容易被选择, 生成结果更加确定。
            queue(list): 队列，辅助异步访问用
            
        Returns:
            response: 响应结果
        """
        
        from http import HTTPStatus
        # from datetime import datetime
        
        # print("E:" + datetime.now().isoformat(timespec='milliseconds'))
        
        responses = self.streamAsync(messages=messages, prompt=prompt, tools=tools, tool_choice=tool_choice, incremental_output=incremental_output,
            model=model, enable_search=enable_search, result_format=result_format, stop=stop, max_tokens=max_tokens, 
            seed=seed, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, presence_penalty=presence_penalty)
        
        # print("F:" + datetime.now().isoformat(timespec='milliseconds'))
        
        answer = []
        async for re in await responses:
            await queue.put({"event": "message", "data": re})
            # print("G:" + datetime.now().isoformat(timespec='milliseconds'))
                
            if re.status_code == HTTPStatus.OK:
                finish = re['output']['choices'][0]['finish_reason']
                if incremental_output:
                    answer.append(re['output']['choices'][0]['message']['content'])
                    # 说明是最后一条，四种结果：null、stop、length、tool_calls
                    if finish != 'null':
                        self.appendToHistory(re, ''.join(answer))
                else:
                    # 说明是最后一条
                    if finish != 'null':
                        self.appendToHistory(re)
                        
        # print("H:" + datetime.now().isoformat(timespec='milliseconds'))
        
        await queue.put(None)


    
    def closeClient(self):
        """ 访问阿里云大模型

        Args:
            无
        Returns:
            无
            
        """
        import gc
        self = None
        gc.collect()
    
    
    
    # 测试 http 访问
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )
    
    # call方式的同步异步
    @app.get("/callTest")
    async def callTest(request: Request, messages=None, prompt=None, tools=None, tool_choice='none',
        model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
        seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None):
        
        from sse_starlette.sse import EventSourceResponse
        
        # # 同步
        # a = Qwen().call(messages=messages, prompt=prompt, tools=tools, tool_choice=tool_choice,
        #     model=model, enable_search=enable_search, result_format=result_format, stop=stop, max_tokens=max_tokens, 
        #     seed=seed, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, presence_penalty=presence_penalty)
        # 异步
        a = await Qwen().callAsync(messages=messages, prompt=prompt, tools=tools, tool_choice=tool_choice,
            model=model, enable_search=enable_search, result_format=result_format, stop=stop, max_tokens=max_tokens, 
            seed=seed, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, presence_penalty=presence_penalty)

        return EventSourceResponse(a)
    
    # stream方式的同步
    @app.get("/streamTest")
    async def streamTest(request: Request, messages=None, prompt=None, tools=None, tool_choice='none',
        model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
        seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None):
        
        from sse_starlette.sse import EventSourceResponse
        # 同步
        a = Qwen().streamWithHttp(messages=messages, prompt=prompt, tools=tools, tool_choice=tool_choice,
            model=model, enable_search=enable_search, result_format=result_format, stop=stop, max_tokens=max_tokens, 
            seed=seed, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, presence_penalty=presence_penalty)
        
        return EventSourceResponse(a)
    
    # stream方式的异步
    @app.get("/streamAsyncTest")
    async def streamAsyncTest(request: Request, messages=None, prompt=None, tools=None, tool_choice='none', incremental_output=False,
        model='qwen-turbo', enable_search=False, result_format='message', stop=None, max_tokens=None, 
        seed=None, top_p=None, top_k=None, temperature=None, repetition_penalty=None, presence_penalty=None):
        
        from sse_starlette.sse import EventSourceResponse
        
        from datetime import datetime
        print("A:" + datetime.now().isoformat(timespec='milliseconds'))
        
        if await request.is_disconnected():
            print("连接已中断")
            return
        
        queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        loop.create_task(Qwen().streamAsyncWithHttp(messages=messages, prompt=prompt, tools=tools, tool_choice=tool_choice, incremental_output=incremental_output,
            model=model, enable_search=enable_search, result_format=result_format, stop=stop, max_tokens=max_tokens, 
            seed=seed, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, presence_penalty=presence_penalty, queue=queue))

        async def fetchQueue():
            print("B:" + datetime.now().isoformat(timespec='milliseconds'))
            while True:
                item = await queue.get()
                if item is None:
                    break
                yield item
                print("C:" + datetime.now().isoformat(timespec='milliseconds'))
                
        print("D:" + datetime.now().isoformat(timespec='milliseconds'))

        return EventSourceResponse(fetchQueue())
    
    
    
if __name__ == '__main__':
    
    import asyncio
    import platform
    
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    import uuid
    client_id = str(uuid.uuid4())
    qwen = Qwen(history_tokens=0, history_percent=0.8, min_history_length=5, record_error_log=False, client_id=client_id)
    
    
    
    
    
    # 计算token值
    # messages = [
    #     { 'role': 'system', 'content': 'You are a helpful assistant.' },
    #     { 'role': 'user', 'content': '这世界有那么多人' }
    # ]
    # t = Qwen.tokenizer(messages)
    # print(t)
    
    # 测试 prompt 参数
    ms = ['这世界有那么多人','贝一科技全球第一','贝多芬的奶奶跳舞']
    for i in range(3):
        t = qwen.call(None, ms[i], max_tokens=30)
        print(t)
    
    
    
    # # # 测试流式访问
    # import uvicorn
    # uvicorn.run(Qwen.app, host="0.0.0.0", port=8000)
    # print('end')
    
    
    
    # 浏览器测试地址
    # http://127.0.0.1:8000/callTest
    # http://127.0.0.1:8000/streamTest
    # http://127.0.0.1:8000/streamAsyncTest
    
    # # 控制台脚本
    # var urlWithParams = "/streamTest?messages=[{ 'role': 'user', 'content': '1+1=' }]&max_tokens=20&client_id=46884688&incremental_output=True&history_tokens=30";
    # var eventSource = new EventSource(urlWithParams);
    # eventSource.onmessage = function(event) {
    #     console.log(event.data);
    # };

    # var urlWithParams = "/streamTest?messages=[{ 'role': 'user', 'content': '1-1=' }]&max_tokens=20&client_id=46884687&incremental_output=False&history_tokens=30";
    # var eventSource = new EventSource(urlWithParams);
    # eventSource.onmessage = function(event) {
    #     console.log(event.data);
    # };
    
    
    
    
    # # 测试多轮对话
    # import uuid
    # import copy
    # # (带角色system)
    # msg = [{ 'role': 'system', 'content': '你是数学专家' }]
    # ms = ['1+1=?', '再加1等于几', '再减1等于几', '再减2等于几', '再减3等于几', '再减4等于几', '再减5等于几']
    # for i in range(7):
    #     m = copy.copy(msg)
    #     if i == 0:
    #         m.extend([ { 'role': 'user', 'content': ms[i] } ])
    #     else:
    #         m = [ { 'role': 'user', 'content': ms[i] } ]
            
    #     # 同步访问
    #     t = qwen.call(m, '', max_tokens=60)
    #     print(t)
    #     # 异步访问
    #     t = asyncio.run(qwen.callAsync(m, '', max_tokens=60))
    #     print(t)
    # (不带角色system)
    # ms = ['1+1=?', '再加1等于几', '再减1等于几', '再减2等于几', '再减3等于几', '再减4等于几', '再减5等于几']
    # for i in range(7):
    #     m = [ { 'role': 'user', 'content': ms[i] } ]
    #     t = qwen.call(m, '', max_tokens=60)
    #     print(t)
    #     t = asyncio.run(qwen.callAsync(m, '', max_tokens=60), debug=False)
    #     print(t)
    
    # # 测试多轮对话(流式)
    # import uuid
    # import copy
    # # (带角色system)
    # msg = [{ 'role': 'system', 'content': '你是数学专家' }]
    # ms = ['1+1=?', '再加1等于几', '再减1等于几', '再减2等于几', '再减3等于几', '再减4等于几', '再减5等于几']
    # for i in range(7):
    #     m = copy.copy(msg)
    #     if i == 0:
    #         m.extend([ { 'role': 'user', 'content': ms[i] } ])
    #     else:
    #         m = [ { 'role': 'user', 'content': ms[i] } ]
            
    #     # 同步访问
    #     t = qwen.stream(m, '', max_tokens=20)
    #     for tt in t:
    #         print(tt)
        # # 异步访问
        # async def print1():
        #     t = await qwen.streamAsync(m, '', max_tokens=20)
        #     async for tt in t:
        #         print(tt)
        # asyncio.run(print1())
        
    # (不带角色system)
    # ms = ['1+1=?', '再加1等于几', '再减1等于几', '再减2等于几', '再减3等于几', '再减4等于几', '再减5等于几']
    # for i in range(7):
    #     m = [ { 'role': 'user', 'content': ms[i] } ]
    #     t = qwen.stream(m, '', max_tokens=20)
    #     for tt in t:
    #         print(tt)
    #     async def print1():
    #         t = await qwen.streamAsync(m, '', max_tokens=20)
    #         async for tt in t:
    #             print(tt)

    #     asyncio.run(print1())
        
        
    
    
    
    # 测试函数调用
    # tools = [
    #     # 工具1 获取当前时刻的时间jin
    #     {
    #         "type": "function",
    #         "function": {
    #             "name": "get_current_time",
    #             "description": "当你想知道现在的时间时非常有用。",
    #             "parameters": {}  # 因为获取当前时间无需输入参数, 因此parameters为空字典
    #         }
    #     },  
    #     # 工具2 获取指定城市的天气
    #     {
    #         "type": "function",
    #         "function": {
    #             "name": "get_current_weather",
    #             "description": "当你想查询指定城市的天气时非常有用。",
    #             "parameters": {  # 查询天气时需要提供位置, 因此参数设置为location
    #                 "type": "object",
    #                 "properties": {
    #                     "location": {
    #                         "type": "string",
    #                         "description": "城市或县区, 比如北京市、杭州市、余杭区等。"
    #                     }
    #                 }
    #             },
    #             "required": [ "location" ]
    #         }
    #     }
    # ]
    # # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
    # messages = [
    #     {
    #         "content": '几点了？',
    #         "role": "user"
    #     }
    # ]
    # a = qwen.call(messages=messages, tools=tools, model="qwen-plus")
    # print(a)
    # a = asyncio.run(qwen.callAsync(messages=messages, tools=tools, model="qwen-plus"))
    # print(a)
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # 其他测试
    # 400：InvalidParameter
    # messages = [ { 'role': 'system', 'content': '你是数学专家' }]
    # 下面的都没问题，但是计算 token 值的时候都异常
    # messages = [ { 'role': 'user', 'content': '你是数学专家' }, { 'role': 'user', 'content': '为啥除0无意义' } ]
    # messages = [ { 'role': 'system', 'content': '你是数学专家' }, { 'role': 'system', 'content': '为啥除0无意义' } ]
    # messages = [ { 'role': 'assistant', 'content': '你是数学专家' }, { 'role': 'assistant', 'content': '为啥除0无意义' } ]
    
    # messages = [ { 'role': 'system', 'content': '你是数学专家' }, { 'role': 'assistant', 'content': '为啥除0无意义' }]
    # messages = [ { 'role': 'system', 'content': '你是数学专家' }, { 'role': 'assistant', 'content': '为啥除0无意义' } , { 'role': 'user', 'content': '因为你是傻蛋' } ]
    # messages = [ { 'role': 'system', 'content': '你是数学专家' }, { 'role': 'user', 'content': '为啥除0无意义' } , { 'role': 'assistant', 'content': '因为你是傻蛋' } ]
    
    # messages = [ { 'role': 'assistant', 'content': '你是数学专家' }, { 'role': 'system', 'content': '为啥除0无意义' } ]
    # messages = [ { 'role': 'user', 'content': '你是数学专家' }, { 'role': 'system', 'content': '为啥除0无意义' } ]
    
    # t = qwen.call(messages, '', max_tokens=100, client_id=client_id, history_tokens=100)
    # print(t)
    
    
    
    # ms = ['这世界有那么多人','贝一科技全球第一','贝多芬奶奶跳舞']
    # for i in range(3):
    #     messages = [
    #         { 'role': 'user', 'content': ms[i] }
    #     ]
    #     t = qwen.call(messages, '', max_tokens=20)
    #     print(t)
    
    messages = [
        # {'role': 'system', 'content': '你是答案选择者，需选择正确答案。'},
        # {'role': 'system', 'content': '你是专家，请选择正确答案。'},
        # {'role': 'user', 'content': '你在干啥？选项有：[[0,"公司在哪"],[1,"公司有几名员工"],[2,"公司叫什么名字"],[3,"公司主要做哪些项目"],[4,"我在唱歌"],[5,"我正在跳舞"]]。请返回正确选项的序号即可。'},
        # {'role': 'user', 'content': '你正在干什么？选项有：[[0,"公司在哪"],[1,"公司有几名员工"],[2,"公司叫什么名字"],[3,"公司主要做哪些项目"],[4,"我在唱歌"],[5,"我正在跳舞"]]。请返回正确选项的序号即可。'},
        # {'role': 'user', 'content': '在干什么？选项有：[[0,"公司在哪"],[1,"公司有几名员工"],[2,"公司叫什么名字"],[3,"公司主要做哪些项目"],[4,"我在唱歌"],[5,"我正在跳舞"]]。请返回正确选项的序号即可。'},
        {'role': 'user', 'content': '有几个人？选项有：[[0,"公司在哪"],[1,"公司有几名员工"],[2,"公司叫什么名字"],[3,"公司主要做哪些项目"],[4,"在唱歌"],[5,"现在在跳舞"]]。请返回正确选项的序号即可。'},
        # {'role': 'user', 'content': '你在干什么？选项有：[[0,"公司在哪"],[1,"公司有几名员工"],[2,"公司叫什么名字"],[3,"公司主要做哪些项目"],[4,"在唱歌"],[5,"正在跳舞"]]。'},
        # {'role': 'user', 'content': '下雨了吗？ 选项有：[(10000,"没有答案则选我"),(0,"公司在哪"),(1,"公司有几名员工"),(2,"公司叫什么名字"),(3,"公司主要做哪些项目"),(4,"在唱歌"),(5,"正在跳舞")]。 请返回正确选项的序号即可,否则返回100。'},
        # {'role': 'user', 'content': '你正在干什么？ 选项有：[(0,"公司在哪"),(1,"公司有几名员工"),(2,"公司叫什么名字"),(3,"公司主要做哪些项目"),(4,"在唱歌"),(5,"正在跳舞"),(10000,"没有答案则选我")]。 请返回正确选项的序号即可。'},
        # {'role': 'user', 'content': '做什么的？选项有：[[0, "公司在哪"],[1, "公司有几名员工"],[2, "公司叫什么名字"],[3, "公司主要做哪些项目"]]。请返回正确答案的序号即可？'},
        # {'role': 'user', 'content': '阿里云提供的哪项服务可以帮助用户进行大规模的数据分析处理？选项有：MaxCompute；ECS；CDN；RDS。，请返回正确答案？不用解释。'},
        # {'role': 'user', 'content': '做什么的？选项有：[公司在哪, 公司有几名员工, 公司叫什么名字, 公司主要做哪些项目]。请返回正确答案？不用解释。'},
        
        # {'role': 'user', 'content': '有什么公司？选项有：[[0, "公司在哪"],[1, "公司有几名员工"],[2, "公司叫什么名字"],[3, "公司主要做哪些项目"]]。请返回正确答案的序号即可？如果没有正确答案，请返回-1。'},
        # {'role': 'user', 'content': '爆竹声中一岁除，春风送暖入屠苏”，这里的“屠苏”指的是？选项有：1、苏州   2、cccccccccccc  3、g  4、庄稼。，请返回正确答案的序号即可？'}
    ]
    # , top_p=0.00000000001
    t = asyncio.run(qwen.callAsync(messages, '', max_tokens=1, model='qwen-max', enable_search=False))
    print(t)
   
    
    
    
    # # 爆竹声中一岁除，春风送暖入屠苏”，这里的“屠苏”指的是
    # # 1、苏州   2、房屋  3、酒  4、庄稼
    
    # ms = ['这世界有那么多人','贝一科技全球第一','贝多芬奶奶跳舞']
    # for i in range(3):
    #     messages = [
    #         { 'role': 'user', 'content': ms[i] }
    #     ]
    #     t = qwen.call(messages, '', max_tokens=20)
    #     print(t)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    