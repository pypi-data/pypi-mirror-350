import sys
import os
import shutil
import re
import argparse # Import argparse for command-line arguments
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from typing import List, Dict, Any, Tuple, Optional

# --- Configuration ---
# You can adjust these categories based on your book collection
CANDIDATE_LABELS = [
    # Technical Categories
    "Software Engineering", "Software Architecture", "Programming Languages", "Algorithms & Data Structures",
    "Cloud Computing", "AWS", "Kubernetes", "DevOps", "Site Reliability Engineering (SRE)",
    "Data Science", "Machine Learning", "Artificial Intelligence (AI)", "Big Data", "Data Engineering",
    "Distributed Systems", "Microservices", "Networking", "Operating Systems", "Databases",
    "Security", "Cybersecurity", "Information Security", "Go (Golang)", "Python", "Rust", "JavaScript",
    "Web Development", "API Design", "System Design", "Computer Science", "IT Certifications",
    "System Administration", "Industrial Engineering", "Materials Engineering", "Electrical Engineering",
    "Civil Engineering", "Mechanical Engineering",

    # General Non-Fiction Categories
    "Psychology", "Personal Development", "Communication Skills", "Management & Leadership",
    "Business", "Economics", "History", "Science", "Biology", "Physics", "Chemistry",
    "Mathematics", "Philosophy", "Health & Wellness", "Religion & Spirituality", "True Crime",
    "Memoir", "Biography", "Autobiography", "Travel", "Cookbooks", "Food & Drink", "Parenting",
    "Education & Teaching", "Art & Photography", "DIY & Hobbies", "Journalism", "Political Science",
    "Essays", "How-To Guides", "Personal Finance", "Relationships",

    # Fiction Categories
    "Fiction", "Fantasy", "Science Fiction", "Romance", "Mystery", "Thriller", "Horror",
    "Action & Adventure", "Historical Fiction", "Literary Fiction", "Young Adult",
    "Children's Literature", "Dystopian", "Magical Realism", "Contemporary Fiction",
    "Paranormal", "Classics", "Graphic Novels", "Poetry", "Humor"
]

# Model for classification
MODEL_NAME = "facebook/bart-large-mnli"
# Confidence threshold: if the top score is below this, move to "Needs Manual Review"
MIN_CONFIDENCE_THRESHOLD = 0.50 # Adjust as needed (e.g., 0.6, 0.7)
NEEDS_REVIEW_FOLDER_NAME = "_Needs Manual Review_"
HYPOTHESIS_TEMPLATE = "This document belongs to the category of {}." # New top-level constant

def extract_title_from_filename(filename: str) -> str:
    """
    Extracts a cleaner title from the filename by removing the extension and common trailing identifiers like ISBNs.
    Example: "My Awesome Book-9781234567890.pdf" -> "My Awesome Book"
    Example: "Another Document.docx" -> "Another Document"
    """
    name_without_ext = os.path.splitext(filename)[0]
    
    # Regex to remove common trailing patterns:
    # - ISBNs (e.g., -978XXXXXXXXXX, _978XXXXXXXXXX)
    # - Common versioning/edition info (e.g., v1.0, Vol 1, 2nd Ed)
    # This regex is designed to be somewhat aggressive, adjust as needed.
    cleaned_title = re.sub(r'[-_]?\b(?:97[89]\d{10}|v\d+\.\d+|Vol\s*\d+|\d+(?:st|nd|rd|th)?\s*Ed(?:ition)?)\b.*$', '', name_without_ext, flags=re.IGNORECASE).strip()
    
    # If the aggressive cleaning results in an empty string, fall back to just removing extension
    if not cleaned_title:
        return name_without_ext.strip()
        
    return cleaned_title

