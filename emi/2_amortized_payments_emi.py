import pandas as pd
import numpy as np
import math

def calculate_variable_emi_amortization(principal, annual_rate, emi_year_1, emi_after_year_1, year_1_months=12):
    """
    Calculates the amortization schedule for a loan with a changing EMI.

    Args:
        principal (float): The initial loan amount.
        annual_rate (float): The annual interest rate (e.g., 0.075).
        emi_year_1 (float): Monthly payment for the first year.
        emi_after_year_1 (float): Monthly payment after the first year.
        year_1_months (int): Number of months for the first EMI phase (default is 12).

    Returns:
        tuple: (DataFrame of the first year's schedule, final loan summary)
    """
    r_monthly = annual_rate / 12
    loan_balance = principal
    monthly_schedule = []
    
    # --- STAGE 1: Higher EMI (First Year) ---
    current_emi = emi_year_1
    print(f"--- Stage 1: {year_1_months} Months at EMI ₹{current_emi:,.2f} ---")
    
    for month in range(1, year_1_months + 1):
        interest_paid = loan_balance * r_monthly
        
        # Check if the loan is already closed
        if loan_balance <= 0:
            interest_paid = 0
            principal_paid = 0
            loan_balance = 0
        elif interest_paid >= current_emi:
            return None, {"error": "EMI is too low to cover monthly interest."}
        else:
            principal_paid = current_emi - interest_paid
            loan_balance -= principal_paid
            
        monthly_schedule.append({
            'Month': month,
            'Starting Principal': principal,
            'EMI': current_emi,
            'Interest Paid': interest_paid,
            'Principal Paid': principal_paid,
            'Outstanding Principal': max(0, loan_balance) # Ensure balance is not negative
        })
        principal = loan_balance # Update principal for the next iteration

    # --- STAGE 2: Lower EMI (Remaining Tenure) ---
    
    # New Principal Outstanding after 12 months
    P_remaining = monthly_schedule[-1]['Outstanding Principal']
    
    if P_remaining <= 0:
        return pd.DataFrame(monthly_schedule), {"result": "Loan fully closed in Stage 1."}
        
    print(f"\n--- Stage 2: Remaining Tenure at EMI ₹{emi_after_year_1:,.2f} ---")
    
    # Check if the new EMI is sufficient for the reduced principal
    if emi_after_year_1 <= P_remaining * r_monthly:
        return pd.DataFrame(monthly_schedule), {"error": "New EMI is too low to service the remaining principal."}
        
    # Calculate remaining tenure (N_remaining) using the amortization formula
    try:
        numerator_N = np.log(1 - (r_monthly * P_remaining) / emi_after_year_1)
        denominator_N = np.log(1 + r_monthly)
        N_remaining_months = -numerator_N / denominator_N
    except (ValueError, ZeroDivisionError) as e:
        return pd.DataFrame(monthly_schedule), {"error": f"Calculation error in Stage 2: {e}"}

    # Final Payment Details
    full_payments_remaining = math.floor(N_remaining_months)
    total_payments = year_1_months + full_payments_remaining + 1
    
    # Calculate final (partial) payment
    # This requires running an amortization for the remaining period to get the final amount
    
    # We will use the formula-based time and then calculate the final payment amount
    
    n = full_payments_remaining
    power_term = np.power(1 + r_monthly, n)
    
    P_outstanding_after_full = (
        P_remaining * power_term - 
        (emi_after_year_1 / r_monthly) * (power_term - 1)
    )

    final_payment_amount = P_outstanding_after_full * (1 + r_monthly)
    
    # Total Time and Interest Calculation
    total_tenure_months = year_1_months + N_remaining_months
    total_tenure_breakdown = f"{int(total_tenure_months // 12)} years and {total_tenure_months % 12:.2f} months"
    
    total_interest_paid_stage_1 = sum(item['Interest Paid'] for item in monthly_schedule)
    
    # Total Interest Paid (Stage 2)
    # Total Paid Stage 2 = full_payments_remaining * emi_after_year_1 + final_payment_amount
    # Total Interest Stage 2 = Total Paid Stage 2 - P_remaining
    total_paid_stage_2 = full_payments_remaining * emi_after_year_1 + final_payment_amount
    total_interest_paid_stage_2 = total_paid_stage_2 - P_remaining
    
    total_interest = total_interest_paid_stage_1 + total_interest_paid_stage_2

    summary = {
        "Principal Remaining (After 12 months)": P_remaining,
        "Remaining Tenure (Months)": N_remaining_months,
        "Total Tenure (Months)": total_tenure_months,
        "Total Tenure Breakdown": total_tenure_breakdown,
        "Total Payments Made": total_payments,
        "Total Full Payments (Stage 2)": full_payments_remaining,
        "Final Payment Amount": final_payment_amount,
        "Total Interest Paid (Stage 1 + 2)": total_interest
    }
    
    return pd.DataFrame(monthly_schedule), summary

# --- Input Parameters ---
P_loan = 5000000.0  # ₹50 Lakh
R_rate = 0.075      # 7.5%
EMI_1 = 150000.0    # ₹1.5 Lakh for the first year
EMI_2 = 100000.0    # ₹1 Lakh afterwards

# Run the calculation
schedule_df, loan_summary = calculate_variable_emi_amortization(P_loan, R_rate, EMI_1, EMI_2)

# --- Output Results ---
print("\n" + "=" * 80)
print(f"LOAN AMORTIZATION SCENARIO: ₹{P_loan:,.2f} @ {R_rate*100}%")
print("=" * 80)

if "error" in loan_summary:
    print(f"Error: {loan_summary['error']}")
else:
    # 1. Output the First Year's Schedule
    print("\n## 💰 Stage 1: Amortization Schedule (Months 1 to 12 at ₹1,50,000 EMI)")
    # Show only the key columns for clarity
    display_df = schedule_df[['Month', 'EMI', 'Interest Paid', 'Principal Paid', 'Outstanding Principal']]
    
    # Format the monetary values
    def format_currency(x):
        return f'₹{x:,.2f}'

    for col in ['EMI', 'Interest Paid', 'Principal Paid', 'Outstanding Principal']:
        display_df[col] = display_df[col].apply(format_currency)
    
    print(display_df.to_markdown(index=False))

    # 2. Output the Summary
    print("\n## ⏱️ Stage 2: Loan Summary After 12 Months (at ₹1,00,000 EMI)")
    print("-" * 50)
    for key, value in loan_summary.items():
        if 'Amount' in key or 'Principal' in key or 'Interest' in key:
            print(f"{key:<35}: ₹{value:,.2f}")
        elif 'Months' in key or 'Payments' in key:
            print(f"{key:<35}: {value:.2f}")
        else:
            print(f"{key:<35}: {value}")
    print("-" * 50)