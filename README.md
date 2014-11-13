##**README**

___Data___ | 
- ***input.csv***
    - This file contains the information provided by crowdworkers.  The five fields are _Name_, _ Humor_, _Appropriate_, _Grammar_, and _Tweet_.  
        -   _Name_ - the worker identifier assigned by the crowdsourcing platform
        -   _Humor_ - a subjective rating of the tweet's comic appeal ranging from 1 to 5
        -   _Appropriate_ - a subjective rating intended to quantify the age bracket for which the tweet is appropiate.  Explicit language, gore, and other similar factors are taken into account.  The rating ranged from 1 to 5.
        -   _Grammar_ - an overall score intended to rate how gramatically correct a tweet is. 
        -   _Tweet_ - the drafted tweet submitted for evaluation by the user
- ***labels.csv***
    - Rather than indexing by worker, this file indexes by _Tweet_ _ID_.  The data fields are _Tweet_ _ID_, _Humor_, _Appropriate_, and _Grammar_.
        - _Tweet_ID_ - a unique identifier atributed to each tweet
        - _Humor_, _Appropriate_, and _Grammar_ are the same metrics used in _input.csv_.
- ***tweet_keys.txt***
    - This file matches tweets to their IDs.  Each tweet is assigned a specific ID because putting the entire tweet in output files could create formatting problems.
- ***worker_quality.csv***
    - This file contains the output of  *quality_control_module.py* and has the _Name_ and _Quality_ fields.
   
        

___src___ | 
- *agregation_module.py*
    - Using a dictionary in Python, this program reads in data from ___input.csv___ and stores each _tweet_ as a key to another dictionary containing the  _Humor_, _Appropriate_, and _Grammar_ scores. It writes ___tweet_keys.txt___  and ___labels.csv___. 
- *quality_control_module.py*
    - This program reads in ___tweet_keys.txt___  and ___labels.csv___ and uses the values to calculate worker quality. 
    - __labels__[_tweets_[ wi ]_] = [1 / ( _| _tweets_[ _wi_] _|_ )]  * Σ (h, a, g ∈ _tweets_[ _wi_]), where w_i_ is the _i_ th worker; tweets is the list of tweets for each worker; and _h_, _a_, and _g_ are the data fields _Humor_, _Appropriate_, and _Grammar_.  The output of this is a dictionary with the average scores for  _Humor_, _Appropriate_, and _Grammar_.
    - _qualities_[ _wi_] _=_ [ Σ tweets[wi],(h,a,g)) ] / [(Σ labels[wi],(h,a,g)) - ( Σ tweets[ _wi_ ],(h,a,g))]



