import argparse
import os
import re
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

class MediaRenamer:
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

    def is_already_renamed(self, filename, prefix):
        """Check if a file is already renamed in the correct format"""
        pattern = re.compile(rf"{re.escape(prefix)}_\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}")
        return bool(pattern.search(filename))

    def rename_media(self, directory, test_mode=True):
        """
        Rename media files in specified directory with timestamp and index
        Args:
            directory (str): Path to directory containing media files
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

            # Get list of media files in the main directory only
            media_files = [f for f in os.listdir(directory) 
                           if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4'))]
            
            if not media_files:
                print(f"No media files found in {directory}")
                return

            # Sort files and limit to 5 if in test mode
            media_files = sorted(media_files)
            if test_mode:
                media_files = media_files[:5]

            # Get custom prefix
            prefix = self.get_prefix_input()
            
            # Create backup directory
            backup_dir = os.path.join(directory, "originals")
            self.path_handler.create_directory(backup_dir)

            # Move files to backup directory first
            for filename in media_files:
                old_path = os.path.join(directory, filename)
                backup_path = os.path.join(backup_dir, filename)
                if not os.path.exists(backup_path):
                    os.rename(old_path, backup_path)

            # Get updated list of moved files
            moved_files = [f for f in os.listdir(backup_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4'))]

            # Process each moved file
            self.renamed_files = []
            for i, filename in enumerate(moved_files, 1):
                backup_path = os.path.join(backup_dir, filename)

                # Skip files that are already renamed
                if self.is_already_renamed(filename, prefix):
                    print(f"Skipping already renamed file: {filename}")
                    continue
                
                # Step 1: Attempt to extract timestamp from filename
                timestamp_match = re.search(r'(\d{8})_(\d{6})|(\d{4})-(\d{2})-(\d{2})', filename)
                if timestamp_match:
                    if timestamp_match.group(1):  # YYYYMMDD_HHMMSS
                        date_part, time_part = timestamp_match.groups()[0:2]
                        formatted_timestamp = f"{date_part[:4]}_{date_part[4:6]}_{date_part[6:]}_{time_part[:2]}_{time_part[2:4]}_{time_part[4:]}"
                    elif timestamp_match.group(3):  # YYYY-MM-DD
                        year, month, day = timestamp_match.groups()[2:5]
                        formatted_timestamp = f"{year}_{month}_{day}_00_00_00"  # Default time to 00:00:00
                else:
                    # Fallback to file creation time
                    creation_time = os.path.getctime(backup_path)
                    timestamp = datetime.fromtimestamp(creation_time)
                    formatted_timestamp = timestamp.strftime('%Y_%m_%d_%H_%M_%S')

                # Step 2: Generate new filename with prefix
                extension = os.path.splitext(filename)[1].lower()
                unique_id = f"_file_no_{i:03d}"
                new_filename = f"{prefix}_{formatted_timestamp}{unique_id}{extension}"
                new_path = os.path.join(directory, new_filename)

                # Rename file in the originals directory
                os.rename(backup_path, new_path)
                self.renamed_files.append((filename, new_filename))
                print(f"Renamed: {filename} -> {new_filename}")

            # Write file list
            self.write_file_list(directory, prefix)

            if test_mode and len(media_files) >= 5:
                response = input("\nWould you like to rename all files in the directory? (y/n): ").lower()
                if response == 'y':
                    print("\nProcessing entire directory...")
                    self.rename_media(directory, test_mode=False)

        except Exception as e:
            print(f"Error processing directory: {str(e)}")
            raise

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Rename media files with timestamp and index')
    parser.add_argument('--directory', required=True, 
                        help='Directory containing media files to rename')
    return parser.parse_args()

def main():
    """Main function"""
    args = parse_arguments()
    renamer = MediaRenamer()
    renamer.rename_media(args.directory)

if __name__ == "__main__":
    main()
