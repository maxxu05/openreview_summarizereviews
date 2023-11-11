import openreview
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime
import os

# https://openreview-py.readthedocs.io/en/latest/ 
# https://readthedocs.org/projects/openreview-py-dm-branch/downloads/pdf/latest/
# https://docs.openreview.net/getting-started/using-the-api/installing-and-instantiating-the-python-client

client = openreview.Client(baseurl='https://api.openreview.net')


papers = {}
# Find invitation ID by running
# print(client.get_group(id='venues').members) # NeurIPS.cc/2022/Track/Datasets_and_Benchmarks/-/Submission
# submissions = client.get_all_notes(invitation="ICLR.cc/2024/Conference/-/Blind_Submission", details='directReplies')
client = openreview.Client(baseurl='https://api2.openreview.net')
submissions = client.get_all_notes(invitation="ICLR.cc/2024/Conference/-/Submission", details='directReplies')
# import pdb; pdb.set_trace()
listofreviewers = set()
for submission in submissions:
    reviews = []
    for review in submission.details['directReplies']:
        if 'rating' in review['content']:
            if review["signatures"][0][-4:] not in listofreviewers:
                listofreviewers.add(review["signatures"][0][-4:])
            else:
                print(review["signatures"][0][-4:])
                import pdb; pdb.set_trace()
            rating = int(review['content']['rating'].split(':')[0])
            confidence = int(review['content']['confidence'].split(':')[0])
            aTup = rating,confidence
            reviews.append(aTup)
    papers[submission.content['title']] = reviews

# Stats Calculation
allRatings = []
allRatingsMeans = []
for paper in papers:
    ratingsList = []
    for pair in papers[paper]:
        ratingsList.append(pair[0])

    #paper specific statistics
    mean = np.mean(ratingsList)
    median = np.median(ratingsList)
    stdev = np.std(ratingsList)

    statsTup = mean, median, stdev
    papers[paper].insert(0, statsTup)
    allRatingsMeans.append(mean)

overallMean = np.mean(allRatingsMeans)
overallMedian = np.median(allRatingsMeans)
overallStdev = np.std(allRatingsMeans)
print(f"Mean, Mean Paper Rating: {overallMean}")
print(f"Median, Mean Paper Rating: {overallMedian}")
print(f"Standard Deviation of Mean Paper Rating: {overallStdev}")
print(f"Total Nonwithdrawn Papers: {len(allRatingsMeans)}")


# Write to spreadsheet
if not os.path.exists("csvs"):
    os.makedirs("csvs")
handle = open(f"csvs/openreview_ratings_{datetime.today().strftime('%Y_%m_%d')}.csv", 'w')
handle.write("Title,Mean,Median,StDev," + "Rating,Confidence,"*8 + "\n")
for title in papers:
    stuff = str(papers[title])
    stuff = stuff.replace("(","").replace(")","").replace("[","").replace("]","")
    handle.write(title.replace("\n","").replace(",","") + "," + stuff + "\n")
handle.close()


# Visualize results
fig, ax = plt.subplots(figsize=(20,10))

counts, bins, patches = ax.hist(allRatingsMeans, bins=50)
# Set the ticks to be at the edges of the bins.
ax.set_xticks(bins)
# Set the xaxis's tick labels to be formatted with 1 decimal place...
ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

# Label the raw counts and the percentages below the x-axis...
bin_centers = 0.5 * np.diff(bins) + bins[:-1]
for count, x in zip(counts, bin_centers):
    # Label the raw counts
    ax.annotate(str(int(count)), xy=(x, 0), xycoords=('data', 'axes fraction'),
        xytext=(0, -18), textcoords='offset points', va='top', ha='center')

    # Label the percentages
    percent = '%0.0f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
        xytext=(0, -32), textcoords='offset points', va='top', ha='center')

if not os.path.exists("figs"):
    os.makedirs("figs")
plt.savefig(f"figs/hist_{datetime.today().strftime('%Y_%m_%d')}.png")
plt.show(block=True)
