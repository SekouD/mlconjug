=======
History
=======


2.1.11 (2018-06-21)
-------------------

* Updated all provided pre-trained prediction models
    - The French Conjugator has accuracy of about 99.94% in predicting the correct conjugation class of a French verb. This is the baseline as i have been working on it for some time now.
    - The English Conjugator has accuracy of about 99.78% in predicting the correct conjugation class of an English verb. This is one of the biggest improvement since version 2.0.0
    - The Spanish Conjugator has accuracy of about 99.65% in predicting the correct conjugation class of a Spanish verb. It has also seen a sizable improvement since version 2.0.0
    - The Romanian Conjugator has accuracy of about 99.06% in predicting the correct conjugation class of a Romanian verb.This is by far the bigger gain. I modified the vectorizer to better take into account the morphological features or romanian verbs. (the previous score was about 86%, so it wil be nice for our romanian friends to have a trusted conjugator)
    - The Portuguese Conjugator has accuracy of about 96.73% in predicting the correct conjugation class of a Portuguese verb.
    - The Italian Conjugator has accuracy of about 94.05% in predicting the correct conjugation class of a Italian verb.



2.1.9 (2018-06-21)
------------------

* Now the Conjugator adds additional information to the Verb object returned.
    - If the verb under consideration is already in Verbiste, the conjugation for the verb is retrieved directly from memory.
    - If the verb under consideration is unknown in Verbiste, the Conjugator class now sets the boolean attribute 'predicted' and the float attribute confidence score to the instance of the Verb object the Conjugator.conjugate(verb) returns.
* Added `Type annotations`_ to the whole library for robustness and ease of scaling-out
* The performance of the Engish and Romanian Models have improved significantly lately. I guess in a few more iteration they will be on par with the French Model which is the best performing at the moment as i have been tuning its parameters for a caouple of year now. Not so much with the other languages, but if you update regularly you will see nice improvents in the 2.2 release.
* Enhanced the localization of the program.
* Now the user interface of mlconjug is avalaible in French, Spanish, Italian, Portuguese and Romanian, in addition to English.
* `All the documentation of the project`_ have been translated in the supported languages.


.. _Type annotations: https://github.com/python/typeshed
.. _All the documentation of the project: https://mlconjug.readthedocs.io/en/latest/


2.1.5 (2018-06-15)
------------------

* Added localization.
* Now the user interface of mlconjug is avalaible in French, Spanish, Italian, Portuguese and Romanian, in addition to English.


2.1.2 (2018-06-15)
------------------

* Added invalid verb detection.


2.1.0 (2018-06-15)
------------------

* Updated all language models for compatibility with scikit-learn 0.19.1.


2.0.0 (2018-06-14)
------------------

* Includes English conjugation model.
* Includes Spanish conjugation model.
* Includes Italian conjugation model.
* Includes Portuguese conjugation model.
* Includes Romanian conjugation model.


1.2.0 (2018-06-12)
------------------

* Refactored the API. Now a Single class Conjugator is needed to interface with the module.
* Includes improved french conjugation model.
* Added support for multiple languages.


1.1.0 (2018-06-11)
------------------

* Refactored the API. Now a Single class Conjugator is needed to interface with the module.
* Includes improved french conjugation model.


1.0.0 (2018-06-10)
------------------

* First release on PyPI.




