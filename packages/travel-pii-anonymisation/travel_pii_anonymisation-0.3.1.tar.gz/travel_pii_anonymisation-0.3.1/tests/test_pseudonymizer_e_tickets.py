import sys
from pathlib import Path
src_path = Path(__file__).parent.parent / 'src/tspii/tools/'
sys.path.append(str(src_path))
import unittest
from pseudonymizer import CustomAnonymizer

class TestTravelSpecificPIIPseudonymization(unittest.TestCase):
    
    def setUp(self):
        # Initialize the CustomPseudonymizer before each test
        self.pseudonymizer   = CustomAnonymizer(add_default_faker_operators=False)
    
    # Add custom recognizers and fake data generators
        self.pseudonymizer.add_custom_recognizers()
        self.pseudonymizer.add_custom_fake_data_generators()
        
    
    def test_pseudonymize_e_ticket(self):
        document_content = "My e-ticket number is 123-4567890123."
        anonymized_content = self.pseudonymizer.anonymize_document(document_content)
        self.assertNotIn("123-4567890123", anonymized_content)
        
    def test_pseudonymize_e_ticket_(self):
        document_content = "My e-ticket number is 123-3049203039."
        anonymized_content = self.pseudonymizer.anonymize_document(document_content)
        self.assertNotIn("123-3049203039", anonymized_content)


if __name__ == '__main__':
    unittest.main()
