import os
import glob
import subprocess

# 確保結果目錄存在
PROJECT_ROOT = "/home/ubuntu/rwa_project"
CONTRACTS_DIR = os.path.join(PROJECT_ROOT, "dataset", "RWA_Contracts")
MULTIMODAL_DIR = os.path.join(PROJECT_ROOT, "dataset", "RWA_Multimodal_Inputs")
os.makedirs(MULTIMODAL_DIR, exist_ok=True)

# 法律意見書模板 (Markdown)
LEGAL_OPINION_TEMPLATE = """# 法律意見書摘要：{name}股票代幣化 ({code})

**日期**：2025 年 11 月 8 日
**發件人**：RWA 實驗室
**收件人**：RWA 智能合約安全檢核框架實驗室

## 1. 目的

本意見書旨在確認將 {name}（股票代碼：{code}）的股票代幣化為鏈上 ERC-20 代幣的法律合規性。

## 2. 關鍵合規要求

根據現行法規，{name} Token 被視為**證券型代幣 (Security Token)**，必須遵守以下核心要求：

| 要求類別 | 具體內容 | 鏈上實現要求 |
| :--- | :--- | :--- |
| **KYC/AML** | 所有代幣持有者和交易對手必須通過 KYC/AML 審查。 | 必須實施**白名單機制**，限制代幣轉移給未經審查的地址。 |
| **轉讓限制** | 必須遵守特定司法管轄區的轉讓限制。 | 智能合約的 `transfer` 函數必須包含**轉讓規則檢查**。 |
| **資產映射** | 鏈上代幣數量必須與鏈下託管的實際股票數量保持 1:1 的映射。 | 必須有**發行者 (Issuer)** 角色，且發行（Mint）和銷毀（Burn）操作必須嚴格受控。 |
| **預言機數據** | 股票價格數據必須來自經認可的、可靠的數據源。 | 智能合約必須檢查預言機數據的**新鮮度 (Freshness)** 和**有效性 (Validity)**。 |

## 3. 結論

{name} Token 的智能合約（{code}.sol）在實施上述要求時，必須確保所有關鍵功能都包含對這些法律要求的程式碼級別檢查。

**本意見書的關鍵詞**：`證券型代幣`, `KYC/AML`, `白名單`, `轉讓限制`, `資產映射`, `預言機數據`, `新鮮度`。
"""

# 資產映射報告模板 (Markdown)
ASSET_MAPPING_REPORT_TEMPLATE = """# {name} ({code}) 資產映射報告摘要

**報告期**：2025 年 Q4
**資產類型**：{asset_type}
**核心問題**：鏈上代幣價值是否準確反映鏈下資產表現（資產映射一致性）。

## 1. 映射一致性指標 (Mapping Consistency Index)

映射一致性指標是衡量鏈上代幣與鏈下資產價值差異的關鍵指標。

| 報告期 | 映射一致性指標 (Basis Points) | 備註 |
| :--- | :--- | :--- |
| 2025 Q4 | {mapping_index} bps | 處於正常波動範圍內。 |
| 2025 Q3 | {mapping_index_prev} bps | 表現穩定。 |

**RWA 框架相關性**：映射一致性指標過大可能導致鏈上代幣的價格與其聲稱代表的資產價值不符，構成**資產映射錯誤**的風險。

## 2. 鏈下資產審計

本報告確認，用於鏈上 {name} 代幣發行的鏈下資產已通過獨立審計，資產儲備與鏈上發行量**保持一致**。

**RWA 框架相關性**：確保鏈上鏈下資產映射的**一致性**是多模態分析的重點。

**本報告的關鍵詞**：`映射一致性`, `資產映射`, `{asset_type}`, `鏈下審計`。
"""

