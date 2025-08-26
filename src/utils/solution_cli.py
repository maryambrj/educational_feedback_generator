# solution_cli.py
"""
Command-line interface for the Solution Generator module
"""

import sys
import os
import argparse
from ..config.config_manager import ConfigManager, LLMFactory
from .solution_generator import SolutionGenerator
from ..ai_grading.enhanced_grading_agent import EnhancedAIGradingAgent

def generate_solutions_for_assignment(assignment_id: str, output_dir: str = None):
    """Generate reference solutions for a specific assignment"""
    
    print(f"🧠 Generating reference solutions for: {assignment_id}")
    
    # Initialize components
    config = ConfigManager()
    llm = LLMFactory.create_llm(config)
    solution_generator = SolutionGenerator(llm, temperature=0.7)  # Higher temp for creativity
    
    # Generate solutions
    solutions = solution_generator.generate_assignment_solutions(assignment_id)
    
    # Export solutions
    if not output_dir:
        output_dir = f"reference_solutions/{assignment_id}"
    
    solution_generator.export_solutions(solutions, output_dir)
    
    # Quality assessment
    print(f"\n📊 Solution Quality Assessment:")
    print("-" * 40)
    
    total_quality = 0
    for problem_id, solution in solutions.items():
        quality = solution_generator.evaluate_solution_quality(solution)
        total_quality += quality.overall_score
        
        status = "✅" if quality.overall_score >= 0.8 else "⚠️" if quality.overall_score >= 0.6 else "❌"
        print(f"{status} {problem_id}: {quality.overall_score:.2f}")
        print(f"   Completeness: {quality.completeness_score:.2f}")
        print(f"   Technical: {quality.technical_accuracy:.2f}")
        print(f"   Clarity: {quality.explanation_clarity:.2f}")
        print(f"   Pedagogical: {quality.pedagogical_value:.2f}")
        
        if quality.overall_score < 0.7:
            print(f"   📝 Note: {quality.notes}")
        print()
    
    avg_quality = total_quality / len(solutions) if solutions else 0
    print(f"📈 Average Quality Score: {avg_quality:.2f}")
    
    if avg_quality >= 0.8:
        print("🎉 Excellent! Solutions are ready for use in grading.")
    elif avg_quality >= 0.6:
        print("👀 Good quality, but consider reviewing flagged solutions.")
    else:
        print("🔍 Consider regenerating solutions or manual review.")
    
    return solutions

def grade_with_solutions(directory_path: str, assignment_id: str):
    """Grade notebooks using reference solutions"""
    
    print(f"🚀 Enhanced grading with reference solutions")
    print(f"📁 Directory: {directory_path}")
    print(f"📚 Assignment: {assignment_id}")
    
    # Initialize enhanced grading agent
    config = ConfigManager()
    llm = LLMFactory.create_llm(config)
    grading_agent = EnhancedAIGradingAgent(llm, use_reference_solutions=True)
    
    # Grade with reference solutions
    results = grading_agent.grade_directory(directory_path, assignment_id, generate_solutions=True)
    
    # Export enhanced results
    output_dir = os.path.join(directory_path, 'enhanced_ai_grading_results')
    grading_agent.export_results(output_dir)
    
    # Summary
    summary = grading_agent.get_grading_summary()
    
    print(f"\n📊 Enhanced Grading Summary:")
    print("-" * 40)
    print(f"📚 Notebooks graded: {summary.get('total_graded', 0)}")
    print(f"🧠 Reference solutions used: {summary.get('reference_solutions_used', False)}")
    print(f"📋 Assignments with solutions: {len(summary.get('assignments_with_solutions', []))}")
    print(f"🔧 Total solutions generated: {summary.get('solution_count', 0)}")
    
    if results:
        total_problems = sum(len(r) for r in results.values())
        print(f"✅ Problems graded: {total_problems}")
        
        # Calculate average scores
        all_scores = [result.total_score for result_list in results.values() for result in result_list]
        all_possible = [result.max_possible for result_list in results.values() for result in result_list]
        
        if all_scores and all_possible:
            avg_score = sum(all_scores) / len(all_scores)
            avg_possible = sum(all_possible) / len(all_possible)
            avg_percentage = (avg_score / avg_possible * 100) if avg_possible > 0 else 0
            print(f"📈 Average score: {avg_score:.1f}/{avg_possible:.1f} ({avg_percentage:.1f}%)")
    
    print(f"\n💾 Results saved to: {output_dir}")
    return results

