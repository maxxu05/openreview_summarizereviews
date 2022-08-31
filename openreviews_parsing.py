import openreview
import numpy as np
import matplotlib.pyplot as plt

# https://openreview-py.readthedocs.io/en/latest/ 
# https://readthedocs.org/projects/openreview-py-dm-branch/downloads/pdf/latest/
# https://docs.openreview.net/getting-started/using-the-api/installing-and-instantiating-the-python-client

client = openreview.Client(baseurl='https://api.openreview.net')


papers = {}
# Find invitation ID by running
# print(client.get_group(id='venues').members)
submissions = client.get_all_notes(invitation="NeurIPS.cc/2022/Track/Datasets_and_Benchmarks/-/Submission", details='directReplies')
# import pdb; pdb.set_trace()
for submission in submissions:
    reviews = []
    for review in submission.details['directReplies']:
        if 'rating' in review['content']:
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

# Visualize results
plt.hist(allRatingsMeans, bins=100)
plt.show(block=True)

# Write to spreadsheet for sanity check
handle = open('openreview_ratings.csv', 'w')
handle.write("Title,Mean,Median,StDev," + "Rating,Confidence,"*8 + "\n")
for title in papers:
    stuff = str(papers[title])
    stuff = stuff.replace("(","").replace(")","").replace("[","").replace("]","")
    handle.write(title.replace("\n","").replace(",","") + "," + stuff + "\n")
handle.close()

