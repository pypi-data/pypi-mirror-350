"""
Mondip ML Tutorials - A comprehensive collection of machine learning tutorials

This package provides hands-on tutorials covering:
- NumPy fundamentals
- Pandas data manipulation  
- Matplotlib visualization
- Scikit-learn machine learning algorithms

Each chapter focuses on practical examples with real datasets.
"""

__version__ = "0.1.0"
__author__ = "xyz"
__email__ = "xyz.email@example.com"
__description__ = "A comprehensive collection of machine learning tutorials using NumPy, Pandas, Matplotlib, and Scikit-learn"

from .tutorials import (
    numpy_ops as chapter_1_numpy,
    pandas_analysis as chapter_2_pandas,
    plot_charts as chapter_3_matplotlib,
    linear_reg as chapter_4_sklearn_basics,
    knn_model as chapter_5_knn,
    dt_weather as chapter_6_decision_tree_weather,
    dt_iris as chapter_6_decision_tree_iris,
    kmeans_cluster as chapter_7_kmeans,
    svm_model as chapter_8_svm,
    rf_model as chapter_9_random_forest,
    nb_titanic as chapter_10_naive_bayes_titanic,
    nb_weather as chapter_10_naive_bayes_weather
)

def run_all_chapters():
    """Run all tutorial chapters in sequence"""
    print("Running Chapter 1: NumPy Operations")
    chapter_1_numpy()
    
    print("\nRunning Chapter 2: Pandas Analysis")
    chapter_2_pandas()
    
    print("\nRunning Chapter 3: Matplotlib Plotting")
    chapter_3_matplotlib()
    
    print("\nRunning Chapter 4: Sklearn Basics & Linear Regression")
    chapter_4_sklearn_basics()
    
    print("\nRunning Chapter 5: K-Nearest Neighbors")
    chapter_5_knn()
    
    print("\nRunning Chapter 6a: Decision Tree - Weather")
    chapter_6_decision_tree_weather()
    
    print("\nRunning Chapter 6b: Decision Tree - Iris")
    chapter_6_decision_tree_iris()
    
    print("\nRunning Chapter 7: K-Means Clustering")
    chapter_7_kmeans()
    
    print("\nRunning Chapter 8: Support Vector Machine")
    chapter_8_svm()
    
    print("\nRunning Chapter 9: Random Forest")
    chapter_9_random_forest()
    
    print("\nRunning Chapter 10a: Naive Bayes - Titanic")
    chapter_10_naive_bayes_titanic()
    
    print("\nRunning Chapter 10b: Naive Bayes - Weather")
    chapter_10_naive_bayes_weather()
    
    print("\nAll chapters completed!")

def mondip():
    """Display package information and available tutorials"""
    print("=" * 60)
    print("MONDIP ML TUTORIALS")
    print("=" * 60)
    print(f"Version: {__version__}")
    print(f"Author: {__author__}")
    print(f"Description: {__description__}")
    print("\nAvailable Tutorials:")
    print("- chapter_1_numpy(): NumPy array operations and statistics")
    print("- chapter_2_pandas(): Pandas DataFrame operations and analysis")
    print("- chapter_3_matplotlib(): Various plotting techniques")
    print("- chapter_4_sklearn_basics(): Data preprocessing and Linear Regression")
    print("- chapter_5_knn(): K-Nearest Neighbors classification")
    print("- chapter_6_decision_tree_weather(): Decision Tree for weather data")
    print("- chapter_6_decision_tree_iris(): Decision Tree for iris dataset")
    print("- chapter_7_kmeans(): K-Means clustering analysis")
    print("- chapter_8_svm(): Support Vector Machine classification")
    print("- chapter_9_random_forest(): Random Forest classification")
    print("- chapter_10_naive_bayes_titanic(): Naive Bayes for Titanic dataset")
    print("- chapter_10_naive_bayes_weather(): Naive Bayes for weather data")
    print("- run_all_chapters(): Execute all tutorials in sequence")
    print("=" * 60)

__all__ = [
    'chapter_1_numpy',
    'chapter_2_pandas', 
    'chapter_3_matplotlib',
    'chapter_4_sklearn_basics',
    'chapter_5_knn',
    'chapter_6_decision_tree_weather',
    'chapter_6_decision_tree_iris',
    'chapter_7_kmeans',
    'chapter_8_svm',
    'chapter_9_random_forest',
    'chapter_10_naive_bayes_titanic',
    'chapter_10_naive_bayes_weather',
    'run_all_chapters',
    'mondip'
]

# Package metadata
__title__ = "mondip-ml-tutorials"
__summary__ = "Machine Learning tutorials with practical examples"
__uri__ = "https://github.com/yourusername/mondip-ml-tutorials"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024 Your Name"