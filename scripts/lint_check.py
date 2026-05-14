import sys
import re
import subprocess

def get_pylint_score(directory="."):
    print(f"Running pylint on {directory}...")
    try:
        # Run pylint and capture output
        result = subprocess.run(
            [sys.executable, "-m", "pylint", "--recursive=y", "."],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Look for the score in the output: "Your code has been rated at 10.00/10"
        match = re.search(r"Your code has been rated at ([-+]?\d*\.\d+|\d+)/10", result.stdout)
        if match:
            return float(match.group(1))
        return 0.0
    except Exception as e:
        print(f"Error running pylint: {e}")
        return 0.0

def main():
    threshold = 8.0
    score = get_pylint_score()
    
    print(f"Current Pylint Score: {score}/10")
    
    if score < threshold:
        print(f"FAILED: Code quality score {score} is below the threshold of {threshold}.")
        sys.exit(1)
    
    print("SUCCESS: Code quality score meets the threshold.")

if __name__ == "__main__":
    main()
