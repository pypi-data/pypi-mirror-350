from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CurrencyType(str, Enum):
    """信用货币类型"""

    # 法定货币
    CNY = "CNY"  # 人民币
    USD = "USD"  # 美元

    # 自定义货币
    LTC = "LTC"  # LLM Token Counts
    UTS = "UTS"  # Usage Times


# Key 相关模型
class KeyCreate(BaseModel):
    """创建密钥请求"""

    user_id: Optional[str] = Field(default=None, description="用户ID", example="user1")
    service_code: str = Field(..., description="服务代码", example="ADM")
    scope: Optional[List[str]] = Field(
        default=None,
        description="作用域，JSON数组格式",
        example=["instance1", "instance2", "instance3"],
    )
    currency_type: Optional[CurrencyType] = Field(
        default=None, description="信用货币类型", example="CNY"
    )
    credit_limit: Optional[float] = Field(
        default=None, description="额度限制", example=1000.0
    )
    expires_at: Optional[datetime] = Field(
        default=None, description="过期时间", example=datetime.now()
    )


class KeyResponse(BaseModel):
    """密钥响应"""

    id: str
    app_id: str
    user_id: str
    service_code: str  # 服务代码
    currency_type: Optional[CurrencyType]  # 信用货币类型，可能为None，表示管理密钥
    scope: Optional[List[str]] = None  # 作用域，JSON数组格式
    instance_name: Optional[str] = None
    credit_limit: float
    credit_used: float
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class KeyConsumeRequest(BaseModel):
    """消费密钥请求"""

    key_id: str = Field(..., description="密钥ID")
    amount: Optional[float] = Field(default=None, description="消费数量")
    details: Optional[Dict[str, Any]] = Field(None, description="详细信息")


class KeyListResponse(BaseModel):
    """密钥列表响应"""

    keys: List[KeyResponse] = Field(default_factory=list, description="密钥列表")


class KeyDeleteResponse(BaseModel):
    """删除密钥响应"""

    success: bool = Field(..., description="是否成功")
    key_id: str = Field(..., description="密钥ID")
