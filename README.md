# EECS 4461 — Cumulative Inquiry Project: Deliverable 3

This repository contains the computational simulation and comparison inquiry for the EECS 4461 Cumulative Inquiry Project (Fall 2026).

## Investigation Overview
- Inquiry Question: How does reserving one immediately visible position for an approaching assessment deadline affect the visibility of urgent deadlines and recent announcements in a simulated course interface?
- Context: Modeled after the layout of Moodle's Dashboard Timeline block.
- Model Scope: Simulates a 30-day course interface displaying 5 immediately visible positions across low, medium, and high announcement volume conditions.

## How to Run

1. Ensure dependencies are installed:

    pip install -r requirements.txt

2. Run the simulation to generate outputs:

    python src/project_model/run.py

This generates all CSV traces, summary tables, and comparison plots directly into outputs/.

## Repository Structure

* `src/project_model/`: Contains my adapted Mesa model for the deadline visibility simulation.
  * `agents.py`: Defines `CourseItemAgent` and item urgency/visibility attributes.
  * `model.py`: Implements `CourseFeedModel` and the 5 slot ordering rules.
  * `run.py`: Script to run the low, medium, and high volume simulations.
* `src/virus_on_network/`: Preserved copy of the original Mesa example with `SOURCE.md` for attribution.
* `docs/figures/`: Preserves the ecosystem map image and editable draw.io source file.
* `outputs/`: Generated raw daily CSVs, summary CSV tables, and plots.
* `requirements.txt`: Python package dependencies.

## Deliverable 3 (DEL03) Updates

### Changes from DEL02
- Kept the simulation code in `src/project_model/` and the original example in `src/virus_on_network/`.
- Ran the comparison between the two feed rules:
  - **Baseline Rule:** Standard reverse-chronological order by post date.
  - **Alternative Rule:** Pinned urgent assessments (due in 3 days or less) to the top of the feed.
- Tested both rules across 3 announcement volumes (Low: 6, Medium: 12, High: 24).
- Saved all output files in the `outputs/` folder:
  - Daily traces: `baseline_raw_00_daily_trace.csv`, `alternative_raw_00_daily_trace.csv`
  - Summary tables: `baseline_processed_00_summary_table.csv`, `alternative_processed_00_summary_table.csv`
  - Plots: `baseline_processed_01_visibility_plot.png`, `alternative_processed_01_visibility_plot.png`, `alternative_processed_02_displacement_plot.png`
- Added the ecosystem map image in `docs/figures/ecosystem_map.png` (with the draw.io source file in `docs/figures/ecosystem_map.drawio`).