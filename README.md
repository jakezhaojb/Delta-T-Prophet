Delta-T-Prophet
=======================================

Introduction
----------------
##### Prophet is a data-analysis tool provided by Delta-T, turning Big Data into insight during graduate programs application.

Primary targets:<br /> 
1. Crawling __grad cafe__ alike websites containing large amounts of application results. <br />
2. Applying Big Data techniques to analyze or visualize the data crawled.<br />
3. Predicting and recommending programs by Machine Learning.<br />

Installation
---------------
python 2.7.5 is recommended and python 3 will not be compatible.<br />
[DPark](https://github.com/douban/dpark) is also recommended for speeding up Prophet. DPark is a MapReduce alike computing framework, which could crawl websites and process data with a parallel style locally or on a [Mesos](http://mesos.apache.org/) cluster.

File format
---------------
e.g "163/169/5.00,3.75,MS,F14,Mar/2014,1"     
###### Take above two lines as examples, both of which can be splited into several sub-string:     
    163/169/5.00 denotes GRE General test, which is indexed by Verbal/Quantitative/A-Writing    
    3.75 is Undergraduted GPA supplied by applicants     
    MS or PhD is the level applied    
    F14 is the abbreviation for Fall 2014, and 'S' will be Spring    
    Mar/2014 is the date applicants are notified    
    1 can be seen as a boolearn variable. True will be Accepted and False Rejected.
