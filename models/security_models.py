# security_models.py
# RWA智能合約安全檢核框架 - 安全核心數據結構

from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


class VulnerabilityType(Enum):
    REENTRANCY = "重入攻擊"
    INTEGER_OVERFLOW = "整數溢位"
    ACCESS_CONTROL = "存取控制"
    TIMESTAMP_DEPENDENCY = "時間戳依賴"
    PRICE_MANIPULATION = "價格操縱"
    COMPLIANCE_VIOLATION = "合規性違反"
    ASSET_VERIFICATION = "資產驗證"
    CROSS_CHAIN_BRIDGE = "跨鏈橋接"
    UNCHECKED_CALL = "未檢查外部調用"
    DENIAL_OF_SERVICE = "拒絕服務"
    FRONT_RUNNING = "搶跑攻擊"
    FLASH_LOAN = "閃電貸攻擊"
    ORACLE_MANIPULATION = "預言機操縱"
    GOVERNANCE_ATTACK = "治理攻擊"
    SANDWICH_ATTACK = "夾子攻擊"
    MEV_ATTACK = "MEV攻擊"
    LIQUIDITY_DRAIN = "流動性枯竭"
    TOKEN_INFLATION = "代幣通脹"
    UNKNOWN = "未知類型"

class SeverityLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class ConfidenceLevel(Enum):
    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    VERY_LOW = "VERY_LOW"

@dataclass
class SecurityFinding:
    vulnerability_type: str
    severity: str
    confidence: float
    location: str
    description: str
    recommendation: str
    cwe_id: str
    timestamp: str
    context: str
    def as_dict(self):
        return asdict(self)

@dataclass
class VulnerabilityPattern:
    name: str
    patterns: List[str]
    danger_contexts: List[str]
    risk_factors: List[str]
    severity_weights: Dict[str, float]
    confidence_base: float
    description: str
    cwe_mapping: Optional[str] = None
    example_exploit: Optional[str] = None
    def as_dict(self):
        return asdict(self)

@dataclass
class PotentialVulnerability:
    vulnerability_type: VulnerabilityType
    pattern_matched: str
    confidence: float
    severity_level: SeverityLevel
    location: str
    line_numbers: List[int]
    context: str
    danger_level: str
    risk_factors: List[str]
    pattern_frequency: int
    context_analysis: Dict[str, Any]
    mitigation_hints: List[str]
    exploit_scenario: Optional[str] = None
    related_patterns: Optional[List[str]] = None
    def as_dict(self):
        d = asdict(self)
        d["vulnerability_type"] = self.vulnerability_type.value if self.vulnerability_type else ""
        d["severity_level"] = self.severity_level.value if self.severity_level else ""
        return d

# 測試入口
if __name__ == "__main__":
    finding = SecurityFinding(
        vulnerability_type="重入攻擊",
        severity="CRITICAL",
        confidence=0.98,
        location="Line 102",
        description="檢測到典型重入攻擊模式",
        recommendation="使用ReentrancyGuard",
        cwe_id="CWE-362",
        timestamp="2025-10-05T18:50:00",
        context="function withdraw()..."
    )
    pattern = VulnerabilityPattern(
        name="重入攻擊",
        patterns=["\\.call\\(", "\\.send\\("],
        danger_contexts=["external", "public"],
        risk_factors=["state_change_after_call"],
        severity_weights={"external_call_with_state_change": 0.9},
        confidence_base=0.7,
        description="發現重入攻擊經典模式",
        cwe_mapping="CWE-362",
        example_exploit="合約多次調用withdraw"
    )
    pvuln = PotentialVulnerability(
        vulnerability_type=VulnerabilityType.REENTRANCY,
        pattern_matched="\\.call(",
        confidence=0.95,
        severity_level=SeverityLevel.CRITICAL,
        location="Line 102",
        line_numbers=[102],
        context="function withdraw()...",
        danger_level="CRITICAL",
        risk_factors=["state_change_after_call"],
        pattern_frequency=2,
        context_analysis={"call_count": 2},
        mitigation_hints=["使用ReentrancyGuard"],
        exploit_scenario="多次重入",
        related_patterns=["external_call"]
    )
    print("SecurityFinding:", finding.as_dict())
    print("VulnerabilityPattern:", pattern.as_dict())
    print("PotentialVulnerability:", pvuln.as_dict())
