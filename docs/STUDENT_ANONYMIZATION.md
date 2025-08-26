# Student Anonymization System

The AI Grader includes a comprehensive student anonymization system that removes student names from the grading process while maintaining secure mapping for final results.

## 🎯 Purpose

**Privacy Protection**: Removes bias and protects student privacy during grading by using anonymous IDs instead of real names.

**Blind Grading**: Enables fair assessment by preventing graders from seeing student identities.

**Secure Mapping**: Maintains encrypted mapping between anonymous IDs and real names for final result association.

## 🏗️ System Architecture

### Core Components

1. **StudentIDManager**: Central manager for ID generation and secure mapping
2. **Anonymous IDs**: Format `STUDENT_XXXX` (e.g., `STUDENT_1001`, `STUDENT_1002`)
3. **Encrypted Mappings**: Secure storage of ID-to-name associations
4. **Integration Points**: Parser, graders, and report generators support anonymization

### Data Flow

```
Real Names → Anonymous IDs → Grading → Results → Name Revelation
    ↓              ↓            ↓          ↓           ↓
[John Smith] → [STUDENT_1001] → [Grade] → [Report] → [John Smith: 85%]
```

## 🚀 Quick Start

### 1. Create Anonymous Grading Session

```bash
# Navigate to utils directory
cd src/utils

# Create anonymous session for an assignment
python student_id_cli.py create hw2_assignment ./notebooks/hw2/
```

This will:
- Generate anonymous IDs for all students
- Create encrypted mapping file
- Export anonymous roster for graders
- Optionally create instructor reveal report

### 2. Grade Using Anonymous IDs

During grading, all student identifiers will be anonymous:
```
STUDENT_1001, STUDENT_1002, STUDENT_1003, ...
```

### 3. Reveal Names After Grading

```bash
# Reveal all mappings
python student_id_cli.py reveal hw2_assignment

# Reveal specific ID
python student_id_cli.py reveal hw2_assignment --id STUDENT_1001

# Process results file with name revelation
python student_id_cli.py reveal hw2_assignment --results grades.csv
```

## 📋 Detailed Usage

### StudentIDManager Class

```python
from src.utils.student_id_manager import StudentIDManager

# Initialize manager
id_manager = StudentIDManager("secure_mappings/")

# Generate anonymous ID
anon_id = id_manager.generate_anonymous_id("Smith, John")
# Returns: "STUDENT_1001"

# Save encrypted mapping
id_manager.save_mapping("hw2_assignment", "secure_password")

# Load mapping for revelation
id_manager.load_mapping("hw2_assignment", "secure_password")

# Reveal real name
real_name = id_manager.get_real_name("STUDENT_1001")
# Returns: "Smith, John"
```

### Integration with NotebookParser

```python
from src.core.notebook_parser import NotebookParser
from src.utils.student_id_manager import StudentIDManager

# Set up anonymization
id_manager = StudentIDManager()
parser = NotebookParser(id_manager=id_manager, use_anonymization=True)

# Parse notebook with anonymization
result = parser.parse_notebook("notebooks/Smith_John.ipynb")

print(result['student_id'])    # "STUDENT_1001"
print(result['real_name'])     # "Smith, John"
print(result['anonymized'])    # True
```

### Integration with Grading

```python
from src.config.data_structures import GradingResult

# Create grading result with anonymous ID
result = GradingResult(
    problem_id="part_1",
    student_id="STUDENT_1001",  # Anonymous ID
    scores={"understanding": 8.5},
    total_score=15.5,
    max_possible=20,
    percentage=77.5,
    feedback="Good work",
    suggestions=["Add more detail"],
    confidence=0.85
)

# Later, reveal the real name
real_name = id_manager.get_real_name(result.student_id)
```

## 🔒 Security Features

### Encrypted Storage

- Mappings stored in encrypted JSON files
- Password-based key derivation (PBKDF2)
- Salt generation for additional security
- Configurable encryption parameters

### Access Control

- **Anonymous Roster**: Shareable with graders (no real names)
- **Mapping Files**: Encrypted, instructor-only access
- **Reveal Reports**: Secure, generated only when needed
- **Memory Clearing**: Sensitive data cleared after use

### Best Practices

#### ✅ DO

- Use strong passwords for mapping encryption
- Store mapping files securely according to institutional policy
- Only reveal names after grading is complete
- Use different passwords for different assignments
- Keep reveal reports in secure, instructor-only directories
- Clear sensitive data from memory after use

#### ❌ DON'T

