# ============================================
# LLM 客户端封装
# 统一封装大模型调用接口，支持 OpenAI 兼容格式
# 支持: DeepSeek / 通义千问 / 智谱AI / Moonshot / OpenAI 等
# ============================================
import json
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class LLMClient:
    """
    大语言模型客户端
    使用 OpenAI 兼容格式，一套代码支持多种大模型
    """
    
    def __init__(self, api_key, base_url, model, temperature=0.7, max_tokens=4096):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        logger.info(f"LLM客户端初始化: model={model}, base_url={base_url}")
    
    def chat(self, messages, temperature=None, max_tokens=None, response_format=None):
        """
        发送对话请求到LLM
        
        Args:
            messages: 消息列表 [{"role": "system/user/assistant", "content": "..."}]
            temperature: 温度参数（可覆盖默认值）
            max_tokens: 最大token数（可覆盖默认值）
            response_format: 响应格式，如 {"type": "json_object"}
        
        Returns:
            str: 模型响应文本
        """
        try:
            kwargs = {
                'model': self.model,
                'messages': messages,
                'temperature': temperature or self.temperature,
                'max_tokens': max_tokens or self.max_tokens,
            }
            if response_format:
                kwargs['response_format'] = response_format
            
            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content
            logger.info(f"LLM调用成功, 消耗tokens: {response.usage.total_tokens if response.usage else 'unknown'}")
            return content
        except Exception as e:
            logger.error(f"LLM调用失败: {str(e)}")
            raise
    
    def chat_json(self, messages, temperature=None, max_tokens=None):
        """
        发送对话请求并解析JSON响应
        自动处理JSON提取（兼容不同模型的输出格式）
        
        Returns:
            dict/list: 解析后的JSON对象
        """
        # 在system消息中强调返回JSON格式
        enhanced_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                enhanced_messages.append({
                    'role': 'system',
                    'content': msg['content'] + '\n\n请务必只返回合法的JSON格式，不要包含任何其他文字说明或markdown代码块标记。'
                })
            else:
                enhanced_messages.append(msg)
        
        try:
            # 尝试使用 json_object 格式
            content = self.chat(enhanced_messages, temperature, max_tokens,
                              response_format={"type": "json_object"})
        except Exception:
            # 降级：不使用response_format
            content = self.chat(enhanced_messages, temperature, max_tokens)
        
        return self._extract_json(content)
    
    def _try_fix_json(self, text):
        """尝试修复不完整的JSON（处理被截断的情况）"""
        original_text = text
        text = text.rstrip()
        
        # 策略1: 找到最后一个完整的 }, 或 ], 作为截断点
        for _ in range(10):  # 最多尝试10次
            last_complete = max(text.rfind('},'), text.rfind('],'))
            if last_complete > len(text) // 2:  # 只有在合理位置才截断
                truncated = text[:last_complete + 1]
                # 计算需要补全的括号
                open_braces = truncated.count('{') - truncated.count('}')
                open_brackets = truncated.count('[') - truncated.count(']')
                fixed = truncated + ']' * open_brackets + '}' * open_braces
                try:
                    return json.loads(fixed)
                except json.JSONDecodeError:
                    text = truncated  # 继续缩短
                    continue
            break
        
        # 策略2: 直接补全括号
        text = original_text.rstrip()
        if text.endswith(','):
            text = text[:-1]
        
        open_braces = text.count('{') - text.count('}')
        open_brackets = text.count('[') - text.count(']')
        
        if open_braces > 0 or open_brackets > 0:
            text += ']' * open_brackets + '}' * open_braces
        
        return text
    
    def _extract_json(self, text):
        """从LLM响应中提取JSON（处理可能的markdown代码块包裹）"""
        text = text.strip()
        
        # 尝试直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # 去除markdown代码块标记
        if text.startswith('```'):
            lines = text.split('\n')
            # 去掉第一行(```json)和最后一行(```)
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            text = '\n'.join(lines).strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # 尝试找到第一个 { 或 [ 开始的JSON
        for i, char in enumerate(text):
            if char in ('{', '['):
                json_text = text[i:]
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError:
                    # 尝试修复不完整的JSON
                    try:
                        fixed = self._try_fix_json(json_text)
                        result = json.loads(fixed)
                        logger.warning(f"JSON已自动修复（补全了未闭合的括号）")
                        return result
                    except json.JSONDecodeError:
                        continue
        
        logger.error(f"无法解析JSON响应: {text[:200]}...")
        raise ValueError(f"无法解析LLM返回的JSON格式")


# 全局LLM客户端实例（在app初始化时设置）
_llm_client = None


def init_llm(app):
    """初始化LLM客户端"""
    global _llm_client
    _llm_client = LLMClient(
        api_key=app.config['LLM_API_KEY'],
        base_url=app.config['LLM_BASE_URL'],
        model=app.config['LLM_MODEL'],
        temperature=app.config['LLM_TEMPERATURE'],
        max_tokens=app.config['LLM_MAX_TOKENS'],
    )
    return _llm_client


def get_llm():
    """获取全局LLM客户端"""
    if _llm_client is None:
        raise RuntimeError("LLM客户端尚未初始化，请先调用 init_llm()")
    return _llm_client
