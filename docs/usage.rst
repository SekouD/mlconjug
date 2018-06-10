=====
Usage
=====

To use MLConjug in a project::

    import mlconjug
    import pickle

    # Specify which data files to use.
    path_verbs = "path/to/verbs-fr.xml"
    path_conjugations = "path/to/conjugation-fr.xml"

    # Create Verbiste instance
    verbiste = mlconjug.Verbiste(path_verbs, path_conjugations, subject='pronoun')

    my_data_set = mlconjug.DataSet(verbiste)
    my_data_set.construct_dict_conjug()
    my_data_set.split_data()

    # Set ngram range
    ngrange = (2,7)

    # Transforms dataset with EndingountVectorizer. Only selects the verb final ngrams.
    vectorizer = mlconjug.EndingCountVectorizer(analyzer="char", binary=True, ngram_range=ngrange)

    # Feature reduction
    feature_reductor = mlconjug.SelectFromModel(mlconjug.LinearSVC(penalty="l1", max_iter=3000, dual=False, verbose=2))

    #Prediction Model
    classifier = mlconjug.SGDClassifier(loss="log", penalty='elasticnet', alpha=1e-5, random_state=42)

    # Initialise ML model for Verbiste
    verbiste.set_model(mlconjug.Model(vectorizer, feature_reductor, classifier))

    #Training and prediction
    verbiste.model.train(my_data_set.liste_verbes, my_data_set.liste_templates)
    predicted = verbiste.model.predict(my_data_set.test_input)
    scores = {}
    scores['precision'], scores['recall'], scores['fbeta-score'], scores['support'] = precision_recall_fscore_support(my_data_set.test_labels, predicted)
    print(scores['precision'])

    # Verify that the model works
    print(verbiste.conjugate("manger").verb_info.template)
    print(verbiste.conjugate("aimer").verb_info.template)
    print(verbiste.conjugate("alabareter").verb_info.template)
    print(verbiste.conjugate("croustiparatir").verb_info.template)
    print(verbiste.conjugate("strobanguer").verb_info.template)
    print(verbiste.conjugate("facebooker").verb_info.template)

    # Save trained model
    with open('path/to/save/model.pickle', 'wb') as file:
        pickle.dump(verbiste.model, file)


To use MLConjug from the command line::

    $ mlconjug <verb> options

