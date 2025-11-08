# knowledge_base.py
# RWA知識庫 - 專業合規、最佳實踐、歷史案例、資產規則功能

import logging
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class RegulatoryRequirement:
    jurisdiction: str
    requirement: str
    description: str
    compliance: str
    penalty: str
    last_updated: str

@dataclass
class BestPractice:
    category: str
    name: str
    description: str
    steps: List[str]
    mitigation: List[str]
    tools: List[str]
    maturity: str

@dataclass
class HistoricalCase:
    name: str
    date: str
    asset_type: str
    vuln_type: str
    loss: float
    root_cause: str
    lessons: List[str]
    prevention: List[str]
    regulatory_response: str

@dataclass
class AssetRule:
    asset_type: str
    requirements: List[str]
    risk_factors: List[str]
    checklist: List[str]
    valuation: List[str]
    custody: List[str]

class RWAKnowledgeBase:
    def __init__(self):
        self.reg_requirements = self._init_reg_requirements()
        self.best_practices = self._init_best_practices()
        self.cases = self._init_cases()
        self.asset_rules = self._init_asset_rules()
        logger.info("知識庫初始化完成")

    def _init_reg_requirements(self) -> List[RegulatoryRequirement]:
        return [
            RegulatoryRequirement("SEC", "KYC/AML", "身份驗證及反洗錢要求", "MANDATORY", "最高$5M罰款或5年監禁", "2024-01-15"),
            RegulatoryRequirement("SEC", "Accredited Investor", "合格投資人檢核", "MANDATORY", "民事罰款", "2024-02-20"),
            RegulatoryRequirement("MAS", "Token Framework", "新加坡數位代幣發行監管", "MANDATORY", "最高100萬新幣罰款", "2024-03-10"),
            RegulatoryRequirement("FCA", "Promotion Rules", "金融推廣與保護投資人原則", "MANDATORY", "無上限罰款", "2024-01-30"),
            RegulatoryRequirement("FINMA", "DLT Guidelines", "分布式帳本合規指引", "RECOMMENDED", "營業限制", "2024-02-15")
        ]

    def _init_best_practices(self) -> List[BestPractice]:
        return [
            BestPractice("合約安全", "多重簽名管理", "核心功能採用多簽錢包", ["選擇多簽方案", "設定阈值", "金鑰管理SOP", "定期更換簽名者"],
                        ["降低故障風險", "防內部惡意"], ["Gnosis Safe", "Multi-Sig Wallet"], "ADVANCED"),
            BestPractice("資產代幣化", "透明化託管", "建立透明託管與驗證", ["選合規託管", "定期評估", "第三方審計", "即時查詢"],
                        ["提升信心", "降低託管漏洞"], ["Chainlink Proof Reserve", "TrustToken"], "ADVANCED"),
            BestPractice("合規監控", "動態合規監控", "合規狀態持續自動監控與異常處理", ["建立儀表板", "自動規則", "異常流程", "定期報告"],
                        ["及時發現合規風險"], ["Chainalysis", "ComplyAdvantage"], "ADVANCED")
        ]

    def _init_cases(self) -> List[HistoricalCase]:
        return [
            HistoricalCase("Terra Luna Collapse", "2022-05-09", "算法幣", "經濟模型缺陷", 60000000000, "脫鉤引發死亡螺旋", ["需真實資產支撐"], ["多元抵押池", "熔斷機制"], "強化穩定幣監管"),
            HistoricalCase("Iron Finance Bank Run", "2021-06-17", "部分抵押幣", "流動風險", 2000000000, "TITAN暴跌致IRON擺脫支撐", ["分散抵押類型"], ["高抵押", "保險基金"], "關注DeFi風險"),
            HistoricalCase("Poly Network Hack", "2021-08-10", "跨鏈資產", "橋接合約漏洞", 611000000, "合約驗證缺陷", ["需多重驗證"], ["多簽驗證", "分階段釋放"], "加強跨鏈風險監管")
        ]

    def _init_asset_rules(self) -> List[AssetRule]:
        return [
            AssetRule("房地產", ["產權清晰", "法定登記", "建設許可", "規劃合規"], ["地理集中", "流動性", "政策變化", "天然災害"],
                      ["證明文件", "估價報告", "保險證明", "合規證明"], ["比較法", "收益法", "成本法"], ["有資質託管", "定期檢查"]),
            AssetRule("債券", ["信用評級", "評級報告", "合法發行", "資訊披露"], ["信用風險", "利率", "流動性", "通脹"],
                      ["財報", "評級報告", "法律意見", "用途說明"], ["現金流法", "收益率比較"], ["合規託管", "付息兌付"])
        ]

    def enhance_findings(self, findings: List[Any]) -> List[Any]:
        # 增強漏洞描述，加入案例、最佳實踐或合規提示
        for finding in findings:
            vt = getattr(finding, 'vulnerability_type', '')
            case = next((c for c in self.cases if vt in c.vuln_type), None)
            if case: finding.description += f"\n參考案例: {case.name}" 
            bp = next((p for p in self.best_practices if vt[:2] in p.category), None)
            if bp: finding.recommendation += f"\n建議: {bp.name}" 
        return findings

    def summary(self) -> Dict[str, Any]:
        return {
            "reg_requirements": [asdict(r) for r in self.reg_requirements],
            "best_practices": [asdict(p) for p in self.best_practices],
            "cases": [asdict(c) for c in self.cases],
            "asset_rules": [asdict(a) for a in self.asset_rules],
            "last_updated": datetime.now().isoformat()
        }

# 單元測試
if __name__ == "__main__":
    kb = RWAKnowledgeBase()
    print("SEC合規要求:")
    for r in kb.reg_requirements:
        if r.jurisdiction == "SEC": print('-', r.requirement, r.description)
    print("\n合約安全最佳實踐:")
    for p in kb.best_practices:
        if p.category == "合約安全": print('-', p.name, p.description)
    print("\n重大案例:")
    for c in kb.cases:
        print('-', c.name, "損失:$", c.loss)
    print("\n摘要:")
    print(kb.summary())