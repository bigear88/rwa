# comprehensive_test.py
# RWA智能合約安全檢核系統 - 全模組綜合測試

from audit_framework import RWASecurityAuditFramework
import json
import time

def print_section(title):
    print("\n" + "=" * 70)
    print(f"{title}")
    print("=" * 70)

def summary_report(audit_result):
    print_section("合約摘要")
    cs = audit_result.get("contract_summary", {})
    print(f"語言: {cs.get('lang')}, 程式行數: {cs.get('lines')}, 函數數量: {cs.get('functions')}")
    print_section("資產資訊")
    asset = audit_result.get("asset_summary", {})
    print(f"總價值: {asset.get('total_value')}, 驗證率: {asset.get('verification_rate')}")
    print_section("合規評估")
    comp = audit_result.get('compliance', {})
    print(f"分數: {comp.get('score')}\n法律/監管架構: {comp.get('legal_frameworks')}")
    print_section("主要安全發現")
    for i, f in enumerate(audit_result.get("security_findings", [])[:5], 1):
        print(f"[{i}] {f['vulnerability_type']}, 嚴重性: {f['severity']}, 描述: {f['description'][:60]}...")
        print(f"  建議: {f['recommendation'][:60]}...")
    print_section("改進建議")
    for r in audit_result.get('recommendations', [])[:3]:
        print("-", r[:90])
    print_section("性能指標")
    perf = audit_result.get("performance", {})
    print(json.dumps(perf, ensure_ascii=False, indent=2))
    print_section("結構化報告(精簡)")
    print(json.dumps(audit_result, indent=2, ensure_ascii=False)[:2000], "\n...")

def make_test_cases():
    return [
        {
            "title": "高風險典型(RWA房地產)",
            "data": {
                "contract_code": "pragma solidity ^0.8.0; contract Risky { function withdraw() public { msg.sender.call(''); } function admin() {selfdestruct(owner);} }",
                "legal_documents": ["SEC Regulation S, 跨境託管缺失"],
                "asset_proofs": [{"asset_id": "NY01", "asset_type": "real_estate", "value": 12000000, "custody_info": ""}],
                "transactions": [{"from_address": "0xa", "to_address": "0xb", "value": 80000000}]
            }
        },
        {
            "title": "中風險(企業債券)",
            "data": {
                "contract_code": "pragma solidity ^0.8.0; contract Bond { function invest(uint amount) public {} }",
                "legal_documents": ["MAS發行規則, KYC標準"],
                "asset_proofs": [{"asset_id": "B777", "asset_type": "bonds", "value": 5000000, "custody_info": "銀行保管"}],
                "transactions": [{"from_address": "0x1", "to_address": "0x2", "value": 15000}]
            }
        },
        {
            "title": "低風險(完整合規)",
            "data": {
                "contract_code": "pragma solidity ^0.8.0; contract Safe { function deposit() public payable {} }",
                "legal_documents": ["FCA全流程合規, 完備KYC/AML"],
                "asset_proofs": [{"asset_id": "GOLD01", "asset_type": "precious_metals", "value": 300000, "custody_info": "合約存證"}],
                "transactions": [{"from_address": "0x3", "to_address": "0x4", "value": 1000}]
            }
        }
    ]

def main():
    print_section("RWA智能合約安全審計-多案例綜合測試")
    framework = RWASecurityAuditFramework()
    cases = make_test_cases()
    for case in cases:
        print_section(f"測試案例: {case['title']}")
        start = time.time()
        result = framework.audit_contract(case["data"])
        summary_report(result)
        print(f"測試耗時: {round(time.time() - start, 3)} 秒\n")

if __name__ == "__main__":
    main()
