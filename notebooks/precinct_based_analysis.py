from pyspark.sql.functions import col
import matplotlib.pyplot as plt

def violating_precicts(nyc_data, print_enable = False):
    nyc_precints = nyc_data.select('violation_precinct')\
                           .groupBy('violation_precinct')\
                           .agg({'violation_precinct':'count'})\
                           .sort('count(violation_precinct)', ascending=False)
    if print_enable:
        nyc_precints.show(5)

    return nyc_precints.take(5)

def issuing_precincts(nyc_data, print_enable = False):
    nyc_precints = nyc_data.select('issuer_precinct')\
                           .groupBy('issuer_precinct')\
                           .agg({'issuer_precinct':'count'})\
                           .sort('count(issuer_precinct)', ascending=False)
    if print_enable:
        nyc_precints.show(5)
    return nyc_precints.take(5)

def violation_code_frequency_top3_precincts(nyc_data, print_enable = False):
    top3_precints = nyc_data.select('issuer_precinct')\
                           .groupBy('issuer_precinct')\
                           .agg({'issuer_precinct':'count'})\
                           .sort('count(issuer_precinct)', ascending=False)\
                           .take(3)
    top3 = [row['issuer_precinct'] for row in top3_precints]
    filtered_data = nyc_data.filter((col('issuer_precinct') == top3[0]) | (col('issuer_precinct') == top3[1]) | (col('issuer_precinct') == top3[2]))
    violation_frequencies = filtered_data.select('violation_code')\
                                         .groupBy('violation_code')\
                                         .agg({'violation_code':'count'})\
                                         .collect()
    if print_enable:
        violations = [row['violation_code'] for row in violation_frequencies]
        frequencies = [row['count(violation_code)'] for row in violation_frequencies]

        fig, ax = plt.subplots(1, 1, figsize=(20,10))
        ax.set_title("Violations Vs Frequencies")
        ax.set_xlabel("Violations")
        ax.set_ylabel("Frequencies")
        ax.bar(violations, frequencies)

    return violation_frequencies