def compare_student_to_reference(student_file: str, assignment_id: str, problem_id: str):
    """Compare a specific student response to reference solution"""
    
    print(f"🔍 Comparing student solution to reference")
    print(f"📄 Student file: {student_file}")
    print(f"📚 Assignment: {assignment_id}")
    print(f"🎯 Problem: {problem_id}")
    
    # Initialize components
    config = ConfigManager()
    llm = LLMFactory.create_llm(config)
    solution_generator = SolutionGenerator(llm)
    grading_agent = EnhancedAIGradingAgent(llm)
    
    # Parse student notebook
    parsed_content = grading_agent.parser.parse_notebook(student_file)
    
    # Find the specific response
    student_response = None
    for response in parsed_content['responses']:
        if response.problem_id == problem_id:
            student_response = response
            break
    
    if not student_response:
        print(f"❌ Problem {problem_id} not found in student notebook")
        return
    
    # Generate or load reference solution
    if assignment_id not in grading_agent.reference_solutions:
        print(f"🧠 Generating reference solutions for {assignment_id}...")
        grading_agent.generate_reference_solutions(assignment_id)
    
    reference_solution = grading_agent.reference_solutions[assignment_id].get(problem_id)
    
    if not reference_solution:
        print(f"❌ Reference solution for {problem_id} not found")
        return
    
    # Compare
    comparison = solution_generator.compare_student_solution(
        student_response.content, reference_solution
    )
    
    # Display results
    print(f"\n📊 Comparison Results:")
    print("-" * 40)
    print(f"🎯 Concept Coverage: {comparison.get('concept_coverage', 0):.2f}")
    print(f"🔄 Approach Similarity: {comparison.get('approach_similarity', 0):.2f}")
    print(f"💻 Code Quality vs Reference: {comparison.get('code_quality_vs_reference', 0):.2f}")
    
    missing_concepts = comparison.get('missing_concepts', [])
    if missing_concepts:
        print(f"\n❌ Missing Concepts:")
        for concept in missing_concepts:
            print(f"  - {concept}")
    
    strengths = comparison.get('strengths', [])
    if strengths:
        print(f"\n✅ Strengths:")
        for strength in strengths:
            print(f"  - {strength}")
    
    improvements = comparison.get('improvement_areas', [])
    if improvements:
        print(f"\n🔧 Areas for Improvement:")
        for improvement in improvements:
            print(f"  - {improvement}")
    
    print(f"\n📝 Overall Analysis:")
    print(comparison.get('overall_comparison', 'No detailed comparison available'))

def view_reference_solution(assignment_id: str, problem_id: str = None):
    """View generated reference solutions"""
    
    config = ConfigManager()
    llm = LLMFactory.create_llm(config)
    solution_generator = SolutionGenerator(llm)
    
    # Generate solutions if needed
    solutions = solution_generator.generate_assignment_solutions(assignment_id)
    
    if problem_id:
        # Show specific problem
        if problem_id in solutions:
            solution = solutions[problem_id]
            print(f"📚 Reference Solution: {assignment_id} - {problem_id}")
            print("=" * 60)
            print(f"🎯 Difficulty: {solution.difficulty_level}")
            print(f"⏱️  Estimated Time: {solution.estimated_time_minutes} minutes")
            print(f"🔑 Key Concepts: {', '.join(solution.key_concepts)}")
            print(f"\n📖 Explanation:")
            print(solution.solution_explanation)
            print(f"\n💻 Code:")
            print(solution.solution_code)
            print(f"\n📊 Expected Outputs:")
            print(solution.expected_outputs)
            print(f"\n🎓 Grading Notes:")
            print(solution.grading_notes)
        else:
            print(f"❌ Problem {problem_id} not found")
    else:
        # Show all problems
        print(f"📚 Reference Solutions for: {assignment_id}")
        print("=" * 60)
        for pid, solution in solutions.items():
            print(f"\n🎯 {pid}")
            print(f"   Difficulty: {solution.difficulty_level}")
            print(f"   Time: {solution.estimated_time_minutes} min")
            print(f"   Concepts: {', '.join(solution.key_concepts[:3])}...")

def main():
    """Main CLI function"""
    
    parser = argparse.ArgumentParser(
        description="AI Solution Generator and Enhanced Grading System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate reference solutions
  python solution_cli.py generate hw2_california_housing
  
  # Grade with reference solutions
  python solution_cli.py grade HW02_renamed hw2_california_housing
  
  # Compare specific student to reference
  python solution_cli.py compare student.ipynb hw2_california_housing part_1
  
  # View reference solutions
  python solution_cli.py view hw2_california_housing
  python solution_cli.py view hw2_california_housing part_1
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate solutions command
    generate_parser = subparsers.add_parser('generate', help='Generate reference solutions')
    generate_parser.add_argument('assignment_id', help='Assignment identifier')
    generate_parser.add_argument('--output', '-o', help='Output directory')
    
    # Grade with solutions command  
    grade_parser = subparsers.add_parser('grade', help='Grade notebooks with reference solutions')
    grade_parser.add_argument('directory', help='Directory containing student notebooks')
    grade_parser.add_argument('assignment_id', help='Assignment identifier')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare student to reference solution')
    compare_parser.add_argument('student_file', help='Student notebook file')
    compare_parser.add_argument('assignment_id', help='Assignment identifier')
    compare_parser.add_argument('problem_id', help='Problem identifier')
    
    # View solutions command
    view_parser = subparsers.add_parser('view', help='View reference solutions')
    view_parser.add_argument('assignment_id', help='Assignment identifier')
    view_parser.add_argument('problem_id', nargs='?', help='Specific problem ID (optional)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'generate':
            generate_solutions_for_assignment(args.assignment_id, args.output)
        
        elif args.command == 'grade':
            grade_with_solutions(args.directory, args.assignment_id)
        
        elif args.command == 'compare':
            compare_student_to_reference(args.student_file, args.assignment_id, args.problem_id)
        
        elif args.command == 'view':
            view_reference_solution(args.assignment_id, args.problem_id)
        
        print(f"\n✅ Command '{args.command}' completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error executing command '{args.command}': {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
    