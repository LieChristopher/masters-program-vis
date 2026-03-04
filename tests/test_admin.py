"""Test script for admin features"""
import json
import os
import sys
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.admin import load_json_data, save_json_data


class TestJSONFormat(unittest.TestCase):
    """Test JSON format validity"""
    
    def test_json_is_valid(self):
        """Test JSON is valid and parseable"""
        with open('data/university_data.json', 'r') as f:
            json.load(f)


class TestJSONLoading(unittest.TestCase):
    """Test loading JSON data"""
    
    def test_load_json_data(self):
        """Test loading JSON data"""
        data = load_json_data()
        self.assertIn('universities', data)
        self.assertIn('scholarships', data)
        self.assertIn('scholarship_availability', data)
        self.assertEqual(len(data['universities']), 15)
        self.assertEqual(len(data['scholarships']), 6)


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity"""
    
    def setUp(self):
        self.data = load_json_data()
    
    def test_university_required_fields(self):
        """Test all universities have required fields"""
        required_fields = ['name', 'country', 'region', 'city', 'tuition_per_year', 
                          'living_per_year', 'duration_years', 'tier', 'salaries',
                          'admission_rate', 'enrollment', 'human_validated', 'last_updated',
                          'tier_override', 'tier_override_reason']
        
        for uni_key, uni_data in self.data['universities'].items():
            for field in required_fields:
                self.assertIn(field, uni_data, f"Missing field '{field}' in {uni_key}")
    
    def test_scholarship_required_fields(self):
        """Test all scholarships have required fields"""
        required_fields = ['name', 'tuition_coverage', 'living_coverage', 
                          'flights_covered', 'return_required', 'success_rate',
                          'human_validated', 'last_updated']
        
        for schol_key, schol_data in self.data['scholarships'].items():
            for field in required_fields:
                self.assertIn(field, schol_data, f"Missing field '{field}' in {schol_key}")
    
    def test_scholarship_availability_references(self):
        """Test scholarship_availability references valid scholarships"""
        for uni_key, schol_list in self.data['scholarship_availability'].items():
            self.assertIn(uni_key, self.data['universities'])
            for schol_key in schol_list:
                if schol_key != "No Scholarship (Self-fund)":
                    self.assertIn(schol_key, self.data['scholarships'])


class TestUniversityEdit(unittest.TestCase):
    """Test editing university data"""
    
    def setUp(self):
        self.data = load_json_data()
        self.original_tuition = self.data['universities']['MIT']['tuition_per_year'].copy()
    
    def tearDown(self):
        # Restore original
        self.data['universities']['MIT']['tuition_per_year'] = self.original_tuition
        save_json_data(self.data)
    
    def test_edit_university(self):
        """Test editing university data"""
        self.data['universities']['MIT']['tuition_per_year'] = {'amount': 60000, 'currency': 'USD'}
        save_json_data(self.data)
        
        reloaded = load_json_data()
        self.assertEqual(reloaded['universities']['MIT']['tuition_per_year']['amount'], 60000)


class TestScholarshipEdit(unittest.TestCase):
    """Test editing scholarship data"""
    
    def setUp(self):
        self.data = load_json_data()
        self.original_coverage = self.data['scholarships']['LPDP']['tuition_coverage']
    
    def tearDown(self):
        # Restore original
        self.data['scholarships']['LPDP']['tuition_coverage'] = self.original_coverage
        save_json_data(self.data)
    
    def test_edit_scholarship(self):
        """Test editing scholarship data"""
        self.data['scholarships']['LPDP']['tuition_coverage'] = 0.95
        save_json_data(self.data)
        
        reloaded = load_json_data()
        self.assertEqual(reloaded['scholarships']['LPDP']['tuition_coverage'], 0.95)


class TestSaveJSON(unittest.TestCase):
    """Test saving JSON data"""
    
    def test_save_and_verify(self):
        """Test saving and verifying JSON data"""
        data = load_json_data()
        test_uni = "TestUniversity"
        
        data['universities'][test_uni] = {
            "name": "Test University",
            "country": "Test",
            "region": "Europe",
            "city": "Test City",
            "tuition_per_year": {"amount": 10000, "currency": "USD"},
            "living_per_year": {"amount": 5000, "currency": "USD"},
            "duration_years": 2,
            "tier": 2,
            "urls": {"website": "", "program_page": "", "admissions": "", "curriculum": ""},
            "salaries": {"Test": 50000},
            "career_attributes": {},
            "program_focus": {},
            "qs_ranking_2026": None,
            "the_ranking_2026": None,
            "csrankings_ai_2026": None,
            "us_news_cs_2026": None,
            "admission_rate": None,
            "enrollment": None,
            "human_validated": False,
            "last_updated": "2026-03-05",
            "tier_override": False,
            "tier_override_reason": ""
        }
        
        save_json_data(data)
        reloaded = load_json_data()
        self.assertIn(test_uni, reloaded['universities'])
        
        # Cleanup
        del reloaded['universities'][test_uni]
        save_json_data(reloaded)


if __name__ == '__main__':
    unittest.main()
