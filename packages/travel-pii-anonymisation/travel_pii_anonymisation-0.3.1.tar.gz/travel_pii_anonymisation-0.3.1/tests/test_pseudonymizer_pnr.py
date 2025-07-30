
import sys
from pathlib import Path
src_path = Path(__file__).parent.parent / 'src/tspii/tools'
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
        
        
    def test_pseudonymize_pnr(self):
        document_content = "My PNR is LHKQK9."
        anonymized_content = self.pseudonymizer.anonymize_document(document_content)
        self.assertNotIn("LHKQK9", anonymized_content)
    
    def test_pseudonymize_pnr_(self):
        document_content = "My PNR is POOWK2."
        anonymized_content = self.pseudonymizer.anonymize_document(document_content)
        self.assertNotIn("POOWK2", anonymized_content)



if __name__ == '__main__':
    unittest.main()
