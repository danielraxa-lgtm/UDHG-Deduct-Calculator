# Insurance Logic Documentation

## 1. Workers' Comp Base Rates
*Base rates per $100 of payroll for supported states.*

| State | State Code | Base Rate (Class 8810 - Clerical) | Base Rate (Default/Other) |
| :--- | :---: | :---: | :---: |
| Arizona | AZ | $0.11 | $1.05 |
| Colorado | CO | $0.15 | $1.20 |
| Florida | FL | $0.22 | $1.45 |
| Maryland | MD | $0.18 | $1.10 |
| Michigan | MI | $0.14 | $1.00 |
| New Jersey | NJ | $0.25 | $1.50 |
| New York | NY | $0.30 | $1.75 |
| Pennsylvania| PA | $0.20 | $1.35 |
| Texas | TX | $0.12 | $0.95 |

> **Note:** These are base rates. Experience Modification Rate (EMR) applies on top of these.

## 2. Fixed Liability Rates
*Standard annual premiums for liability coverage.*

| Coverage Type | Annual Premium | Limit |
| :--- | :---: | :--- |
| **General Liability (GL)** | $650.00 | $1M / $2M Aggregate |
| **Umbrella Policy** | $400.00 | $1M Excess |

## 3. Calculation Logic for Deductions

### Total Deduction Formula
The total deduction is calculated as the sum of the Workers' Comp premium and the Liability portion.

$$
\text{Total Deduction} = \text{WC Premium} + \text{Liability Premium}
$$

### Workers' Comp Calculation
$$
\text{WC Premium} = \left( \frac{\text{Gross Payroll}}{100} \right) \times \text{State Rate} \times \text{EMR}
$$

* **Gross Payroll**: The total wages paid for the period.
* **State Rate**: Based on the table above.
* **EMR**: Experience Modification Rate (default = 1.0).
