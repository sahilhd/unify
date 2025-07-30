# Resend Email Integration Setup Guide

This guide will help you set up Resend for email verification in UniLLM.

## 🚀 **Step 1: Sign Up for Resend**

1. Go to [resend.com](https://resend.com)
2. Click "Get Started" and create an account
3. Verify your email address
4. You'll get **3,000 emails/month free** (100/day)

## 🔑 **Step 2: Get Your API Key**

1. After signing up, go to your Resend dashboard
2. Navigate to "API Keys" in the sidebar
3. Click "Create API Key"
4. Give it a name like "UniLLM Email Service"
5. Copy the API key (starts with `re_`)

## 📧 **Step 3: Set Up Domain (Optional but Recommended)**

### **Option A: Use Resend's Domain (Quick Start)**
- You can use `@resend.dev` domain for testing
- Set `RESEND_FROM_EMAIL=noreply@resend.dev` in your environment

### **Option B: Use Your Own Domain (Production)**
1. In Resend dashboard, go to "Domains"
2. Click "Add Domain"
3. Enter your domain (e.g., `yourdomain.com`)
4. Add the DNS records provided by Resend
5. Wait for verification (usually 5-10 minutes)
6. Set `RESEND_FROM_EMAIL=noreply@yourdomain.com`

## ⚙️ **Step 4: Configure Environment Variables**

Add these to your `.env` file:

```bash
# Email (Resend)
RESEND_API_KEY=re_your_api_key_here
RESEND_FROM_EMAIL=noreply@yourdomain.com
```

## 🧪 **Step 5: Test the Integration**

### **Install Dependencies:**
```bash
cd api_gateway
pip install resend==0.6.0
```

### **Test Email Sending:**
```python
# Test script
import os
from dotenv import load_dotenv
from email_service import email_service

load_dotenv()

# Test verification email
success = email_service.send_verification_email(
    "test@example.com", 
    "https://unillm-frontend.railway.app/verify-email?token=test_token"
)
print(f"Email sent: {success}")
```

## 📊 **Step 6: Monitor Email Delivery**

1. Go to Resend dashboard
2. Check "Activity" tab to see sent emails
3. Monitor delivery rates and bounces
4. Check "Analytics" for detailed metrics

## 🔧 **Step 7: Deploy to Railway**

1. Add environment variables to Railway:
   - `RESEND_API_KEY`
   - `RESEND_FROM_EMAIL`

2. Deploy your updated code

## 📧 **Email Templates**

The integration includes two beautiful email templates:

### **Verification Email:**
- Professional design with UniLLM branding
- Clear call-to-action button
- Fallback text link
- Mobile-responsive

### **Welcome Email:**
- Sent after successful verification
- Welcome message and next steps
- Dashboard link
- Feature highlights

## 🎯 **Features Included:**

✅ **Automatic email sending** on registration  
✅ **Resend verification** for users who didn't receive email  
✅ **Welcome email** after successful verification  
✅ **Beautiful HTML templates** with UniLLM branding  
✅ **Error handling** and logging  
✅ **Fallback mode** (logs emails when Resend not configured)  
✅ **Mobile-responsive** email design  

## 💰 **Pricing:**

- **Free Tier**: 3,000 emails/month (100/day)
- **Paid Plans**: Starting at $20/month for 50,000 emails
- **Perfect for**: Startups and small to medium projects

## 🚨 **Troubleshooting**

### **Emails Not Sending:**
1. Check `RESEND_API_KEY` is set correctly
2. Verify domain is configured (if using custom domain)
3. Check Resend dashboard for errors
4. Review server logs for error messages

### **Emails Going to Spam:**
1. Use a custom domain (not @resend.dev)
2. Set up proper DNS records
3. Warm up your domain gradually
4. Monitor sender reputation

### **Rate Limiting:**
- Free tier: 100 emails/day
- Upgrade plan if you exceed limits
- Implement email queuing for high volume

## 📈 **Monitoring & Analytics**

Resend provides excellent analytics:
- Delivery rates
- Open rates
- Click rates
- Bounce rates
- Geographic data

## 🔒 **Security Best Practices**

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** periodically
4. **Monitor for suspicious activity**
5. **Set up webhook notifications** for important events

## 🎉 **You're All Set!**

Your UniLLM application now has professional email verification with:
- Beautiful, branded email templates
- Reliable delivery via Resend
- Comprehensive error handling
- Easy monitoring and analytics

Users will receive professional verification emails and can start using your platform immediately after verification! 