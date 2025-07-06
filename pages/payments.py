import streamlit as st

st.set_page_config(page_title="Pricing & Payment Terms", page_icon="💳")

st.title("💳 Pricing & Payment Terms")
st.markdown("---")

st.markdown("""
### Overview

Delta Desk is a subscription-based financial analytics platform. By subscribing to our services, you agree to the following terms regarding pricing, payments, renewals, and cancellations. Access subscription sign-up here 
(https://buy.stripe.com/cNi7sMfbygdL3ezffj1wY00)

---

### Subscription Plans

We offer multiple subscription tiers, including:

- **Monthly Plan:** Recurring monthly payment
- **Annual Plan:** Recurring yearly payment with discounted pricing

All prices are displayed in USD and exclude any applicable taxes.

---

### Billing & Renewals

- Your subscription will automatically renew at the end of each billing cycle unless you cancel prior to renewal.
- You authorize Delta Desk (via Stripe) to charge your payment method at the beginning of each billing cycle.
- You will receive an email confirmation after each successful payment.

---

### Cancellations & Refunds

- You may cancel your subscription at any time from your account portal.
- Canceling prevents future billing; however, no partial refunds are issued for the current billing period.
- In exceptional cases, you may contact support at npastori@umich.edu to request a refund, which will be evaluated at our sole discretion.

---

### Legal Terms

- By subscribing, you agree not to share or resell access to Delta Desk.
- Unauthorized access or commercial exploitation of this platform without a license will result in account termination and potential legal action.
- All content, design, and functionality are © Nicholas Pastori. All rights reserved.

---
""")
