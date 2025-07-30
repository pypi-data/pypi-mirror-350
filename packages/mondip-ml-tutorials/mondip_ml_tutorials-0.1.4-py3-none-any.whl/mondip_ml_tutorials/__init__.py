"""
Mondip ML Tutorials - A comprehensive collection of machine learning tutorials

This package provides hands-on tutorials covering:
- NumPy fundamentals
- Pandas data manipulation  
- Matplotlib visualization
- Scikit-learn machine learning algorithms

Each chapter focuses on practical examples with real datasets.
"""

__version__ = "0.1.4"
__author__ = "xyz"
__email__ = "xyz.email@example.com"
__description__ = "A comprehensive collection of machine learning tutorials using NumPy, Pandas, Matplotlib, and Scikit-learn"

from .tutorials import (
    chapter_1_numpy,
    chapter_2_pandas,
    chapter_3_matplotlib,
    chapter_4_sklearn_basics,
    chapter_5_knn,
    chapter_6_decision_tree,
    chapter_7_kmeans,
    chapter_8_svm,
    chapter_9_random_forest,
    chapter_10_naive_bayes,
    run_all_chapters,
    mondip
)

__all__ = [
    'chapter_1_numpy',
    'chapter_2_pandas', 
    'chapter_3_matplotlib',
    'chapter_4_sklearn_basics',
    'chapter_5_knn',
    'chapter_6_decision_tree',
    'chapter_7_kmeans',
    'chapter_8_svm',
    'chapter_9_random_forest',
    'chapter_10_naive_bayes',
    'run_all_chapters',
    'mondip'
]

# Package metadata
__title__ = "mondip-ml-tutorials"
__summary__ = "Machine Learning tutorials with practical examples"
__uri__ = "https://github.com/yourusername/mondip-ml-tutorials"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024 Your Name"