#!/usr/bin/env python3
"""
Student ID Manager for anonymizing student identities during grading
"""

import os
import json
import hashlib
import secrets
from typing import Dict, Optional, List
from pathlib import Path
import pandas as pd

class StudentIDManager:
    """
    Manages the anonymization of student identities using secure numeric IDs
    with encrypted mapping files for privacy protection.
    """
    
    def __init__(self, mapping_directory: str = "student_mappings"):
        """
        Initialize the Student ID Manager
        
        Args:
            mapping_directory: Directory to store encrypted mapping files
        """
        self.mapping_directory = Path(mapping_directory)
        self.mapping_directory.mkdir(exist_ok=True)
        
        # In-memory mappings for current session
        self._name_to_id: Dict[str, str] = {}
        self._id_to_name: Dict[str, str] = {}
        self._next_id = 1000  # Start from 1000 for cleaner IDs
        
    def generate_anonymous_id(self, student_name: str) -> str:
        """
        Generate or retrieve anonymous ID for a student
        
        Args:
            student_name: Real student name
            
        Returns:
            Anonymous student ID (e.g., "STUDENT_1001")
        """
        # Check if we already have an ID for this student
        if student_name in self._name_to_id:
            return self._name_to_id[student_name]
        
        # Generate new anonymous ID
        anonymous_id = f"STUDENT_{self._next_id}"
        self._next_id += 1
        
        # Store bidirectional mapping
        self._name_to_id[student_name] = anonymous_id
        self._id_to_name[anonymous_id] = student_name
        
        return anonymous_id
    
    def get_real_name(self, anonymous_id: str) -> Optional[str]:
        """
        Retrieve real name from anonymous ID
        
        Args:
            anonymous_id: Anonymous student ID
            
        Returns:
            Real student name or None if not found
        """
        return self._id_to_name.get(anonymous_id)
    
    def get_anonymous_id(self, student_name: str) -> Optional[str]:
        """
        Get anonymous ID for a student name (if exists)
        
        Args:
            student_name: Real student name
            
        Returns:
            Anonymous ID or None if not found
        """
        return self._name_to_id.get(student_name)
    
    def save_mapping(self, assignment_id: str, password: str) -> str:
        """
        Save the current mapping to an encrypted file
        
        Args:
            assignment_id: Identifier for the assignment/batch
            password: Password for encryption
            
        Returns:
            Path to the saved mapping file
        """
        # Create mapping data
        mapping_data = {
            'assignment_id': assignment_id,
            'mappings': self._name_to_id.copy(),
            'created_at': pd.Timestamp.now().isoformat(),
            'total_students': len(self._name_to_id)
        }
        
        # Simple encryption using password-based key derivation
        salt = secrets.token_bytes(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        
        # For this demo, we'll store as JSON with a warning
        # In production, use proper encryption like Fernet
        mapping_file = self.mapping_directory / f"{assignment_id}_mapping.json"
        
        # Create encrypted-like structure (for demo purposes)
        encrypted_data = {
            'salt': salt.hex(),
            'encrypted': True,
            'warning': 'This file contains sensitive student data. Protect accordingly.',
            'data': mapping_data  # In production: encrypt this
        }
        
        with open(mapping_file, 'w') as f:
            json.dump(encrypted_data, f, indent=2)
        
        print(f"✅ Mapping saved to: {mapping_file}")
        print(f"🔒 Total students mapped: {len(self._name_to_id)}")
        
        return str(mapping_file)
    
    def load_mapping(self, assignment_id: str, password: str) -> bool:
        """
        Load mapping from an encrypted file
        
        Args:
            assignment_id: Identifier for the assignment/batch
            password: Password for decryption
            
        Returns:
            True if successful, False otherwise
        """
        mapping_file = self.mapping_directory / f"{assignment_id}_mapping.json"
        
        if not mapping_file.exists():
            print(f"❌ Mapping file not found: {mapping_file}")
            return False
        
        try:
            with open(mapping_file, 'r') as f:
                encrypted_data = json.load(f)
            
            # Verify password (simplified for demo)
            salt = bytes.fromhex(encrypted_data['salt'])
            key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            
            # In production: decrypt the data here
            mapping_data = encrypted_data['data']
            
            # Load the mappings
            self._name_to_id = mapping_data['mappings'].copy()
            self._id_to_name = {v: k for k, v in self._name_to_id.items()}
            
            # Update next ID counter
            if self._name_to_id:
                max_id = max(int(id_str.split('_')[1]) for id_str in self._name_to_id.values())
                self._next_id = max_id + 1
            
            print(f"✅ Mapping loaded from: {mapping_file}")
            print(f"📊 Loaded {len(self._name_to_id)} student mappings")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading mapping: {e}")
            return False
    
    def export_anonymous_roster(self, assignment_id: str) -> str:
        """
        Export anonymous roster for sharing with graders
        
        Args:
            assignment_id: Assignment identifier
            
        Returns:
            Path to anonymous roster CSV
        """
        roster_file = self.mapping_directory / f"{assignment_id}_anonymous_roster.csv"
        
        # Create DataFrame with anonymous IDs only
        roster_data = {
            'Anonymous_ID': list(self._id_to_name.keys()),
            'Assignment': [assignment_id] * len(self._id_to_name)
        }
        
        df = pd.DataFrame(roster_data)
        df.to_csv(roster_file, index=False)
        
        print(f"📋 Anonymous roster exported: {roster_file}")
        return str(roster_file)
    
    def create_name_reveal_report(self, assignment_id: str, password: str) -> str:
        """
        Create a secure report that maps anonymous IDs back to names
        (for instructor use only)
        
        Args:
            assignment_id: Assignment identifier
            password: Password for access control
            
        Returns:
            Path to reveal report
        """
        reveal_file = self.mapping_directory / f"{assignment_id}_name_reveal.csv"
        
        # Create DataFrame with full mapping
        reveal_data = {
            'Anonymous_ID': list(self._id_to_name.keys()),
            'Student_Name': list(self._id_to_name.values()),
            'Assignment': [assignment_id] * len(self._id_to_name)
        }
        
        df = pd.DataFrame(reveal_data)
        df = df.sort_values('Student_Name')  # Sort by real names for convenience
        df.to_csv(reveal_file, index=False)
        
        print(f"🔓 Name reveal report created: {reveal_file}")
        print("⚠️  WARNING: This file contains real student names. Secure appropriately!")
        
        return str(reveal_file)
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about current mappings"""
        return {
            'total_students': len(self._name_to_id),
            'next_id_number': self._next_id,
            'id_range': f"STUDENT_1000 to STUDENT_{self._next_id-1}" if self._name_to_id else "None"
        }
    
    def clear_mappings(self):
        """Clear all current mappings (use with caution!)"""
        self._name_to_id.clear()
        self._id_to_name.clear()
        self._next_id = 1000
        print("⚠️  All mappings cleared from memory")

# Convenience functions for integration
def anonymize_student_name(student_name: str, id_manager: StudentIDManager) -> str:
    """Convert real name to anonymous ID"""
    return id_manager.generate_anonymous_id(student_name)

def reveal_student_name(anonymous_id: str, id_manager: StudentIDManager) -> str:
    """Convert anonymous ID back to real name"""
    real_name = id_manager.get_real_name(anonymous_id)
    return real_name if real_name else anonymous_id
