=====
Usage
=====

To use MLConjug in a project with the provided pre-trained conjugation model::

    import mlconjug

    # To use mlconjug with the default parameters and a pre-trained conjugation model.
    default_conjugator = mlconjug.Conjugator()

    # Verify that the model works
    test1 = default_conjugator.conjugate("manger").conjug_info['indicative']['simple-past']['1p']
    test2 = default_conjugator.conjugate("partir").conjug_info['indicative']['simple-past']['1p']
    test3 = default_conjugator.conjugate("facebooker").conjug_info['indicative']['simple-past']['1p']
    test4 = default_conjugator.conjugate("astigratir").conjug_info['indicative']['simple-past']['1p']
    test5 = default_conjugator.conjugate("mythoner").conjug_info['indicative']['simple-past']['1p']
    print(test1)
    print(test2)
    print(test3)
    print(test4)
    print(test5)


To use MLConjug in a project and train a new model::

    # Specify which data files to use.
    path_verbs = "path/to/verbs-fr.xml"
    path_conjugations = "path/to/conjugation-fr.xml"

    # Create Verbiste instance
    verbiste = mlconjug.Verbiste(path_verbs, path_conjugations, subject='pronoun')

    # Set ngram range for the Feature Extractor
    ngrange = (2,7)

    # Transforms dataset with EndingountVectorizer. Only selects the verb's final ngrams.
    vectorizer = mlconjug.EndingCountVectorizer(analyzer="char", binary=True, ngram_range=ngrange)

    # Feature reduction
    feature_reductor = mlconjug.SelectFromModel(mlconjug.LinearSVC(penalty="l1", max_iter=16000, dual=False, verbose=2))

    #Prediction Classifier
    classifier = mlconjug.SGDClassifier(loss="log", penalty='elasticnet', max_iter=8000, alpha=1e-5, random_state=42)

    # Initialize Conjugator
    model = mlconjug.Model(vectorizer, feature_reductor, classifier)
    conjugator = mlconjug.Conjugator(model, verbiste)

    #Training and prediction
    conjugator.model.train(conjugator.data_set.train_input, conjugator.data_set.train_labels)
    predicted = conjugator.model.predict(conjugator.data_set.test_input)
    scores = {}
    scores['precision'] = mlconjug.precision_recall_fscore_support(my_data_set.test_labels, predicted)[0]
    print(scores['precision'])

    # Verify that the model works
    test1 = default_conjugator.conjugate("manger").conjug_info['indicative']['simple-past']['1p']
    test2 = default_conjugator.conjugate("partir").conjug_info['indicative']['simple-past']['1p']
    test3 = default_conjugator.conjugate("facebooker").conjug_info['indicative']['simple-past']['1p']
    test4 = default_conjugator.conjugate("astigratir").conjug_info['indicative']['simple-past']['1p']
    test5 = default_conjugator.conjugate("mythoner").conjug_info['indicative']['simple-past']['1p']
    print(test1)
    print(test2)
    print(test3)
    print(test4)
    print(test5)

    # Save trained model
    with open('path/to/save/data/trained_model-fr.pickle', 'wb') as file:
        pickle.dump(conjugator.model, file)


To use MLConjug from the command line::

    $ mlconjug <verb> options

