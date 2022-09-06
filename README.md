# Summarizing Review Score for All Submissions for a Openreview Conference

This is a quick script for parsing through and summarizing the reviews of a conference hosted on Openreview. Currently the code is set up for the 2022 NeurIPS Dataset and Benchmarks Track, but it can be easily modified by changing the invitiation ID in the script. 


<p align="center">
<img src="figs/hist_2022_09_06/.png" width=75% height=75%> 
</p>
<p> Visualization of Openreview Ratings for 2022 NeurIPS Dataset and Benchmarks Track Conference Papers </p>


## Installing dependencies

For this, we use [miniconda](https://docs.conda.io/en/latest/miniconda.html) to manage dependencies. After setting it up, you can install the environment:

    conda env create -f environment.yml
    conda activate openreview_summarizereviews

## Running Script

Run the script below. For other conferences, simply look up their corresponding invitation ID, and change line 18 in openreviews_parsing.py to it.

    python openreviews_parsing.py

