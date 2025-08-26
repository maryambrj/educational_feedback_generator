#!/usr/bin/env python3
"""
CLI tool for managing student ID anonymization and mappings
"""

import argparse
import getpass
import sys
import os
from pathlib import Path
from student_id_manager import StudentIDManager

def create_anonymous_grading_session(args):
    """Initialize a new anonymous grading session"""
    print(f"🎯 Creating Anonymous Grading Session: {args.assignment_id}")
    print("=" * 60)
    
    # Create ID manager
    id_manager = StudentIDManager(args.mapping_dir)
    
    # Get notebook directory
    notebooks_dir = Path(args.notebooks_dir)
    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return 1
    
    # Find all notebook files
    notebook_files = list(notebooks_dir.glob("*.ipynb"))
    if not notebook_files:
        print(f"❌ No notebook files found in: {notebooks_dir}")
        return 1
    
    print(f"📚 Found {len(notebook_files)} notebooks")
    
    # Generate anonymous IDs for all students
    student_mappings = []
    for notebook_file in notebook_files:
        # Extract student name from filename
        filename = notebook_file.name
        student_name = filename.replace('.ipynb', '').replace('_', ' ')
        
        # Generate anonymous ID
        anonymous_id = id_manager.generate_anonymous_id(student_name)
        student_mappings.append((student_name, anonymous_id, filename))
        
        print(f"  📝 {student_name} → {anonymous_id}")
    
    # Get password for encryption
    print("\n🔒 Setting up secure mapping storage...")
    password = getpass.getpass("Enter password for mapping encryption: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if password != confirm_password:
        print("❌ Passwords do not match!")
        return 1
    
    # Save encrypted mapping
    mapping_file = id_manager.save_mapping(args.assignment_id, password)
    
    # Export anonymous roster
    roster_file = id_manager.export_anonymous_roster(args.assignment_id)
    
    # Create reveal report (instructor only)
    if args.create_reveal:
        reveal_file = id_manager.create_name_reveal_report(args.assignment_id, password)
        print(f"🔓 Name reveal report: {reveal_file}")
        print("   WARNING: Secure this file - it contains real names!")
    
    print("\n✅ Anonymous grading session created!")
    print("\n📊 Summary:")
    print(f"   • Students: {len(student_mappings)}")
    print(f"   • Mapping file: {mapping_file}")
    print(f"   • Anonymous roster: {roster_file}")
    print("\n🚀 Next steps:")
    print("   1. Share the anonymous roster with graders")
    print("   2. Use anonymous IDs during grading")
    print("   3. Use reveal command after grading to match results back to names")
    
    return 0

def reveal_student_names(args):
    """Reveal real names from anonymous IDs"""
    print(f"🔓 Revealing Student Names for: {args.assignment_id}")
    print("=" * 60)
    
    # Create ID manager and load mapping
    id_manager = StudentIDManager(args.mapping_dir)
    
    # Get password
    password = getpass.getpass("Enter mapping password: ")
    
    # Load mapping
    if not id_manager.load_mapping(args.assignment_id, password):
        print("❌ Failed to load mapping. Check assignment ID and password.")
        return 1
    
    # Process reveal request
    if args.anonymous_id:
        # Single ID lookup
        real_name = id_manager.get_real_name(args.anonymous_id)
        if real_name:
            print(f"👤 {args.anonymous_id} → {real_name}")
        else:
            print(f"❌ Anonymous ID not found: {args.anonymous_id}")
    
    elif args.results_file:
        # Process results file
        print(f"📄 Processing results file: {args.results_file}")
        reveal_results_file(args.results_file, id_manager, args.output_file)
    
    else:
        # Show all mappings
        stats = id_manager.get_statistics()
        print(f"📊 Total students: {stats['total_students']}")
        print(f"🆔 ID range: {stats['id_range']}")
        
        print("\n👥 All mappings:")
        for anonymous_id, real_name in sorted(id_manager._id_to_name.items()):
            print(f"   {anonymous_id} → {real_name}")
    
    return 0

def reveal_results_file(results_file: str, id_manager: StudentIDManager, output_file: str = None):
    """Reveal names in a results file (CSV)"""
    import pandas as pd
    
    try:
        # Read results file
        df = pd.read_csv(results_file)
        
        # Find student ID columns (flexible matching)
        id_columns = []
        for col in df.columns:
            if any(term in col.lower() for term in ['student', 'id']):
                id_columns.append(col)
        
        if not id_columns:
            print("❌ No student ID columns found in results file")
            return
        
        print(f"🔍 Found potential ID columns: {id_columns}")
        
        # Create revealed version
        df_revealed = df.copy()
        
        for col in id_columns:
            if col in df.columns:
                # Create new column with real names
                real_names = []
                for anonymous_id in df[col]:
                    real_name = id_manager.get_real_name(str(anonymous_id))
                    real_names.append(real_name if real_name else str(anonymous_id))
                
                df_revealed[f"{col}_RealName"] = real_names
        
        # Save revealed file
        if output_file is None:
            base_name = Path(results_file).stem
            output_file = f"{base_name}_with_names.csv"
        
        df_revealed.to_csv(output_file, index=False)
        print(f"✅ Revealed results saved to: {output_file}")
        
        # Show sample
        print("\n📋 Sample of revealed data:")
        print(df_revealed.head().to_string())
        
    except Exception as e:
        print(f"❌ Error processing results file: {e}")

def list_assignments(args):
    """List all available assignment mappings"""
    mapping_dir = Path(args.mapping_dir)
    
    if not mapping_dir.exists():
        print(f"❌ Mapping directory not found: {mapping_dir}")
        return 1
    
    # Find mapping files
    mapping_files = list(mapping_dir.glob("*_mapping.json"))
    
    if not mapping_files:
        print(f"📂 No assignment mappings found in: {mapping_dir}")
        return 0
    
    print(f"📚 Available Assignment Mappings ({len(mapping_files)}):")
    print("=" * 60)
    
    for mapping_file in sorted(mapping_files):
        assignment_id = mapping_file.stem.replace('_mapping', '')
        print(f"  📋 {assignment_id}")
        
        # Try to read basic info (without password)
        try:
            import json
            with open(mapping_file, 'r') as f:
                data = json.load(f)
            
            if 'data' in data and 'total_students' in data['data']:
                student_count = data['data']['total_students']
                created_at = data['data'].get('created_at', 'Unknown')
                print(f"      Students: {student_count}")
                print(f"      Created: {created_at}")
            
        except Exception:
            print("      (Cannot read details without password)")
        
        print()
    
    return 0

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Student ID Anonymization Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create anonymous session
  python student_id_cli.py create hw2_assignment ./notebooks

  # Reveal single ID
  python student_id_cli.py reveal hw2_assignment --id STUDENT_1001

  # Reveal results file
  python student_id_cli.py reveal hw2_assignment --results grades.csv

  # List all assignments
  python student_id_cli.py list
        """
    )
    
    parser.add_argument(
        '--mapping-dir', 
        default='student_mappings',
        help='Directory for storing mapping files (default: student_mappings)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create anonymous grading session')
    create_parser.add_argument('assignment_id', help='Assignment identifier')
    create_parser.add_argument('notebooks_dir', help='Directory containing student notebooks')
    create_parser.add_argument('--create-reveal', action='store_true', 
                             help='Create name reveal report (instructor only)')
    
    # Reveal command
    reveal_parser = subparsers.add_parser('reveal', help='Reveal student names')
    reveal_parser.add_argument('assignment_id', help='Assignment identifier')
    reveal_parser.add_argument('--id', dest='anonymous_id', help='Specific anonymous ID to reveal')
    reveal_parser.add_argument('--results', dest='results_file', help='Results CSV file to process')
    reveal_parser.add_argument('--output', dest='output_file', help='Output file for revealed results')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available assignments')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == 'create':
        return create_anonymous_grading_session(args)
    elif args.command == 'reveal':
        return reveal_student_names(args)
    elif args.command == 'list':
        return list_assignments(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
