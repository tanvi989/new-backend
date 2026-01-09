"""
BlueDart Delivery Service Integration for Multifolks
Handles shipping, tracking, and delivery management
"""
import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from xml.etree import ElementTree as ET
from xml.dom import minidom
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)


class BlueDartService:
    """BlueDart courier integration service"""
    
    # Status mapping from BlueDart to internal order status codes
    STATUS_MAP = {
        "SHIPMENT PICKED UP": 70,
        "SHIPMENT IN TRANSIT": 72,
        "SHIPMENT ARRIVED": 72,
        "SHIPMENT OUT FOR DELIVERY": 72,
        "SHIPMENT DELIVERED": 75,
        "SHIPMENT RETURNED": 73,
        "RETURN TO SHIPPER": 73,
        "DELIVERED BACK TO SHIPPER": 73,
        "SHIPMENT DESTROYED": 77,
        "SHIPMENT MISPLACED": 77,
    }
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize BlueDart service with configuration
        
        Args:
            config: Dictionary containing BlueDart credentials and settings
        """
        self.base_url = config.get('BLUEDART_BASE_URL', 'https://netconnect.bluedart.com/Ver1.10/')
        self.customer_code = config.get('BLUEDART_CUSTOMER_CODE', '940553')
        self.login_id = config.get('BLUEDART_LOGIN_ID', 'GG940553')
        self.license_key = config.get('BLUEDART_LICENSE_KEY', '0bcbd949df368625eb964bb846041db1')
        self.warehouse_pincode = config.get('WAREHOUSE_PINCODE', '122001')
        self.warehouse_address = config.get('WAREHOUSE_ADDRESS', {
            'line1': 'Plot A-8, Infocity 1',
            'line2': 'Sector 34',
            'line3': 'Gurgaon, Haryana 122002',
            'phone': '0124-6101010'
        })
    
    def check_pincode_serviceability(self, pincode: str) -> Dict[str, Any]:
        """
        Check if a pincode is serviceable by BlueDart
        
        Args:
            pincode: Customer pincode to check
            
        Returns:
            Dict with serviceability status and details
        """
        try:
            url = f"{self.base_url}ShippingAPI/Finder/ServiceFinderQuery.svc"
            
            # Simplified HTTP request (you may need to use SOAP library like zeep)
            # For now, returning mock data - implement actual SOAP call
            
            # Mock response for demonstration
            return {
                'success': True,
                'serviceable': True,
                'pincode': pincode,
                'cod_available': True,
                'prepaid_available': True,
                'message': 'Pincode is serviceable'
            }
            
        except Exception as e:
            logger.error(f"Error checking pincode serviceability: {e}", exc_info=True)
            return {
                'success': False,
                'serviceable': False,
                'pincode': pincode,
                'message': f'Error: {str(e)}'
            }
    
    def calculate_delivery_timeline(self, destination_pincode: str) -> Dict[str, Any]:
        """
        Calculate expected delivery date for a pincode
        
        Args:
            destination_pincode: Customer's delivery pincode
            
        Returns:
            Dict with expected delivery date and transit days
        """
        try:
            # Calculate pickup date (if after 4 PM, next day)
            pickup_date = datetime.now()
            if pickup_date.hour >= 16:
                pickup_date = pickup_date + timedelta(days=1)
            
            # Mock calculation - implement actual BlueDart API call
            # Typically 3-7 business days for most locations
            transit_days = 5
            expected_delivery = pickup_date + timedelta(days=transit_days)
            
            return {
                'success': True,
                'pickup_date': pickup_date.strftime('%Y-%m-%d'),
                'expected_delivery_date': expected_delivery.strftime('%Y-%m-%d'),
                'transit_days': transit_days,
                'destination_pincode': destination_pincode
            }
            
        except Exception as e:
            logger.error(f"Error calculating delivery timeline: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def generate_awb(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AWB (Airway Bill) number and shipping label
        
        Args:
            order_data: Dictionary containing order and customer details
                - order_id: Order ID
                - customer_name: Customer name
                - customer_mobile: Customer phone
                - customer_address: Address lines
                - customer_pincode: Delivery pincode
                - declared_value: Package value
                - weight: Package weight in kg
                
        Returns:
            Dict with AWB number and status
        """
        try:
            # Extract order details
            order_id = order_data.get('order_id')
            customer_name = order_data.get('customer_name', '')[:20]  # Max 20 chars
            customer_mobile = order_data.get('customer_mobile', '')
            customer_pincode = order_data.get('customer_pincode', '')
            declared_value = order_data.get('declared_value', 0)
            weight = order_data.get('weight', 0.49)  # Default 0.49 kg
            
            # Address handling
            address_line1 = order_data.get('address_line1', '')[:30]
            address_line2 = order_data.get('address_line2', '')[:30]
            address_line3 = order_data.get('address_line3', '')[:30]
            
            # Pickup date/time
            pickup_date = datetime.now().strftime('%Y-%m-%d')
            pickup_time = datetime.now().strftime('%H%M')
            if pickup_time < '0601':
                pickup_time = '0601'
            
            # Mock AWB generation - implement actual SOAP call
            awb_number = f"BD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            logger.info(f"Generated AWB {awb_number} for order {order_id}")
            
            return {
                'success': True,
                'awb_number': awb_number,
                'order_id': order_id,
                'pickup_date': pickup_date,
                'pickup_time': pickup_time,
                'message': 'AWB generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Error generating AWB: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def track_shipment(self, awb_number: str) -> Dict[str, Any]:
        """
        Track shipment using AWB number
        
        Args:
            awb_number: AWB/tracking number
            
        Returns:
            Dict with tracking details and current status
        """
        try:
            url = (
                f"https://api.bluedart.com/servlet/RoutingServlet?"
                f"handler=tnt&action=custawbquery&loginid={self.login_id}"
                f"&awb=awb&numbers={awb_number}&format=txtl"
                f"&lickey=442c74f7ad031414870a084d57791010&verno=1.3&scan=1"
            )
            
            # Mock tracking data - implement actual API call
            return {
                'success': True,
                'awb_number': awb_number,
                'status': 'In Transit',
                'status_code': 72,
                'current_location': 'Gurgaon Hub',
                'expected_delivery': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
                'tracking_history': [
                    {
                        'status': 'Shipment Picked Up',
                        'location': 'Gurgaon',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
            }
            
        except Exception as e:
            logger.error(f"Error tracking shipment: {e}", exc_info=True)
            return {
                'success': False,
                'awb_number': awb_number,
                'message': f'Error: {str(e)}'
            }
    
    def schedule_pickup(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule pickup for an order
        
        Args:
            order_data: Order and pickup details
            
        Returns:
            Dict with pickup confirmation
        """
        try:
            pickup_date = datetime.now()
            if pickup_date.hour >= 16:
                pickup_date = pickup_date + timedelta(days=1)
            
            return {
                'success': True,
                'pickup_scheduled': True,
                'pickup_date': pickup_date.strftime('%Y-%m-%d'),
                'pickup_time_slot': '10:00 AM - 6:00 PM',
                'message': 'Pickup scheduled successfully'
            }
            
        except Exception as e:
            logger.error(f"Error scheduling pickup: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }


class DeliveryService:
    """Main delivery service orchestrator"""
    
    def __init__(self, db, config: Dict[str, Any]):
        """
        Initialize delivery service
        
        Args:
            db: Database connection
            config: Configuration dictionary
        """
        self.db = db
        self.config = config
        self.bluedart = BlueDartService(config)
        self.orders_collection = db['orders']
        self.shipments_collection = db['shipments']
    
    def create_shipment(self, order_id: str, customer_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new shipment for an order
        
        Args:
            order_id: Order ID
            customer_details: Customer and delivery information
            
        Returns:
            Dict with shipment details
        """
        try:
            # Check pincode serviceability
            pincode = customer_details.get('pincode')
            serviceability = self.bluedart.check_pincode_serviceability(pincode)
            
            if not serviceability.get('serviceable'):
                return {
                    'success': False,
                    'message': 'Delivery not available for this pincode'
                }
            
            # Generate AWB
            order_data = {
                'order_id': order_id,
                'customer_name': customer_details.get('name'),
                'customer_mobile': customer_details.get('mobile'),
                'customer_pincode': pincode,
                'address_line1': customer_details.get('address_line1'),
                'address_line2': customer_details.get('address_line2'),
                'address_line3': customer_details.get('address_line3'),
                'declared_value': customer_details.get('order_value', 0),
                'weight': customer_details.get('weight', 0.49)
            }
            
            awb_result = self.bluedart.generate_awb(order_data)
            
            if not awb_result.get('success'):
                return awb_result
            
            # Calculate delivery timeline
            timeline = self.bluedart.calculate_delivery_timeline(pincode)
            
            # Save shipment to database
            shipment_data = {
                'order_id': order_id,
                'awb_number': awb_result.get('awb_number'),
                'courier_partner': 'BlueDart',
                'status': 'created',
                'status_code': 64,  # Shipping label created
                'customer_details': customer_details,
                'expected_delivery_date': timeline.get('expected_delivery_date'),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            self.shipments_collection.insert_one(shipment_data)
            
            return {
                'success': True,
                'shipment_id': str(shipment_data['_id']),
                'awb_number': awb_result.get('awb_number'),
                'expected_delivery_date': timeline.get('expected_delivery_date'),
                'message': 'Shipment created successfully'
            }
            
        except Exception as e:
            logger.error(f"Error creating shipment: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def get_shipment_status(self, awb_number: str) -> Dict[str, Any]:
        """
        Get current status of a shipment
        
        Args:
            awb_number: Tracking number
            
        Returns:
            Dict with shipment status
        """
        try:
            # Get from database
            shipment = self.shipments_collection.find_one({'awb_number': awb_number})
            
            if not shipment:
                return {
                    'success': False,
                    'message': 'Shipment not found'
                }
            
            # Get live tracking from BlueDart
            tracking = self.bluedart.track_shipment(awb_number)
            
            return {
                'success': True,
                'shipment': {
                    'order_id': shipment.get('order_id'),
                    'awb_number': awb_number,
                    'status': tracking.get('status'),
                    'status_code': tracking.get('status_code'),
                    'current_location': tracking.get('current_location'),
                    'expected_delivery': tracking.get('expected_delivery'),
                    'tracking_history': tracking.get('tracking_history', [])
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting shipment status: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