def load_classifier_model() -> Any:
    """
    Loads the Hugging Face zero-shot classification model.
    Attempts to use GPU if available, otherwise falls back to CPU.
    Returns the classifier pipeline or None if an error occurs.
    """
    print(f"Loading classification model '{MODEL_NAME}'. This may take a while on the first run...")

    device = -1  # Default to CPU
    device_info = "CPU"

    try:
        import torch
        if torch.cuda.is_available():
            device = 0  # Use the first GPU
            device_info = "CUDA GPU"
    except ImportError:
        print("Warning: PyTorch is not installed. Install with 'pip install torch' for GPU acceleration.")
        # device remains -1 (CPU)
        device_info = "CPU (PyTorch not found)"
    except Exception as e:
        print(f"Warning: Could not check for GPU availability due to an error: {e}. Defaulting to CPU.")
        # device remains -1 (CPU)
        device_info = "CPU (GPU check failed)"

    print(f"{device_info} detected. Using {device_info} for classification.")

    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer, device=device)
        print("Model loaded successfully.")
        return classifier
    except Exception as e:
        print(f"Error loading the Hugging Face model: {e}")
        print("Please ensure you have an internet connection and the 'transformers' library is installed correctly.")
        print("You might need to install PyTorch or TensorFlow as well: pip install torch (or tensorflow)")
        return None

