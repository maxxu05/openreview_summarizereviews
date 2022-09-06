# Summarizing Review Score for All Submissions for a Openreview Conference

This is a quick script for parsing through and summarizing the reviews of a conference hosted on Openreview. The script will print out the Mean Mean-Score-of-a-Submission, Median Mean-Score-of-a-Submission, Std Dev Mean-Score-of-a-Submission, as well as displaying a histogram visualization and saving the CSV of the tabulated scores of all non-withdrawn submissions.


<p align="center">
<img src="figs/hist_2022_09_06 .png" width=100% height=100%> 
</p>
<p> Visualization of Openreview Ratings for 2022 NeurIPS Dataset and Benchmarks Track Conference Papers </p>


## Installing dependencies

For this, we use [miniconda](https://docs.conda.io/en/latest/miniconda.html) to manage dependencies. After setting it up, you can install the environment:

    conda env create -f environment.yml
    conda activate openreview_summarizereviews

## Running Script

Run the script below. For other conferences, simply look up their corresponding invitation ID, and change line 18 in openreviews_parsing.py to it.

    python openreviews_parsing.py