def get_contract_info():
    """從 RWA_Contracts 目錄中讀取合約資訊"""
    contract_files = glob.glob(os.path.join(CONTRACTS_DIR, "*.sol"))
    info_list = []
    
    # 讀取 generate_rwa_contracts.py 中的配置表來獲取名稱和類型
    # 由於無法直接導入，這裡使用一個簡化的映射或從文件名中提取
    
    # 簡化提取邏輯：假設文件名是股票代碼
    for filepath in contract_files:
        filename = os.path.basename(filepath)
        code = filename.replace(".sol", "")
        
        # 排除 AAPL.sol, AAPL_Clean.sol, AAPL_Vulnerable.sol, tw50.sol, tsmc2330.sol, largan3008.sol
        if not code.isdigit() and code not in ["AAPL", "AAPL_Clean", "AAPL_Vulnerable", "tw50", "tsmc2330", "largan3008"]:
            continue
            
        # 為了簡化，我們只處理數字代碼的合約，並假設它們是股票
        if code.isdigit():
            name = f"台灣上市公司 ({code})"
            asset_type = "股票"
        elif code == "tw50":
            name = "台灣五十 ETF"
            asset_type = "ETF"
        elif code == "tsmc2330":
            name = "台積電"
            asset_type = "股票"
        elif code == "largan3008":
            name = "大立光"
            asset_type = "股票"
        elif code in ["AAPL", "AAPL_Clean", "AAPL_Vulnerable"]:
            name = "蘋果公司 (AAPL) 模擬"
            asset_type = "股票"
        else:
            continue

        info_list.append({"code": code, "name": name, "asset_type": asset_type})
        
    return info_list

def generate_multimodal_files():
    """生成多模態輸入文件"""
    contract_infos = get_contract_info()
    
    # 排除已存在的 TSMC2330_Legal_Opinion.pdf, Fubon2881_Capital_Adequacy.csv, TW50_Index_Tracking_Report.md
    existing_files = [
        "TSMC2330_Legal_Opinion.pdf", 
        "Fubon2881_Capital_Adequacy.csv", 
        "TW50_Index_Tracking_Report.md"
    ]
    
    generated_count = 0
    
    for info in contract_infos:
        code = info["code"]
        name = info["name"]
        asset_type = info["asset_type"]
        
        # 1. 法律意見書 (PDF)
        md_content = LEGAL_OPINION_TEMPLATE.format(code=code, name=name)
        md_path = os.path.join(MULTIMODAL_DIR, f"{code}_Legal_Opinion.md")
        pdf_path = os.path.join(MULTIMODAL_DIR, f"{code}_Legal_Opinion.pdf")
        
        # 檢查是否是已存在的 TSMC2330 檔案，如果是則跳過 MD 生成，因為 PDF 已經存在
        if f"{code}_Legal_Opinion.pdf" not in existing_files:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            # 轉換為 PDF
            try:
                subprocess.run(["manus-md-to-pdf", md_path, pdf_path], check=True, capture_output=True)
                os.remove(md_path) # 刪除中間的 MD 文件
                generated_count += 1
            except subprocess.CalledProcessError as e:
                print(f"Error converting {md_path} to PDF: {e.stderr.decode()}")
        
        # 2. 資產映射報告 (Markdown)
        md_filename = f"{code}_Asset_Mapping_Report.md"
        if md_filename not in existing_files:
            mapping_index = np.random.randint(10, 50) # 模擬隨機的映射指數
            mapping_index_prev = np.random.randint(10, 50)
            
            md_content = ASSET_MAPPING_REPORT_TEMPLATE.format(
                code=code, 
                name=name, 
                asset_type=asset_type,
                mapping_index=mapping_index,
                mapping_index_prev=mapping_index_prev
            )
            
            md_path = os.path.join(MULTIMODAL_DIR, md_filename)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            generated_count += 1
            
    print(f"Total new multimodal files generated: {generated_count}")

if __name__ == "__main__":
    # 確保 numpy 已導入
    import numpy as np
    generate_multimodal_files()
