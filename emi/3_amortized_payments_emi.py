import pandas as pd
import numpy as np
import math

def calculate_variable_emi_amortization(principal, annual_rate, emi_year_1, emi_after_year_1, year_1_months):
    """
    Calculates the full, month-by-month amortization schedule for a loan with a changing EMI.
    
    Args:
        principal (float): The initial loan amount.
        annual_rate (float): The annual interest rate (e.g., 0.075).
        emi_year_1 (float): Monthly payment for the first phase.
        emi_after_year_1 (float): Monthly payment after the first phase.
        year_1_months (int): Number of months for the first EMI phase.

    Returns:
        tuple: (DataFrame of the full schedule, final loan summary)
    """
    r_monthly = annual_rate / 12
    loan_balance = principal
    monthly_schedule = []
    
    # --- STAGE 1: First EMI Phase ---
    current_emi = emi_year_1
    
    # Check if the initial EMI is sufficient
    if current_emi <= loan_balance * r_monthly:
        return pd.DataFrame(), {"error": "Initial EMI (Payment 1) is too low to cover monthly interest."}

    for month in range(1, year_1_months + 1):
        interest_paid = loan_balance * r_monthly
        
        # Check if the loan closes in Stage 1
        if loan_balance * (1 + r_monthly) <= current_emi:
            final_payment_amount = loan_balance * (1 + r_monthly)
            principal_paid = final_payment_amount - interest_paid
            monthly_schedule.append({
                'Month': month,
                'EMI': final_payment_amount,
                'Interest Paid': interest_paid,
                'Principal Paid': principal_paid,
                'Outstanding Principal': 0.0,
                'Phase': 1
            })
            loan_balance = 0.0
            break # Loan closed in Stage 1

        principal_paid = current_emi - interest_paid
        loan_balance -= principal_paid
            
        monthly_schedule.append({
            'Month': month,
            'EMI': current_emi,
            'Interest Paid': interest_paid,
            'Principal Paid': principal_paid,
            'Outstanding Principal': loan_balance,
            'Phase': 1
        })

    # --- STAGE 2: Second EMI Phase ---
    P_remaining = loan_balance # Principal Outstanding after Stage 1
    start_month = len(monthly_schedule)

    if P_remaining > 0:
        current_emi = emi_after_year_1
        
        # Check if the new EMI is sufficient
        if current_emi <= P_remaining * r_monthly:
            return pd.DataFrame(monthly_schedule), {"error": "Final EMI (Payment 2) is too low to service the remaining principal."}
            
        # Continue amortization month-by-month until closure
        month_counter = start_month + 1
        while P_remaining > 0:
            interest_paid = P_remaining * r_monthly
            
            # Check for final payment
            if P_remaining * (1 + r_monthly) <= current_emi:
                final_payment_amount = P_remaining * (1 + r_monthly)
                principal_paid = final_payment_amount - interest_paid
                
                monthly_schedule.append({
                    'Month': month_counter,
                    'EMI': final_payment_amount,
                    'Interest Paid': interest_paid,
                    'Principal Paid': principal_paid,
                    'Outstanding Principal': 0.0,
                    'Phase': 2
                })
                P_remaining = 0.0
            else:
                principal_paid = current_emi - interest_paid
                P_remaining -= principal_paid
                
                monthly_schedule.append({
                    'Month': month_counter,
                    'EMI': current_emi,
                    'Interest Paid': interest_paid,
                    'Principal Paid': principal_paid,
                    'Outstanding Principal': P_remaining,
                    'Phase': 2
                })
            
            month_counter += 1

    # --- Summary Calculation ---
    full_schedule_df = pd.DataFrame(monthly_schedule)
    
    total_tenure_months = full_schedule_df['Month'].iloc[-1]
    total_tenure_breakdown = f"{int(total_tenure_months // 12)} years and {total_tenure_months % 12:.0f} months"
    total_interest = full_schedule_df['Interest Paid'].sum()
    
    summary = {
        "Total Tenure (Months)": total_tenure_months,
        "Total Tenure Breakdown": total_tenure_breakdown,
        "Total Payments Made": total_tenure_months,
        "Total Interest Paid": total_interest,
        "Principal Remaining (After Payment 1 Phase)": full_schedule_df[full_schedule_df['Phase'] == 1]['Outstanding Principal'].iloc[-1] if not full_schedule_df[full_schedule_df['Phase'] == 1].empty else principal,
        "Final Payment Amount": full_schedule_df['EMI'].iloc[-1]
    }
    
    return full_schedule_df, summary


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
    print("\nError: Please enter valid numeric values.")
    exit()

# Run the calculation
schedule_df, loan_summary = calculate_variable_emi_amortization(P_loan, R_rate, EMI_1, EMI_2, TENURE_1)

# --- Output Results ---
print("\n" + "=" * 80)
print("FINAL AMORTIZATION REPORT")
print("=" * 80)

if "error" in loan_summary:
    print(f"\nERROR: {loan_summary['error']}")
else:
    # 1. Output the Summary
    print("## ⏱️ Loan Summary (Full Term)")
    print("-" * 50)
    for key, value in loan_summary.items():
        if 'Amount' in key or 'Principal' in key or 'Interest' in key:
            print(f"{key:<35}: ₹{value:,.2f}")
        elif 'Months' in key or 'Payments' in key:
            # Display whole numbers for months/tenure
            print(f"{key:<35}: {value:.0f}" if isinstance(value, (int, float)) else f"{key:<35}: {value}")
        else:
            print(f"{key:<35}: {value}")
    print("-" * 50)

    # 2. Output the Full Schedule
    
    # Prepare unformatted data for the final display to let to_markdown handle it correctly
    display_df = schedule_df[['Month', 'Phase', 'EMI', 'Interest Paid', 'Principal Paid', 'Outstanding Principal']].copy()
    display_df['Phase'] = display_df['Phase'].apply(lambda x: f'Pmt 1 (₹{EMI_1:,.0f})' if x == 1 else f'Pmt 2 (₹{EMI_2:,.0f})')
    
    print("\n## 📑 Full Amortization Schedule (Month-by-Month)")
    print("All currency values are formatted to two decimal places with comma separators.")
    print("-" * 80)
    
    # CORRECTED LINE: Using the standard floatfmt=",.2f"
    print(display_df.to_markdown(index=False, floatfmt=",.2f"))

print("\n--- End of Report ---")
