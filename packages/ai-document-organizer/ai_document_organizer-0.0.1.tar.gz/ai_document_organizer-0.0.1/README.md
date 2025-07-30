# Document Organizer using Hugging Face

This Python script helps you organize your documents into categorized folders using a pre-trained Hugging Face zero-shot classification model. It can classify documents based on their filenames and move them into relevant categories, or flag them for manual review if confidence is low.

## Features

* **Zero-Shot Classification:** Categorizes documents without needing prior training on your specific data, leveraging the `facebook/bart-large-mnli` model.

* **Customizable Categories:** Easily define your own list of categories relevant to your document collection.

* **Filename-based Classification:** Extracts a clean title from the filename for classification, removing noise like file extensions and ISBNs.

* **Confidence Thresholding:** Documents with low classification confidence are moved to a special "Needs Manual Review" folder.

* **Dry Run Mode:** Preview the organization structure and proposed actions before any files are moved or folders are created.

* **Optional Filename Filtering:** Use regular expressions to process only specific types of files (e.g., only PDF documents).

* **GPU Acceleration (Optional):** Automatically attempts to use a CUDA-enabled GPU for faster classification if PyTorch and a compatible GPU are detected.

## Getting Started

### Prerequisites

Before running the script, ensure you have Python 3.8+ installed. You'll also need to install the necessary Python libraries.

1.  **Create a Virtual Environment (Recommended):**

    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

2.  **Install Dependencies:**

    ```
    pip install -r requirements.txt
    ```

    **`requirements.txt` content:**

    ```
    transformers
    torch # Or tensorflow, depending on your preference and GPU setup
    ```

    * **For GPU support:** If you have an NVIDIA GPU, ensure you install PyTorch with CUDA support. Visit [PyTorch's official website](https://pytorch.org/get-started/locally/) to get the exact `pip` command for your system and CUDA version (e.g., `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`).

### Usage

1.  **Place your documents:** Put all the documents you want to organize into a single folder.

2.  **Run the script:** Navigate to the `src` directory (or the directory containing `main_organizer.py`) in your terminal and run the script.

    ```
    python main_organizer.py <path_to_your_documents_folder> [OPTIONS]
    ```

    **Example (Dry Run):**

    ```
    python main_organizer.py /path/to/my/documents --dry-run
    ```

    This will show you a tree-like structure of how your files would be organized without making any changes.

    **Example (Live Run with PDF filter):**

    ```
    python main_organizer.py /path/to/my/documents --filter-regex ".*\.pdf$"
    ```

    This will classify and move only `.pdf` files.

### Command-Line Arguments

* `<target_folder>` (positional argument): The full path to the folder containing your documents. This is a mandatory argument.

* `--dry-run`: (Optional flag) If present, the script will only print the proposed organization structure and not move any files or create any folders. This is highly recommended for a first run.

* `--filter-regex <pattern>`: (Optional argument) Provide a regular expression pattern to filter the filenames. Only files matching this regex will be processed. For example, `".*\\.txt$"` to process only text files.

## Configuration

You can customize the behavior of the organizer by modifying the following constants at the top of `main_organizer.py`:

* `CANDIDATE_LABELS`: A list of strings representing the categories you want your documents to be organized into. Be as specific or general as needed for your collection.

* `MODEL_NAME`: The name of the Hugging Face model used for zero-shot classification. `facebook/bart-large-mnli` is a good general-purpose model.

* `MIN_CONFIDENCE_THRESHOLD`: A float between 0.0 and 1.0. If the model's confidence for the top predicted category is below this threshold, the document will be moved to the `_Needs Manual Review_` folder.

* `NEEDS_REVIEW_FOLDER_NAME`: The name of the folder where documents with low confidence or processing errors will be placed.

* `HYPOTHESIS_TEMPLATE`: The template string used to frame the classification query to the model. Changing this (e.g., to "This book is about {}." or "The subject of this paper is {}." ) might influence classification accuracy.

## How it Works

1.  **Initialization:** Loads the specified Hugging Face zero-shot classification model. It attempts to detect and utilize a CUDA-enabled GPU for faster processing.

2.  **Planning Phase (`plan_book_organization`):**

    * Scans the `target_folder` for files (optionally filtered by a regex).

    * For each file, it extracts a cleaned title (removing extensions, ISBNs, etc.).

    * It then uses the zero-shot classification model to determine the most likely category from your `CANDIDATE_LABELS` based on the cleaned title.

    * If the confidence score for the top category is below `MIN_CONFIDENCE_THRESHOLD`, the file is assigned to the `_Needs Manual Review_` category.

    * This phase builds an in-memory dictionary representing the proposed final organization (`{category: [filenames]}`).

3.  **Execution Phase (`_execute_dry_run_organization` or `_execute_live_run_organization`):**

    * **Dry Run:** Prints the `planned_organization` dictionary in a clear, tree-like format, showing where each file would go. No file system changes are made.

    * **Live Run:** Creates the necessary category folders (if they don't exist) and then moves each file to its designated category folder. It includes checks to prevent overwriting existing files.

## Contributing

Feel free to fork this repository, open issues, or submit pull requests to improve the script.