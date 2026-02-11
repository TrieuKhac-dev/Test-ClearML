"""
clearml_upload_dataset.py
Upload a local file or folder as a ClearML dataset, with optional parent for versioning.

Usage:
    python clearml_upload_dataset.py --project "Project Name" --name "Dataset Name" --folder path/to/folder
    python clearml_upload_dataset.py --project "Project Name" --name "Dataset Name" --file path/to/file
    python clearml_upload_dataset.py --project "Project Name" --name "Dataset Name" --file path/to/file --parent <parent_dataset_id>
"""

import argparse
import os
from clearml import Dataset

def main():
    parser = argparse.ArgumentParser(description="Upload a local folder or file as a ClearML dataset.")
    parser.add_argument('--project', required=True, help='ClearML project name')
    parser.add_argument('--name', required=True, help='Dataset name')
    parser.add_argument('--folder', help='Path to local data folder')
    parser.add_argument('--file', help='Path to a single file to upload')
    parser.add_argument('--parent', help='Parent dataset id (for versioning, diff/delta)')
    args = parser.parse_args()

    if not args.folder and not args.file:
        raise ValueError("You must provide either --folder or --file.")

    # Create dataset, with parent if provided
    if args.parent:
        print(f"Creating ClearML dataset: project='{args.project}', name='{args.name}', parent='{args.parent}'")
        dataset = Dataset.create(dataset_project=args.project, dataset_name=args.name, parent_datasets=[args.parent])
    else:
        print(f"Creating ClearML dataset: project='{args.project}', name='{args.name}'")
        dataset = Dataset.create(dataset_project=args.project, dataset_name=args.name)

    # Add file or folder
    if args.file:
        if not os.path.isfile(args.file):
            raise FileNotFoundError(f"File not found: {args.file}")
        print(f"Adding file: {args.file}")
        dataset.add_files(path=args.file)
    elif args.folder:
        if not os.path.isdir(args.folder):
            raise NotADirectoryError(f"Folder not found: {args.folder}")
        print(f"Adding files from: {args.folder}")
        dataset.add_files(path=args.folder)

    print("Uploading dataset to ClearML server...")
    dataset.upload()

    print("Finalizing dataset...")
    dataset.finalize()

    print(f"Done! Dataset id: {dataset.id}")
    print("You can now use this dataset id in your training scripts.")

if __name__ == "__main__":
    main()
