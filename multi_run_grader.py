#!/usr/bin/env python3
"""
Multi-Run AI Grader - Grades notebooks multiple times with different models
"""

import sys
import os
import yaml
import csv
import statistics
from pathlib import Path
from typing import Dict, List, Any
import time

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded .env file")
except ImportError:
    print("Warning: python-dotenv not installed. Environment variables from .env won't be loaded.")
    print("Install with: pip install python-dotenv")

def load_multi_run_config(config_path: str = "config/multi_run_config.yaml") -> Dict:
    """Load multi-run configuration"""
    if not os.path.exists(config_path):
        print(f"❌ Multi-run config not found: {config_path}")
        print("💡 Create the config file or use single-run grading")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_single_grading(notebook_dir: str, assignment_id: str, run_config: Dict, run_name: str) -> Dict:
    """Run grading with a specific model configuration"""
    
    print(f"\n🤖 Running: {run_name}")
    print(f"   Model: {run_config['provider']}/{run_config['model']}")
    print(f"   Temperature: {run_config['temperature']}")
    
    # Add project root to path for imports
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    try:
        # Import the grading modules
        import src.config.config_manager as config_mod
        import src.ai_grading.ai_grading_agent as ai_mod
        import src.reports.report_generator as report_mod
        
        # Create temporary config for this run
        temp_config = {
            'llm_settings': {
                'provider': run_config['provider'],
                'model': run_config['model'],
                'temperature': run_config['temperature'],
                'max_tokens': 1500,
                'api_key': ''  # Will use .env
            },
            'grading_settings': {
                'confidence_threshold': 0.7,
                'auto_flag_low_confidence': True,
                'enable_detailed_feedback': True
            }
        }
        
        # Override the config manager's config
        config_manager = config_mod.ConfigManager()
        config_manager.config = temp_config
        
        # Create LLM and grading agent
        llm = config_mod.LLMFactory.create_llm(config_manager)
        ai_grader = ai_mod.AIGradingAgent(llm)
        
        # Run the grading
        print("   🧠 Running AI analysis...")
        ai_results = ai_grader.grade_directory(notebook_dir, assignment_id)
        
        if not ai_results:
            print(f"   ❌ No results from {run_name}")
            return {}
            
        # Export results to run-specific directory
        run_output_dir = os.path.join(notebook_dir, f'multi_run_results/{run_name.replace(" ", "_")}')
        os.makedirs(run_output_dir, exist_ok=True)
        
        # Create report generator for this run
        all_results = []
        for student_results in ai_results.values():
            if isinstance(student_results, list):
                all_results.extend(student_results)
        
        if all_results:
            report_gen = report_mod.ReportGenerator(all_results)
            report_gen.export_results(run_output_dir)
            
        print(f"   ✅ {run_name} completed - {len(all_results)} results")
        
        return {
            'run_name': run_name,
            'config': run_config,
            'results': ai_results,
            'all_results': all_results,
            'output_dir': run_output_dir
        }
        
    except Exception as e:
        print(f"   ❌ Error in {run_name}: {e}")
        return {}

def summarize_feedback(feedbacks: List[str]) -> str:
    """Summarize multiple feedback texts into a single consolidated feedback"""
    
    if not feedbacks:
        return "No feedback available"
    
    if len(feedbacks) == 1:
        return feedbacks[0]
    
    # For now, create a simple summary by combining unique points
    # In a real implementation, you might use an LLM to summarize
    
    all_points = []
    for feedback in feedbacks:
        # Extract key points (simple heuristic)
        sentences = feedback.replace('.', '.\n').split('\n')
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and sentence not in all_points:
                all_points.append(sentence)
    
    # Combine into summary
    if len(all_points) <= 3:
        return " ".join(all_points)
    else:
        return f"Multiple models provided consistent feedback: {' '.join(all_points[:3])} [Summary of {len(feedbacks)} model responses]"

