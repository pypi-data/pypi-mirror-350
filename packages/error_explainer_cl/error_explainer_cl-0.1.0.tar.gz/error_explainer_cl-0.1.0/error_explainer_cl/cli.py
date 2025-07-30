import argparse
from error_explainer_cl import resolver

def main():
    parser_arg = argparse.ArgumentParser(description="🐍 Explain Python errors quickly.")
    parser_arg.add_argument("error_type", help="Type the Python error name (e.g., ModuleNotFoundError)")
    args = parser_arg.parse_args()

    result = resolver.find_solution(args.error_type)

    if result:
        print("\n💥 Error Match Found:\n")
        print(f"🧠 Error: {result['error']}")
        print(f"📖 Explanation: {result['explanation']}")
        print(f"🛠️ Fix: {result['fix']}")
    else:
        print("❌ No match found. Try updating your knowledge base or check your spelling.")
