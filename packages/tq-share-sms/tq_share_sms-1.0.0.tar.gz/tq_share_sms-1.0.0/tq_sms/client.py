"""
TQ短信验证码API客户端
"""

import time
import requests
from typing import Optional, Dict, Any


class TQSmsClient:
    """TQ短信验证码API客户端"""
    
    def __init__(self, username: str = None, password: str = None, token: str = None):
        """
        初始化客户端
        
        Args:
            username: 用户名（如果提供token则可为空）
            password: 密码（如果提供token则可为空）
            token: 已有的token（可选）
        """
        self.base_url = "https://api.tqsms.xyz"
        self.token = token
        self.username = username
        self.password = password
        
        # 如果没有token但有用户名密码，则自动登录
        if not self.token and self.username and self.password:
            self.login()
    
    def _request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        带无限重试的请求方法
        
        Args:
            method: HTTP方法
            url: 请求URL
            **kwargs: 其他请求参数
            
        Returns:
            Response对象
        """
        while True:
            try:
                response = requests.request(method, url, **kwargs)
                return response
            except requests.exceptions.RequestException:
                # 等待1秒后重试
                time.sleep(1)
                continue
    
    def login(self) -> Dict[str, Any]:
        """
        登录获取token
        
        Returns:
            包含token的响应数据
        """
        if not self.username or not self.password:
            raise ValueError("用户名和密码不能为空")
        
        # 添加1秒休眠
        time.sleep(1)
        
        url = f"{self.base_url}/api/login"
        params = {
            "username": self.username,
            "password": self.password
        }
        
        response = self._request_with_retry("GET", url, params=params)
        data = response.json()
        
        if data.get("success"):
            self.token = data["data"]["token"]
            return data
        else:
            raise Exception(f"登录失败: {data.get('msg', '未知错误')}")
    
    def get_wallet(self) -> Dict[str, Any]:
        """
        获取用户余额
        
        Returns:
            余额信息
        """
        if not self.token:
            raise ValueError("请先登录获取token")
        
        # 添加1秒休眠
        time.sleep(1)
        
        url = f"{self.base_url}/api/getWallet"
        params = {"token": self.token}
        
        response = self._request_with_retry("GET", url, params=params)
        data = response.json()
        
        if data.get("success"):
            return data
        else:
            raise Exception(f"获取余额失败: {data.get('msg', '未知错误')}")
    
    def get_phone(self, channel_id: str, phone_num: Optional[str] = None, 
                  operator: Optional[str] = None, scope: Optional[str] = None) -> Dict[str, Any]:
        """
        获取手机号
        
        Args:
            channel_id: 渠道ID
            phone_num: 指定手机号码（可选）
            operator: 0=全部，5=虚拟，4=非虚拟（可选）
            scope: 指定号段，多个号段用逗号隔开（可选）
            
        Returns:
            手机号信息
        """
        if not self.token:
            raise ValueError("请先登录获取token")
        
        # 添加1秒休眠
        time.sleep(1)
        
        url = f"{self.base_url}/api/getPhone"
        params = {
            "token": self.token,
            "channelId": channel_id
        }
        
        if phone_num:
            params["phoneNum"] = phone_num
        if operator:
            params["operator"] = operator
        if scope:
            params["scope"] = scope
        
        response = self._request_with_retry("GET", url, params=params)
        data = response.json()
        
        if data.get("success"):
            return data
        else:
            raise Exception(f"获取手机号失败: {data.get('msg', '未知错误')}")
    
    def get_code(self, channel_id: str, phone_num: str) -> Dict[str, Any]:
        """
        获取验证码
        
        Args:
            channel_id: 渠道ID
            phone_num: 手机号码
            
        Returns:
            验证码信息
        """
        if not self.token:
            raise ValueError("请先登录获取token")
        
        # 添加1秒休眠
        time.sleep(1)
        
        url = f"{self.base_url}/api/getCode"
        params = {
            "token": self.token,
            "channelId": channel_id,
            "phoneNum": phone_num
        }
        
        response = self._request_with_retry("GET", url, params=params)
        data = response.json()
        
        if data.get("success"):
            return data
        else:
            raise Exception(f"获取验证码失败: {data.get('msg', '未知错误')}")
    
    def blacklist_phone(self, channel_id: str, phone_no: str) -> Dict[str, Any]:
        """
        拉黑手机号码
        
        Args:
            channel_id: 渠道ID
            phone_no: 手机号码
            
        Returns:
            操作结果
        """
        if not self.token:
            raise ValueError("请先登录获取token")
        
        # 添加1秒休眠
        time.sleep(1)
        
        url = f"{self.base_url}/api/phoneCollectAdd"
        params = {
            "token": self.token,
            "channelId": channel_id,
            "phoneNo": phone_no,
            "type": 0
        }
        
        response = self._request_with_retry("GET", url, params=params)
        data = response.json()
        
        if data.get("success"):
            return data
        else:
            raise Exception(f"拉黑手机号失败: {data.get('msg', '未知错误')}")
    
    def get_code_with_retry(self, channel_id: str, phone_num: str, max_retries: int = 100) -> Optional[str]:
        """
        获取验证码（带重试）
        
        Args:
            channel_id: 渠道ID
            phone_num: 手机号码
            max_retries: 最大重试次数（默认100次）
            
        Returns:
            验证码字符串，获取失败返回None
        """
        for i in range(max_retries):
            result = self.get_code(channel_id, phone_num)
            if result.get("data", {}).get("code"):
                return result["data"]["code"]
            
            # 等待刷新时间
            refresh_time = result.get("data", {}).get("refreshTime", 5000)
            time.sleep(refresh_time / 1000)  # 转换为秒
        
        return None 