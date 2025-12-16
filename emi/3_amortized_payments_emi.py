import pandas as pd
import numpy as np
import math

def calculate_variable_emi_amortization(principal, annual_rate, emi_year_1, emi_after_year_1, year_1_months):
    """
    Calculates the amortization schedule for a loan with a changing EMI.
    
    Args:
        principal (float): The initial loan amount.
        annual_rate (float): The annual interest rate (e.g., 0.075).
        emi_year_1 (float): Monthly payment for the first phase.
        emi_after_year_1 (float): Monthly payment after the first phase.
        year_1_months (int): Number of months for the first EMI phase.

    Returns:
        tuple: (DataFrame of the first phase's schedule, final loan summary)
    """
    r_monthly = annual_rate / 12
    loan_balance = principal
    monthly_schedule = []
    
    # --- STAGE 1: First EMI Phase ---
    current_emi = emi_year_1
    print(f"\n--- Stage 1: {year_1_months} Months at EMI ₹{current_emi:,.2f} ---")
    
    # Check if the initial EMI is sufficient
    if current_emi <= loan_balance * r_monthly:
        return pd.DataFrame(), {"error": "Initial EMI (Payment 1) is too low to cover monthly interest."}

    for month in range(1, year_1_months + 1):
        interest_paid = loan_balance * r_monthly
        principal_paid = current_emi - interest_paid
        
        # Check if the loan closes in Stage 1
        if principal_paid >= loan_balance:
            principal_paid = loan_balance
            loan_balance = 0
            monthly_schedule.append({
                'Month': month,
                'EMI': current_emi,
                'Interest Paid': interest_paid,
                'Principal Paid': principal_paid,
                'Outstanding Principal': 0
            })
            break # Exit loop if loan closes early
        
        loan_balance -= principal_paid
            
        monthly_schedule.append({
            'Month': month,
            'EMI': current_emi,
            'Interest Paid': interest_paid,
            'Principal Paid': principal_paid,
            'Outstanding Principal': loan_balance
        })

    # --- STAGE 2: Second EMI Phase ---
    
    P_remaining = loan_balance # Principal Outstanding after Stage 1
    
    if P_remaining <= 0:
        return pd.DataFrame(monthly_schedule), {"result": "Loan fully closed in Stage 1."}
        
    print(f"\n--- Stage 2: Remaining Tenure at EMI ₹{emi_after_year_1:,.2f} ---")
    
    # Check if the new EMI is sufficient for the reduced principal
    if emi_after_year_1 <= P_remaining * r_monthly:
        return pd.DataFrame(monthly_schedule), {"error": "Final EMI (Payment 2) is too low to service the remaining principal."}
        
    # Calculate remaining tenure (N_remaining)
    numerator_N = np.log(1 - (r_monthly * P_remaining) / emi_after_year_1)
    denominator_N = np.log(1 + r_monthly)
    N_remaining_months = -numerator_N / denominator_N

    # Final Payment Details
    full_payments_remaining = math.floor(N_remaining_months)
    
    n = full_payments_remaining
    power_term = np.power(1 + r_monthly, n)
    
    P_outstanding_after_full = (
        P_remaining * power_term - 
        (emi_after_year_1 / r_monthly) * (power_term - 1)
    )

    final_payment_amount = P_outstanding_after_full * (1 + r_monthly)
    
    # Total Time and Interest Calculation
    total_tenure_months = len(monthly_schedule) + N_remaining_months
    total_tenure_breakdown = f"{int(total_tenure_months // 12)} years and {total_tenure_months % 12:.2f} months"
    
    total_interest_paid_stage_1 = sum(item['Interest Paid'] for item in monthly_schedule)
    total_paid_stage_2 = full_payments_remaining * emi_after_year_1 + final_payment_amount
    total_interest_paid_stage_2 = total_paid_stage_2 - P_remaining
    
    total_interest = total_interest_paid_stage_1 + total_interest_paid_stage_2

    summary = {
        "Principal Remaining (After Stage 1)": P_remaining,
        "Remaining Tenure (Months)": N_remaining_months,
        "Total Tenure (Months)": total_tenure_months,
        "Total Tenure Breakdown": total_tenure_breakdown,
        "Total Payments Made": len(monthly_schedule) + full_payments_remaining + 1,
        "Final Payment Amount": final_payment_amount,
        "Total Interest Paid (Stage 1 + 2)": total_interest
    }
    
    return pd.DataFrame(monthly_schedule), summary


# --- Interactive Input Section ---
print("=" * 60)
print("HOME LOAN AMORTIZATION CALCULATOR (Variable EMI)")
print("=" * 60)

try:
    # Fixed Loan Parameters
    P_loan = 5000000.0  # ₹50 Lakh
    R_rate = 0.075      # 7.5%
    
    print(f"Base Loan: ₹{P_loan:,.2f} at {R_rate*100}% Annual Rate.")
    
    # User Input
    EMI_1 = float(input("Enter Payment 1 (EMI for first phase, e.g., 150000): ₹"))
    EMI_2 = float(input("Enter Payment 2 (EMI for subsequent phase, e.g., 100000): ₹"))
    TENURE_1 = int(input("Enter Duration of Payment 1 (in months, e.g., 12): "))

except ValueError:
    print("\nError: Please enter valid numeric values for the EMIs and an integer for months.")
    exit()

# Run the calculation
schedule_df, loan_summary = calculate_variable_emi_amortization(P_loan, R_rate, EMI_1, EMI_2, TENURE_1)

# --- Output Results ---
print("\n" + "=" * 80)
print("FINAL AMORTIZATION REPORT")
print("=" * 80)

if "error" in loan_summary:
    print(f"\nERROR: {loan_summary['error']}")
elif "result" in loan_summary:
    print(f"\nSUCCESS: {loan_summary['result']}")
    print("\n## 💰 Amortization Schedule (First Phase)")
    print(schedule_df[['Month', 'EMI', 'Interest Paid', 'Principal Paid', 'Outstanding Principal']].to_markdown(index=False, floatfmt=", .2f"))
else:
    # 1. Output the First Phase's Schedule
    print(f"\n## 💰 Stage 1: Amortization Schedule (Months 1 to {TENURE_1})")
    display_df = schedule_df[['Month', 'EMI', 'Interest Paid', 'Principal Paid', 'Outstanding Principal']].copy()
    
    # Format the monetary values for display
    def format_currency(x):
        return f'₹{x:,.2f}'

    for col in ['EMI', 'Interest Paid', 'Principal Paid', 'Outstanding Principal']:
        display_df[col] = display_df[col].apply(format_currency)
    
    print(display_df.to_markdown(index=False))

    # 2. Output the Summary
    print("\n## ⏱️ Stage 2: Loan Summary After Initial Phase")
    print("-" * 50)
    for key, value in loan_summary.items():
        if 'Amount' in key or 'Principal' in key or 'Interest' in key:
            print(f"{key:<35}: ₹{value:,.2f}")
        elif 'Months' in key or 'Payments' in key:
            print(f"{key:<35}: {value:.2f}")
        else:
            print(f"{key:<35}: {value}")
    print("-" * 50)

print("\n--- End of Report ---")