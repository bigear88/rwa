# inference_engine.py
# LLM推理引擎，串接漏洞生成器與漏洞判別器，主流程實作

import logging
from typing import List, Dict, Any

# 假設同目錄下引入
from vulnerability_generator import VulnerabilityGenerator, PotentialVulnerability
from vulnerability_discriminator import VulnerabilityDiscriminator, SecurityFinding

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMInferenceEngine:
    """
    LLM推理引擎 - 它自動初始化漏洞生成器與漏洞判別器，
    提供analyze_contract主流程接口，對外輸入預處理合約資料，輸出結構化安全發現結果。
    """

    def __init__(self):
        try:
            self.generator = VulnerabilityGenerator()
            self.discriminator = VulnerabilityDiscriminator()
            logger.info("LLMInferenceEngine 初始化完成")
        except Exception as e:
            logger.error(f"初始化LLMInferenceEngine失敗: {e}")
            raise RuntimeError("LLMInferenceEngine初始化失敗")

    def analyze_contract(self, processed_data: Dict[str, Any]) -> List[SecurityFinding]:
        """
        整合漏洞生成與判別兩大模組，輸出安全發現列表。
        """
        logger.info("⏳(1/2) 啟動漏洞生成器進行智能合約potential風險識別 ...")
        try:
            potential_vulns = self.generator.generate_vulnerabilities(processed_data)
        except Exception as e:
            logger.error(f"漏洞生成階段異常: {e}")
            potential_vulns = []

        logger.info(f"檢測到 {len(potential_vulns)} 個潛在漏洞，進入判別校核 ...")
        try:
            findings = self.discriminator.verify_vulnerabilities([
                pv.__dict__ if hasattr(pv, '__dict__') else pv for pv in potential_vulns
            ])
        except Exception as e:
            logger.error(f"漏洞判別階段異常: {e}")
            findings = []

        logger.info(f"分析完畢，輸出安全發現數量：{len(findings)}")
        return findings

# 單元測試入口
if __name__ == "__main__":
    # 模擬一組processed_data
    processed_data = {
        "contract_code": "pragma solidity ^0.8.0;\ncontract Demo { function withdraw() public { msg.sender.call(''); } }",
        "functions": [
            {"name": "withdraw", "line_number": 2, "signature": "function withdraw() public", "visibility": "public",
             "state_mutability": "", "modifiers": [], "parameters": [], "return_type": None, "is_payable": False, "is_critical": True}
        ]
    }
    engine = LLMInferenceEngine()
    findings = engine.analyze_contract(processed_data)
    print("分析結果：")
    for f in findings:
        print(f)
