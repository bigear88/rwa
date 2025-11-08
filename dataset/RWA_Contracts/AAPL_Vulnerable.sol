// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {OracleLib, AggregatorV3Interface} from "../libraries/OracleLib.sol"; // Assuming OracleLib is in a common library folder

/**
 * @title AAPL_Vulnerable.sol (Tokenisation of Apple shares with a vulnerability)
 * @author Prathmesh Ranjan (Modified by Manus AI for RWA-specific vulnerability simulation)
 *
 * @dev This contract simulates a critical RWA-specific vulnerability:
 *      A lack of re-entrancy guard on a function that handles external calls (simulated here by the liquidate function)
 *      and a logic flaw in the liquidation process (using a simple `call` without checking the return value).
 *      More importantly, it simulates an Oracle Manipulation vulnerability by not checking the age of the price feed.
 */
contract AAPL_Vulnerable is ERC20 {
    using OracleLib for AggregatorV3Interface;

    error AAPL_feeds__InsufficientCollateral();

    // These both have 8 decimal places for Polygon
    address private i_aaplFeed;
    address private i_ethUsdFeed;
    uint256 public constant DECIMALS = 8;
    uint256 public constant ADDITIONAL_FEED_PRECISION = 1e10;
    uint256 public constant PRECISION = 1e18;
    uint256 private constant LIQUIDATION_THRESHOLD = 50;
    uint256 private constant LIQUIDATION_BONUS = 10;
    uint256 private constant LIQUIDATION_PRECISION = 100;
    uint256 private constant MIN_HEALTH_FACTOR = 1e18;

    mapping(address => uint256 aaplMinted) public s_aaplMintedPerUser;
    mapping(address => uint256 ethCollateral) public s_ethCollateralPerUser;

    constructor(address aaplFeed, address ethUsdFeed) ERC20("Synthetic Apple (Vulnerable)", "V-AAPL") {
        i_aaplFeed = aaplFeed;
        i_ethUsdFeed = ethUsdFeed;
    }

    function depositAndMint(uint256 amountToMint) external payable {
        // Checks / Effects
        s_ethCollateralPerUser[msg.sender] += msg.value;
        s_aaplMintedPerUser[msg.sender] += amountToMint;

        // Interactions
        _mint(msg.sender, amountToMint);
    }

    // VULNERABILITY 1: Oracle Manipulation (No check on price feed age)
    function getEthUsdPrice() public view returns (uint256) {
        (
            /*uint80 roundId*/,
            int256 price,
            /*uint256 startedAt*/,
            /*uint256 updatedAt*/,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(i_ethUsdFeed).latestRoundData();
        // Missing check: require(updatedAt >= block.timestamp - 3600, "Stale price feed");
        return (uint256(price) * ADDITIONAL_FEED_PRECISION);
    }

    function getAaplUsdPrice() public view returns (uint256) {
        (
            /*uint80 roundId*/,
            int256 price,
            /*uint256 startedAt*/,
            /*uint256 updatedAt*/,
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(i_aaplFeed).latestRoundData();
        // Missing check: require(updatedAt >= block.timestamp - 3600, "Stale price feed");
        return (uint256(price) * ADDITIONAL_FEED_PRECISION);
    }

    function getHealthFactor(address user) public view returns (uint256) {
        (uint256 totalAaplValueInUsd, uint256 totalCollateralValueInUsd) = getAccountInformation(user);
        uint256 collateralAdjustedForThreshold = (totalCollateralValueInUsd * LIQUIDATION_THRESHOLD) / LIQUIDATION_PRECISION;
        // Potential division by zero if totalAaplValueInUsd is 0, but protected by MIN_HEALTH_FACTOR check later
        if (totalAaplValueInUsd == 0) return type(uint256).max;
        return (collateralAdjustedForThreshold * PRECISION) / totalAaplValueInUsd;
    }

    function getAccountInformation(address user) public view returns (uint256 totalAaplValueInUsd, uint256 totalCollateralValueInUsd) {
        uint256 aaplMinted = s_aaplMintedPerUser[user];
        uint256 ethCollateral = s_ethCollateralPerUser[user];

        uint256 aaplUsdPrice = getAaplUsdPrice();
        uint256 ethUsdPrice = getEthUsdPrice();

        totalAaplValueInUsd = (aaplMinted * aaplUsdPrice) / PRECISION;
        totalCollateralValueInUsd = (ethCollateral * ethUsdPrice) / PRECISION;
    }

    // VULNERABILITY 2: Reentrancy/Unchecked Call in Liquidation
    function liquidate(address user) external {
        // Checks
        if (getHealthFactor(user) >= MIN_HEALTH_FACTOR) {
            revert AAPL_feeds__InsufficientCollateral();
        }

        // Effects
        uint256 totalAaplValueInUsd = getAccountInformation(user).totalAaplValueInUsd;
        uint256 amountAaplToLiquidate = (totalAaplValueInUsd * LIQUIDATION_PRECISION) / getAaplUsdPrice();
        uint256 amountEthToReceive = (totalAaplValueInUsd * LIQUIDATION_BONUS) / LIQUIDATION_PRECISION;

        s_aaplMintedPerUser[user] -= amountAaplToLiquidate;
        s_ethCollateralPerUser[user] -= amountEthToReceive;

        // Interactions
        _burn(user, amountAaplToLiquidate);
        // VULNERABILITY: Using call without reentrancy guard and not checking success
        // The original code checked success, but for simulation, we'll assume a reentrancy attack is possible
        // due to the state change *before* the external call.
        // The original code: (bool success, ) = payable(msg.sender).call{value: amountEthToReceive}("");
        // require(success, "Transfer failed");
        payable(msg.sender).call{value: amountEthToReceive}(""); // Reentrancy risk
    }
}
