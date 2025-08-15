import os
import sys
import argparse

def rename_notebooks(directory, target_directory=None):
    """
    Rename Jupyter notebooks from a directory following a specific naming convention.
    
    Args:
        directory (str): Source directory containing the notebooks
        target_directory (str): Target directory for renamed notebooks. If None, creates a "_renamed" subdirectory
    
    Returns:
        tuple: (list of renamed files, target_directory path)
    """
    # Store the renaming results
    renamed_files = []
    
    # If no target directory specified, create one based on source directory
    if target_directory is None:
        target_directory = f"{directory}_renamed"
    
    # Check if the target directory exists, if not create it
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Created target directory: {target_directory}")

    # Check if source directory exists
    if not os.path.exists(directory):
        print(f"Error: Source directory '{directory}' does not exist.")
        return [], target_directory

    # Get list of notebook files
    notebook_files = [f for f in os.listdir(directory) if f.endswith(".ipynb")]
    
    if not notebook_files:
        print(f"No Jupyter notebooks found in '{directory}'")
        return [], target_directory
    
    print(f"Found {len(notebook_files)} notebook(s) in '{directory}'")

    # Iterate over all notebook files
    for filename in notebook_files:
        print(f"Processing: {filename}")
        
        # Split the filename on the dash and strip any leading/trailing spaces
        parts = filename.split(" - ")
        
        if len(parts) >= 3:  # Check if the filename format is correct
            person_name = parts[1].strip()
            
            # Split the person name into first and last names
            name_parts = person_name.split()
            
            if len(name_parts) >= 2:  # Ensure we have at least first and last name
                # Create new name: Last_First or Last_First_Middle
                new_name = f"{name_parts[-1]}_{name_parts[0]}"
                if len(name_parts) > 2:
                    # Add middle names/initials
                    for middle in name_parts[1:-1]:
                        new_name += f"_{middle}"
                
                new_filename = f"{new_name}.ipynb"
                old_file_path = os.path.join(directory, filename)
                new_file_path = os.path.join(target_directory, new_filename)
                
                try:
                    # Copy the file to new location with new name
                    import shutil
                    shutil.copy2(old_file_path, new_file_path)
                    renamed_files.append((filename, new_filename))
                    print(f"  ✓ Renamed '{filename}' to '{new_filename}'")
                except Exception as e:
                    print(f"  ✗ Error renaming '{filename}': {e}")
            else:
                print(f"  ✗ Could not parse name from: {person_name}")
        else:
            print(f"  ✗ Filename format is incorrect for file: {filename}")
            print(f"      Expected format: 'Something - FirstName LastName - Something.ipynb'")
    
    print(f"\nRenaming complete!")
    print(f"Successfully renamed {len(renamed_files)} file(s)")
    print(f"Renamed files saved to: {target_directory}")
    
    return renamed_files, target_directory

def main():
    """
    Main function to handle command line arguments and user input.
    """
    parser = argparse.ArgumentParser(
        description="Rename Jupyter notebooks following LastName_FirstName convention",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rename_notebooks.py                          # Interactive mode
  python rename_notebooks.py Homework/HW01           # Specify source directory
  python rename_notebooks.py Homework/HW01 --target Homework/HW01_graded
        """
    )
    
    parser.add_argument('source_directory', nargs='?', 
                       help='Source directory containing notebooks to rename')
    parser.add_argument('--target', '-t', dest='target_directory',
                       help='Target directory for renamed notebooks (optional)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Force interactive mode even if source directory is provided')
    
    args = parser.parse_args()
    
    # Determine source directory
    source_directory = args.source_directory
    
    # Interactive mode if no directory provided or explicitly requested
    if source_directory is None or args.interactive:
        print("=== Jupyter Notebook Renaming Tool ===")
        print("This tool renames notebooks from 'Format - FirstName LastName - Format.ipynb'")
        print("to 'LastName_FirstName.ipynb' format.\n")
        
        while True:
            source_directory = input("Enter the path to the folder containing notebooks: ").strip()
            if source_directory:
                # Handle quoted paths
                source_directory = source_directory.strip('"\'')
                break
            print("Please enter a valid directory path.")
        
        # Ask for target directory if not provided
        if not args.target_directory:
            target_input = input(f"Enter target directory (press Enter for '{source_directory}_renamed'): ").strip()
            target_directory = target_input.strip('"\'') if target_input else None
        else:
            target_directory = args.target_directory
    else:
        target_directory = args.target_directory
    
    # Perform the renaming
    print(f"\nProcessing notebooks in: {source_directory}")
    if target_directory:
        print(f"Target directory: {target_directory}")
    
    renamed_files, final_target_directory = rename_notebooks(source_directory, target_directory)
    
    if renamed_files:
        print(f"\n=== Summary ===")
        print(f"Source directory: {source_directory}")
        print(f"Target directory: {final_target_directory}")
        print(f"Files renamed: {len(renamed_files)}")
        
        # Show renamed files
        print(f"\nRenamed files:")
        for old_name, new_name in renamed_files:
            print(f"  {old_name} → {new_name}")
        
        # Ask if user wants to proceed with grading
        print(f"\n=== Next Steps ===")
        print(f"To grade these notebooks, run:")
        print(f"python notebook_grader.py '{final_target_directory}' grades.csv")
        
        proceed = input("\nWould you like to proceed with grading now? (y/n): ").strip().lower()
        if proceed in ['y', 'yes']:
            try:
                from notebook_grader import process_student_notebooks
                output_csv = input("Enter output CSV filename (or press Enter for 'grades.csv'): ").strip()
                if not output_csv:
                    output_csv = 'grades.csv'
                
                print(f"\nStarting grading process...")
                process_student_notebooks(final_target_directory, output_csv)
                
            except ImportError:
                print("notebook_grader.py not found in the same directory.")
                print(f"Please run: python notebook_grader.py '{final_target_directory}' grades.csv")
            except Exception as e:
                print(f"Error during grading: {e}")
                print(f"Please run manually: python notebook_grader.py '{final_target_directory}' grades.csv")
    
    return final_target_directory

if __name__ == "__main__":
    main()