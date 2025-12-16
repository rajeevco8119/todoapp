import numpy as np
import math

def calculate_loan_tenure(principal, annual_rate, monthly_emi):
    """
    Calculates the exact loan tenure (in months) and the final payment details.

    Args:
        principal (float): The initial loan amount (P).
        annual_rate (float): The annual interest rate (e.g., 0.075 for 7.5%).
        monthly_emi (float): The fixed amount paid monthly (M).

    Returns:
        dict: A dictionary containing the tenure in months, years/months, 
              total number of payments, and the final payment amount.
    """
    if principal <= 0 or annual_rate <= 0 or monthly_emi <= 0:
        return {"error": "Principal, rate, and EMI must be positive."}

    # 1. Calculate Monthly Interest Rate (r)
    r_monthly = annual_rate / 12

    # 2. Check if the EMI is sufficient to cover the monthly interest
    monthly_interest = principal * r_monthly
    if monthly_emi <= monthly_interest:
        return {
            "error": "EMI is too low",
            "required_emi_min": monthly_interest + 1 # EMI must be greater than this
        }

    # 3. Calculate Exact Time Duration (N) in months
    # N = - [ ln(1 - (r*P)/M) ] / [ ln(1 + r) ]
    try:
        numerator_N = np.log(1 - (r_monthly * principal) / monthly_emi)
        denominator_N = np.log(1 + r_monthly)
        N_months = -numerator_N / denominator_N
    except (ValueError, ZeroDivisionError) as e:
        return {"error": f"Calculation error: {e}"}


    # 4. Determine Payment Breakdown
    full_payments = math.floor(N_months)
    final_payment_month = full_payments + 1

    # 5. Calculate Outstanding Principal after 'full_payments'
    # P_n = P * (1+r)^n - M * [((1+r)^n - 1)/r]
    n = full_payments
    power_term = np.power(1 + r_monthly, n)

    P_outstanding_after_full = (
        principal * power_term - 
        (monthly_emi / r_monthly) * (power_term - 1)
    )

    # 6. Calculate the Final Payment (F)
    # F = P_n * (1 + r)
    final_payment_amount = P_outstanding_after_full * (1 + r_monthly)

    # 7. Structure the result
    years = int(N_months // 12)
    remaining_months = N_months % 12
    
    return {
        "tenure_months_exact": N_months,
        "tenure_breakdown": f"{years} years and {remaining_months:.2f} months",
        "total_payments": final_payment_month,
        "full_payments": full_payments,
        "final_payment_amount": final_payment_amount
    }

# --- Example Usage ---
# Your case: ₹50 Lakh loan, 7.5% rate, ₹1 Lakh EMI
P_loan = 5000000.0
R_rate = 0.075
M_emi = int(input("Enter monthly EMI: "))

result = calculate_loan_tenure(
    principal=P_loan, 
    annual_rate=R_rate, 
    monthly_emi=M_emi
)

# Outputting the result
print("--- Loan Tenure Calculation ---")
print(f"Principal: ₹{P_loan:,.2f}")
print(f"Annual Rate: {R_rate*100:.2f}%")
print(f"Monthly EMI: ₹{M_emi:,.2f}")
print("-" * 30)

if "error" in result:
    print(f"ERROR: {result['error']}")
    if "required_emi_min" in result:
         print(f"Minimum required EMI (to cover monthly interest): ₹{result['required_emi_min']:,.2f}")
else:
    print(f"Exact Tenure: {result['tenure_months_exact']:.4f} months")
    print(f"Time Breakdown: {result['tenure_breakdown']}")
    print(f"Total Payments: {result['total_payments']} payments")
    print(f"Final Payment Amount (in month {result['total_payments']}): ₹{result['final_payment_amount']:,.2f}")