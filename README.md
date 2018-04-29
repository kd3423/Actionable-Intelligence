# Actionable-Intelligence
Extracting Actionable Intelligence from e-commerce product reviews

## Flow to run the scripts for Frequent features, Opinion words and Infrequent features
Given you have data in same format as all_reviews.csv
```
$ check_senti.py
```
This script will create pos_tags and also give polarity score for each review, all of which will be saved to a txt file

NEXT
```
$ make_transaction.py
```
This will create the required file for apriorCBA

NEXT
```
$ apriorCBA.py
```
This script will find the frequent features and save the list in a txt file

NEXT
```
$ getOpinionWords.py
```
This script will get all the opinion words based on the frequent features list and save the list to txt file

NEXT
```
$ getInfrequentFeatures.py
```
This script will get all the infrequent features from the reviews and save them to a txt file


