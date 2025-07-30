import pytest
from mondip_ml_tutorials import tutorials


def test_imports():
    """Test that all main functions can be imported"""
    assert hasattr(tutorials, 'chapter_1_numpy')
    assert hasattr(tutorials, 'chapter_2_pandas')
    assert hasattr(tutorials, 'run_all_chapters')


def test_chapter_functions_exist():
    """Test that all chapter functions exist"""
    chapter_functions = [
        'chapter_1_numpy',
        'chapter_2_pandas',
        'chapter_3_matplotlib',
        'chapter_4_sklearn_basics',
        'chapter_5_knn',
        'chapter_6_decision_tree',
        'chapter_7_kmeans',
        'chapter_8_svm',
        'chapter_9_random_forest',
        'chapter_10_naive_bayes'
    ]
    
    for func_name in chapter_functions:
        assert hasattr(tutorials, func_name)
        assert callable(getattr(tutorials, func_name))


def test_version():
    """Test version is accessible"""
    import mondip_ml_tutorials
    assert hasattr(mondip_ml_tutorials, '__version__')