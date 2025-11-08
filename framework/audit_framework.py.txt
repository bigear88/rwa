# audit_framework.py
# RWA智能合約安全審計主框架

import logging
from typing import List, Dict, Any
from datetime import datetime

from multimodal_processor import MultimodalInputProcessor
from inference_engine import LLMInferenceEngine, SecurityFinding
from knowledge_base import RWAKnowledgeBase
from continuous_learning import ContinuousLearningSystem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RWASecurityAuditFramework:
    """
    主框架: 整合多模態處理、LLM推理、安全知識庫、持續學習，產生結構化審計報告
    """
    def __init__(self):
        self.input_processor = MultimodalInputProcessor()
        self.inference_engine = LLMInferenceEngine()
        self.knowledge_base = RWAKnowledgeBase()
        self.learning_system = ContinuousLearningSystem()
        self.statistics = {"audits": [], "total_processed": 0}
        logger.info("審計主框架初始化完成")

    def audit_contract(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("開始執行RWA智能合約安全審計")
        start_time = datetime.now()

        # 1、多模態輸入處理
        try:
            processed = self.input_processor.process_smart_contract(contract_data.get("contract_code", ""))
            if "legal_documents" in contract_data:
                processed.update(self.input_processor.process_legal_documents(contract_data["legal_documents"]))
            if "asset_proofs" in contract_data:
                processed.update(self.input_processor.process_asset_proofs(contract_data["asset_proofs"]))
            if "transactions" in contract_data:
                processed.update(self.input_processor.process_transaction_history(contract_data["transactions"]))
            logger.info("多模態處理完成")
        except Exception as e:
            logger.error(f"多模態處理錯誤: {e}")
            processed = {}

        # 2、LLM推理分析
        try:
            findings = self.inference_engine.analyze_contract(processed)
            logger.info(f"推理分析完成，發現漏洞：{len(findings)}")
        except Exception as e:
            logger.error(f"LLM推理失敗: {e}")
            findings = []

        # 3、知識庫增強
        try:
            enhanced_findings = self.knowledge_base.enhance_findings(findings)
            logger.info("知識庫增強完成")
        except Exception as e:
            logger.error(f"知識庫增強失敗: {e}")
            enhanced_findings = findings

        # 4、合規與資產狀態分析
        compliance_score = processed.get("average_compliance_score", 0)
        verification_rate = processed.get("verification_rate", 1.0)
        asset_value = processed.get("total_value", 0)

        # 5、持續學習性能紀錄
        try:
            perf_metrics = self.learning_system.monitor_performance(
                enhanced_findings, enhanced_findings, (datetime.now() - start_time).total_seconds()
            )
            logger.info("性能監控完成")
        except Exception as e:
            logger.error(f"持續學習性能紀錄失敗: {e}")
            perf_metrics = {}

        # 6、產生完整報告
        audit_report = {
            "audit_id": f"RWA-{hash(datetime.now()) & 0xfff:x}",
            "timestamp": datetime.now().isoformat(),
            "contract_summary": {
                "lang": processed.get("language", "unknown"),
                "lines": processed.get("basic_analysis", {}).get("total_lines", 0),
                "functions": len(processed.get("functions", [])),
            },
            "asset_summary": {
                "total_value": asset_value,
                "verification_rate": verification_rate
            },
            "compliance": {
                "score": compliance_score,
                "legal_frameworks": processed.get("regulatory_frameworks", [])
            },
            "security_findings": [f.__dict__ if hasattr(f, '__dict__') else f for f in enhanced_findings],
            "performance": perf_metrics if isinstance(perf_metrics, dict) else perf_metrics.__dict__,
            "statistics": {
                "total_audits": len(self.statistics["audits"]) + 1,
                "average_processing_time": float(perf_metrics.get("processing_time", 0)) if perf_metrics else None,
            },
            "recommendations": [f.recommendation for f in enhanced_findings],
        }
        self.statistics["audits"].append(audit_report)
        self.statistics["total_processed"] += 1
        logger.info("審計流程完成，結果已輸出")
        return audit_report

# 單元測試
if __name__ == "__main__":
    test_data = {
        "contract_code": "pragma solidity ^0.8.0;\ncontract Demo { function withdraw() public { msg.sender.call(''); } }",
        "legal_documents": ["SEC Regulation D, KYC policy"],
        "asset_proofs": [{"asset_id": "A1", "asset_type": "real_estate", "value": 123456, "custody_info": ""}],
        "transactions": [{"from_address": "0xabc", "to_address": "0xdef", "value": 10000}]
    }
    framework = RWASecurityAuditFramework()
    result = framework.audit_contract(test_data)
    print("---------審計報告---------")
    for k, v in result.items():
        print(f"{k}: {v}")
