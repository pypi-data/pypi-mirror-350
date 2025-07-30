# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250526-104237
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
封装LLM理解自然语言能力，并输出JSON数据
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from weberFuncs import PrintTimeMsg, PrettyPrintStr
from weberFuncs import JoinGetFileNameFmSrcFile
from openai import OpenAI
import os
import glob
import json
from dotenv import load_dotenv
# from strictjson import strict_json
# 修改了 strictjson/strict_json.py 部分代码，而得到 wyf_strict_json
from wyf_strict_json import strict_json


class LlmGenJson:
    def __init__(self, sWorkDir='', sEnvFN='.env'):
        self.sWorkDir = sWorkDir
        if not self.sWorkDir:
            self.sWorkDir = JoinGetFileNameFmSrcFile(__file__, [], 2)
        PrintTimeMsg(f'LlmGenJson.sWorkDir={sWorkDir}=')
        self.sSystemPromptDir = os.path.join(self.sWorkDir, 'SystemPrompt')
        sFullEnvFN = sEnvFN
        if self.sWorkDir:
            sFullEnvFN = os.path.join(self.sWorkDir, sEnvFN)
        bLoad = load_dotenv(dotenv_path=sFullEnvFN, verbose=True)  # load environment variables from .env
        PrintTimeMsg(f"LlmGenJson.load_dotenv({sFullEnvFN})={bLoad}")
        sOpenAiUrl = os.getenv("OPENAI_BASE_URL")
        sOpenAiKey = os.getenv("OPENAI_API_KEY")
        self.sOpenAiModel = os.getenv("OPENAI_MODEL")
        PrintTimeMsg(f'LlmGenJson.sOpenAiUrl={sOpenAiUrl}, sOpenAiModel={self.sOpenAiModel}')
        self.openai = OpenAI(api_key=sOpenAiKey, base_url=sOpenAiUrl)  # 兼容 OpenAI 客户端

    def _loadHigherVersion(self, sPromptTemplateId, sExtFN):
        # 从系统提示语模板目录下加载最大版本的系统提示语或输出JSON格式
        # 提示语模板位于工作目录的 SystemPrompt 子目录下
        # <sPromptTemplateId>_v<NN>.md 格式 或 <sPromptTemplateId>_v<NN>.json 格式
        # 传入的 sPromptTemplateId 用于匹配相同前缀的文件名
        # 传入的 sExtFN 用于匹配文件扩展名
        # 并按文件名从小到大排序，取最大的文件内容
        sPatternFN = f'{sPromptTemplateId}*{sExtFN}'
        lsPatternFN = glob.glob(sPatternFN, root_dir=self.sSystemPromptDir)
        # PrintTimeMsg(f'_loadHigherVersion({sPatternFN}).lsPatternFN={lsPatternFN}')
        sContent = ''
        if lsPatternFN:
            lsSorted = sorted(lsPatternFN, reverse=True)
            sMatchFN = lsSorted[0]
            # PrintTimeMsg(f'_loadHigherVersion.sMatchFN={sMatchFN}')
            sFullFN = os.path.join(self.sSystemPromptDir, sMatchFN)
            with open(sFullFN, 'r', encoding='utf8') as f:
                sContent = f.read()
            PrintTimeMsg(f'_loadHigherVersion({sPromptTemplateId},{sExtFN})={sMatchFN}={len(sContent)}')
        else:
            PrintTimeMsg(f'_loadHigherVersion({sPromptTemplateId},{sExtFN})=NotMatch=Null!')
        return sContent

    def _loadSystemPrompt(self, sPromptTemplateId):
        # 从系统提示语模板目录下加载最大版本的系统提示语
        return self._loadHigherVersion(sPromptTemplateId, '.md')

    def _loadOuputFormat(self, sPromptTemplateId):
        # 从系统提示语模板目录下加载最大版本的系统提示语
        sJons = self._loadHigherVersion(sPromptTemplateId, '.json')
        try:
            dictJson = json.loads(sJons)
        except Exception as e:
            PrintTimeMsg(f"_loadOuputFormat.sJons={sJons}=e={repr(e)}=")
            dictJson = {}
        PrintTimeMsg(f'_loadOuputFormat.dictJson={dictJson}=')
        return dictJson

    def llm(self, system_prompt: str, user_prompt: str) -> str:
        # 定义 strict_json 所需要的llm回调函数
        response = self.openai.chat.completions.create(
            model=self.sOpenAiModel,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content

    def strict_json_llm(self, sPromptSystem, sPromptUser, dictOutFormat):
        # 采用 strict_json 方式调用LLM
        # sPromptSystem=系统提示语
        # sPromptUser=用户提示语
        # dictOutFormat=输出结果格式描述字典

        oSJ = strict_json(sPromptSystem, sPromptUser,
                          output_format=dictOutFormat,
                          num_tries=1,
                          llm=self.llm)
        # PrintTimeMsg(f'strict_json_llm({sPromptUser},fmt={dictOutFormat})={oSJ}')
        PrintTimeMsg(f'strict_json_llm({sPromptUser})={oSJ}=')
        return oSJ

    def test_strict_json_llm(self):
        # oR = self.llm(system_prompt = 'You are a classifier to classify the sentiment of a sentence',
        #     user_prompt = 'It is a hot and sunny day')
        # PrintTimeMsg(f'test_strictjson.oR={oR}')
        # self.strict_json_llm('You are a poem extender',
        #                      'It is a beautiful and sunny day',
        #                      dictOutFormat = {'Poem with three more sentences Array': 'Write three more sentences to complete the poem, type: array'}
        #                      )

        self.strict_json_llm('You are a classifier to classify the sentiment of a sentence',
                             'It is a hot and sunny day',
                             dictOutFormat={'Classification': 'Positive or Negative'}
                             )
#         self.strict_json_llm('You are a poem extender',
#                              'It is a beautiful and sunny day',
#                              dictOutFormat={'Sentiment': ['Type of Sentiment',
#                                                    'Strength of Sentiment, type: Enum[1, 2, 3, 4, 5]'],
#                                     'Adjectives': "Name and Description as separate keys, type: List[Dict['Name', 'Description']]",
#                                     'Words': {
#                                         'Number of words': 'Word count',
#                                         'Language': {
#                                               'English': 'Whether it is English, type: bool',
#                                               'Chinese': 'Whether it is Chinese, type: bool'
#                                                   },
#                                         'Proper Words': 'Whether the words are proper in the native language, type: bool'
#                                         }
#                                     }
#                              )

#         text = '''Base Functionalities (see Tutorial.ipynb)
# Ensures LLM outputs into a dictionary based on a JSON format (HUGE: Nested lists and dictionaries now supported)
# Supports int, float, str, dict, list, Dict[], List[], Enum[], bool type forcing with LLM-based error correction, as well as LLM-based error correction using type: ensure <restriction>, and (advanced) custom user checks using custom_checks
# Easy construction of LLM-based functions using Function (Note: renamed from strict_function to keep in line with naming convention of capitalised class groups. strict_function still works for legacy support.)
# Easy integration with OpenAI JSON Mode by setting openai_json_mode = True
# Exposing of llm variable for strict_json and Function for easy use of self-defined LLMs'''
#         self.strict_json_llm('''Output the types that are supported by StrictJSON, including uppercase types
# Example Output Type Array: ['int', 'float', 'Enum[]'] ''',
#                              text,
#                              dictOutFormat = {'Output Type Array': 'Output types, type: array'}
#                              )
#         self.strict_json_llm('''Output the types that are supported by StrictJSON, including uppercase types
# Example Output Type Array: ['int', 'float', 'Enum[]'] ''',
#                              text,
#                              dictOutFormat = {'Output Types': 'Output types separated by ;'}
#                              )

    def NaturalLanguageToJson(self, sPromptTemplateId, sPromptUser):
        # 采用 模板 方式调用LLM
        # sPromptTemplateId=模板标识
        # sPromptUser=用户提示语
        sPromptSystem = self._loadSystemPrompt(sPromptTemplateId)
        dictOutFormat = self._loadOuputFormat(sPromptTemplateId)
        return self.strict_json_llm(sPromptSystem, sPromptUser, dictOutFormat)


def mainLlmGenJson():
    o = LlmGenJson()
    # o._loadSystemPrompt('')
    # o._loadSystemPrompt('Translate_prompt')
    # o._loadSystemPrompt('Translate_stem')
    # o.test_strict_json_llm()
    # return
    # o.NaturalLanguageToJson('解析定时任务时间参数-v00', '凌晨6点30分打卡')  # v00 的确不行
    o.NaturalLanguageToJson('解析定时任务时间参数', '每天凌晨6点30分打卡')
    # o.NaturalLanguageToJson('解析定时任务时间参数', '凌晨6点30分打卡')

    return


if __name__ == '__main__':
    mainLlmGenJson()
