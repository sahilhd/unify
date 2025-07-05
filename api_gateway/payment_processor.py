"""
Payment Processing Module for UniLLM

Handles Stripe integration for credit purchases and billing management.
"""

import os
import stripe
from decimal import Decimal
from typing import Dict, Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database import User, BillingHistory
from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY

class PaymentProcessor:
    """Handles payment processing and credit purchases"""
    
    # Credit package pricing (in USD)
    CREDIT_PACKAGES = {
        100: 10.00,    # $10 for 100 credits
        500: 45.00,    # $45 for 500 credits (10% discount)
        1000: 80.00,   # $80 for 1000 credits (20% discount)
        2000: 150.00,  # $150 for 2000 credits (25% discount)
        5000: 350.00,  # $350 for 5000 credits (30% discount)
    }
    
    @classmethod
    def create_payment_intent(cls, user: User, credit_amount: int) -> Dict:
        """
        Create a Stripe payment intent for credit purchase
        
        Args:
            user: The user making the purchase
            credit_amount: Number of credits to purchase
            
        Returns:
            Payment intent data
        """
        if credit_amount not in cls.CREDIT_PACKAGES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid credit amount. Available amounts: {list(cls.CREDIT_PACKAGES.keys())}"
            )
        
        amount_usd = cls.CREDIT_PACKAGES[credit_amount]
        
        try:
            # Create payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount_usd * 100),  # Stripe uses cents
                currency="usd",
                metadata={
                    "user_id": user.id,
                    "user_email": user.email,
                    "credit_amount": credit_amount,
                    "amount_usd": str(amount_usd)
                },
                description=f"Purchase {credit_amount} credits for {user.email}",
                receipt_email=user.email
            )
            
            return {
                "client_secret": payment_intent.client_secret,
                "payment_intent_id": payment_intent.id,
                "amount_usd": amount_usd,
                "credit_amount": credit_amount
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment processing error: {str(e)}"
            )
    
    @classmethod
    def process_payment_success(cls, db: Session, payment_intent_id: str) -> Dict:
        """
        Process successful payment and add credits to user account
        
        Args:
            db: Database session
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Updated user data
        """
        try:
            # Retrieve payment intent from Stripe
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if payment_intent.status != "succeeded":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Payment not completed"
                )
            
            # Extract metadata
            user_id = payment_intent.metadata.get("user_id")
            credit_amount = int(payment_intent.metadata.get("credit_amount"))
            amount_usd = float(payment_intent.metadata.get("amount_usd"))
            
            # Get user
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Add credits to user account
            user.credits += Decimal(str(credit_amount))
            
            # Log billing transaction
            billing_record = BillingHistory(
                user_id=user.id,
                amount=amount_usd,
                description=f"Credit purchase: {credit_amount} credits via Stripe",
                transaction_type="credit_purchase",
                stripe_payment_intent_id=payment_intent_id
            )
            
            db.add(billing_record)
            db.commit()
            db.refresh(user)
            
            return {
                "message": "Payment processed successfully",
                "credits_added": credit_amount,
                "amount_paid": amount_usd,
                "new_balance": float(user.credits),
                "user_id": user.id
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}"
            )
    
    @classmethod
    def get_credit_packages(cls) -> List[Dict]:
        """Get available credit packages with pricing"""
        return [
            {
                "credits": credits,
                "price_usd": price,
                "price_per_credit": round(price / credits, 3),
                "discount_percent": cls._calculate_discount(credits)
            }
            for credits, price in cls.CREDIT_PACKAGES.items()
        ]
    
    @classmethod
    def _calculate_discount(cls, credit_amount: int) -> int:
        """Calculate discount percentage for credit package"""
        base_price = credit_amount * 0.10  # $0.10 per credit base price
        actual_price = cls.CREDIT_PACKAGES[credit_amount]
        discount = ((base_price - actual_price) / base_price) * 100
        return int(discount)
    
    @classmethod
    def refund_payment(cls, db: Session, payment_intent_id: str, reason: str = "Customer request") -> Dict:
        """
        Process refund for a payment
        
        Args:
            db: Database session
            payment_intent_id: Stripe payment intent ID
            reason: Reason for refund
            
        Returns:
            Refund confirmation
        """
        try:
            # Create refund in Stripe
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                reason="requested_by_customer"
            )
            
            # Get original billing record
            billing_record = db.query(BillingHistory).filter(
                BillingHistory.stripe_payment_intent_id == payment_intent_id
            ).first()
            
            if billing_record:
                # Log refund transaction
                refund_record = BillingHistory(
                    user_id=billing_record.user_id,
                    amount=-billing_record.amount,  # Negative amount for refund
                    description=f"Refund: {reason}",
                    transaction_type="refund",
                    stripe_refund_id=refund.id
                )
                db.add(refund_record)
                db.commit()
            
            return {
                "message": "Refund processed successfully",
                "refund_id": refund.id,
                "status": refund.status
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Refund error: {str(e)}"
            )

class WebhookHandler:
    """Handles Stripe webhook events"""
    
    @classmethod
    def handle_webhook(cls, payload: bytes, signature: str, db: Session) -> Dict:
        """
        Process Stripe webhook events
        
        Args:
            payload: Raw webhook payload
            signature: Webhook signature
            db: Database session
            
        Returns:
            Processing result
        """
        try:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload, signature, STRIPE_WEBHOOK_SECRET
            )
            
            # Handle different event types
            if event["type"] == "payment_intent.succeeded":
                return cls._handle_payment_success(event, db)
            elif event["type"] == "payment_intent.payment_failed":
                return cls._handle_payment_failure(event, db)
            elif event["type"] == "charge.refunded":
                return cls._handle_refund(event, db)
            else:
                return {"status": "ignored", "event_type": event["type"]}
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payload"
            )
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature"
            )
    
    @classmethod
    def _handle_payment_success(cls, event: Dict, db: Session) -> Dict:
        """Handle successful payment webhook"""
        payment_intent = event["data"]["object"]
        return PaymentProcessor.process_payment_success(db, payment_intent["id"])
    
    @classmethod
    def _handle_payment_failure(cls, event: Dict, db: Session) -> Dict:
        """Handle failed payment webhook"""
        payment_intent = event["data"]["object"]
        # Log failed payment for analytics
        return {"status": "payment_failed", "payment_intent_id": payment_intent["id"]}
    
    @classmethod
    def _handle_refund(cls, event: Dict, db: Session) -> Dict:
        """Handle refund webhook"""
        charge = event["data"]["object"]
        # Update billing records if needed
        return {"status": "refund_processed", "charge_id": charge["id"]} 