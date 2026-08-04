"""
Master Lab Execution Script
Executes all steps of the Lab, generates datasets, runs Prophet forecasting, produces evaluation metrics, and saves high-resolution plots.
"""
import os
import sys
from generate_data import generate_synthetic_metrics
from forecast_pipeline import run_forecasting_pipeline


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    data_path = os.path.join(base_dir, "synthetic_metrics.csv")
    plots_dir = os.path.join(project_root, "plots")

    print("================ 🚀 WEEK 4 LAB PIPELINE ================")
    print("Step 1: Generating synthetic metrics dataset...")
    generate_synthetic_metrics(output_path=data_path, n_days=7)

    print("\nSteps 2-5: Running Prophet forecasting & evaluation pipeline...")
    results = run_forecasting_pipeline(csv_path=data_path, output_dir=plots_dir)

    print("================ 🏁 LAB EXECUTION COMPLETE ================")
    print(f"Metrics Output Directory: {plots_dir}")
    print(f"Achieved MAE             : {results['mae']:.2f}% CPU")
    print(f"Achieved MAPE            : {results['mape']:.2f}%")
    print(f"Scaling Recommendation   : {results['decision']}")
    print("===========================================================\n")


if __name__ == "__main__":
    main()
