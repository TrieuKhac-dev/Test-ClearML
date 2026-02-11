"""
clearml_delete_dataset.py - Script to delete a ClearML dataset by id

Usage:
    python clearml_delete_dataset.py --id <dataset_id>
"""
import argparse
from clearml import Dataset



parser = argparse.ArgumentParser(description="Delete a ClearML dataset by id or name.")
parser.add_argument('--id', help='Dataset id to delete')
parser.add_argument('--name', help='Dataset name to delete (optionally with --project)')
parser.add_argument('--project', help='Project name (used with --name)')
parser.add_argument('--yes', action='store_true', help='Delete without confirmation prompt')
parser.add_argument('--exact', action='store_true', help='Delete dataset with exact name match (default: substring match)')
args = parser.parse_args()

def delete_by_id(dataset_id):
    print(f"Deleting ClearML dataset: {dataset_id}")
    try:
        Dataset.delete(dataset_id=dataset_id, force=True)
        print(f"Dataset {dataset_id} deleted successfully.")
    except Exception as e:
        print(f"Failed to delete dataset: {e}")

def delete_by_name(name, project=None, exact=False):
    print(f"Searching for datasets with name: '{name}'" + (f", project: '{project}'" if project else "") + (", exact match" if exact else ", substring match"))
    found = []
    for ds in Dataset.list_datasets() or []:
        ds_name = ds.get('name') or ''
        ds_project = ds.get('project')
        name_match = (ds_name == name) if exact else (name in ds_name)
        if name_match and (project is None or ds_project == project):
            found.append(ds)
    if not found:
        print("No matching datasets found.")
        return
    print(f"Found {len(found)} dataset(s):")
    for ds in found:
        print(f"  - id: {ds.get('id')}, name: {ds.get('name')}, project: {ds.get('project')}, version: {ds.get('version')}")
    if not args.yes:
        confirm = input("Delete all these datasets? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Aborted.")
            return
    for ds in found:
        delete_by_id(ds.get('id'))


if args.id:
    delete_by_id(args.id)
elif args.name:
    delete_by_name(args.name, args.project, exact=args.exact)
else:
    print("You must provide either --id or --name.")
