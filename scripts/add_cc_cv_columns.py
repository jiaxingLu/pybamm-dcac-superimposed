"""
One-shot data augmentation: add CC_min and CV_min columns to the master CSV.

Source: hand-extracted from MJ1 experimental docx (Day 7, 2026-04-26).
Target: data/figure1_master_table_cleaned.csv

Validation: CC_min + CV_min should equal total_time_min within ±0.1 min.
Run: python scripts/add_cc_cv_columns.py
"""
import re
from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# Hand-extracted CC and CV times from MJ1 docx (Day 7, 2026-04-26)
# Format: "Xmin Ys" or "X min Y s" — both accepted
# ---------------------------------------------------------------------------
RAW = """
0.1+0.9C 1τ:    459min42s    63min42s
0.1+0.2C 1τ:    556min29s    37min0s
0.2+0.3C 1τ:    252min11s    55min28s
0.2+0.3C 10τ:   236min22s    62min19s
0.2+0.3C 34.8τ: 248min01s    58min32s
0.2+0.8C 0.1τ:  229min39s    64min45s
0.2+0.8C 1τ:    226min31s    65min29s
0.2+0.8C 10τ:   212min37s    68min14s
0.3+0.7C 0.1τ:  156min33s    66min01s
0.3+0.7C 1τ:    149min34s    65min43s
0.3+0.7C 10τ:   142min40s    68min15s
0.3+0.4C 0.1τ:  158min23s    62min30s
0.3+0.4C 1τ:    157min42s    62min54s
0.3+0.4C 10τ:   153min42s    63min24s
0.4+0.6C 0.5τ:  113min07s    62min59s
0.4+0.5C 1.67τ: 113min03s    64min03s
0.4+0.6C 1.67τ: 112min57s    62min50s
0.4+0.6C 5τ:    106min30s    67min47s
0.4+0.6C 10τ:   107min03s    74min08s
0.5+0.5C 1τ:    88min55s     68min58s
0.9+0.1C 16.7τ: 48min28s     66min36s
0.9+0.1C 1.67τ: 48min47s     66min16s
0.9+0.1C 10τ:   48min16s     67min35s
0.9+0.1C 1τ:    49min05s     66min20s
0.1C_DC:        568min39s    24min26s
0.2C_DC:        275min56s    40min50s
0.3C_DC:        174min18s    49min24s
0.4C_DC:        127min12s    53min37s
0.5C_DC:        95min48s     63min10s
0.9C_DC:        49min29s     65min22s
"""

def parse_minsec(s: str) -> float:
    """Parse 'XminYs' or 'X min Y s' into decimal minutes."""
    s = s.strip().replace(" ", "")  # normalize whitespace
    m = re.match(r"^(\d+)min(\d+)s?$", s)
    if not m:
        raise ValueError(f"Cannot parse: {s!r}")
    minutes = int(m.group(1))
    seconds = int(m.group(2))
    return minutes + seconds / 60.0

def parse_table(raw: str) -> dict:
    """Returns {condition: (cc_min, cv_min)}."""
    out = {}
    for line in raw.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        # Format: "Condition: CC_str    CV_str"
        cond_part, time_part = line.split(":", 1)
        condition = cond_part.strip()
        # Two whitespace-separated time tokens
        parts = time_part.split()
        if len(parts) < 2:
            raise ValueError(f"Bad line (need 2 time tokens): {line!r}")
        cc_str, cv_str = parts[0], parts[1]
        out[condition] = (parse_minsec(cc_str), parse_minsec(cv_str))
    return out

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
CSV_PATH = Path("data/figure1_master_table_cleaned.csv")
assert CSV_PATH.exists(), f"Run from repo root. CSV not found: {CSV_PATH}"

# Parse the hand-extracted table
extracted = parse_table(RAW)
print(f"Parsed {len(extracted)} (condition, CC_min, CV_min) records from RAW.")

# Read the CSV
df = pd.read_csv(CSV_PATH)
print(f"Loaded CSV: {len(df)} rows.")

# Add columns
df["CC_min"] = pd.NA
df["CV_min"] = pd.NA

# Match by Condition column
n_matched = 0
warnings = []
for cond, (cc, cv) in extracted.items():
    mask = df["Condition"] == cond
    if mask.sum() == 0:
        warnings.append(f"NOT IN CSV: {cond!r}")
        continue
    if mask.sum() > 1:
        warnings.append(f"MULTI MATCH: {cond!r}")
        continue
    
    df.loc[mask, "CC_min"] = cc
    df.loc[mask, "CV_min"] = cv
    n_matched += 1
    
    # Validation: CC + CV ≈ total_time_min (within 0.1 min tolerance)
    total = df.loc[mask, "total_time_min"].iloc[0]
    if pd.notna(total):
        diff = abs((cc + cv) - total)
        if diff > 1.5:
            warnings.append(
                f"INCONSISTENT [{cond}]: CC+CV={cc+cv:.2f} vs total={total:.2f} "
                f"(Δ={diff:.2f} min)"
            )

print(f"\nMatched {n_matched}/{len(extracted)} conditions.")

if warnings:
    print(f"\n⚠ {len(warnings)} warning(s):")
    for w in warnings:
        print(f"  {w}")
else:
    print("\n✓ No warnings. All CC+CV consistent with total_time_min within 0.1 min.")

# Sanity preview
print("\nPreview (first 5 + last 5 rows):")
print(df[["Condition", "DC_C", "AC_C", "f_Hz", "CC_min", "CV_min", "total_time_min"]].head())
print()
print(df[["Condition", "DC_C", "AC_C", "f_Hz", "CC_min", "CV_min", "total_time_min"]].tail())

# Write back
df.to_csv(CSV_PATH, index=False)
print(f"\n✓ Written: {CSV_PATH}")
