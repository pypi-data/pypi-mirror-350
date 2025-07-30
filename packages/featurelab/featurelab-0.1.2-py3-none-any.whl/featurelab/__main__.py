import argparse
import pandas as pd
from featurelab.utils import FeatureUtils
from featurelab.visualizer import Visualizer

def main():
    parser = argparse.ArgumentParser(
        description="FeatureLab CLI - Feature Engineering Toolkit"
    )
    parser.add_argument("csv", help="Path to input CSV file")
    parser.add_argument("--info", action="store_true", help="Show detected column types")
    parser.add_argument("--memory-opt", action="store_true", help="Optimize memory usage and save output")
    parser.add_argument("--visualize-missing", action="store_true", help="Show missing value matrix")
    parser.add_argument("--output", type=str, help="Path to save optimized CSV (used with --memory-opt)")
    parser.add_argument("--correlation", action="store_true", help="Show correlation matrix heatmap")
    parser.add_argument("--duplicates", action="store_true", help="Visualize duplicate rows")
    parser.add_argument("--categorical", type=str, help="Visualize distribution of a categorical column")
    parser.add_argument("--outliers", type=str, help="Visualize outliers in a numeric column")

    args = parser.parse_args()
    df = pd.read_csv(args.csv)

    if args.info:
        print("Detected column types:")
        print(FeatureUtils.detect_column_types(df))

    if args.memory_opt:
        df_opt = FeatureUtils.memory_optimize(df)
        if args.output:
            df_opt.to_csv(args.output, index=False)
            print(f"Optimized CSV saved to {args.output}")
        else:
            print("Memory optimization complete. Use --output to save the result.")

    if args.visualize_missing:
        viz = Visualizer()
        viz.plot_null_matrix(df)

    if args.correlation:
        viz = Visualizer()
        viz.plot_correlation_matrix(df)

    if args.duplicates:
        viz = Visualizer()
        viz.plot_duplicates(df)

    if args.categorical:
        if args.categorical in df.columns:
            viz = Visualizer()
            viz.plot_categorical(df[args.categorical])
        else:
            print(f"Column '{args.categorical}' not found in the data.")

    if args.outliers:
        if args.outliers in df.columns:
            viz = Visualizer()
            data = df[args.outliers]
            outliers = None  # You can implement outlier detection if needed
            viz.plot_outliers(data, outliers, args.outliers)
        else:
            print(f"Column '{args.outliers}' not found in the data.")

if __name__ == "__main__":
    main()