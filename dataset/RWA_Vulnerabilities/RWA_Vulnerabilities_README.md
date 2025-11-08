# RWA Synthetic Vulnerability Dataset

This directory contains the synthetic test cases designed to evaluate the RWA Security Framework's ability to detect complex, RWA-specific logical and compliance vulnerabilities that traditional static analysis tools often miss.

The dataset is generated based on the experimental design outlined in the thesis: "基於大型語言模型的RWA智能合約安全檢核框架".

## 檔案結構

### `rwa_synthetic_vulnerability_dataset.json`

此 JSON 檔案包含 **25 個**模擬的 RWA 特定漏洞案例。每個案例都以結構化的方式描述，以便於框架進行訓練、測試和評估。

每個 JSON 物件包含以下欄位：

| 欄位名稱 | 說明 | 範例值 |
| :--- | :--- | :--- |
| `case_id` | 唯一的案例識別碼。 | `RWA-SYN-001` |
| `vulnerability_type` | 漏洞的類型，特別強調 RWA 相關的邏輯或合規問題。 | `Compliance Bypass (KYC/AML)` |
| `description` | 漏洞的詳細描述，解釋其邏輯缺陷。 | `The transfer function lacks a check against the KYC/AML whitelist...` |
| `severity` | 漏洞的嚴重程度（Critical, High, Medium, Low）。 | `Critical` |
| `affected_contract_type` | 該漏洞可能影響的合約類型（例如：TSMC2330, TW50, 或 All RWA Contracts）。 | `TSMC2330` |
| `mitigation_suggestion` | 針對該漏洞的修復建議。 | `Implement a require(isCompliant(to)) check in the _transfer function.` |

## 涵蓋的漏洞類別

此數據集主要涵蓋了論文中強調的 RWA 特有風險：

1.  **合規性違規 (Compliance Bypass)**：例如 KYC/AML 檢查繞過、制裁名單檢查缺失。
2.  **資產映射錯誤 (Asset Mapping Error)**：例如鏈上狀態與鏈下資產法律狀態不一致、元數據不匹配。
3.  **預言機操縱 (Oracle Manipulation)**：例如價格新鮮度檢查缺失、單一預言機依賴。
4.  **業務邏輯缺陷 (Business Logic Flaw)**：例如抵押品計算錯誤、緊急關閉機制缺失。

這個數據集將作為評估「本框架 (多模態)」相較於傳統工具優勢的關鍵測試集。
