def sales_email_en(row, reason, offer):
    """
    English template for sales representatives.
    """
    return f"""
Subject: Action Needed — {row['name']} ({row['customer_id']})

Hi Team,

Please reach out to **{row['name']}** regarding their **{row['car_model']}**.

**Reason:** {reason}  
**Churn Risk:** {row['churn_risk_bucket']} ({row['churn_risk_score']:.2f})  
**Lease Ends In:** {row['days_until_lease_end']} days  
**Recommended Offer:** {offer}

Let’s secure this renewal before the customer is at risk of churning.

Regards,  
Customer Intelligence Agent
"""


def sales_email_ar(row, reason, offer):
    """
    Arabic template (Modern Standard Arabic).
    """
    return f"""
الموضوع: مطلوب إجراء — {row['name']} ({row['customer_id']})

مرحباً فريق المبيعات،

يرجى التواصل مع العميل **{row['name']}** بخصوص مركبته **{row['car_model']}**.

**السبب:** {reason}  
**مستوى خطر فقدان العميل:** {row['churn_risk_bucket']} ({row['churn_risk_score']:.2f})  
**عدد الأيام المتبقية على انتهاء العقد:** {row['days_until_lease_end']} يوم  
**العرض المقترح:** {offer}

دعونا نضمن تجديد العقد قبل أن نفقد العميل.

مع التحية،  
نظام الذكاء للعملاء
"""


def sales_email_manager(row, reason, offer):
    """
    Escalation template for sales managers (English).
    """
    return f"""
Subject: URGENT Escalation — {row['name']} ({row['customer_id']})

Dear Sales Manager,

A high-value/high-risk customer requires immediate attention.

Customer: {row['name']}  
Car Model: {row['car_model']}  
Days Until Lease End: {row['days_until_lease_end']}  
Churn Risk: {row['churn_risk_bucket']} ({row['churn_risk_score']:.2f})

Reason: {reason}  
Recommended Offer: {offer}

Kindly assign this to the appropriate salesperson immediately.

Regards,  
Customer Intelligence Agent
"""
