#!/usr/bin/env python3
"""Generate RelGate architecture figure as PDF using matplotlib."""

import sys
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch
except ImportError:
    sys.exit("Install matplotlib: pip install matplotlib")

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "paper" / "figures" / "relgate_architecture.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)


def draw():
    fig, ax = plt.subplots(1, 1, figsize=(6.5, 2.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis('off')

    box_style = dict(boxstyle="round,pad=0.15", facecolor="#E8F4FD", edgecolor="#2C3E50", linewidth=1.2)
    gate_style = dict(boxstyle="round,pad=0.12", facecolor="#FFF3CD", edgecolor="#856404", linewidth=1.0)
    decision_style = dict(boxstyle="round,pad=0.15", facecolor="#D4EDDA", edgecolor="#155724", linewidth=1.2)

    # Boxes
    ax.text(0.8, 1.5, "Change\nBundle", ha='center', va='center', fontsize=8, fontweight='bold',
            bbox=box_style)
    ax.text(2.8, 1.5, "Review Mode\nM0/M1/M2", ha='center', va='center', fontsize=8,
            bbox=box_style)
    ax.text(4.8, 1.5, "LLM\nReview", ha='center', va='center', fontsize=8,
            bbox=box_style)
    ax.text(6.8, 1.5, "Gate Scoring\nG1–G7", ha='center', va='center', fontsize=8,
            bbox=gate_style)
    ax.text(9.0, 1.5, "Decision", ha='center', va='center', fontsize=8, fontweight='bold',
            bbox=decision_style)

    # Arrows
    arrow_props = dict(arrowstyle='->', color='#2C3E50', lw=1.5)
    ax.annotate('', xy=(1.8, 1.5), xytext=(1.5, 1.5), arrowprops=arrow_props)
    ax.annotate('', xy=(3.8, 1.5), xytext=(3.6, 1.5), arrowprops=arrow_props)
    ax.annotate('', xy=(5.9, 1.5), xytext=(5.7, 1.5), arrowprops=arrow_props)
    ax.annotate('', xy=(8.1, 1.5), xytext=(7.7, 1.5), arrowprops=arrow_props)

    # Labels below
    ax.text(6.8, 0.5, "Evidence\nVerification", ha='center', va='center', fontsize=7,
            style='italic', color='#555555')
    ax.annotate('', xy=(6.8, 0.9), xytext=(6.8, 1.1),
                arrowprops=dict(arrowstyle='->', color='#888888', lw=1.0))

    # Decision outcomes
    ax.text(9.0, 0.55, "READY | FIX | UNKNOWN", ha='center', va='center', fontsize=6.5,
            color='#155724')

    plt.tight_layout(pad=0.2)
    fig.savefig(OUT, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Architecture figure saved to {OUT}")


if __name__ == "__main__":
    draw()
