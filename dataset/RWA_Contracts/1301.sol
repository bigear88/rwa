// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

interface AggregatorV3Interface {
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
}

/**
 * @title FPC1301.sol (Tokenisation of Formosa Plastics - 1301)
 * @author RWA 實驗室
 *
 * @dev RWA Configuration:
 * - Type: 大型股
 * - Collateral Ratio: 150% (Implied)
 * - Oracle Update Frequency: 3600 seconds (Max Stale Time)
 * - Liquidity Requirement: Standard
 * - Special Note: International market linkage is high
 */
contract FPC1301 is ERC20 {
    address private i_priceFeed;
    address public immutable issuer;

    uint256 public constant PRICE_FEED_DECIMALS = 8;
    uint256 public constant PRECISION = 1e18;
    uint256 public constant MAX_STALE_TIME = 3600; // Max seconds before price is considered stale
    uint256 public constant LIQUIDATION_THRESHOLD = 150; // Used for collateralized assets

    error PriceFeed_Invalid();
    error StalePrice();

    constructor(address priceFeed) ERC20("Formosa Plastics Token", "FPC") {
        i_priceFeed = priceFeed;
        issuer = msg.sender;
    }

    modifier onlyIssuer() {
        if (msg.sender != issuer) {
            revert("Only issuer can perform this action");
        }
        _;
    }

    function getAssetPrice() public view returns (uint256 price) {
        (
            /*uint80 roundId*/,
            int256 answer,
            /*uint256 startedAt*/,
            uint256 updatedAt,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(i_priceFeed).latestRoundData();

        if (updatedAt < block.timestamp - MAX_STALE_TIME) {
            revert StalePrice();
        }
        
        if (answer <= 0) {
            revert PriceFeed_Invalid();
        }

        return (uint256(answer) * (PRECISION / (10**PRICE_FEED_DECIMALS)));
    }

    function mint(address to, uint256 amount) external onlyIssuer {
        // In a real system, this would check collateral and compliance
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external onlyIssuer {
        // In a real system, this would trigger off-chain redemption
        _burn(from, amount);
    }
    
    // RWA-Specific Compliance Check Placeholder
    function isCompliant(address user) public view returns (bool) {
        // This function should be the target for compliance vulnerability detection
        return true; 
    }
}
