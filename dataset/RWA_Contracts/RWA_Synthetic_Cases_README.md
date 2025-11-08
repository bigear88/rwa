# RWA Synthetic Vulnerability Cases

This directory contains synthetic smart contract examples designed to test the RWA Security Framework's ability to detect vulnerabilities specific to Real World Assets (RWA) tokenization.

These cases are intended to simulate the "RWA 特定合成案例" mentioned in the thesis's experimental design.

## Contracts:

1.  **AAPL_Clean.sol**: A clean, over-collateralized tokenization contract for Apple stock (AAPL), based on the QuillAudits example. This serves as a secure baseline.
2.  **AAPL_Vulnerable.sol**: A modified version of `AAPL_Clean.sol` that includes two RWA-relevant vulnerabilities:
    *   **Oracle Manipulation**: Missing check for stale price feed data.
    *   **Reentrancy/Unchecked Call**: State change before external call in the `liquidate` function.

## Placeholder for Future Cases:

To fully cover the thesis's requirements, future synthetic cases should include:

*   **Compliance Bypass**: Logic that allows a non-KYC/AML approved address to receive tokens.
*   **Asset Mapping Error**: Flaw in the logic that links the on-chain token to the off-chain asset's legal status (e.g., failure to pause transfers when the off-chain asset is legally frozen).
*   **Business Logic Flaw**: Incorrect calculation of collateral ratio or liquidation price due to complex RWA business rules.

## Data Structure for Synthetic Cases:

For the RWA Security Framework, each synthetic case should ideally be accompanied by a JSON file detailing the expected vulnerability:

| Field | Description | Example |
| :--- | :--- | :--- |
| `contract_name` | Name of the contract file. | `AAPL_Vulnerable.sol` |
| `vulnerability_type` | The category of the vulnerability (e.g., RWA_ORACLE_MANIPULATION). | `RWA_ORACLE_MANIPULATION` |
| `line_number` | The line number where the vulnerability is located. | `100` |
| `description` | A brief description of the flaw. | `Missing check for stale price feed data in getEthUsdPrice.` |
| `severity` | The severity level (e.g., Critical, High, Medium). | `Critical` |

A file named `rwa_synthetic_vulnerabilities.json` will be created as a placeholder for this structured data.