- Share mapping files or passwords with student graders
- Store real names in grading spreadsheets or shared documents
- Reveal names during the grading process
- Use weak or reused passwords
- Leave reveal reports in publicly accessible directories
- Keep mappings in memory longer than necessary

## 🔧 CLI Reference

### Create Anonymous Session

```bash
python student_id_cli.py create <assignment_id> <notebooks_dir> [options]

Options:
  --create-reveal    Create instructor reveal report
  --mapping-dir DIR  Custom mapping directory (default: student_mappings)
```

### Reveal Names

```bash
python student_id_cli.py reveal <assignment_id> [options]

Options:
  --id ANON_ID           Reveal specific anonymous ID
  --results FILE.csv     Process results file with name revelation
  --output FILE.csv      Output file for revealed results
  --mapping-dir DIR      Custom mapping directory
```

### List Assignments

```bash
python student_id_cli.py list [options]

Options:
  --mapping-dir DIR      Custom mapping directory
```

## 📊 File Outputs

### Anonymous Roster (`assignment_anonymous_roster.csv`)
```csv
Anonymous_ID,Assignment
STUDENT_1001,hw2_assignment
STUDENT_1002,hw2_assignment
STUDENT_1003,hw2_assignment
```

### Name Reveal Report (`assignment_name_reveal.csv`)
```csv
Anonymous_ID,Student_Name,Assignment
STUDENT_1001,Smith John,hw2_assignment
STUDENT_1002,Doe Jane,hw2_assignment
STUDENT_1003,Garcia Maria,hw2_assignment
```

### Grading Results with Revelation
```csv
Anonymous_ID,Problem_ID,Score,Percentage,Anonymous_ID_RealName
STUDENT_1001,part_1,15.5,77.5,Smith John
STUDENT_1002,part_1,18.0,90.0,Doe Jane
```

## 🔄 Workflow Examples

### Complete Anonymization Workflow

```bash
# 1. Create anonymous session
python student_id_cli.py create midterm_exam ./notebooks/midterm/

# 2. Share anonymous roster with graders
# File: student_mappings/midterm_exam_anonymous_roster.csv

# 3. Conduct grading using anonymous IDs
# All grading tools now use STUDENT_XXXX identifiers

# 4. After grading, reveal names in results
python student_id_cli.py reveal midterm_exam --results final_grades.csv

# 5. Final output includes both anonymous IDs and real names
```

### Emergency Name Lookup

```bash
# Quick lookup of single student
python student_id_cli.py reveal midterm_exam --id STUDENT_1015
# Output: STUDENT_1015 → Johnson, Sarah
```

### Batch Processing

```bash
# Process multiple result files
python student_id_cli.py reveal midterm_exam --results rubric_scores.csv --output rubric_with_names.csv
python student_id_cli.py reveal midterm_exam --results ai_feedback.csv --output feedback_with_names.csv
```

## 🚨 Troubleshooting

### Common Issues

**"Mapping file not found"**
- Verify assignment ID spelling
- Check mapping directory path
- Ensure create command completed successfully

**"Failed to load mapping"**
- Verify password is correct
- Check file permissions
- Ensure mapping file not corrupted

**"Anonymous ID not found"**
- Verify ID format (STUDENT_XXXX)
- Check if ID was generated in this assignment
- Ensure mapping loaded correctly

### Data Recovery

If mapping files are lost:
1. Check backup locations
2. Recreate from original notebook filenames if necessary
3. Maintain separate secure backup of critical mappings

## 🔮 Advanced Features

### Custom ID Formats

Modify `StudentIDManager` to use custom ID formats:
```python
# In generate_anonymous_id method
anonymous_id = f"ANON_{self._next_id:04d}"  # ANON_0001, ANON_0002, etc.
```

### Integration with LMS

Export anonymous rosters in LMS-compatible formats:
```python
# Custom export for specific LMS requirements
def export_lms_format(self, assignment_id: str, lms_type: str):
    # Implementation for Canvas, Blackboard, etc.
    pass
```

### Audit Logging

Track all anonymization operations:
```python
# Add to StudentIDManager
def log_operation(self, operation: str, details: dict):
    # Log to secure audit file
    pass
```

## 📚 Related Documentation

- [System Architecture](SYSTEM_ARCHITECTURE.md)
- [Security Guidelines](SECURITY.md)
- [API Reference](API_REFERENCE.md)
- [Integration Guide](INTEGRATION.md)

---

**⚠️ Important**: This anonymization system is designed for educational grading purposes. For production use in sensitive environments, additional security measures and compliance reviews may be required.