def aggregate_results(run_results: List[Dict], config: Dict) -> Dict:
    """Aggregate results from multiple runs into single averaged results"""
    
    if not run_results:
        return {}
    
    print("\n📊 Aggregating results from all runs into single final grades...")
    
    # Group results by student and problem
    student_problem_data = {}
    
    for run_data in run_results:
        if not run_data.get('all_results'):
            continue
        
        for result in run_data['all_results']:
            student_id = result.student_id
            problem_id = result.problem_id
            key = f"{student_id}|{problem_id}"
            
            if key not in student_problem_data:
                student_problem_data[key] = {
                    'student_id': student_id,
                    'problem_id': problem_id,
                    'scores': [],
                    'confidences': [],
                    'feedbacks': [],
                    'suggestions': [],
                    'max_possible': result.max_possible
                }
            
            student_problem_data[key]['scores'].append(result.total_score)
            student_problem_data[key]['confidences'].append(result.confidence)
            student_problem_data[key]['feedbacks'].append(result.feedback)
            student_problem_data[key]['suggestions'].extend(result.suggestions)
    
    # Create final averaged results
    from src.config.data_structures import GradingResult
    
    final_results = []
    for key, data in student_problem_data.items():
        if len(data['scores']) >= 1:
            # Calculate averages
            avg_score = statistics.mean(data['scores'])
            avg_confidence = statistics.mean(data['confidences'])
            score_variance = statistics.stdev(data['scores']) if len(data['scores']) > 1 else 0
            
            # Merge feedback
            merged_feedback = summarize_feedback(data['feedbacks'])
            
            # Merge suggestions (unique only)
            unique_suggestions = list(set(data['suggestions']))[:5]  # Limit to 5
            
            # Flag high variance
            high_variance = score_variance > config.get('aggregation', {}).get('variance_threshold', 15)
            
            # Create averaged result
            averaged_result = GradingResult(
                problem_id=data['problem_id'],
                student_id=data['student_id'],
                scores={},  # Individual criterion scores not tracked in multi-run
                total_score=round(avg_score, 1),
                max_possible=data['max_possible'],
                percentage=round((avg_score / data['max_possible']) * 100, 1),
                feedback=f"{merged_feedback}" + (f" [Score variance: {score_variance:.1f}]" if high_variance else ""),
                suggestions=unique_suggestions,
                confidence=round(avg_confidence, 2),
                flagged_for_review=high_variance or avg_confidence < 0.7
            )
            
            final_results.append(averaged_result)
    
    return final_results

