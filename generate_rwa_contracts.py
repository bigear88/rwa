import os

# 股票類型與配置表
CONFIG_TABLE = {
    "大型股": {"collateral_ratio": "150", "update_frequency": "3600", "liquidity_req": "Standard", "special_note": "International market linkage is high"},
    "中型股": {"collateral_ratio": "175", "update_frequency": "1800", "liquidity_req": "Medium", "special_note": "Enhanced liquidity monitoring required"},
    "小型股": {"collateral_ratio": "200", "update_frequency": "900", "liquidity_req": "High", "special_note": "High volatility, requires market maker mechanism"},
    "金融股": {"collateral_ratio": "150", "update_frequency": "3600", "liquidity_req": "Standard", "special_note": "Subject to special financial supervision (e.g., capital adequacy check)"},
    "高波動產業": {"collateral_ratio": "200", "update_frequency": "300", "liquidity_req": "High", "special_note": "Extreme price volatility, requires special risk control (e.g., circuit breaker)"},
    "ETF": {"collateral_ratio": "150", "update_frequency": "3600", "liquidity_req": "Standard", "special_note": "Requires tracking index deviation"},
}

# 模擬的台灣上市公司列表 (共 20 個，涵蓋不同類型)
CONTRACTS_TO_GENERATE = [
    # 大型股 (市值 >1000億)
    {"code": "2317", "name": "Hon Hai Precision", "symbol": "HHPC", "type": "大型股"},
    {"code": "2454", "name": "MediaTek", "symbol": "MTK", "type": "大型股"},
    {"code": "1301", "name": "Formosa Plastics", "symbol": "FPC", "type": "大型股"},
    {"code": "2881", "name": "Fubon Financial", "symbol": "Fubon", "type": "金融股"},
    
    # 中型股 (市值 100-1000億)
    {"code": "3034", "name": "Novatek", "symbol": "NVTK", "type": "中型股"},
    {"code": "3406", "name": "Largan Precision", "symbol": "LARGAN", "type": "中型股"}, # Already have 3008, using a different one for variety
    {"code": "2308", "name": "Delta Electronics", "symbol": "DELTA", "type": "中型股"},
    {"code": "2357", "name": "ASUS", "symbol": "ASUS", "type": "中型股"},
    
    # 小型股 (市值 <100億)
    {"code": "3231", "name": "Wistron", "symbol": "WIST", "type": "小型股"},
    {"code": "6116", "name": "Catcher Technology", "symbol": "CATCH", "type": "小型股"},
    {"code": "3045", "name": "Taiwan Mobile", "symbol": "TWM", "type": "小型股"},
    
    # 金融股
    {"code": "2882", "name": "Cathay Financial", "symbol": "Cathay", "type": "金融股"},
    {"code": "2884", "name": "Mega Financial", "symbol": "Mega", "type": "金融股"},
    {"code": "2891", "name": "CTBC Financial", "symbol": "CTBC", "type": "金融股"},
    
    # 高波動產業 (航運股、生技股)
    {"code": "2603", "name": "Evergreen Marine", "symbol": "EMC", "type": "高波動產業"},
    {"code": "2615", "name": "Yang Ming Marine", "symbol": "YMM", "type": "高波動產業"},
    {"code": "4147", "name": "Taimed Biologics", "symbol": "TAIMED", "type": "高波動產業"},
    
    # ETF
    {"code": "0056", "name": "Fubon Taiwan Dividend", "symbol": "FBDV", "type": "ETF"},
    {"code": "006208", "name": "Yuanta Taiwan 50", "symbol": "YT50", "type": "ETF"},
    {"code": "00878", "name": "Cathay Sustainable", "symbol": "CATHS", "type": "ETF"},
]

# RWA 合約模板
CONTRACT_TEMPLATE = """// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {{ERC20}} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

interface AggregatorV3Interface {{
    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}}

/**
 * @title {symbol}{code}.sol (Tokenisation of {name} - {code})
 * @author RWA 實驗室
 *
 * @dev RWA Configuration:
 * - Type: {type}
 * - Collateral Ratio: {collateral_ratio}% (Implied)
 * - Oracle Update Frequency: {update_frequency} seconds (Max Stale Time)
 * - Liquidity Requirement: {liquidity_req}
 * - Special Note: {special_note}
 */
contract {symbol}{code} is ERC20 {{
    address private i_priceFeed;
    address public immutable issuer;

    uint256 public constant PRICE_FEED_DECIMALS = 8;
    uint256 public constant PRECISION = 1e18;
    uint256 public constant MAX_STALE_TIME = {update_frequency}; // Max seconds before price is considered stale
    uint256 public constant LIQUIDATION_THRESHOLD = {collateral_ratio}; // Used for collateralized assets

    error PriceFeed_Invalid();
    error StalePrice();

    constructor(address priceFeed) ERC20("{name} Token", "{symbol}") {{
        i_priceFeed = priceFeed;
        issuer = msg.sender;
    }}

    modifier onlyIssuer() {{
        if (msg.sender != issuer) {{
            revert("Only issuer can perform this action");
        }}
        _;
    }}

    function getAssetPrice() public view returns (uint256 price) {{
        (
            /*uint80 roundId*/,
            int256 answer,
            /*uint256 startedAt*/,
            uint256 updatedAt,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(i_priceFeed).latestRoundData();

        if (updatedAt < block.timestamp - MAX_STALE_TIME) {{
            revert StalePrice();
        }}
        
        if (answer <= 0) {{
            revert PriceFeed_Invalid();
        }}

        return (uint256(answer) * (PRECISION / (10**PRICE_FEED_DECIMALS)));
    }}

    function mint(address to, uint256 amount) external onlyIssuer {{
        // In a real system, this would check collateral and compliance
        _mint(to, amount);
    }}

    function burn(address from, uint256 amount) external onlyIssuer {{
        // In a real system, this would trigger off-chain redemption
        _burn(from, amount);
    }}
    
    // RWA-Specific Compliance Check Placeholder
    function isCompliant(address user) public view returns (bool) {{
        // This function should be the target for compliance vulnerability detection
        return true; 
    }}
}}
"""

def generate_contracts(output_dir):
    """根據配置表生成智能合約文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    for contract_info in CONTRACTS_TO_GENERATE:
        config = CONFIG_TABLE[contract_info["type"]]
        
        # 替換模板中的佔位符
        content = CONTRACT_TEMPLATE.format(
            code=contract_info["code"],
            name=contract_info["name"],
            symbol=contract_info["symbol"],
            type=contract_info["type"],
            collateral_ratio=config["collateral_ratio"],
            update_frequency=config["update_frequency"],
            liquidity_req=config["liquidity_req"],
            special_note=config["special_note"]
        )
        
        filename = f"{contract_info['code']}.sol"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        generated_files.append(filepath)
        
    print(f"Successfully generated {len(generated_files)} RWA contracts in {output_dir}")
    return generated_files

if __name__ == "__main__":
    # 輸出目錄為 rwa_project/dataset/RWA_Contracts
    RWA_CONTRACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "RWA_Contracts")
    generate_contracts(RWA_CONTRACTS_DIR)
