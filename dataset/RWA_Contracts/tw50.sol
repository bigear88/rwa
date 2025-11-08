// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
// Assuming OracleLib is available for AggregatorV3Interface interaction, as in AAPL.sol
// For simplicity in this simulation, we will define the interface directly.
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
 * @title TW50.sol (Tokenisation of Taiwan 50 ETF - 0050)
 * @author Manus AI
 *
 * @dev This token represents a share of the Taiwan 50 ETF (0050).
 * It is a simple RWA token pegged to the ETF's price via an Oracle.
 * It is NOT collateralized in this simplified version, focusing on the price feed and mint/redeem logic.
 */
contract TW50 is ERC20 {
    // Placeholder for the Chainlink-like price feed address for TW50/TWD or TW50/USD
    address private i_tw50PriceFeed;
    
    // The token issuer/minting authority
    address public immutable issuer;

    // Standard precision for price feeds (e.g., 8 decimals)
    uint256 public constant PRICE_FEED_DECIMALS = 8;
    uint256 public constant PRECISION = 1e18; // Standard ERC20 decimals

    // Error for when the price feed is stale or returns an invalid price
    error TW50_PriceFeed_Invalid();

    constructor(address tw50PriceFeed) ERC20("Taiwan 50 ETF Token", "TW50") {
        i_tw50PriceFeed = tw50PriceFeed;
        issuer = msg.sender;
    }

    modifier onlyIssuer() {
        if (msg.sender != issuer) {
            revert("Only issuer can perform this action");
        }
        _;
    }

    /**
     * @dev Fetches the latest TW50 price from the oracle.
     * @return price The TW50 price scaled to 1e18 precision.
     */
    function getTw50Price() public view returns (uint256 price) {
        (
            /*uint80 roundId*/,
            int256 answer,
            /*uint256 startedAt*/,
            uint256 updatedAt,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(i_tw50PriceFeed).latestRoundData();

        // Check for stale price (e.g., older than 1 hour = 3600 seconds)
        if (updatedAt < block.timestamp - 3600) {
            revert TW50_PriceFeed_Invalid();
        }
        
        // Check for non-positive price
        if (answer <= 0) {
            revert TW50_PriceFeed_Invalid();
        }

        // Scale the price from 8 decimals (typical Chainlink) to 18 decimals (standard token)
        // (answer * 1e18) / 10**PRICE_FEED_DECIMALS
        return (uint256(answer) * (PRECISION / (10**PRICE_FEED_DECIMALS)));
    }

    /**
     * @dev Mints TW50 tokens. Only the issuer can mint.
     * In a real RWA system, this would be tied to the deposit of the underlying asset.
     * @param to The address to mint tokens to.
     * @param amount The amount of tokens to mint (in 18 decimals).
     */
    function mint(address to, uint256 amount) external onlyIssuer {
        // In a real system, this would check if the underlying asset was deposited.
        // For simulation, we assume the issuer has verified the off-chain asset.
        _mint(to, amount);
    }

    /**
     * @dev Burns TW50 tokens. Only the issuer can burn.
     * In a real RWA system, this would be tied to the redemption of the underlying asset.
     * @param from The address to burn tokens from.
     * @param amount The amount of tokens to burn (in 18 decimals).
     */
    function burn(address from, uint256 amount) external onlyIssuer {
        // In a real system, this would trigger the off-chain asset redemption.
        _burn(from, amount);
    }
    
    // --- RWA-Specific Logic Placeholder ---
    // This function simulates a compliance check that would be required for a security token.
    // The framework should check if this is properly implemented.
    function isCompliant(address user) public view returns (bool) {
        // Placeholder for KYC/AML check logic
        // In a real system, this would query an external compliance oracle or a mapping.
        return true; 
    }
}
