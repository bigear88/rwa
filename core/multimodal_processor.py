# multimodal_processor.py
# 基於大型語言模型的RWA智能合約安全檢核框架 - 多模態輸入處理模組

import json
import hashlib
import logging
import re
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AssetType(Enum):
    """資產類型枚舉"""
    REAL_ESTATE = "real_estate"
    CORPORATE_BONDS = "corporate_bonds"
    COMMODITIES = "commodities"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    EQUITY_SECURITIES = "equity_securities"
    GOVERNMENT_BONDS = "government_bonds"
    PRECIOUS_METALS = "precious_metals"
    CARBON_CREDITS = "carbon_credits"

class ComplianceFramework(Enum):
    """合規框架枚舉"""
    SEC = "SEC"
    MAS = "MAS"
    FCA = "FCA"
    CFTC = "CFTC"
    FINMA = "FINMA"
    ESMA = "ESMA"

@dataclass
class ContractFunction:
    """智能合約函數信息"""
    name: str
    line_number: int
    signature: str
    visibility: str
    state_mutability: str
    modifiers: List[str]
    parameters: List[str]
    return_type: Optional[str]
    is_payable: bool
    is_critical: bool

@dataclass
class SecurityPattern:
    """安全模式檢測結果"""
    pattern_type: str
    count: int
    locations: List[int]
    risk_level: str
    description: str

@dataclass
class AssetVerification:
    """資產驗證結果"""
    asset_id: str
    verification_status: bool
    verification_score: float
    issues: List[str]
    documents_complete: bool
    custody_verified: bool
    valuation_current: bool