def plan_book_organization(
    folder_path: str,
    categories: List[str],
    min_confidence: float,
    classifier: Any,
    filename_regex: Optional[str] = None # New optional argument for regex filter
) -> Dict[str, List[str]]:
    """
    Plans the organization of files. It classifies each file and determines
    its intended destination, returning a dictionary where keys are categories
    and values are lists of filenames belonging to that category.
    No file system operations are performed in this function.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return {}

    # Initialize the structure with the 'Needs Manual Review' category
    organized_structure: Dict[str, List[str]] = {NEEDS_REVIEW_FOLDER_NAME: []}
    for category in categories:
        organized_structure[category] = []

    print(f"\nScanning folder: {folder_path}")

    # Compile regex if provided
    compiled_regex = None
    if filename_regex:
        try:
            compiled_regex = re.compile(filename_regex)
            print(f"  Applying filename filter regex: '{filename_regex}'")
        except re.error as e:
            print(f"Error: Invalid regex pattern '{filename_regex}': {e}. Skipping regex filter.")
            compiled_regex = None


    for filename in os.listdir(folder_path):
        source_file_path = os.path.join(folder_path, filename)

        # Skip if it's not a file (e.g., it's a directory)
        if not os.path.isfile(source_file_path):
            continue
        
        # Apply filename regex filter if provided
        if compiled_regex and not compiled_regex.search(filename):
            print(f"Skipping '{filename}': Does not match filename filter regex.")
            continue

        # Check if the file is already in a subfolder that is one of our categories
        # This prevents re-processing files that are already organized
        parent_dir_name = os.path.basename(os.path.dirname(source_file_path))
        if parent_dir_name in categories or parent_dir_name == NEEDS_REVIEW_FOLDER_NAME:
            print(f"Skipping '{filename}': already appears to be in a category folder '{parent_dir_name}'.")
            continue

        print(f"\nProcessing '{filename}'...")
        # Use the cleaned title for classification
        file_title_for_classification = extract_title_from_filename(filename)
        print(f"  Using cleaned title for classification: '{file_title_for_classification}'")

        try:
            # Classify the file title with an improved hypothesis template
            classification = classifier(file_title_for_classification, categories, hypothesis_template=HYPOTHESIS_TEMPLATE)

            top_category_label = classification['labels'][0]
            confidence_score = classification['scores'][0]

            chosen_category_folder_name: str

            chosen_category_folder_name = top_category_label if confidence_score >= min_confidence else NEEDS_REVIEW_FOLDER_NAME
            print(f"  Classified as: '{top_category_label}' (Confidence: {confidence_score:.2f}). Target folder: '{chosen_category_folder_name}'")
            
            # Add the filename to the determined category list
            organized_structure[chosen_category_folder_name].append(filename)

        except Exception as e:
            print(f"  Error processing file '{filename}': {e}. Adding to '{NEEDS_REVIEW_FOLDER_NAME}'.")
            organized_structure[NEEDS_REVIEW_FOLDER_NAME].append(filename)
    
    return organized_structure

def _execute_dry_run_organization(
    folder_path: str,
    organized_structure: Dict[str, List[str]]
) -> int:
    """
    Executes the dry run logic for file organization.
    Prints the proposed organization structure in a tree-like view.
    Returns the count of proposed moves/folder creations.
    """
    print("\n--- DRY RUN MODE ENABLED: No files will be moved or folders created. ---")
    print("\nProposed Organization Structure (Tree View):")
    dry_run_actions_count = 0
    for category, filenames in organized_structure.items():
        if filenames:
            print(f"\n├── {category}/")
            for filename in filenames:
                print(f"│   └── {filename}")
                # Re-evaluate actions_performed for dry run based on potential moves
                source_file_path = os.path.join(folder_path, filename)
                destination_file_path = os.path.join(folder_path, category, filename)
                
                if os.path.abspath(source_file_path) != os.path.abspath(destination_file_path) and \
                   not os.path.exists(destination_file_path):
                    dry_run_actions_count += 1
                    
    return dry_run_actions_count

def _execute_live_run_organization(
    folder_path: str,
    organized_structure: Dict[str, List[str]]
) -> int:
    """
    Executes the live run logic for file organization.
    Performs actual file system operations (creating folders, moving files).
    Returns the count of successfully moved files/ensured folders.
    """
    print("\n--- LIVE RUN MODE ENABLED: Files will be moved and folders created. ---")
    os.makedirs(os.path.join(folder_path, NEEDS_REVIEW_FOLDER_NAME), exist_ok=True) # Ensure review folder exists

    actions_performed = 0
    for category, filenames in organized_structure.items():
        if not filenames:
            continue

        print(f"\nProcessing Category: '{category}'")
        category_path = os.path.join(folder_path, category)
        os.makedirs(category_path, exist_ok=True) # Ensure category folder exists

        for filename in filenames:
            source_file_path = os.path.join(folder_path, filename)
            destination_file_path = os.path.join(category_path, filename)

            if not os.path.exists(source_file_path):
                print(f"  Skipping '{filename}': Source file not found at '{source_file_path}'.")
            elif os.path.abspath(source_file_path) == os.path.abspath(destination_file_path):
                print(f"  File '{filename}' is already in the target folder '{category}'. Skipping move.")
            elif os.path.exists(destination_file_path):
                print(f"  Warning: File '{filename}' already exists in '{category}'. Skipping move to avoid overwrite.")
            else:
                try:
                    shutil.move(source_file_path, destination_file_path)
                    print(f"  Moved '{filename}' to: '{category_path}'")
                    actions_performed += 1
                except Exception as e:
                    print(f"  Error moving '{filename}' to '{category_path}': {e}")
    return actions_performed

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:] # Use actual command-line arguments if none provided

    parser = argparse.ArgumentParser(description="Organize documents using Hugging Face zero-shot classification.")
    parser.add_argument("target_folder", help="The full path to the folder containing your documents.")
    parser.add_argument("--dry-run", action="store_true", help="Run in DRY RUN mode (show actions, no changes).")
    parser.add_argument("--filter-regex", type=str, help="Optional: A regular expression to filter filenames (e.g., '.*\\.pdf$' to process only PDF files).")
    
    args = parser.parse_args(argv)

    target_folder = args.target_folder
    is_dry_run = args.dry_run
    filename_filter_regex = args.filter_regex

    print("--- Document Organizer using Hugging Face ---")
    
    if not os.path.isdir(target_folder):
        print(f"Invalid folder path: '{target_folder}'. Please provide a valid directory.")
    else:
        print(f"\nCategories that will be used:")
        # Print categories as a simple comma-separated list
        print(f"  {', '.join(CANDIDATE_LABELS)}")
            
        print(f"Documents with classification confidence below {MIN_CONFIDENCE_THRESHOLD*100:.0f}% will be moved to '{NEEDS_REVIEW_FOLDER_NAME}'.")
        
        # Load the classifier model once
        classifier_model = load_classifier_model()
        if classifier_model is None:
            exit() # Exit if model loading failed

        print(f"\nPlanning organization for documents in '{os.path.abspath(target_folder)}'...")
        # Pass the filename_regex to the planning function
        planned_organization = plan_book_organization(
            target_folder, CANDIDATE_LABELS, MIN_CONFIDENCE_THRESHOLD, classifier_model, filename_regex=filename_filter_regex
        )

        print(f"\nExecuting organization for documents in '{os.path.abspath(target_folder)}'...")
        
        files_processed = sum(len(files) for files in planned_organization.values())
        actions_performed = 0

        if is_dry_run:
            actions_performed = _execute_dry_run_organization(target_folder, planned_organization)
        else:
            actions_performed = _execute_live_run_organization(target_folder, planned_organization)
        
        print(f"\n--- Organization Complete ({'DRY RUN' if is_dry_run else 'LIVE RUN'}) ---")
        print(f"Total files considered for processing: {files_processed} actions: {actions_performed}")



if __name__ == "__main__":
    main()