# RWA Security Framework (Real-World Asset Security Framework)

本專案是「基於大型語言模型的DeFi智能合約漏洞檢測方法研究」論文的實驗程式碼框架。

## 專案結構

```
rwa_project/
├── core/
│   ├── multimodal_processor.py    # 多模態輸入處理
│   ├── vulnerability_generator.py  # 漏洞生成器  
│   ├── vulnerability_discriminator.py # 漏洞判別器
│   ├── inference_engine.py        # LLM推理引擎
│   └── knowledge_base.py          # RWA知識庫
├── learning/
│   └── continuous_learning.py     # 持續學習機制
├── framework/
│   └── audit_framework.py.txt     # 主框架整合
├── models/
│   └── security_models.py         # 安全模型定義
└── tests/
    └── comprehensive_test.py.txt   # 綜合測試
```

## 部署與執行

1. **環境設定**: 
   - 安裝Python依賴：`pip install -r requirements.txt` (需自行創建)
   - 配置LLM API Key

2. **執行測試**:
   - 運行綜合測試：`python tests/comprehensive_test.py.txt`

## 貢獻

歡迎對本專案提出建議或貢獻程式碼。
