import requests
import sys
import json
from datetime import datetime

class DivineCoCookieAPITester:
    def __init__(self, base_url="https://divine-orders.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if not success:
                details += f" (Expected: {expected_status})"
                try:
                    error_data = response.json()
                    details += f", Response: {error_data}"
                except:
                    details += f", Response: {response.text[:200]}"

            self.log_test(name, success, details)
            return success, response.json() if success and response.content else {}

        except Exception as e:
            self.log_test(name, False, f"Exception: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test API root endpoint"""
        return self.run_test("API Root", "GET", "", 200)

    def test_admin_login_valid(self):
        """Test admin login with valid credentials"""
        return self.run_test(
            "Admin Login (Valid)",
            "POST",
            "admin/login",
            200,
            data={"username": "admin", "password": "admin123"}
        )

    def test_admin_login_invalid(self):
        """Test admin login with invalid credentials"""
        success, response = self.run_test(
            "Admin Login (Invalid)",
            "POST",
            "admin/login",
            200,
            data={"username": "wrong", "password": "wrong"}
        )
        # Check if response indicates failure
        if success and response.get('success') == False:
            self.log_test("Admin Login Response Check", True, "Correctly rejected invalid credentials")
            return True, response
        else:
            self.log_test("Admin Login Response Check", False, "Should reject invalid credentials")
            return False, response

    def test_create_order(self):
        """Test creating a new order"""
        order_data = {
            "customer_name": "Test Customer",
            "phone": "09123456789",
            "address": "123 Test Street, Manila",
            "items": [
                {
                    "flavor": "Chocolate Chips",
                    "option": "piece",
                    "quantity": 2,
                    "price": 45
                },
                {
                    "flavor": "White Matcha",
                    "option": "box",
                    "quantity": 1,
                    "price": 260
                }
            ],
            "total": 350,
            "payment_method": "GCash"
        }
        
        success, response = self.run_test(
            "Create Order",
            "POST",
            "orders",
            200,
            data=order_data
        )
        
        if success:
            # Validate response structure
            required_fields = ['order_id', 'customer_name', 'phone', 'address', 'items', 'total', 'status', 'created_at']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                self.log_test("Order Response Structure", False, f"Missing fields: {missing_fields}")
                return False, response
            else:
                self.log_test("Order Response Structure", True, "All required fields present")
                return True, response
        
        return success, response

    def test_get_orders(self):
        """Test retrieving all orders"""
        return self.run_test("Get Orders", "GET", "orders", 200)

    def test_get_inventory(self):
        """Test inventory/sales summary endpoint"""
        success, response = self.run_test("Get Inventory", "GET", "inventory", 200)
        
        if success:
            # Validate inventory response structure
            required_fields = ['total_orders', 'total_revenue', 'best_selling_flavor', 'inventory']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                self.log_test("Inventory Response Structure", False, f"Missing fields: {missing_fields}")
                return False, response
            
            # Check inventory items structure
            if 'inventory' in response and len(response['inventory']) > 0:
                inventory_item = response['inventory'][0]
                required_item_fields = ['flavor', 'pieces_sold', 'boxes_sold', 'total_quantity']
                missing_item_fields = [field for field in required_item_fields if field not in inventory_item]
                
                if missing_item_fields:
                    self.log_test("Inventory Item Structure", False, f"Missing fields: {missing_item_fields}")
                    return False, response
                else:
                    self.log_test("Inventory Item Structure", True, "All required fields present")
            
            self.log_test("Inventory Response Structure", True, "All required fields present")
        
        return success, response

    def test_update_order_status(self):
        """Test updating order status"""
        # First create an order to update
        success, order_response = self.test_create_order()
        if not success:
            self.log_test("Update Order Status", False, "Failed to create order for testing")
            return False, {}
        
        order_id = order_response.get('order_id')
        if not order_id:
            self.log_test("Update Order Status", False, "No order_id in create response")
            return False, {}
        
        # Update the order status
        return self.run_test(
            "Update Order Status",
            "PATCH",
            f"orders/{order_id}",
            200,
            data={"status": "completed"}
        )

    def test_cookie_flavors_coverage(self):
        """Test that all 6 cookie flavors are supported"""
        expected_flavors = [
            "Chocolate Chips",
            "White Matcha", 
            "Deep Choco",
            "S'mores",
            "Monster Cookie",
            "Cheesy Velvet"
        ]
        
        # Get inventory to check flavors
        success, response = self.run_test("Cookie Flavors Coverage", "GET", "inventory", 200)
        
        if success and 'inventory' in response:
            available_flavors = [item['flavor'] for item in response['inventory']]
            missing_flavors = [flavor for flavor in expected_flavors if flavor not in available_flavors]
            
            if missing_flavors:
                self.log_test("All Cookie Flavors Present", False, f"Missing flavors: {missing_flavors}")
                return False, response
            else:
                self.log_test("All Cookie Flavors Present", True, f"All {len(expected_flavors)} flavors found")
                return True, response
        
        return success, response

    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Starting DivineCo Cookie API Tests...")
        print("=" * 50)
        
        # Test API availability
        self.test_root_endpoint()
        
        # Test admin authentication
        self.test_admin_login_valid()
        self.test_admin_login_invalid()
        
        # Test order management
        self.test_create_order()
        self.test_get_orders()
        self.test_update_order_status()
        
        # Test inventory/sales
        self.test_get_inventory()
        self.test_cookie_flavors_coverage()
        
        # Print summary
        print("\n" + "=" * 50)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return 1

def main():
    tester = DivineCoCookieAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())