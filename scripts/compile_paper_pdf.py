#!/usr/bin/env python3
"""
Compiles the research paper into a publication-grade PDF document
with embedded publication figures, benchmark tables, and mathematical formulas.
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)

PAPER_DIR = Path("/root/code/active/pkl-benchmark/paper")
FIG_DIR = PAPER_DIR / "figures"
OUTPUT_PDF = PAPER_DIR / "pkl_bench_paper.pdf"


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor('#1A2530'),
        spaceAfter=10
    )

    author_style = ParagraphStyle(
        'DocAuthor',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=15
    )

    abstract_heading = ParagraphStyle(
        'AbstractHeading',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=6
    )

    abstract_body = ParagraphStyle(
        'AbstractBody',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        alignment=4,
        textColor=colors.HexColor('#2C3E50'),
        leftIndent=20,
        rightIndent=20,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1F4E79'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#2C3E50'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor('#222222'),
        spaceAfter=8
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor('#555555'),
        spaceBefore=4,
        spaceAfter=10
    )

    elements = []

    # Title & Metadata
    elements.append(Paragraph("PKL-Bench: A Multi-Tier Benchmark Dataset and Evaluation Suite for Asymmetric Game Dynamics in the Pro Kabaddi League", title_style))
    elements.append(Paragraph("<b>Ritesh</b><br/><code>193809232+Prompt-0@users.noreply.github.com</code> | <a href='https://github.com/Prompt-0/pkl-bench'>https://github.com/Prompt-0/pkl-bench</a>", author_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#BDC3C7'), spaceBefore=2, spaceAfter=12))

    # Abstract
    elements.append(Paragraph("ABSTRACT", abstract_heading))
    abstract_text = (
        "While sports analytics benchmarks such as SoccerNet and NBA Play-by-Play have accelerated machine learning "
        "in symmetric invasion and continuous-transition games, contact invasion sports governed by asymmetric pursuit-evasion "
        "dynamics remain underrepresented in computational literature. In this paper, we introduce <b>PKL-Bench</b>, the first "
        "comprehensive, research-grade benchmark dataset and evaluation harness for professional Kabaddi. Spanning all 10 complete "
        "seasons (2014–2024) of the Pro Kabaddi League (PKL), PKL-Bench harmonizes 1,060 matches, 26,760 player boxscores, and "
        "103,176 timestamped, discrete raid events into a standardized 5-tier relational schema distributed in both Apache Parquet "
        "and Frictionless CSV formats. We formulate Kabaddi as an asymmetric, discrete-time Markov Decision Process (MDP) exhibiting "
        "discrete structural phase transitions—including the bonus-line deactivation threshold (N_def = 6) and the super tackle "
        "regime (N_def ≤ 3). We establish a strict mathematical score conservation theorem, proving 100.0% accounting adherence "
        "across all 1,060 matches, and implement an out-of-sample temporal evaluation protocol (Train: Seasons 1–8, Validation: Season 9, "
        "Test: Season 10) preventing lookahead leakage. Finally, we provide standardized baseline implementations and leaderboards across "
        "four foundational tasks: discrete raid outcome prediction, dynamic in-game win probability modeling, pre-match spread forecasting, "
        "and context-adjusted player valuation. PKL-Bench is openly released under CC-BY-4.0 accompanied by a complete Gebru-compliant Datasheet."
    )
    elements.append(Paragraph(abstract_text, abstract_body))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#BDC3C7'), spaceBefore=2, spaceAfter=14))

    # 1. Introduction
    elements.append(Paragraph("1. Introduction", h1_style))
    elements.append(Paragraph(
        "Sports analytics has emerged as a fertile testbed for artificial intelligence, driving advances in multi-agent reinforcement learning (MARL), "
        "spatio-temporal tracking, and dynamic win probability modeling. However, modern research is overwhelmingly concentrated in association football, "
        "basketball, and cricket. These sports share fundamental structural symmetries: teams field equal numbers of players who freely transition between "
        "attack and defense on open playing surfaces.<br/><br/>"
        "In contrast, <b>Kabaddi</b>—an ancient contact sport originating on the Indian subcontinent that now draws over 230 million annual television viewers "
        "via the Pro Kabaddi League (PKL)—exhibits fundamentally distinct game-theoretic characteristics. Kabaddi is an <b>asymmetric, sequential zero-sum "
        "pursuit-evasion game</b>. In each raid, exactly one attacker (the raider) enters the opponent's territory to confront an organized defensive unit of "
        "N_def ∈ {1, ..., 7} players within a strict 30-second shot clock. The sport features rule-induced non-linearities: when the defense drops to ≤ 3 players, "
        "the payoff for a successful tackle doubles (Super Tackle); when two consecutive raids yield no points, the third raid triggers mandatory offensive execution (Do-or-Die).",
        body_style
    ))

    # Figure 1: Phase Transitions
    fig1_path = FIG_DIR / "fig1_phase_transitions.png"
    if fig1_path.exists():
        elements.append(Image(str(fig1_path), width=500, height=205))
        elements.append(Paragraph("<b>Figure 1:</b> Strategic Phase Transitions in Kabaddi. (Left) Empirical distribution of raid outcome categories across 103,176 events in PKL-Bench. (Right) Raider strike rate and super tackle probability as a function of defender count, highlighting the Bonus Line activation threshold and the Super Tackle regime.", caption_style))

    # 2. Dataset Architecture
    elements.append(Paragraph("2. Dataset Architecture & Multi-Tier Hierarchy", h1_style))
    elements.append(Paragraph(
        "PKL-Bench structures data into five relational tiers distributed in both <b>Apache Parquet</b> (compressed with Snappy, strongly typed) "
        "and <b>Frictionless CSV</b> formats:",
        body_style
    ))

    # Table: Dataset Summary
    table_data = [
        ["Tier", "Entity", "Rows", "Parquet Size", "CSV Size", "Description"],
        ["Tier 0", "Seasons", "10", "0.01 MB", "0.00 MB", "Seasons S1–S10, formats, champions & runners-up"],
        ["Tier 0", "Teams", "12", "0.00 MB", "0.00 MB", "12 franchise registries, codes, cities, debut years"],
        ["Tier 0", "Venues", "28", "0.00 MB", "0.00 MB", "Stadium directory, host cities, matches hosted"],
        ["Tier 1", "Players", "805", "0.03 MB", "0.04 MB", "Master athlete registry, roles, positions, career totals"],
        ["Tier 2", "Matches", "1,060", "0.06 MB", "0.22 MB", "Final scores, toss results, margins, point breakdowns"],
        ["Tier 3", "Boxscores", "26,760", "0.29 MB", "2.55 MB", "Player match stats (raids, tackles, super 10s, cards)"],
        ["Tier 4", "Play-by-Play", "103,176", "1.31 MB", "12.29 MB", "Sequential raid events (clocks, score diffs, outcomes)"],
    ]
    t1 = Table(table_data, colWidths=[45, 75, 45, 65, 60, 210])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (4, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9F9')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t1)
    elements.append(Paragraph("<b>Table 1:</b> Summary of PKL-Bench relational dataset tiers across 10 seasons.", caption_style))

    # Figure 4: Score Distributions
    fig4_path = FIG_DIR / "fig4_score_and_raid_distributions.png"
    if fig4_path.exists():
        elements.append(Image(str(fig4_path), width=500, height=205))
        elements.append(Paragraph("<b>Figure 2:</b> Empirical Scoring Dynamics Across 1,060 Matches. (Left) Total match points distribution (mean: 67.2 pts). (Right) Margin of victory distribution, demonstrating that over 32% of fixtures are decided by ≤ 5 points.", caption_style))

    # 3. Mathematical Score Conservation Law
    elements.append(Paragraph("3. Mathematical Score Conservation Law", h1_style))
    elements.append(Paragraph(
        "<b>Theorem 1 (Conservation of Kabaddi Scoring).</b> <i>In any regulation Kabaddi match, for each team i ∈ {1, 2}, "
        "the total score S_i is an exact linear sum of disjoint point sources:</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Total Score_i = Raid Points_i + Tackle Points_i + All-Out Points_i + Extra Points_i</b><br/>"
        "<i>where Raid Points_i = Touch_i + Bonus_i, Tackle Points_i = Capture_i + Super Tackle Bonus_i, and All-Out Points_i = 2 × All-Outs Inflicted_i.</i><br/><br/>"
        "<b>Empirical Verification:</b> We executed automated score conservation auditing across all 1,060 matches using <code>pkl_bench.validator</code>. "
        "The conservation theorem holds with <b>100.0% adherence</b> on both Team 1 and Team 2, with <b>0 discrepancies</b> flagged across the 10-season corpus.",
        body_style
    ))

    # 4. Benchmark Tasks & Leaderboard
    elements.append(Paragraph("4. Benchmark Tasks & Official Leaderboard", h1_style))
    elements.append(Paragraph(
        "To prevent lookahead data leakage, PKL-Bench enforces a strict chronological partition: "
        "<b>Train: Seasons 1–8 (787 matches)</b>, <b>Validation: Season 9 (137 matches)</b>, and <b>Test: Season 10 (136 matches)</b> held strictly out-of-sample.",
        body_style
    ))

    # Table: Leaderboard
    lb_data = [
        ["Benchmark Task", "Model", "Primary Metric", "Secondary Metric", "Tertiary Metric"],
        ["Task 1: Raid Outcome", "Majority Baseline", "Accuracy: 0.4770", "Macro-F1: 0.1292", "Log-Loss: 18.8520"],
        ["Task 1: Raid Outcome", "Multinomial Logistic", "Accuracy: 0.5107", "Macro-F1: 0.2186", "Log-Loss: 1.0705"],
        ["Task 1: Raid Outcome", "HistGradientBoosting", "Accuracy: 0.5319", "Macro-F1: 0.2328", "Log-Loss: 0.9804"],
        ["Task 2: Win Probability", "Logistic Leverage", "Brier: 0.2270", "ECE: 0.1882", "Log-Loss: 0.6446"],
        ["Task 2: Win Probability", "Calibrated GBDT", "Brier: 0.1991", "ECE: 0.1561", "Log-Loss: 0.5827"],
        ["Task 3: Match Forecasting", "Random Guess", "Accuracy: 0.5000", "Brier: 0.2500", "ROC-AUC: 0.5000"],
        ["Task 3: Match Forecasting", "Dynamic Kabaddi Elo", "Accuracy: 0.7059", "Brier: 0.1968", "ROC-AUC: 0.7707 (MAE: 9.23)"],
    ]
    t2 = Table(lb_data, colWidths=[110, 110, 95, 95, 90])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9F9')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t2)
    elements.append(Paragraph("<b>Table 2:</b> Official PKL-Bench Baseline Leaderboard evaluated on the unseen Season 10 test set.", caption_style))

    # Figure 2 & 3
    fig2_path = FIG_DIR / "fig2_win_prob_calibration.png"
    if fig2_path.exists():
        elements.append(Image(str(fig2_path), width=500, height=205))
        elements.append(Paragraph("<b>Figure 3:</b> In-Game Win Probability Dynamics (Task 2). (Left) Reliability calibration curves. (Right) Win probability trajectories for tight comeback vs decisive blowout matches.", caption_style))

    fig3_path = FIG_DIR / "fig3_elo_trajectories.png"
    if fig3_path.exists():
        elements.append(Image(str(fig3_path), width=480, height=240))
        elements.append(Paragraph("<b>Figure 4:</b> Franchise Elo Trajectories Across 10 Seasons (Task 3). Dynamic ratings of leading PKL franchises across 1,060 matches.", caption_style))

    # 5. Conclusion & Open Science
    elements.append(Paragraph("5. Conclusion & Open Science Release", h1_style))
    elements.append(Paragraph(
        "PKL-Bench establishes the first standardized, mathematically verified benchmark dataset for professional Kabaddi. "
        "By releasing this resource under <b>CC-BY-4.0</b> with reproducible baselines and strict temporal splits, we provide the computational "
        "research community with a fertile testbed for asymmetric game theory, multi-agent reinforcement learning, and calibrated sports analytics.<br/><br/>"
        "The complete dataset, Python SDK (<code>pip install -e .</code>), CLI evaluation harness, and documentation are available at: "
        "<b>https://github.com/Prompt-0/pkl-bench</b>.",
        body_style
    ))

    doc.build(elements)
    print(f"✓ Successfully compiled publication PDF: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_pdf()
