# UDHG Deduction Calculator: Formulas and Rates

## Calculation Logic

The Deduction Calculator determines the Workers' Compensation premium deduction based on the state of operation and the gross payroll amount.

### 1. Formula
For the specific states listed below, the **Adjusted Rate** is calculated using the following formula:

$$\text{Adjusted Rate} = \text{Base Rate} \times \text{EMR} \times (1 - \text{Large Deductible Factor})$$

The final **Total WC Premium** is calculated as:

$$\text{Total Premium} = \left( \frac{\text{Gross Payroll}}{100} \right) \times \text{Adjusted Rate}$$

### 2. Default Rate
For any state **not** listed in the table below, a flat default rate is applied:
* **Default Rate:** $0.1665 per $100 of payroll.

---

## Rate Table (Effective 6/1/2025)

The following specific rates are hardcoded into the calculator:

| State | Class Code | Description | Base Rate | EMR | LDF | Adjusted Rate (Approx) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AZ** | 5102 | Door & Window Installation | 3.31 | 0.95 | 0.2737 | **2.28385** |
| **CO** | 5102 | Door & Window Installation | 3.29 | 0.95 | 0.0549 | **2.95391** |
| **FL** | 5102 | Door & Window Installation | 5.33 | 0.95 | 0.2124 | **3.98801** |
| **MD** | 5102 | Door/Frame/Sash Erection | 4.09 | 0.95 | 0.0548 | **3.67257** |
| **MI** | 5146 | Furniture Install | 7.54 | 0.65 | 0.1100 | **4.36189** |
| **NJ** | 5103 | Sheet Metal Ext Wall Inst | 6.28 | 1.115 | 0.0829 | **6.42172** |
| **NY** | 5102 | Door/Frame/Sash Erection | 11.17 | 1.87 | 0.0832 | **19.15003** |
| **PA** | 658 | Arch Bronze/Iron/Brass | 6.43 | 1.143 | 0.1931 | **5.93030** |
| **TX** | 5102 | Alum Door/Window Inst | 2.15 | 0.95 | 0.0800 | **1.87910** |
