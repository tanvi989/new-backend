import stripe
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId
import config

# Initialize Stripe
stripe.api_key = config.STRIPE_SECRET_KEY


class StripePaymentService:
    """
    Stripe Payment Service for Multifolks
    Handles payment session creation, confirmation, and refunds
    """
    
    def __init__(self, db_connection):
        """
        Initialize the payment service
        
        Args:
            db_connection: MongoDB database connection
        """
        self.db = db_connection
        self.orders_collection = self.db['orders']
        self.payments_collection = self.db['payments']
    
    def create_checkout_session(
        self,
        order_id: str,
        amount: float,
        user_email: str,
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe Checkout Session
        
        Args:
            order_id: Unique order identifier
            amount: Payment amount in GBP
            user_email: Customer email
            user_id: User ID
            metadata: Additional metadata to attach to the session
            
        Returns:
            Dictionary containing session_id and payment_url
        """
        try:
            # Convert amount to pence (Stripe uses smallest currency unit)
            amount_in_pence = int(float(amount) * 100)
            
            # Prepare metadata
            session_metadata = {
                'order_id': order_id,
                'user_id': str(user_id),
                'created_at': datetime.utcnow().isoformat()
            }
            
            if metadata:
                session_metadata.update(metadata)
            
            # Create Stripe Checkout
            print(f"🔵 Creating Stripe session for order: {order_id}")
            print(f"🔵 Amount: {amount} {config.CURRENCY.upper()}")
            print(f"🔵 Success URL: {config.PAYMENT_SUCCESS_URL}?order_id={order_id}")
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],  # Can add 'paypal', etc.
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': config.CURRENCY,
                        'product_data': {
                            'name': f'Order {order_id}',
                        },
                        'unit_amount': int(amount * 100),
                    },
                    'quantity': 1,
                }],
                metadata=session_metadata,
                success_url=f"{config.PAYMENT_SUCCESS_URL}?order_id={order_id}&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=config.PAYMENT_CANCEL_URL,
                # expires_at removed - Stripe uses default 24h expiration
                client_reference_id=str(user_id),
                customer_email=user_email,
            )
            
            print(f"✅ Stripe session created: {session.id}")
            print(f"✅ Payment URL: {session.url}")
            
            # Store payment session in database
            payment_record = {
                'order_id': order_id,
                'user_id': user_id,
                'session_id': session.id,
                'amount': amount,
                'currency': config.CURRENCY,
                'status': 'pending',
                'created_at': datetime.utcnow(),
                'payment_method': 'stripe',
                'metadata': session_metadata
            }
            
            self.payments_collection.insert_one(payment_record)
            
            return {
                'success': True,
                'session_id': session.id,
                'payment_url': session.url,
                'expires_at': session.expires_at
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'stripe_error'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'server_error'
            }
    
    def confirm_payment(self, session_id: str, cart_service=None) -> Dict[str, Any]:
        """
        Confirm payment from Stripe session and create order
        
        Args:
            session_id: Stripe checkout session ID
            cart_service: CartService instance to get cart data
            
        Returns:
            Dictionary with confirmation status
        """
        try:
            # Retrieve session from Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status != 'paid':
                return {
                    'success': False,
                    'status': session.payment_status,
                    'message': 'Payment not completed'
                }
            
            # Get order_id and user_id from metadata
            order_id = session.metadata.get('order_id')
            user_id = session.metadata.get('user_id')
            
            if not order_id:
                return {
                    'success': False,
                    'message': 'Order ID not found in session metadata'
                }
            
            # Update payment record
            payment_update = {
                'status': 'completed',
                'payment_intent_id': session.payment_intent,
                'completed_at': datetime.utcnow(),
                'payment_status': session.payment_status
            }
            
            self.payments_collection.update_one(
                {'session_id': session_id},
                {'$set': payment_update}
            )
            
            # Create order from cart if cart_service is provided
            if cart_service and user_id:
                order_created = self.create_order_from_cart(
                    user_id=user_id,
                    order_id=order_id,
                    session=session,
                    cart_service=cart_service
                )
                
                if not order_created.get('success'):
                    print(f"Warning: Order creation failed: {order_created.get('error')}")
            else:
                # Fallback: Just update order payment status
                self.orders_collection.update_one(
                    {'order_id': order_id},
                    {'$set': {
                        'payment_status': 'paid',
                        'payment_method': 'stripe',
                        'payment_intent_id': session.payment_intent,
                        'updated_at': datetime.utcnow()
                    }},
                    upsert=True
                )
            
            return {
                'success': True,
                'order_id': order_id,
                'payment_intent_id': session.payment_intent,
                'amount_total': session.amount_total / 100,  # Convert back to GBP
                'currency': session.currency
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'stripe_error'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'server_error'
            }
    
    def create_order_from_cart(
        self,
        user_id: str,
        order_id: str,
        session: Any,
        cart_service
    ) -> Dict[str, Any]:
        """
        Create order from cart data after successful payment
        
        Args:
            user_id: User ID
            order_id: Order ID
            session: Stripe session object
            cart_service: CartService instance
            
        Returns:
            Dictionary with order creation status
        """
        try:
            # Get cart data
            cart_result = cart_service.get_cart_summary(user_id)
            
            if not cart_result.get('success'):
                return {
                    'success': False,
                    'error': 'Failed to retrieve cart data'
                }
            
            cart_data = cart_result.get('data', {})
            items = cart_data.get('items', [])
            
            if not items:
                return {
                    'success': False,
                    'error': 'Cart is empty'
                }
            
            # Get user details
            users_collection = self.db['users']
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            
            # Create order document
            order = {
                'order_id': order_id,
                'user_id': user_id,
                'user_email': user.get('email', '') if user else '',
                'user_name': f"{user.get('firstName', '')} {user.get('lastName', '')}".strip() if user else '',
                'items': items,
                'subtotal': cart_data.get('subtotal', 0),
                'shipping_cost': cart_data.get('shipping_cost', 0),
                'discount': cart_data.get('discount', 0),
                'total': session.amount_total / 100,
                'payment_status': 'paid',
                'payment_method': 'stripe',
                'payment_intent_id': session.payment_intent,
                'order_status': 'pending',
                'shipping_method': cart_data.get('shipping_method', {}),
                'coupon': cart_data.get('coupon', {}),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # Insert order
            self.orders_collection.insert_one(order)
            
            # Save total payable to user document for easy retrieval
            try:
                users_collection = self.db['users']
                total_payable = session.amount_total / 100  # Convert from pence to GBP
                users_collection.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$set': {
                        'last_order_total_payable': total_payable,
                        'last_order_id': order_id,
                        'last_order_date': datetime.utcnow()
                    }}
                )
                print(f"✅ Saved total payable £{total_payable} to user {user_id}")
            except Exception as e:
                print(f"⚠️ Warning: Failed to update user document with total payable: {str(e)}")
            
            # Clear cart
            cart_service.clear_cart(user_id)
            
            return {
                'success': True,
                'order_id': order_id,
                'message': 'Order created successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    
    def create_refund(
        self,
        payment_intent_id: str,
        amount: Optional[float] = None,
        reason: str = 'requested_by_customer'
    ) -> Dict[str, Any]:
        """
        Create a refund for a payment
        
        Args:
            payment_intent_id: Stripe payment intent ID
            amount: Amount to refund (None for full refund)
            reason: Reason for refund
            
        Returns:
            Dictionary with refund status
        """
        try:
            refund_params = {
                'payment_intent': payment_intent_id,
                'reason': reason
            }
            
            if amount:
                refund_params['amount'] = int(float(amount) * 100)  # Convert to pence
            
            refund = stripe.Refund.create(**refund_params)
            
            # Update payment record
            self.payments_collection.update_one(
                {'payment_intent_id': payment_intent_id},
                {'$set': {
                    'refund_id': refund.id,
                    'refund_status': refund.status,
                    'refunded_at': datetime.utcnow()
                }}
            )
            
            return {
                'success': True,
                'refund_id': refund.id,
                'status': refund.status,
                'amount': refund.amount / 100 if refund.amount else None
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'stripe_error'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'server_error'
            }
    
    def get_payment_status(self, order_id: str) -> Dict[str, Any]:
        """
        Get payment status for an order
        
        Args:
            order_id: Order ID
            
        Returns:
            Payment status information
        """
        try:
            payment = self.payments_collection.find_one({'order_id': order_id})
            
            if not payment:
                return {
                    'success': False,
                    'message': 'Payment not found'
                }
            
            return {
                'success': True,
                'order_id': order_id,
                'status': payment.get('status'),
                'amount': payment.get('amount'),
                'currency': payment.get('currency'),
                'payment_method': payment.get('payment_method'),
                'created_at': payment.get('created_at'),
                'completed_at': payment.get('completed_at')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
