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
      

    def test_pseudonymize_registration(self):
        document_content = "My registration number is updated with SSOP92KR."
        anonymized_content = self.pseudonymizer.anonymize_document(document_content)
        self.assertNotIn("SSOP92KR", anonymized_content)



    def test_pseudonymize_flight_numbers(self):
        document_content = "The disruption of flight DL1234 "
        anonymized_content = self.pseudonymizer.anonymize_document(document_content)

        self.assertNotIn("DL1234", anonymized_content)



    def test_pseudonymize_contact_information(self):
        document_content = "My email is johndoe@example.com."
        anonymized_content = self.pseudonymizer.anonymize_document(document_content)

        self.assertNotIn("999-888-7777", anonymized_content)
        self.assertNotIn("johndoe@example.com", anonymized_content)



if __name__ == '__main__':
    unittest.main()