def create_final_output(final_results: List, notebook_dir: str, assignment_id: str):
    """Create final consolidated output that matches single-run format"""
    
    print("\n📈 Creating final consolidated results...")
    
    # Import report generator
    import src.reports.report_generator as report_mod
    
    # Create standard output directories  
    ai_output_dir = os.path.join(notebook_dir, 'ai_grading_results')
    os.makedirs(ai_output_dir, exist_ok=True)
    
    # Generate standard CSV output
    csv_file = os.path.join(ai_output_dir, 'ai_grading_results.csv')
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Student Name', 'Problem ID', 'Total Score', 'Max Possible', 'Percentage', 'Confidence', 'Flagged for Review']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in final_results:
            writer.writerow({
                'Student Name': result.student_id,
                'Problem ID': result.problem_id,
                'Total Score': result.total_score,
                'Max Possible': result.max_possible,
                'Percentage': f"{result.percentage}%",
                'Confidence': result.confidence,
                'Flagged for Review': 'Yes' if result.flagged_for_review else 'No'
            })
    
    # Generate individual feedback files
    detailed_feedback_dir = os.path.join(ai_output_dir, 'detailed_feedback')
    os.makedirs(detailed_feedback_dir, exist_ok=True)
    
    # Group results by student for feedback files
    student_results = {}
    for result in final_results:
        student_id = result.student_id
        if student_id not in student_results:
            student_results[student_id] = []
        student_results[student_id].append(result)
    
    # Create detailed feedback files
    for student_id, results in student_results.items():
        feedback_file = os.path.join(detailed_feedback_dir, f"{student_id}_ai_feedback.txt")
        
        with open(feedback_file, 'w', encoding='utf-8') as f:
            f.write(f"AI Grading Feedback - {student_id}\n")
            f.write("=" * 50 + "\n")
            f.write(f"Assignment: {assignment_id}\n")
            f.write(f"Graded using: Multi-model ensemble (5 models averaged)\n\n")
            
            for result in results:
                f.write(f"Problem: {result.problem_id}\n")
                f.write(f"Score: {result.total_score}/{result.max_possible} ({result.percentage}%)\n")
                f.write(f"Confidence: {result.confidence}\n")
                f.write(f"Feedback: {result.feedback}\n")
                
                if result.suggestions:
                    f.write("Suggestions for Improvement:\n")
                    for suggestion in result.suggestions:
                        f.write(f"  • {suggestion}\n")
                
                f.write("\n" + "-" * 30 + "\n\n")
    
    # Generate flagged for review CSV
    flagged_results = [r for r in final_results if r.flagged_for_review]
    if flagged_results:
        flagged_file = os.path.join(ai_output_dir, 'flagged_for_review.csv')
        
        with open(flagged_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Student Name', 'Problem ID', 'Score', 'Confidence', 'Reason', 'Feedback']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in flagged_results:
                reason = "High variance between models" if "variance" in result.feedback else "Low confidence"
                writer.writerow({
                    'Student Name': result.student_id,
                    'Problem ID': result.problem_id,
                    'Score': f"{result.total_score}/{result.max_possible}",
                    'Confidence': result.confidence,
                    'Reason': reason,
                    'Feedback': result.feedback[:100] + "..." if len(result.feedback) > 100 else result.feedback
                })
    
    # Create combined HTML report using standard function
    # Convert results back to the format expected by create_combined_report
    ai_results_dict = {}
    for result in final_results:
        student_id = result.student_id
        if student_id not in ai_results_dict:
            ai_results_dict[student_id] = []
        ai_results_dict[student_id].append(result)
    
    # Generate HTML report
    output_csv = os.path.join(notebook_dir, "traditional_grades.csv")  # For compatibility
    report_mod.create_combined_report(notebook_dir, output_csv, ai_results_dict, assignment_id, "homework")
    
    print(f"✅ Final results saved to: {ai_output_dir}/")
    print(f"   📊 Grades CSV: ai_grading_results.csv")
    print(f"   📝 Individual feedback files: detailed_feedback/")
    print(f"   📈 HTML Report: combined_grading_report.html")
    
    # Print summary
    print("\n📋 Multi-Run Summary:")
    flagged_count = sum(1 for r in final_results if r.flagged_for_review)
    avg_score = statistics.mean([r.total_score for r in final_results]) if final_results else 0
    print(f"   📊 Total problems graded: {len(final_results)}")
    print(f"   🎯 Average score across all: {avg_score:.1f}")
    print(f"   🔍 Flagged for review: {flagged_count}")
    print(f"   📁 Results directory: {ai_output_dir}")

def main():
    """Main multi-run grading function"""
    
    if len(sys.argv) != 3:
        print("Usage: python multi_run_grader.py <notebook_directory> <assignment_id>")
        print("Example: python multi_run_grader.py 'Homework/HW01' hw1_assignment")
        sys.exit(1)
    
    notebook_dir = sys.argv[1]
    assignment_id = sys.argv[2]
    
    print("🎯 Multi-Run AI Grading System")
    print("=" * 50)
    print(f"📚 Notebooks: {notebook_dir}")
    print(f"📋 Assignment: {assignment_id}")
    
    # Load configuration
    config = load_multi_run_config()
    
    if not config.get('multi_run_grading', {}).get('enabled', False):
        print("❌ Multi-run grading is disabled in config")
        sys.exit(1)
    
    runs_config = config.get('multi_run_grading', {}).get('runs', [])
    print(f"🔄 Configured for {len(runs_config)} runs")
    
    # Check if notebook directory exists
    if not os.path.exists(notebook_dir):
        print(f"❌ Directory not found: {notebook_dir}")
        sys.exit(1)
    
    # Run grading with each model
    run_results = []
    
    for i, run_config in enumerate(runs_config, 1):
        run_name = run_config.get('name', f'Run_{i}')
        print(f"\n{'='*20} Run {i}/{len(runs_config)} {'='*20}")
        
        result = run_single_grading(notebook_dir, assignment_id, run_config, run_name)
        if result:
            run_results.append(result)
        
        # Brief pause between runs to avoid rate limiting
        time.sleep(1)
    
    if not run_results:
        print("❌ No successful runs completed")
        sys.exit(1)
    
    # Aggregate and create final consolidated results
    final_results = aggregate_results(run_results, config)
    
    if final_results:
        create_final_output(final_results, notebook_dir, assignment_id)
    else:
        print("❌ No final results generated")
        sys.exit(1)
    
    print("\n🎉 Multi-run grading completed!")
    print(f"✅ Successfully completed {len(run_results)}/{len(runs_config)} runs")
    print("📊 Final grades are averages of all successful model runs")

if __name__ == "__main__":
    main()