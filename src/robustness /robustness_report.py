def robustness_table(rows, metric="accuracy"):
    return [{"noise_level": row.get("noise_level"), metric: row.get(metric)} for row in rows if float(row.get("missing_rate",0.0)) == 0.0 and float(row.get("segment_fraction",0.0)) == 0.0]
