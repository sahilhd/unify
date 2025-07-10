# 🏦 Payment Processing Setup Guide

This guide will help you set up payment processing for UniLLM using Stripe, enabling users to purchase credits and manage their billing.

## 🎯 Overview

The payment system includes:
- **Stripe Integration** for secure payment processing
- **Credit Packages** with volume discounts
- **Webhook Handling** for payment confirmations
- **Refund Processing** for customer support
- **Billing History** tracking

## 📋 Prerequisites

1. **Stripe Account**: Sign up at [stripe.com](https://stripe.com)
2. **Domain**: Your API gateway needs a public domain for webhooks
3. **SSL Certificate**: Required for production webhooks

## 🔧 Step 1: Stripe Account Setup

### 1.1 Create Stripe Account
1. Go to [stripe.com](https://stripe.com) and sign up
2. Complete account verification
3. Switch to **Test Mode** for development

### 1.2 Get API Keys
1. Go to **Developers → API Keys**
2. Copy your keys:
   - **Publishable Key**: `pk_test_...` (public)
   - **Secret Key**: `sk_test_...` (private)

### 1.3 Configure Webhooks
1. Go to **Developers → Webhooks**
2. Click **Add endpoint**
3. Set endpoint URL: `https://your-domain.com/billing/webhook`
4. Select events:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
   - `charge.refunded`
5. Copy the **Webhook Secret**: `whsec_...`

## 🔧 Step 2: Environment Configuration

### 2.1 Update Environment Variables
Add these to your `.env` file:

```bash
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

### 2.2 Install Dependencies
```bash
cd api_gateway
pip install -r requirements.txt
```

## 🔧 Step 3: Database Migration

The payment system adds new fields to the billing history table:

```sql
-- New fields added to billing_history table
ALTER TABLE billing_history ADD COLUMN stripe_payment_intent_id VARCHAR;
ALTER TABLE billing_history ADD COLUMN stripe_refund_id VARCHAR;
```

## 🔧 Step 4: Frontend Integration

### 4.1 Install Stripe.js
Add to your frontend `package.json`:
```json
{
  "dependencies": {
    "@stripe/stripe-js": "^2.4.0"
  }
}
```

### 4.2 Update Billing Component
The billing component now integrates with Stripe for real payments.

## 🧪 Step 5: Testing

### 5.1 Test Payment Flow
1. **Start the server**:
   ```bash
   cd api_gateway
   python main_phase2.py
   ```

2. **Test credit purchase**:
   ```bash
   curl -X POST "http://localhost:8000/billing/create-payment-intent" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"credit_amount": 100}'
   ```

3. **Use test card numbers**:
   - Success: `4242 4242 4242 4242`
   - Decline: `4000 0000 0000 0002`
   - Expiry: Any future date
   - CVC: Any 3 digits

### 5.2 Test Webhooks
Use Stripe CLI for local testing:
```bash
# Install Stripe CLI
stripe listen --forward-to localhost:8000/billing/webhook

# Test webhook
stripe trigger payment_intent.succeeded
```

## 💳 Credit Package Pricing

The system includes these credit packages:

| Credits | Price | Price/Credit | Discount |
|---------|-------|--------------|----------|
| 100     | $10   | $0.100       | 0%       |
| 500     | $45   | $0.090       | 10%      |
| 1,000   | $80   | $0.080       | 20%      |
| 2,000   | $150  | $0.075       | 25%      |
| 5,000   | $350  | $0.070       | 30%      |

## 🔄 Payment Flow

### 1. User Initiates Purchase
```javascript
// Frontend creates payment intent
const response = await fetch('/billing/create-payment-intent', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${apiKey}` },
  body: JSON.stringify({ credit_amount: 500 })
});
const { client_secret } = await response.json();
```

### 2. Stripe Payment
```javascript
// Frontend processes payment with Stripe
const { error } = await stripe.confirmCardPayment(client_secret, {
  payment_method: { card: cardElement }
});
```

### 3. Payment Confirmation
```javascript
// Frontend confirms payment
const result = await fetch('/billing/confirm-payment', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${apiKey}` },
  body: JSON.stringify({ payment_intent_id: paymentIntent.id })
});
```

### 4. Webhook Processing
- Stripe sends webhook to `/billing/webhook`
- System verifies payment and adds credits
- User receives confirmation

## 🛡️ Security Considerations

### 1. Webhook Verification
- Always verify webhook signatures
- Use HTTPS in production
- Validate payment amounts

### 2. API Key Security
- Store Stripe keys securely
- Use environment variables
- Never expose secret keys

### 3. Payment Validation
- Verify payment amounts match expected
- Check payment status before adding credits
- Log all transactions

## 🚀 Production Deployment

### 1. Switch to Live Mode
1. In Stripe Dashboard, switch to **Live Mode**
2. Update environment variables with live keys
3. Update webhook endpoint URL

### 2. SSL Certificate
- Ensure your domain has valid SSL
- Required for Stripe webhooks

### 3. Monitoring
- Monitor webhook delivery in Stripe Dashboard
- Set up alerts for failed payments
- Track payment success rates

## 🔧 API Endpoints

### Payment Endpoints
- `POST /billing/create-payment-intent` - Create payment intent
- `POST /billing/confirm-payment` - Confirm payment
- `GET /billing/credit-packages` - Get available packages
- `POST /billing/webhook` - Stripe webhook handler
- `POST /billing/refund` - Process refunds (admin)

### Example Usage
```bash
# Get credit packages
curl "http://localhost:8000/billing/credit-packages"

# Create payment intent
curl -X POST "http://localhost:8000/billing/create-payment-intent" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"credit_amount": 500}'

# Confirm payment
curl -X POST "http://localhost:8000/billing/confirm-payment" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"payment_intent_id": "pi_1234567890"}'
```

## 🐛 Troubleshooting

### Common Issues

1. **Webhook Not Receiving Events**
   - Check webhook endpoint URL
   - Verify SSL certificate
   - Check webhook secret

2. **Payment Intent Creation Fails**
   - Verify Stripe API keys
   - Check credit amount is valid
   - Ensure user authentication

3. **Credits Not Added After Payment**
   - Check webhook processing
   - Verify payment intent status
   - Check database connection

### Debug Mode
Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python main_phase2.py
```

## 📊 Analytics & Monitoring

### Key Metrics to Track
- Payment success rate
- Average order value
- Credit package popularity
- Refund rate
- Webhook delivery success

### Stripe Dashboard
- Monitor payments in real-time
- View webhook delivery logs
- Track revenue and disputes

## 🔄 Next Steps

After setting up payment processing:

1. **Implement Subscription Plans** - Monthly/yearly billing
2. **Add Usage Alerts** - Low credit notifications
3. **Implement Auto-recharge** - Automatic credit purchases
4. **Add Invoice Generation** - PDF invoices for customers
5. **Implement Tax Calculation** - Automatic tax handling

## 📞 Support

- **Stripe Support**: [support.stripe.com](https://support.stripe.com)
- **UniLLM Issues**: GitHub repository issues
- **Documentation**: [stripe.com/docs](https://stripe.com/docs)

---

**Ready to start accepting payments?** Follow this guide step by step to get your payment system up and running! 🚀 