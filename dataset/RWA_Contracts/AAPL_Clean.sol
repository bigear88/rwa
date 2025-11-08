// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {OracleLib, AggregatorV3Interface} from "./libraries/OracleLib.sol";

/**
 * @title AAPL.sol (Tokenisation of Apple shares)
 * @author Prathmesh Ranjan
 *
 * * This is a token each representing an Apple share with the properties:
 * - Exogenously Collateralized
 * - Apple Share Pegged
 * - Algorithmically Stable
 *
 * * Our system should always be "overcollateralized". At no point, should the value of
 * all collateral < the $ backed value of all the AAPL.
 *
 * @dev the codebase will mint AAPL based on the collateral
 * * deposited into this contract. In this example, ETH is the
 * * collateral that we will use to mint AAPL.
 */
contract AAPL is ERC20 {
    using OracleLib for AggregatorV3Interface;

    error AAPL_feeds__InsufficientCollateral();

    // These both have 8 decimal places for Polygon
    // https://docs.chain.link/data-feeds/price-feeds/addresses?network=polygon
    address private i_aaplFeed;
    address private i_ethUsdFeed;
    uint256 public constant DECIMALS = 8;
    uint256 public constant ADDITIONAL_FEED_PRECISION = 1e10;
    uint256 public constant PRECISION = 1e18;
    uint256 private constant LIQUIDATION_THRESHOLD = 50; // This means you need to be 200% over-collateralized
    uint256 private constant LIQUIDATION_BONUS = 10; // This means you get assets at a 10% discount when liquidating
    uint256 private constant LIQUIDATION_PRECISION = 100;
    uint256 private constant MIN_HEALTH_FACTOR = 1e18;

    mapping(address => uint256 aaplMinted) public s_aaplMintedPerUser;
    mapping(address => uint256 ethCollateral) public s_ethCollateralPerUser;

    constructor(address aaplFeed, address ethUsdFeed) ERC20("Synthetic Apple", "AAPL") {
        i_aaplFeed = aaplFeed;
        i_ethUsdFeed = ethUsdFeed;
    }

    /**
     * @dev User must deposit at least 200% of the value of the AAPL they want to mint
     */
    function depositAndMint(uint256 amountToMint) external payable {
        // Checks / Effects
        s_ethCollateralPerUser[msg.sender] += msg.value;
        s_aaplMintedPerUser[msg.sender] += amountToMint;

        // Interactions
        _mint(msg.sender, amountToMint);
    }

    function getEthUsdPrice() public view returns (uint256) {
        (, int256 price, , , ) = AggregatorV3Interface(i_ethUsdFeed).latestRoundData();
        // 1e8 * 1e10 = 1e18
        return (uint256(price) * ADDITIONAL_FEED_PRECISION);
    }

    function getAaplUsdPrice() public view returns (uint256) {
        (, int256 price, , , ) = AggregatorV3Interface(i_aaplFeed).latestRoundData();
        // 1e8 * 1e10 = 1e18
        return (uint256(price) * ADDITIONAL_FEED_PRECISION);
    }

    function getHealthFactor(address user) public view returns (uint256) {
        (uint256 totalAaplValueInUsd, uint256 totalCollateralValueInUsd) = getAccountInformation(user);
        uint256 collateralAdjustedForThreshold = (totalCollateralValueInUsd * LIQUIDATION_THRESHOLD) / LIQUIDATION_PRECISION;
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
        (bool success, ) = payable(msg.sender).call{value: amountEthToReceive}("");
        require(success, "Transfer failed");
    }
}
