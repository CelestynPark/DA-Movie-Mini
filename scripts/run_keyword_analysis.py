import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analysis_keywords import main

if __name__ == '__main__':
    main()