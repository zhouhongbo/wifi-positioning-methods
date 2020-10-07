This folder contains the WiFi RSS fingerprint data described in <Long-Term Wi-Fi fingerprinting dataset for robust indoor positioning,G.M. Mendoza-Silva et al., 2017> and available at Zenodo repository, DOI 10.5281/zenodo.1066041.

* Each subfolder contains the measurements of each dataset that belongs to a collection month.
* Each dataset is represented by four files: the RSS, the time, the coordinates, and the identifiers files, so that the ith row of each of them holds the respective information of the ith fingerprint of the dataset.
* Each column in the RSS file represents intesity measurement values (dBm) for a specific wireless access point. If the access point was not detected for a fingerprint, its intensity value is 100 in that fingerprint.
* The naming convention for representing a dataset is 'dddnnttt.csv', where ddd is either 'trn' (training) or 'tst' (test), nn is two a two digit number (e.g., '01'), and ttt is the dataset' information contained in the file, which can be 'rss' for a RSS information file, 'crd' for coordinates file, 'tms' for the time file, and 'ids' for the identifiers file.
* Most of samples were collected using a Samsung Galaxy S3 smartphone. Only files corresponding to training 2 and tests 6-10 from month 25 were collected using a Samsung Galaxy A5 (2017) smartphone.
