# RWA Multimodal Inputs Dataset

This directory contains simulated non-code documents and data structures used as **multimodal inputs** for the RWA Security Framework experiment.

The purpose of this dataset is to demonstrate the framework's ability to process and integrate information from diverse sources (code, legal documents, financial data) to detect RWA-specific vulnerabilities, proving that the mechanism is asset-type agnostic.

## 檔案列表

| 檔案名稱 | 類型 | 相關資產類型 | 核心 RWA 議題 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| `TSMC2330_Legal_Opinion.pdf` | PDF (法律文件) | 科技股 (台積電) | 合規性 (KYC/AML, 轉讓限制) | 模擬法律意見書，用於提取合規性要求。 |
| `Fubon2881_Capital_Adequacy.csv` | CSV (結構化數據) | 金融股 (富邦金) | 抵押品/發行要求 (資本適足率) | 模擬金融機構的資本數據，用於檢查發行合規性。 |
| `TW50_Index_Tracking_Report.md` | Markdown (報告文件) | ETF (台灣五十) | 資產映射 (追蹤誤差) | 模擬指數追蹤報告，用於檢查鏈上代幣與鏈下資產的一致性。 |

## 實驗意義

這些文件證明了框架的**多模態輸入處理層**能夠靈活適應不同資產類型的特定文件格式與數據結構：

*   **PDF/Markdown**：用於提取非結構化的法律和報告文本中的**合規性要求**和**資產映射邏輯**。
*   **CSV/JSON**：用於處理結構化的**金融數據**，例如抵押率、資本適足率等，以驗證業務邏輯的正確性。

框架通過將這些信息與智能合約程式碼（例如 `isCompliant()` 函數）進行交叉驗證，來檢測傳統工具無法發現的 RWA 特定邏輯漏洞。
