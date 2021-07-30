# A data set for a particular model has a large number of features. We suspect that not all of them are useful.
# Gathering the feature scores for the resulting model has confirmed our suspicions. Feature extraction for
# this data set takes a long time but training the model is fairly quick. We need to deliver the model soon, so we've
# decided to just remove from the data set the features that have no value, and then retrain the model.
#
# This script removes all feature data which has been found to add no value. It takes a file containing the original
# feature data and, using a file containing scores for each feature with a score > 0, creates a new feature file with
# the masked feature data.
#
# Assumptions about the feature data:
# 1. Feature data row format is a comma-separated list:
#           ID, label, feature 0 value,..., feature n value
#    where all feature values are float
# 2. All rows have the same number of values
# 3. The resulting output file must contain the ID and label in addition to the masked features
#
# Assumptions about the feature score data:
# 1. A feature score row is of the following format:
#       f<0-based feature number> <score>
#   For example:
#       f590 1912.0991193927057
# 2. Only features with a non-zero score will be present in the file
# 3. The rows in the file are ordered by highest-scoring feature to lowest non-zero-scoring feature

import argparse
import pandas
import numpy.ma as ma

# ID, label, and a bunch of vales for that feature in each row.
# ID, feature score (sorted descending)

def apply_feature_mask(feature_data_file, feature_score_file, output_file):
    # Merge the data frames on ID (like a left join in SQL).
    interim = pd.merge(feature_data_file, feature_score_file, how='"left", on="ID")
    # Split the feature score into its own column.
    for i in range(len(interim['score'])):
        interim['score_only'][i] = interim['score'][i].split(' ')[1:]
    interim2 = ma.masked_equal(interim['score_only'], NaN) # Mask the NaN values in score_only
    interim2 = ma.mask_rows(interim) # Mask entire rows with masks from above
    interim2['ID'] = interim['ID']
    interim2['label'] = interim['label']
    intermin2.to_csv(output_file)   # Generate the output file.


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--feature-score-file', type=str, required=True, help='File containing feature scores'
    )
    parser.add_argument(
        '-f', '--feature-data-file', type=str, required=True, help='File containing unmasked feature data'
    )
    parser.add_argument('-o', '--output-file', type=str, required=True,
                        help='Output file containing masked feature data')
    args = parser.parse_args()

    kwargs = {}
    kwargs['feature_data_file'] = args.feature_data_file
    kwargs['feature_score_file'] = args.feature_score_file
    kwargs['output_file'] = args.output_file

    apply_feature_mask(**kwargs)
