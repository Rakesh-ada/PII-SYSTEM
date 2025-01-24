import re
from presidio_analyzer import AnalyzerEngine

def extract_name_with_presidio(text):
    """Extract Name using Presidio."""
    try:
        # Initialize the Presidio Analyzer
        analyzer = AnalyzerEngine()

        # Analyze the text to find a PERSON entity (name)
        results = analyzer.analyze(text=text, entities=["PERSON"], language="en")
        
        # If a name is found, return the first result's text (access from the text passed in)
        if results:
            # Extract the text using the start and end indices and remove any '\n' characters
            name = text[results[0].start:results[0].end]
            name_cleaned = name.split("\n")[0].strip()  # Remove anything after a newline and strip extra spaces
            return name_cleaned
        else:
            return None
    except Exception as e:
        print(f"Error extracting name with Presidio: {e}")
        return None
def detect_dob_with_regex(text):
    """Detect Date of Birth (DOB) using regular expressions."""
    try:
        # Regex pattern for detecting Date of Birth in formats like DD/MM/YYYY or MM/DD/YYYY
        # This will match both colon (:) and semicolon (;) after 'Date of Birth' or 'DOB'
        dob_pattern = r"(?:Date of Birth|DOB)[\s:;]*([\d]{2}/[\d]{2}/[\d]{4})"
        
        # Find all matches
        dob_matches = re.finditer(dob_pattern, text)
        dob_data = [
            {
                "entity": "DOB",
                "start": match.start(),
                "end": match.end(),
                "text": match.group(1)  # Extract the date part (DD/MM/YYYY)
            }
            for match in dob_matches
        ]
        return dob_data

    except Exception as e:
        print(f"Error detecting DOB with regex: {e}")
        return []

def detect_pii(text):
    """Detect PII (Name, DOB, Aadhaar Number, Gender, Address) using rule-based patterns and Presidio for Name and DOB."""
    try:
        # Define patterns for Aadhaar number, VID, Gender, and Address
        aadhar_pattern = r"\b\d{4} \d{4} \d{4}\b"  # Aadhaar number format: XXXX XXXX XXXX
        vid_pattern = r"\b\d{4} \d{4} \d{4} \d{4}\b"  # Virtual ID format: XXXX XXXX XXXX XXXX
        gender_pattern = r"\b(Female|Male|Other)\b"  # Matches Gender keywords: Female, Male, Other
        address_pattern = r"([A-Za-z\s,]+)\s-\s(\d{6})"  # Matches "Address: ..." or multiline addresses

        # Detect Aadhaar numbers
        aadhar_matches = re.finditer(aadhar_pattern, text)
        aadhar_data = [
            {
                "entity": "UID",
                "start": match.start(),
                "end": match.end(),
                "text": match.group()
            }
            for match in aadhar_matches
        ]

        # Detect VID numbers
        vid_matches = re.finditer(vid_pattern, text)
        vid_numbers = [match.group() for match in vid_matches]

        # Remove Aadhaar numbers if their first 4 characters match any VID's first 4 characters
        vid_first_4 = {vid[:4] for vid in vid_numbers}
        aadhar_data = [
            entry for entry in aadhar_data if entry["text"][:4] not in vid_first_4
        ]

        # Remove duplicate Aadhaar numbers, keeping only the first one found
        seen_aadhaar = set()
        aadhar_data = [
            entry for entry in aadhar_data if entry["text"] not in seen_aadhaar and not seen_aadhaar.add(entry["text"])
        ]

        # Extract Name using Presidio
        name_data = []
        name = extract_name_with_presidio(text)
        if name:
            name_data = [
                {
                    "entity": "NAME",
                    "start": text.find(name),
                    "end": text.find(name) + len(name),
                    "text": name
                }
            ]

         # Detect Date of Birth using regex
        dob_data = detect_dob_with_regex(text)

        # Detect Gender
        gender_matches = re.finditer(gender_pattern, text, re.IGNORECASE)
        gender_data = [
            {
                "entity": "GENDER",
                "start": match.start(),
                "end": match.end(),
                "text": match.group()
            }
            for match in gender_matches
        ]

        # Standardize the gender value to "Male" for all variations (e.g., "MALE", "male")
        standardized_gender = None
        for gender in gender_data:
            if gender["text"].lower() == "male":
                standardized_gender = {
                    "entity": "GENDER",
                    "start": gender["start"],
                    "end": gender["end"],
                    "text": "Male"
                }
                break

        if standardized_gender:
            gender_data = [standardized_gender]  # Replace all gender entries with the standardized one

        # Detect Address (find a block of text following "Address" or similar keywords)
        address_matches = re.finditer(address_pattern, text, re.MULTILINE)
        address_data = [
            {
                "entity": "ADDRESS",
                "start": match.start(),
                "end": match.end(),
                "text": match.group(1).strip(),
                "pin_code": match.group(2)  # Extract the pin code
            }
            for match in address_matches
        ]

        # Combine all the results
        pii_data = name_data + aadhar_data + dob_data + gender_data
        return pii_data

    except Exception as e:
        print(f"Error detecting PII: {e}")
        return []

# Example Usage
if __name__ == "__main__":
    # Example text extracted from an Aadhaar card image
    sample_text = """
    Government of India

    Rakesh Adak
    Date of Birth: 29/08/2005
    Male/ MALE

    2845 8687 1313
    2845 8687 1313

    Address:
    123 Main Street,
    Some City,
    Some State - 123456
    """
    pii_results = detect_pii(sample_text)
    print("PII detected in Image:")
    for pii in pii_results:
        print(pii)
