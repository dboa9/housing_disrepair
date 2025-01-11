"""
File: photo-renamer.py
Location: /housing_disrepair/photo-renamer.py
Description: Script to rename photos with consistent naming convention and generate file list
"""

import argparse
import os
from datetime import datetime


class PathHandler:
    def __init__(self):
        self.invalid_chars = '<>:"/\\|?*'
        
    def sanitize_path(self, path):
        """Sanitize the file path by preserving path structure"""
        parts = path.split(os.sep)
        sanitized_parts = []
        for part in parts:
            sanitized = part
            for char in self.invalid_chars:
                if char not in ('/', '\\'):
                    sanitized = sanitized.replace(char, '')
            sanitized_parts.append(sanitized)
        return os.sep.join(sanitized_parts)

    def create_directory(self, directory):
        """Create directory if it doesn't exist"""
        if not os.path.exists(directory):
            os.makedirs(directory)

class PhotoRenamer:
    def __init__(self):
        self.path_handler = PathHandler()
        self.renamed_files = []

    def get_prefix_input(self):
        """Get custom prefix from user input"""
        return input("Enter prefix for filenames (e.g., 'DUMPED RUBBISH'): ").strip()

    def write_file_list(self, directory, prefix):
        """Write list of renamed files to a text file"""
        output_file = os.path.join(directory, f"{prefix}_renamed_files.txt")
        with open(output_file, 'w') as f:
            f.write("Renamed Files:\n")
            f.write("-" * 50 + "\n")
            for _, new_name in self.renamed_files:
                f.write(f"{new_name}\n")
        print(f"\nFile list written to: {output_file}")

    def rename_photos(self, directory, test_mode=True):
        """
        Rename photos in specified directory with timestamp and index
        Args:
            directory (str): Path to directory containing photos
            test_mode (bool): If True, only process first 5 files
        """
        try:
            # Handle WSL paths correctly
            if directory.startswith('/mnt/'):
                normalized_path = directory
            else:
                normalized_path = os.path.normpath(directory)
                normalized_path = self.path_handler.sanitize_path(normalized_path)
            
            directory = normalized_path
            
            if not os.path.exists(directory):
                raise ValueError(f"Directory does not exist: {directory}")

            # Get list of image files
            image_files = [f for f in os.listdir(directory) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if not image_files:
                print(f"No image files found in {directory}")
                return

            # Sort files and limit to 5 if in test mode
            image_files = sorted(image_files)
            if test_mode:
                image_files = image_files[:5]

            # Get custom prefix
            prefix = self.get_prefix_input()
            
            # Create backup directory
            backup_dir = os.path.join(directory, "originals")
            self.path_handler.create_directory(backup_dir)

            # Process each image
            self.renamed_files = []
            for i, filename in enumerate(image_files, 1):
                old_path = os.path.join(directory, filename)
                
                # Get file creation time
                creation_time = os.path.getctime(old_path)
                timestamp = datetime.fromtimestamp(creation_time)
                
                # Generate new filename with prefix
                extension = os.path.splitext(filename)[1].lower()
                new_filename = f"{prefix}_{timestamp.strftime('%Y_%m_%d_%H_%M_%S')}_image_no_{i:03d}{extension}"
                new_path = os.path.join(directory, new_filename)

                # Backup original file
                backup_path = os.path.join(backup_dir, filename)
                os.rename(old_path, backup_path)
                
                # Create renamed copy
                with open(backup_path, 'rb') as src, open(new_path, 'wb') as dst:
                    dst.write(src.read())
                
                self.renamed_files.append((filename, new_filename))
                print(f"Renamed: {filename} -> {new_filename}")

            # Write file list
            self.write_file_list(directory, prefix)

            if test_mode and len(image_files) >= 5:
                response = input("\nWould you like to rename all files in the directory? (y/n): ").lower()
                if response == 'y':
                    print("\nProcessing entire directory...")
                    self.rename_photos(directory, test_mode=False)

        except Exception as e:
            print(f"Error processing directory: {str(e)}")
            raise

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Rename photos with timestamp and index')
    parser.add_argument('--directory', required=True, 
                      help='Directory containing photos to rename')
    return parser.parse_args()

def main():
    """Main function"""
    args = parse_arguments()
    renamer = PhotoRenamer()
    renamer.rename_photos(args.directory)

if __name__ == "__main__":
    main()