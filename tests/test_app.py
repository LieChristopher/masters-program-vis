"""Tests for currency conversion and core app logic"""
import json
import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_test_data():
    """Load data files for testing"""
    with open('data/university_data.json', 'r') as f:
        uni_data = json.load(f)
    with open('data/exchange_rates.json', 'r') as f:
        rates = json.load(f)
    return uni_data, rates


def get_cost_in_idr(cost_dict, rates):
    """Convert cost dict to IDR"""
    amount = cost_dict['amount']
    currency = cost_dict['currency']
    return amount * rates['rates_to_idr'][currency]


def get_cost_in_usd(cost_dict, rates):
    """Convert cost dict to USD via IDR"""
    usd_to_idr = rates['rates_to_idr']['USD']
    idr = get_cost_in_idr(cost_dict, rates)
    return idr / usd_to_idr


class TestCurrencyConversion(unittest.TestCase):
    """Test currency conversion logic"""
    
    def setUp(self):
        self.uni_data, self.rates = load_test_data()
    
    def test_usd_conversion(self):
        """Test USD conversion (should be 1:1)"""
        mit = self.uni_data['universities']['MIT']
        tuition_usd = get_cost_in_usd(mit['tuition_per_year'], self.rates)
        self.assertEqual(tuition_usd, 55000)
    
    def test_non_usd_conversion(self):
        """Test non-USD currency conversion"""
        for uni_key, uni in self.uni_data['universities'].items():
            tuition = uni['tuition_per_year']
            if tuition['currency'] != 'USD':
                usd = get_cost_in_usd(tuition, self.rates)
                idr = get_cost_in_idr(tuition, self.rates)
                self.assertGreater(usd, 0)
                self.assertGreater(idr, 0)
                break


class TestExchangeRates(unittest.TestCase):
    """Test exchange rate coverage"""
    
    def setUp(self):
        self.uni_data, self.rates = load_test_data()
    
    def test_all_currencies_have_rates(self):
        """Test that all currencies in data have exchange rates"""
        available_rates = set(self.rates['rates_to_idr'].keys())
        
        used_currencies = set()
        for uni in self.uni_data['universities'].values():
            used_currencies.add(uni['tuition_per_year']['currency'])
            used_currencies.add(uni['living_per_year']['currency'])
        
        missing = used_currencies - available_rates
        self.assertFalse(missing, f"Missing exchange rates for: {missing}")


class TestCostCalculations(unittest.TestCase):
    """Test total cost calculations"""
    
    def setUp(self):
        self.uni_data, self.rates = load_test_data()
    
    def test_mit_cost_calculation(self):
        """Test MIT cost calculations"""
        mit = self.uni_data['universities']['MIT']
        tuition_usd = get_cost_in_usd(mit['tuition_per_year'], self.rates)
        living_usd = get_cost_in_usd(mit['living_per_year'], self.rates)
        total_per_year = tuition_usd + living_usd
        total_program = total_per_year * mit['duration_years']
        
        self.assertEqual(total_per_year, 80000)
        self.assertEqual(total_program, 160000)


class TestScholarshipCoverage(unittest.TestCase):
    """Test scholarship coverage calculations"""
    
    def setUp(self):
        self.uni_data, self.rates = load_test_data()
    
    def test_lpdp_coverage(self):
        """Test LPDP full coverage"""
        lpdp = self.uni_data['scholarships']['LPDP']
        self.assertEqual(lpdp['tuition_coverage'], 1.0)
        self.assertEqual(lpdp['living_coverage'], 1.0)
        self.assertTrue(lpdp['flights_covered'])


class TestDataIntegrity(unittest.TestCase):
    """Test data structure integrity"""
    
    def setUp(self):
        self.uni_data, self.rates = load_test_data()
    
    def test_university_required_fields(self):
        """Test all universities have required fields"""
        required_fields = ['name', 'country', 'city', 'tuition_per_year', 
                          'living_per_year', 'duration_years', 'tier', 'salaries']
        
        for uni_key, uni in self.uni_data['universities'].items():
            for field in required_fields:
                self.assertIn(field, uni, f"{uni_key} missing field: {field}")
            
            self.assertIn('amount', uni['tuition_per_year'])
            self.assertIn('currency', uni['tuition_per_year'])
            self.assertIn('amount', uni['living_per_year'])
            self.assertIn('currency', uni['living_per_year'])
    
    def test_scholarship_required_fields(self):
        """Test all scholarships have required fields"""
        required_fields = ['name', 'tuition_coverage', 'living_coverage', 
                          'flights_covered', 'return_required']
        
        for schol_key, schol in self.uni_data['scholarships'].items():
            for field in required_fields:
                self.assertIn(field, schol, f"{schol_key} missing field: {field}")


class TestScholarshipAvailability(unittest.TestCase):
    """Test scholarship-university availability matrix"""
    
    def setUp(self):
        self.uni_data, self.rates = load_test_data()
    
    def test_availability_references(self):
        """Test scholarship availability matrix references valid entities"""
        universities = set(self.uni_data['universities'].keys())
        scholarships = set(self.uni_data['scholarships'].keys())
        
        for uni_key, schol_list in self.uni_data['scholarship_availability'].items():
            self.assertIn(uni_key, universities)
            for schol_key in schol_list:
                self.assertIn(schol_key, scholarships)


if __name__ == '__main__':
    unittest.main()
