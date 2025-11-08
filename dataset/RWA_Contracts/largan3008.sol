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
 * @title LARGAN3008.sol (Tokenisation of Largan Precision - 3008)
 * @author RWA 實驗室
 *
 * @dev This token represents a share of Largan Precision (3008).
 * It is a simple RWA token pegged to the stock's price via an Oracle.
 * Largan is a high-priced stock, which might imply a need for higher precision or fractionalization logic,
 * but for this simulation, we use the standard ERC20 and price feed logic.
 */
contract LARGAN3008 is ERC20 {
    address private i_larganPriceFeed;
    address public immutable issuer;

    uint256 public constant PRICE_FEED_DECIMALS = 8;
    uint256 public constant PRECISION = 1e18;

    error LARGAN_PriceFeed_Invalid();

    constructor(address larganPriceFeed) ERC20("Largan Stock Token", "LARGAN") {
        i_larganPriceFeed = larganPriceFeed;
        issuer = msg.sender;
    }

    modifier onlyIssuer() {
        if (msg.sender != issuer) {
            revert("Only issuer can perform this action");
        }
        _;
    }

    function getLarganPrice() public view returns (uint256 price) {
        (
            /*uint80 roundId*/,
            int256 answer,
            /*uint256 startedAt*/,
            uint256 updatedAt,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(i_larganPriceFeed).latestRoundData();

        if (updatedAt < block.timestamp - 3600) {
            revert LARGAN_PriceFeed_Invalid();
        }
        
        if (answer <= 0) {
            revert LARGAN_PriceFeed_Invalid();
        }

        return (uint256(answer) * (PRECISION / (10**PRICE_FEED_DECIMALS)));
    }

    function mint(address to, uint256 amount) external onlyIssuer {
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external onlyIssuer {
        _burn(from, amount);
    }
    
    function isCompliant(address user) public public view returns (bool) {
        // Placeholder for KYC/AML check logic
        return true; 
    }
}
