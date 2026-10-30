import os
import matplotlib.pyplot as plt
import pandas as pd
from src.project_model.model import CourseFeedModel

OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    volumes = ["low", "medium", "high"]
    results = []

    for vol in volumes:
        # 1) run Baseline code
        base_sim = CourseFeedModel(rule="baseline", volume=vol)
        for _ in range(30):
            base_sim.step()
        base_df = base_sim.datacollector.get_model_vars_dataframe()

        # save medium trace for baseline as required by DEL02
        if vol == "medium":
            base_df.to_csv(os.path.join(OUT_DIR, "baseline_raw_00_daily_trace.csv"), index=False)

        # 2) run Alternative code
        alt_sim = CourseFeedModel(rule="alternative", volume=vol)
        for _ in range(30):
            alt_sim.step()
        alt_df = alt_sim.datacollector.get_model_vars_dataframe()

        # save medium trace for alternative as required by deliverable 2
        if vol == "medium":
            alt_df.to_csv(os.path.join(OUT_DIR, "alternative_raw_00_daily_trace.csv"), index=False)

        total_urgent = base_df["Urgent_Eligible"].sum()
        base_vis = base_df["Urgent_Visible"].sum()
        alt_vis = alt_df["Urgent_Visible"].sum()
        displaced = alt_df["Displaced_Announcements"].sum()

        results.append({
            "volume": vol.capitalize(),
            "urgent_occurrences": total_urgent,
            "baseline_vis_pct": (base_vis / total_urgent) * 100,
            "alternative_vis_pct": (alt_vis / total_urgent) * 100,
            "displaced_announcements": displaced
        })

    summary = pd.DataFrame(results)
    
    print("\n--- Simulation Summary ---")
    
    print(summary.to_string(index=False))

    # save summary tables
    summary[["volume", "urgent_occurrences", "baseline_vis_pct"]].to_csv(
        os.path.join(OUT_DIR, "baseline_processed_00_summary_table.csv"), index=False
    )
    summary[["volume", "urgent_occurrences", "alternative_vis_pct", "displaced_announcements"]].to_csv(
        os.path.join(OUT_DIR, "alternative_processed_00_summary_table.csv"), index=False
    )

    # plot 1: Baseline Urgent Visibility
    plt.figure(figsize=(7, 4.5))
    plt.bar(summary["volume"], summary["baseline_vis_pct"], color="#1f77b4", width=0.4)
    plt.ylabel("Urgent Deadline Visibility (%)")
    plt.xlabel("Announcement Volume")
    plt.title("Baseline: Urgent Deadline Visibility Across Conditions")
    plt.ylim(0, 110)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "baseline_processed_01_visibility_plot.png"), dpi=300)
    plt.close()


    # plot 2: Alternative Urgent Visibility
    plt.figure(figsize=(7, 4.5))
    plt.bar(summary["volume"], summary["alternative_vis_pct"], color="#ff7f0e", width=0.4)
    plt.ylabel("Urgent Deadline Visibility (%)")
    plt.xlabel("Announcement Volume")
    plt.title("Alternative: Urgent Deadline Visibility Across Conditions")
    plt.ylim(0, 110)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "alternative_processed_01_visibility_plot.png"), dpi=300)
    plt.close()

    # plot 3: Alternative Announcement Displacement
    plt.figure(figsize=(7, 4.5))
    plt.bar(summary["volume"], summary["displaced_announcements"], color="#d62728", width=0.4)
    plt.ylabel("Displaced Announcement Occurrences")
    plt.xlabel("Announcement Volume")
    plt.title("Alternative: Displaced Announcements Across Conditions")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "alternative_processed_02_displacement_plot.png"), dpi=300)
    plt.close()
    print("\nAll outputs successfully saved to outputs/")

if __name__ == "__main__":
    run()

