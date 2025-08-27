#!/usr/bin/env python3
"""
AI Grading Wrapper - Handles import issues for AI grading functionality
"""

import sys
import os
from pathlib import Path

def run_ai_grading(notebook_directory, assignment_id, output_csv):
    """
    Run AI grading with proper import handling
    """
    # Add project root to path (not src/)
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    try:
        # Import specific modules directly to avoid circular imports from __init__.py files
        import src.config.config_manager as config_mod
        import src.ai_grading.ai_grading_agent as ai_mod
        import src.reports.report_generator as report_mod
        
        ConfigManager = config_mod.ConfigManager
        LLMFactory = config_mod.LLMFactory
        AIGradingAgent = ai_mod.AIGradingAgent
        ReportGenerator = report_mod.ReportGenerator
        create_combined_report = report_mod.create_combined_report
        
        print("🤖 Loading AI grading configuration...")
        
        # Load configuration
        config = ConfigManager()
        llm = LLMFactory.create_llm(config)
        print(f"✅ Using LLM: {llm.get_model_name()}")
        
        # Create AI grading agent
        ai_grader = AIGradingAgent(llm)
        
        # Grade all notebooks
        print("🧠 Running AI content analysis...")
        ai_results = ai_grader.grade_directory(notebook_directory, assignment_id)
        
        if ai_results:
            # Export AI results
            ai_output_dir = os.path.join(notebook_directory, 'ai_grading_results')
            os.makedirs(ai_output_dir, exist_ok=True)
            
            # Create report generator
            import src.config.data_structures as data_mod
            GradingResult = data_mod.GradingResult
            if ai_results and isinstance(list(ai_results.values())[0], list):
                all_results = []
                for student_results in ai_results.values():
                    if isinstance(student_results, list):
                        all_results.extend(student_results)
                
                report_gen = ReportGenerator(all_results)
                report_gen.export_results(ai_output_dir)
            
            # Create combined report
            create_combined_report(notebook_directory, output_csv, ai_results, assignment_id, "homework")
            
            print(f"✅ AI analysis completed successfully!")
            print(f"📊 AI results saved to: {ai_output_dir}")
            print(f"📈 Combined report: {os.path.join(notebook_directory, 'combined_grading_report.html')}")
            return True
        else:
            print("⚠️ No AI grading results generated")
            return False
            
    except Exception as e:
        print(f"❌ AI grading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ai_grading_wrapper.py <notebook_directory> <assignment_id> <output_csv>")
        sys.exit(1)
        
    success = run_ai_grading(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0 if success else 1)