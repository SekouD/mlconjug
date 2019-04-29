=====
Usage
=====

.. NOTE:: The default language is French.
    When called without specifying a language, the library will try to conjugate the verb in French.

To use MLConjug in a project with the provided pre-trained conjugation models::

    import mlconjug

    # To use mlconjug with the default parameters and a pre-trained conjugation model.
    default_conjugator = mlconjug.Conjugator(language='fr')

    # Verify that the model works
    test1 = default_conjugator.conjugate("manger").conjug_info['Indicatif']['Passé Simple']['1p']
    test2 = default_conjugator.conjugate("partir").conjug_info['Indicatif']['Passé Simple']['1p']
    test3 = default_conjugator.conjugate("facebooker").conjug_info['Indicatif']['Passé Simple']['1p']
    test4 = default_conjugator.conjugate("astigratir").conjug_info['Indicatif']['Passé Simple']['1p']
    test5 = default_conjugator.conjugate("mythoner").conjug_info['Indicatif']['Passé Simple']['1p']
    print(test1)
    print(test2)
    print(test3)
    print(test4)
    print(test5)

    # You can now iterate over all conjugated forms of a verb by using the newly added Verb.iterate() method.
    default_conjugator = mlconjug.Conjugator(language='en')
    test_verb = default_conjugator.conjugate("be")
    all_conjugated_forms = test_verb.iterate()
    print(all_conjugated_forms)

To use MLConjug in a project and train a new model::

    # Set a language to train the Conjugator on
    lang = 'fr'

    # Set a ngram range sliding window for the vectorizer
    ngrange = (2,7)

    # Transforms dataset with CountVectorizer. We pass the function extract_verb_features to the CountVectorizer.
    vectorizer = mlconjug.CountVectorizer(analyzer=partial(mlconjug.extract_verb_features, lang=lang, ngram_range=ngrange),
                                 binary=True)

    # Feature reduction
    feature_reductor = mlconjug.SelectFromModel(mlconjug.LinearSVC(penalty="l1", max_iter=12000, dual=False, verbose=0))

    # Prediction Classifier
    classifier = mlconjug.SGDClassifier(loss="log", penalty='elasticnet', l1_ratio=0.15, max_iter=4000, alpha=1e-5, random_state=42, verbose=0)

    # Initialize Data Set
    dataset = mlconjug.DataSet(mlconjug.Verbiste(language=lang).verbs)
    dataset.construct_dict_conjug()
    dataset.split_data(proportion=0.9)

    # Initialize Conjugator
    model = mlconjug.Model(vectorizer, feature_reductor, classifier)
    conjugator = mlconjug.Conjugator(lang, model)

    #Training and prediction
    conjugator.model.train(dataset.train_input, dataset.train_labels)
    predicted = conjugator.model.predict(dataset.test_input)

    # Assess the performance of the model's predictions
    score = len([a == b for a, b in zip(predicted, dataset.test_labels) if a == b]) / len(predicted)
    print('The score of the model is {0}'.format(score))

    # Verify that the model works
    test1 = conjugator.conjugate("manger").conjug_info['Indicatif']['Passé Simple']['1p']
    test2 = conjugator.conjugate("partir").conjug_info['Indicatif']['Passé Simple']['1p']
    test3 = conjugator.conjugate("facebooker").conjug_info['Indicatif']['Passé Simple']['1p']
    test4 = conjugator.conjugate("astigratir").conjug_info['Indicatif']['Passé Simple']['1p']
    test5 = conjugator.conjugate("mythoner").conjug_info['Indicatif']['Passé Simple']['1p']
    print(test1)
    print(test2)
    print(test3)
    print(test4)
    print(test5)

    # Save trained model
    with open('path/to/save/data/trained_model-fr.pickle', 'wb') as file:
        pickle.dump(conjugator.model, file)


To use MLConjug from the command line::

    $ mlconjug manger

    $ mlconjug bring -l en

    $ mlconjug gallofar --language es