class MultimodalInputProcessor:
    """
    多模態輸入處理層
    
    負責處理智能合約源代碼、法律文件、資產證明文件、交易歷史等
    多元化數據源，提供統一的數據預處理和特徵提取功能。
    """
    
    def __init__(self):
        """初始化多模態輸入處理器"""
        self.supported_languages = ["solidity", "vyper"]
        self.security_keywords = self._init_security_keywords()
        self.compliance_keywords = self._init_compliance_keywords()
        self.asset_type_mapping = self._init_asset_type_mapping()
        self.risk_indicators = self._init_risk_indicators()
        
        logger.info("多模態輸入處理層初始化完成")
    
    def _init_security_keywords(self) -> Dict[str, List[str]]:
        """初始化安全相關關鍵詞"""
        return {
            "reentrancy": ["call", "send", "transfer", "delegatecall", "call.value"],
            "access_control": ["onlyOwner", "onlyAdmin", "require", "modifier", "msg.sender", "tx.origin"],
            "overflow": ["add", "sub", "mul", "div", "++", "--", "+=", "-=", "*=", "/="],
            "timestamp": ["block.timestamp", "now", "block.number", "block.difficulty"],
            "randomness": ["blockhash", "block.difficulty", "keccak256", "sha256"],
            "external_calls": ["call", "delegatecall", "staticcall", "send", "transfer"],
            "state_changes": ["storage", "mapping", "struct", "array"],
            "gas": ["gasleft", "gas", "gasLimit", "gasPrice"],
            "assembly": ["assembly", "inline", "low-level"],
            "selfdestruct": ["selfdestruct", "suicide"],
            "fallback": ["fallback", "receive", "payable"]
        }
    
    def _init_compliance_keywords(self) -> Dict[str, List[str]]:
        """初始化合規相關關鍵詞"""
        return {
            "kyc_aml": [
                "know your customer", "kyc", "anti-money laundering", "aml",
                "customer due diligence", "cdd", "enhanced due diligence", "edd",
                "politically exposed person", "pep", "sanctions screening",
                "source of funds", "beneficial ownership", "identity verification"
            ],
            "accredited_investor": [
                "accredited investor", "qualified purchaser", "sophisticated investor",
                "high net worth", "institutional investor", "retail investor",
                "professional client", "eligible counterparty"
            ],
            "disclosure": [
                "risk disclosure", "material information", "prospectus", "offering document",
                "private placement memorandum", "ppm", "form d", "filing",
                "financial statements", "audit", "transparency"
            ],
            "regulatory_compliance": [
                "regulation d", "rule 506", "securities act", "investment company act",
                "investment advisers act", "commodity exchange act", "cftc", "sec",
                "registration", "exemption", "safe harbor", "no-action letter"
            ],
            "investor_protection": [
                "investor protection", "suitability", "best execution", "fiduciary duty",
                "conflict of interest", "fair dealing", "market manipulation",
                "insider trading", "front running"
            ]
        }
    
    def _init_asset_type_mapping(self) -> Dict[str, AssetType]:
        """初始化資產類型映射"""
        return {
            "real estate": AssetType.REAL_ESTATE,
            "property": AssetType.REAL_ESTATE,
            "commercial real estate": AssetType.REAL_ESTATE,
            "residential real estate": AssetType.REAL_ESTATE,
            "mixed use real estate": AssetType.REAL_ESTATE,
            "bond": AssetType.CORPORATE_BONDS,
            "corporate bond": AssetType.CORPORATE_BONDS,
            "government bond": AssetType.GOVERNMENT_BONDS,
            "treasury": AssetType.GOVERNMENT_BONDS,
            "commodity": AssetType.COMMODITIES,
            "gold": AssetType.PRECIOUS_METALS,
            "silver": AssetType.PRECIOUS_METALS,
            "platinum": AssetType.PRECIOUS_METALS,
            "patent": AssetType.INTELLECTUAL_PROPERTY,
            "trademark": AssetType.INTELLECTUAL_PROPERTY,
            "copyright": AssetType.INTELLECTUAL_PROPERTY,
            "carbon credit": AssetType.CARBON_CREDITS,
            "carbon offset": AssetType.CARBON_CREDITS,
            "equity": AssetType.EQUITY_SECURITIES,
            "stock": AssetType.EQUITY_SECURITIES
        }
    
    def _init_risk_indicators(self) -> Dict[str, Dict[str, float]]:
        """初始化風險指標權重"""
        return {
            "code_complexity": {
                "high_function_count": 0.3,
                "deep_nesting": 0.4,
                "long_functions": 0.2,
                "many_dependencies": 0.1
            },
            "asset_risk": {
                "low_verification_rate": 0.4,
                "insufficient_insurance": 0.3,
                "concentrated_geography": 0.2,
                "outdated_valuation": 0.1
            },
            "transaction_risk": {
                "high_volatility": 0.3,
                "unusual_patterns": 0.4,
                "large_transactions": 0.2,
                "frequent_small_transactions": 0.1
            }
        }
    
    def process_smart_contract(self, contract_code: str, 
                              contract_language: str = "solidity") -> Dict[str, Any]:
        """
        處理智能合約源代碼
        
        Args:
            contract_code: 智能合約源代碼
            contract_language: 合約語言 (solidity, vyper)
            
        Returns:
            處理後的合約分析結果
        """
        try:
            logger.info(f"開始處理 {contract_language} 智能合約...")
            
            # 基本代碼分析
            basic_analysis = self._analyze_basic_structure(contract_code)
            
            # AST解析
            ast_info = self._parse_contract_ast(contract_code, contract_language)
            
            # 函數提取與分析
            functions = self._extract_and_analyze_functions(contract_code)
            
            # 依賴關係分析
            dependencies = self._analyze_dependencies(contract_code)
            
            # 安全模式檢測
            security_patterns = self._detect_security_patterns(contract_code)
            
            # 複雜度分析
            complexity_metrics = self._calculate_complexity_metrics(contract_code, functions)
            
            # 狀態變數分析
            state_variables = self._analyze_state_variables(contract_code)
            
            # 事件分析
            events = self._analyze_events(contract_code)
            
            # 修飾符分析
            modifiers = self._analyze_modifiers(contract_code)
            
            # 繼承關係分析
            inheritance = self._analyze_inheritance(contract_code)
            
            # 代碼質量評估
            code_quality = self._assess_code_quality(contract_code, functions, security_patterns)
            
            result = {
                "contract_code": contract_code,
                "language": contract_language,
                "basic_analysis": basic_analysis,
                "ast_info": ast_info,
                "functions": [func.__dict__ for func in functions],
                "dependencies": dependencies,
                "security_patterns": [pattern.__dict__ for pattern in security_patterns],
                "complexity_metrics": complexity_metrics,
                "state_variables": state_variables,
                "events": events,
                "modifiers": modifiers,
                "inheritance": inheritance,
                "code_quality": code_quality,
                "code_hash": hashlib.sha256(contract_code.encode()).hexdigest(),
                "processing_timestamp": datetime.now().isoformat()
            }
            
            logger.info("智能合約處理完成")
            return result
            
        except Exception as e:
            logger.error(f"智能合約處理錯誤: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def process_legal_documents(self, legal_docs: List[str], 
                               document_types: List[str] = None) -> Dict[str, Any]:
        """
        處理法律文件
        
        Args:
            legal_docs: 法律文件列表
            document_types: 文件類型列表 (optional)
            
        Returns:
            法律文件分析結果
        """
        try:
            logger.info(f"開始處理 {len(legal_docs)} 份法律文件...")
            
            processed_docs = []
            total_compliance_score = 0
            regulatory_frameworks = set()
            compliance_coverage = {
                "kyc_aml": False,
                "investor_accreditation": False,
                "disclosure_requirements": False,
                "custody_arrangements": False,
                "risk_disclosure": False
            }
            
            for i, doc in enumerate(legal_docs):
                doc_type = document_types[i] if document_types and i < len(document_types) else "general"
                
                # 基本文檔分析
                doc_analysis = self._analyze_document_structure(doc)
                
                # 合規要求提取
                compliance_requirements = self._extract_compliance_requirements(doc)
                
                # 司法管轄區識別
                jurisdiction = self._identify_jurisdiction(doc)
                regulatory_frameworks.add(jurisdiction)
                
                # 關鍵條款提取
                key_terms = self._extract_key_terms(doc)
                
                # 風險因子識別
                risk_factors = self._identify_risk_factors(doc)
                
                # 合規評分計算
                compliance_score = self._calculate_compliance_score(doc, compliance_requirements)
                total_compliance_score += compliance_score
                
                # 更新合規覆蓋狀況
                self._update_compliance_coverage(doc, compliance_coverage)
                
                # 法律實體識別
                legal_entities = self._identify_legal_entities(doc)
                
                # 日期和期限提取
                dates_and_deadlines = self._extract_dates_and_deadlines(doc)
                
                doc_info = {
                    "document_index": i,
                    "document_type": doc_type,
                    "content_length": len(doc),
                    "analysis": doc_analysis,
                    "compliance_requirements": compliance_requirements,
                    "jurisdiction": jurisdiction,
                    "key_terms": key_terms,
                    "risk_factors": risk_factors,
                    "compliance_score": compliance_score,
                    "legal_entities": legal_entities,
                    "dates_and_deadlines": dates_and_deadlines,
                    "content_hash": hashlib.sha256(doc.encode()).hexdigest()
                }
                processed_docs.append(doc_info)
            
            avg_compliance_score = total_compliance_score / len(legal_docs) if legal_docs else 0
            
            # 整體合規狀態評估
            overall_compliance = self._assess_overall_compliance(
                avg_compliance_score, compliance_coverage, regulatory_frameworks
            )
            
            result = {
                "legal_documents": processed_docs,
                "total_documents": len(legal_docs),
                "average_compliance_score": avg_compliance_score,
                "regulatory_frameworks": list(regulatory_frameworks),
                "compliance_coverage": compliance_coverage,
                "overall_compliance": overall_compliance,
                "processing_timestamp": datetime.now().isoformat()
            }
            
            logger.info("法律文件處理完成")
            return result
            
        except Exception as e:
            logger.error(f"法律文件處理錯誤: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def process_asset_proofs(self, asset_proofs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        處理資產證明文件
        
        Args:
            asset_proofs: 資產證明文件列表
            
        Returns:
            資產證明分析結果
        """
        try:
            logger.info(f"開始處理 {len(asset_proofs)} 項資產證明...")
            
            verified_assets = []
            total_value = 0
            verification_results = []
            asset_type_distribution = defaultdict(int)
            geographic_distribution = defaultdict(float)
            risk_assessment = {
                "high_risk_assets": 0,
                "medium_risk_assets": 0,
                "low_risk_assets": 0
            }
            
            for proof in asset_proofs:
                # 資產驗證
                verification_result = self._verify_asset_proof(proof)
                verification_results.append(verification_result)
                
                # 資產類型識別
                asset_type = self._identify_asset_type(proof)
                asset_type_distribution[asset_type.value if asset_type else "unknown"] += 1
                
                # 資產風險評估
                asset_risk = self._assess_asset_risk(proof, verification_result)
                
                # 地理分佈分析
                geographic_info = self._extract_geographic_info(proof)
                if geographic_info:
                    geographic_distribution[geographic_info] += proof.get("value", 0)
                
                # 估值分析
                valuation_analysis = self._analyze_valuation(proof)
                
                # 流動性評估
                liquidity_assessment = self._assess_asset_liquidity(proof, asset_type)
                
                # 保險覆蓋分析
                insurance_analysis = self._analyze_insurance_coverage(proof)
                
                asset_info = {
                    "asset_id": proof.get("asset_id"),
                    "asset_type": asset_type.value if asset_type else "unknown",
                    "value": proof.get("value", 0),
                    "verification_result": verification_result.__dict__,
                    "risk_assessment": asset_risk,
                    "geographic_info": geographic_info,
                    "valuation_analysis": valuation_analysis,
                    "liquidity_assessment": liquidity_assessment,
                    "insurance_analysis": insurance_analysis,
                    "custody_info": proof.get("custody_info"),
                    "last_update": proof.get("valuation_date") or proof.get("last_update")
                }
                
                verified_assets.append(asset_info)
                total_value += asset_info["value"]
                
                # 更新風險統計
                if asset_risk["risk_level"] == "HIGH":
                    risk_assessment["high_risk_assets"] += 1
                elif asset_risk["risk_level"] == "MEDIUM":
                    risk_assessment["medium_risk_assets"] += 1
                else:
                    risk_assessment["low_risk_assets"] += 1
            
            # 整體組合分析
            portfolio_analysis = self._analyze_asset_portfolio(
                verified_assets, asset_type_distribution, geographic_distribution
            )
            
            # 計算關鍵指標
            verification_rate = len([v for v in verification_results if v.verification_status]) / len(verification_results) if verification_results else 0
            insurance_coverage_ratio = self._calculate_insurance_coverage_ratio(verified_assets)
            diversification_score = self._calculate_diversification_score(asset_type_distribution, geographic_distribution)
            
            result = {
                "verified_assets": verified_assets,
                "total_assets": len(asset_proofs),
                "total_value": total_value,
                "verification_rate": verification_rate,
                "verification_issues": [issue for result in verification_results for issue in result.issues],
                "asset_type_distribution": dict(asset_type_distribution),
                "geographic_distribution": dict(geographic_distribution),
                "risk_assessment": risk_assessment,
                "portfolio_analysis": portfolio_analysis,
                "insurance_coverage_ratio": insurance_coverage_ratio,
                "diversification_score": diversification_score,
                "processing_timestamp": datetime.now().isoformat()
            }
            
            logger.info("資產證明處理完成")
            return result
            
        except Exception as e:
            logger.error(f"資產證明處理錯誤: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def process_transaction_history(self, transactions: List[Dict[str, Any]], 
                                  analysis_window_days: int = 30) -> Dict[str, Any]:
        """
        處理交易歷史
        
        Args:
            transactions: 交易歷史列表
            analysis_window_days: 分析時間窗口（天數）
            
        Returns:
            交易歷史分析結果
        """
        try:
            logger.info(f"開始處理 {len(transactions)} 筆交易記錄...")
            
            if not transactions:
                return {"message": "無交易數據", "timestamp": datetime.now().isoformat()}
            
            # 基本統計分析
            basic_stats = self._calculate_transaction_statistics(transactions)
            
            # 交易模式分析
            pattern_analysis = self._analyze_transaction_patterns(transactions)
            
            # 異常交易檢測
            anomaly_detection = self._detect_transaction_anomalies(transactions)
            
            # 流動性分析
            liquidity_analysis = self._analyze_transaction_liquidity(transactions)
            
            # 地址行為分析
            address_behavior = self._analyze_address_behavior(transactions)
            
            # 時間序列分析
            time_series_analysis = self._analyze_transaction_time_series(transactions, analysis_window_days)
            
            # 網路效應分析
            network_analysis = self._analyze_transaction_network(transactions)
            
            # 風險評估
            risk_assessment = self._assess_transaction_risks(
                transactions, anomaly_detection, address_behavior
            )
            
            # Gas費用分析
            gas_analysis = self._analyze_gas_patterns(transactions)
            
            # 合規風險分析
            compliance_risk = self._assess_transaction_compliance_risk(transactions, address_behavior)
            
            result = {
                "total_transactions": len(transactions),
                "analysis_period_days": analysis_window_days,
                "basic_statistics": basic_stats,
                "pattern_analysis": pattern_analysis,
                "anomaly_detection": anomaly_detection,
                "liquidity_analysis": liquidity_analysis,
                "address_behavior": address_behavior,
                "time_series_analysis": time_series_analysis,
                "network_analysis": network_analysis,
                "risk_assessment": risk_assessment,
                "gas_analysis": gas_analysis,
                "compliance_risk": compliance_risk,
                "processing_timestamp": datetime.now().isoformat()
            }
            
            logger.info("交易歷史處理完成")
            return result
            
        except Exception as e:
            logger.error(f"交易歷史處理錯誤: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    # ========== 智能合約分析相關方法 ==========
    
    def _analyze_basic_structure(self, contract_code: str) -> Dict[str, Any]:
        """分析合約基本結構"""
        lines = contract_code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_lines": len([line for line in lines if line.strip().startswith('//')]),
            "blank_lines": len(lines) - len(non_empty_lines),
            "average_line_length": np.mean([len(line) for line in lines]),
            "max_line_length": max(len(line) for line in lines) if lines else 0
        }
    
    def _parse_contract_ast(self, contract_code: str, language: str) -> Dict[str, Any]:
        """解析合約抽象語法樹"""
        ast_info = {
            "contracts_count": contract_code.count("contract "),
            "interfaces_count": contract_code.count("interface "),
            "libraries_count": contract_code.count("library "),
            "functions_count": contract_code.count("function "),
            "modifiers_count": contract_code.count("modifier "),
            "events_count": contract_code.count("event "),
            "structs_count": contract_code.count("struct "),
            "enums_count": contract_code.count("enum "),
            "imports_count": contract_code.count("import "),
            "pragma_directives": re.findall(r'pragma\s+\w+\s+[^;]+;', contract_code)
        }
        
        # Solidity特定分析
        if language.lower() == "solidity":
            ast_info.update({
                "mappings_count": contract_code.count("mapping("),
                "arrays_count": contract_code.count("[]"),
                "inheritance_count": contract_code.count(" is "),
                "using_statements": contract_code.count("using "),
                "assembly_blocks": contract_code.count("assembly {")
            })
        
        return ast_info
    
    def _extract_and_analyze_functions(self, contract_code: str) -> List[ContractFunction]:
        """提取並分析函數"""
        functions = []
        lines = contract_code.split('\n')
        
        for i, line in enumerate(lines):
            if re.search(r'\bfunction\s+\w+', line):
                func_info = self._analyze_single_function(line, i + 1, lines)
                if func_info:
                    functions.append(func_info)
        
        return functions
    
    def _analyze_single_function(self, line: str, line_number: int, 
                                all_lines: List[str]) -> Optional[ContractFunction]:
        """分析單個函數"""
        try:
            # 提取函數名
            func_match = re.search(r'function\s+(\w+)', line)
            if not func_match:
                return None
            
            func_name = func_match.group(1)
            
            # 提取可見性
            visibility = self._extract_visibility(line)
            
            # 提取狀態可變性
            state_mutability = self._extract_state_mutability(line)
            
            # 提取修飾符
            modifiers = self._extract_function_modifiers(line)
            
            # 提取參數
            parameters = self._extract_function_parameters(line)
            
            # 提取返回類型
            return_type = self._extract_return_type(line)
            
            # 判斷是否為payable
            is_payable = "payable" in line
            
            # 判斷是否為關鍵函數
            is_critical = self._is_critical_function(func_name, line)
            
            return ContractFunction(
                name=func_name,
                line_number=line_number,
                signature=line.strip(),
                visibility=visibility,
                state_mutability=state_mutability,
                modifiers=modifiers,
                parameters=parameters,
                return_type=return_type,
                is_payable=is_payable,
                is_critical=is_critical
            )
            
        except Exception as e:
            logger.warning(f"函數分析錯誤 (行 {line_number}): {e}")
            return None
    
    def _detect_security_patterns(self, contract_code: str) -> List[SecurityPattern]:
        """檢測安全模式"""
        patterns = []
        
        for pattern_type, keywords in self.security_keywords.items():
            locations = []
            count = 0
            
            lines = contract_code.split('\n')
            for i, line in enumerate(lines):
                for keyword in keywords:
                    if keyword in line:
                        locations.append(i + 1)
                        count += 1
            
            if count > 0:
                risk_level = self._assess_pattern_risk_level(pattern_type, count)
                description = self._generate_pattern_description(pattern_type, count)
                
                patterns.append(SecurityPattern(
                    pattern_type=pattern_type,
                    count=count,
                    locations=locations,
                    risk_level=risk_level,
                    description=description
                ))
        
        return patterns
    
    def _calculate_complexity_metrics(self, contract_code: str, 
                                    functions: List[ContractFunction]) -> Dict[str, Any]:
        """計算複雜度指標"""
        lines = contract_code.split('\n')
        
        # 圈複雜度計算
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(contract_code)
        
        # 嵌套深度
        max_nesting_depth = self._calculate_max_nesting_depth(lines)
        
        # 函數複雜度
        function_complexity = self._calculate_function_complexity_distribution(functions)
        
        # Halstead複雜度
        halstead_metrics = self._calculate_halstead_metrics(contract_code)
        
        return {
            "cyclomatic_complexity": cyclomatic_complexity,
            "max_nesting_depth": max_nesting_depth,
            "function_complexity_distribution": function_complexity,
            "halstead_metrics": halstead_metrics,
            "maintainability_index": self._calculate_maintainability_index(
                len(lines), cyclomatic_complexity, halstead_metrics
            )
        }
    
    # ========== 法律文件分析相關方法 ==========
    
    def _analyze_document_structure(self, document: str) -> Dict[str, Any]:
        """分析文檔結構"""
        sections = re.split(r'\n\s*\d+\.\s+', document)
        paragraphs = document.split('\n\n')
        
        return {
            "word_count": len(document.split()),
            "character_count": len(document),
            "paragraph_count": len(paragraphs),
            "section_count": len(sections),
            "average_paragraph_length": np.mean([len(p.split()) for p in paragraphs if p.strip()]),
            "has_table_of_contents": "table of contents" in document.lower(),
            "has_definitions": "definition" in document.lower(),
            "has_appendices": "appendix" in document.lower()
        }
    
    def _extract_compliance_requirements(self, document: str) -> List[Dict[str, Any]]:
        """提取合規要求"""
        requirements = []
        doc_lower = document.lower()
        
        for category, keywords in self.compliance_keywords.items():
            matches = []
            for keyword in keywords:
                if keyword in doc_lower:
                    matches.append(keyword)
            
            if matches:
                requirements.append({
                    "category": category,
                    "keywords_found": matches,
                    "relevance_score": len(matches) / len(keywords)
                })
        
        return requirements
    
    def _identify_jurisdiction(self, document: str) -> str:
        """識別司法管轄區"""
        jurisdiction_indicators = {
            ComplianceFramework.SEC: ["SEC", "Securities and Exchange Commission", "United States", "US", "Federal Register"],
            ComplianceFramework.MAS: ["MAS", "Monetary Authority of Singapore", "Singapore"],
            ComplianceFramework.FCA: ["FCA", "Financial Conduct Authority", "United Kingdom", "UK"],
            ComplianceFramework.CFTC: ["CFTC", "Commodity Futures Trading Commission"],
            ComplianceFramework.FINMA: ["FINMA", "Swiss Financial Market Supervisory Authority", "Switzerland"],
            ComplianceFramework.ESMA: ["ESMA", "European Securities and Markets Authority", "European Union", "EU"]
        }
        
        doc_upper = document.upper()
        jurisdiction_scores = {}
        
        for framework, indicators in jurisdiction_indicators.items():
            score = 0
            for indicator in indicators:
                score += doc_upper.count(indicator.upper())
            if score > 0:
                jurisdiction_scores[framework.value] = score
        
        if jurisdiction_scores:
            return max(jurisdiction_scores, key=jurisdiction_scores.get)
        
        return "UNKNOWN"
    
    # ========== 資產證明分析相關方法 ==========
    
    def _verify_asset_proof(self, proof: Dict[str, Any]) -> AssetVerification:
        """驗證資產證明"""
        required_fields = ["asset_id", "asset_type", "value", "custody_info"]
        optional_fields = ["valuation_date", "insurance_coverage", "audit_report", 
                          "appraisal_firm", "property_address"]
        
        issues = []
        score = 0
        
        # 檢查必要欄位
        for field in required_fields:
            if field not in proof or not proof[field]:
                issues.append(f"Missing or empty required field: {field}")
            else:
                score += 20  # 每個必要欄位20分
        
        # 檢查可選欄位
        for field in optional_fields:
            if field in proof and proof[field]:
                score += 5  # 每個可選欄位5分
        
        # 檢查資產價值合理性
        value = proof.get("value", 0)
        if isinstance(value, (int, float)):
            if value <= 0:
                issues.append("Invalid asset value: must be positive")
            elif value > 1000000000:  # 10億以上
                issues.append("Extremely high asset value requires additional verification")
        else:
            issues.append("Asset value must be numeric")
        
        # 檢查估值日期
        valuation_date = proof.get("valuation_date")
        if valuation_date:
            if self._is_valuation_outdated(valuation_date):
                issues.append("Asset valuation is outdated (>6 months)")
        
        # 檢查保險覆蓋
        insurance_coverage = proof.get("insurance_coverage", 0)
        if isinstance(insurance_coverage, (int, float)) and insurance_coverage < value * 0.8:
            issues.append("Insufficient insurance coverage (<80% of asset value)")
        
        documents_complete = len([f for f in optional_fields if proof.get(f)]) >= 3
        custody_verified = bool(proof.get("custody_info"))
        valuation_current = not self._is_valuation_outdated(valuation_date) if valuation_date else False
        
        return AssetVerification(
            asset_id=proof.get("asset_id", ""),
            verification_status=len(issues) == 0 and score >= 85,
            verification_score=min(score, 100),
            issues=issues,
            documents_complete=documents_complete,
            custody_verified=custody_verified,
            valuation_current=valuation_current
        )
    
    def _identify_asset_type(self, proof: Dict[str, Any]) -> Optional[AssetType]:
        """識別資產類型"""
        asset_type_str = proof.get("asset_type", "").lower()
        
        # 直接匹配
        for key, asset_type in self.asset_type_mapping.items():
            if key in asset_type_str:
                return asset_type
        
        # 基於其他欄位推斷
        if any(keyword in str(proof).lower() for keyword in ["property", "real estate", "building"]):
            return AssetType.REAL_ESTATE
        elif any(keyword in str(proof).lower() for keyword in ["bond", "debenture", "note"]):
            return AssetType.CORPORATE_BONDS
        elif any(keyword in str(proof).lower() for keyword in ["gold", "silver", "platinum", "metal"]):
            return AssetType.PRECIOUS_METALS
        
        return None
    
    # ========== 交易歷史分析相關方法 ==========
    
    def _calculate_transaction_statistics(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """計算交易基本統計"""
        values = [t.get("value", 0) for t in transactions if isinstance(t.get("value"), (int, float))]
        
        if not values:
            return {"message": "No valid transaction values found"}
        
        return {
            "total_transactions": len(transactions),
            "total_volume": sum(values),
            "average_value": np.mean(values),
            "median_value": np.median(values),
            "std_deviation": np.std(values),
            "min_value": min(values),
            "max_value": max(values),
            "value_percentiles": {
                "25th": np.percentile(values, 25),
                "75th": np.percentile(values, 75),
                "90th": np.percentile(values, 90),
                "95th": np.percentile(values, 95)
            }
        }
    
    def _detect_transaction_anomalies(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """檢測交易異常"""
        anomalies = {
            "statistical_outliers": [],
            "zero_value_transactions": [],
            "extremely_large_transactions": [],
            "duplicate_transactions": [],
            "suspicious_patterns": []
        }
        
        values = [t.get("value", 0) for t in transactions if isinstance(t.get("value"), (int, float))]
        
        if not values:
            return anomalies
        
        mean_value = np.mean(values)
        std_value = np.std(values)
        
        for i, transaction in enumerate(transactions):
            value = transaction.get("value", 0)
            
            # 統計異常
            if std_value > 0 and abs(value - mean_value) > 3 * std_value:
                anomalies["statistical_outliers"].append({
                    "index": i,
                    "transaction": transaction,
                    "z_score": abs(value - mean_value) / std_value
                })
            
            # 零值交易
            if value == 0:
                anomalies["zero_value_transactions"].append({
                    "index": i,
                    "transaction": transaction
                })
            
            # 極大交易
            if value > mean_value * 100:
                anomalies["extremely_large_transactions"].append({
                    "index": i,
                    "transaction": transaction,
                    "ratio_to_mean": value / mean_value if mean_value > 0 else float('inf')
                })
        
        return anomalies
    
    # ========== 輔助方法 ==========
    
    def _extract_visibility(self, line: str) -> str:
        """提取函數可見性"""
        visibilities = ["public", "private", "internal", "external"]
        for visibility in visibilities:
            if visibility in line:
                return visibility
        return "unknown"
    
    def _extract_state_mutability(self, line: str) -> str:
        """提取狀態可變性"""
        if "pure" in line:
            return "pure"
        elif "view" in line:
            return "view"
        elif "payable" in line:
            return "payable"
        else:
            return "nonpayable"
    
    def _extract_function_modifiers(self, line: str) -> List[str]:
        """提取函數修飾符"""
        modifiers = []
        common_modifiers = [
            "payable", "view", "pure", "onlyOwner", "nonReentrant", 
            "whenNotPaused", "onlyAdmin", "onlyMinter"
        ]
        for modifier in common_modifiers:
            if modifier in line:
                modifiers.append(modifier)
        return modifiers
    
    def _is_critical_function(self, func_name: str, line: str) -> bool:
        """判斷是否為關鍵函數"""
        critical_keywords = [
            "mint", "burn", "transfer", "withdraw", "deposit", "pause", 
            "unpause", "upgrade", "destroy", "selfdestruct", "owner", 
            "admin", "emergency", "rescue"
        ]
        
        func_name_lower = func_name.lower()
        line_lower = line.lower()
        
        return any(keyword in func_name_lower or keyword in line_lower 
                  for keyword in critical_keywords)
    
    def _assess_pattern_risk_level(self, pattern_type: str, count: int) -> str:
        """評估模式風險等級"""
        risk_thresholds = {
            "reentrancy": {"high": 3, "medium": 1},
            "external_calls": {"high": 5, "medium": 2},
            "assembly": {"high": 2, "medium": 1},
            "selfdestruct": {"high": 1, "medium": 0}
        }
        
        thresholds = risk_thresholds.get(pattern_type, {"high": 5, "medium": 2})
        
        if count >= thresholds["high"]:
            return "HIGH"
        elif count >= thresholds["medium"]:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_pattern_description(self, pattern_type: str, count: int) -> str:
        """生成模式描述"""
        descriptions = {
            "reentrancy": f"檢測到 {count} 個可能的重入攻擊點",
            "access_control": f"發現 {count} 個存取控制相關模式",
            "external_calls": f"識別出 {count} 個外部調用",
            "timestamp": f"發現 {count} 個時間戳依賴",
            "assembly": f"檢測到 {count} 個彙編代碼塊"
        }
        
        return descriptions.get(pattern_type, f"檢測到 {count} 個 {pattern_type} 模式")
    
    def _calculate_cyclomatic_complexity(self, contract_code: str) -> int:
        """計算圈複雜度"""
        complexity_indicators = ["if", "else", "for", "while", "case", "&&", "||", "?"]
        complexity = 1  # 基礎複雜度
        
        for indicator in complexity_indicators:
            complexity += contract_code.count(indicator)
        
        return complexity
    
    def _calculate_max_nesting_depth(self, lines: List[str]) -> int:
        """計算最大嵌套深度"""
        max_depth = 0
        current_depth = 0
        
        for line in lines:
            stripped = line.strip()
            if '{' in stripped:
                current_depth += stripped.count('{')
                max_depth = max(max_depth, current_depth)
            if '}' in stripped:
                current_depth -= stripped.count('}')
        
        return max_depth
    
    def _calculate_halstead_metrics(self, contract_code: str) -> Dict[str, float]:
        """計算Halstead複雜度指標"""
        # 簡化的Halstead指標計算
        operators = re.findall(r'[+\-*/=<>!&|^%]', contract_code)
        operands = re.findall(r'\b\w+\b', contract_code)
        
        n1 = len(set(operators))  # 不同運算符數量
        n2 = len(set(operands))   # 不同操作數數量
        N1 = len(operators)       # 總運算符數量
        N2 = len(operands)        # 總操作數數量
        
        if n1 == 0 or n2 == 0:
            return {"volume": 0, "difficulty": 0, "effort": 0}
        
        volume = (N1 + N2) * np.log2(n1 + n2)
        difficulty = (n1 / 2) * (N2 / n2)
        effort = difficulty * volume
        
        return {
            "volume": volume,
            "difficulty": difficulty,
            "effort": effort
        }
    
    def _calculate_maintainability_index(self, lines_of_code: int, 
                                       cyclomatic_complexity: int,
                                       halstead_metrics: Dict[str, float]) -> float:
        """計算可維護性指數"""
        if lines_of_code == 0:
            return 0
        
        halstead_volume = halstead_metrics.get("volume", 1)
        
        # 簡化的可維護性指數公式
        mi = 171 - 5.2 * np.log(halstead_volume) - 0.23 * cyclomatic_complexity - 16.2 * np.log(lines_of_code)
        
        return max(0, min(100, mi))  # 限制在0-100範圍內
    
    def _is_valuation_outdated(self, valuation_date: str) -> bool:
        """檢查估值是否過時"""
        try:
            if isinstance(valuation_date, str):
                # 嘗試解析日期
                date_obj = datetime.fromisoformat(valuation_date.replace('Z', '+00:00'))
            else:
                return True
            
            # 檢查是否超過6個月
            days_old = (datetime.now().replace(tzinfo=date_obj.tzinfo) - date_obj).days
            return days_old > 180
            
        except:
            return True
    
    def get_processor_info(self) -> Dict[str, Any]:
        """獲取處理器資訊"""
        return {
            "supported_languages": self.supported_languages,
            "security_keywords_count": {k: len(v) for k, v in self.security_keywords.items()},
            "compliance_keywords_count": {k: len(v) for k, v in self.compliance_keywords.items()},
            "supported_asset_types": [asset_type.value for asset_type in AssetType],
            "supported_compliance_frameworks": [framework.value for framework in ComplianceFramework],
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat()
        }

# 使用範例
if __name__ == "__main__":
    processor = MultimodalInputProcessor()
    
    # 顯示處理器資訊
    info = processor.get_processor_info()
    print("多模態輸入處理器資訊:")
    print(json.dumps(info, indent=2, ensure_ascii=False))