"""
clearml_find_dataset.py - Script to search for ClearML datasets by name, project, or pattern

Usage:
    python clearml_find_dataset.py [--name <name>] [--project <project>] [--pattern <pattern>]
    Nếu không truyền tham số, sẽ in ra toàn bộ danh sách dataset.
"""
import argparse
from clearml import Dataset

parser = argparse.ArgumentParser(description="Search for ClearML datasets by id, name and/or project, with optional exact match.")
parser.add_argument('--id', help='Dataset id to search for')
parser.add_argument('--name', help='Dataset name to search for')
parser.add_argument('--project', help='Project name to search for')
parser.add_argument('--exact', action='store_true', help='Match name/project exactly (default: substring match)')
args = parser.parse_args()

# Ràng buộc: nếu có --exact thì phải có --name hoặc --project
if args.exact and not (args.name or args.project):
    parser.error('--exact requires --name and/or --project')

def match(ds):
    if args.id:
        return ds.get('id') == args.id
    ds_name = ds.get('name','')
    ds_project = ds.get('project','')
    if args.name:
        if args.exact:
            if ds_name != args.name:
                return False
        else:
            if args.name not in ds_name:
                return False
    if args.project:
        if args.exact:
            if ds_project != args.project:
                return False
        else:
            if args.project not in ds_project:
                return False
    return True



all_ds = Dataset.list_datasets() or []
if not (args.id or args.name or args.project):
    # Nếu không truyền tham số, in toàn bộ danh sách
    print(f"Found {len(all_ds)} dataset(s):")
    for ds in all_ds:
        print(f"  - id: {ds.get('id')}, name: {ds.get('name')}, project: {ds.get('project')}, version: {ds.get('version')}")
else:
    results = [ds for ds in all_ds if match(ds)]
    if not results:
        print("No matching datasets found.")
    else:
        print(f"Found {len(results)} dataset(s):")
        for ds in results:
            print(f"  - id: {ds.get('id')}, name: {ds.get('name')}, project: {ds.get('project')}, version: {ds.get('version')}")
