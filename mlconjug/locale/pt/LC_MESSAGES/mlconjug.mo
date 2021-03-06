��    %      D  5   l      @  �   A    �  �     �   �  �   ]  �   >  �   �  �   �  �   �	  �   e
    7  �   V  r    �  �  �     x   �  .  4  a  c  6   �  5   �  6   2  9   i  7   �  6   �        +  �   8  �    �   �  &  �  H  �     .   l   K   -   �   2   �   G   !  s  a!  �   �"  *  �#  �   �$  �   z%  �   ?&  �   ='    �'    �(  �   *  �   �*  ]  �+  �   "-  �  .  �  �/  �   1  �   2  Z  �2  �  �3  7   �6  5   �6  5   $7  7   Z7  4   �7  5   �7  9  �7  '  79  �   _:    G;    J=  L  j>  �  �@  "   >C  l   aC  .   �C  9   �C  E   7D                                                            !          
                     $            #   "       %                                           	                       
        Assigns the provided pre-trained scikit-learn model to be able to conjugate unknown verbs.

        :param model: scikit-learn Classifier or Pipeline.

         
        Gets conjugation information corresponding to the given template.

        :param template: string.
            Name of the verb ending pattern.
        :return: OrderedDict or None.
            OrderedDict containing the conjugated suffixes of the template.

         
        Gets verb information and returns a VerbInfo instance.

        :param verb: string.
            Verb to conjugate.
        :return: VerbInfo object or None.

         
        Load and parses the conjugations from xml file.

        :param conjugations_file: string or path object.
            Path to the conjugation xml file.

         
        Load and parses the inflected forms of the tense from xml file.

        :param tense: string.
            The current tense being processed.
        :return: list.
            List of conjugated suffixes.

         
        Load and parses the verbs from xml file.

        :param verbs_file: string or path object.
            Path to the verbs xml file.

         
        Parses XML file

        :param file: FileObject.
            XML file containing the conjugation templates
        :return: OrderedDict.
            An OrderedDict containing all the conjugation templates in the file.

         
        Parses XML file

        :param file: FileObject.
            XML file containing the verbs.
        :return: OrderedDict.
            An OrderedDict containing the verb and its template for all verbs in the file.

         
        Parses a verb and returns the ending ngrams.

        :param verb: string.
            Verb to vectorize.
        :return: list.
            Final ngrams of the verb.
         
        Predicts the conjugation class of the provided list of verbs.

        :param verbs: list.
            List of verbs.
        :return: list.
            List of predicted conjugation groups.

         
        Splits the data into a training and a testing set.

        :param threshold: int.
            Minimum size of conjugation class to be split.
        :param proportion: float.
            Proportion of samples in the training set.
            Must be between 0 and 1.

         
        Trains the model on the supplied samples and labels.

        :param samples: list.
            List of verbs.
        :param labels: list.
            List of verb templates.

         
        | Checks if the verb is a valid verb in the given language.
        | English words are always treated as possible verbs.
        | Verbs in other languages are filtered by their endings.

        :param verb: string.
            The verb conjugate.
        :return: bool.
            True if the verb is a valid verb in the language. False otherwise.

         
        | Detects the allowed endings for verbs in the supported languages.
        | All the supported languages except for English restrict the form a verb can take.
        | As English is much more productive and varied in the morphology of its verbs, any word is allowed as a verb.

        :return: set.
            A set containing the allowed endings of verbs in the target language.

         
        | Populates the dictionary containing the conjugation templates.
        | Populates the lists containing the verbs and their templates.

         
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.

         
        | Populates the inflected forms of the verb.
        | This is the generic version of this method.
        | It does not add personal pronouns to the conjugated forms.
        | This method can handle any new language if the conjugation structure conforms to the Verbiste XML Schema.

         
        | This is the main method of this class.
        | It first checks to see if the verb is in Verbiste.
        | If it is not, and a pre-trained scikit-learn model has been supplied, the method then calls the model
        to predict the conjugation class of the provided verb.

        | Returns a Verb object or None.

        :param verb: string.
            Verb to conjugate.
        :param subject: string.
            Toggles abbreviated or full pronouns.
            The default value is 'abbrev'.
            Select 'pronoun' for full pronouns.
        :return: Verb object or None.

         
    This class defines the English Verb Object.

     
    This class defines the French Verb Object.

     
    This class defines the Italian Verb Object.

     
    This class defines the Portuguese Verb Object.

     
    This class defines the Romanian Verb Object.

     
    This class defines the Spanish Verb Object.

     
    This class defines the Verb Object.

    :param verb_info: VerbInfo Object.
    :param conjug_info: OrderedDict.
    :param subject: string.
        Toggles abbreviated or full pronouns.
        The default value is 'abbrev'.
        Select 'pronoun' for full pronouns.

     
    This class defines the Verbiste verb information structure.

    :param infinitive: string.
        Infinitive form of the verb.
    :param root: string.
        Lexical root of the verb.
    :param template: string.
        Name of the verb ending pattern.

     
    This is the class handling the Verbiste xml files.

    :param language: string.
    | The language of the conjugator. The default value is fr for French.
    | The allowed values are: fr, en, es, it, pt, ro.

     
    | Custom Vectorizer optimized for extracting verbs features.
    | The Vectorizer subclasses sklearn.feature_extraction.text.CountVectorizer .
    | As in Indo-European languages verbs are inflected by adding a morphological suffix,
    the vectorizer extracts verb endings and produces a vector representation of the verb with binary features.

    | The features are the verb ending ngrams. (ngram_range is set at class instanciation).

     
    | This class holds and manages the data set.
    | Defines helper functions for managing Machine Learning tasks like constructing a training and testing set.

    :param VerbisteObj:
        Instance of a Verbiste object.

     
    | This class manages the scikit-learn model.
    | The Pipeline includes a feature vectorizer, a feature selector and a classifier.
    | If any of the vectorizer, feature selector or classifier is not supplied at instance declaration,
    the __init__ method will provide good default values that get more than 92% prediction accuracy.

    :param vectorizer: scikit-learn Vectorizer.
    :param feature_selector: scikit-learn Classifier with a fit_transform() method
    :param classifier: scikit-learn Classifier with a predict() method

     
    | This is the main class of the project.
    | The class manages the Verbiste data set and provides an interface with the scikit-learn model.
    | If no parameters are provided, the default language is set to french and the pre-trained french conjugation model is used.
    | The class defines the method conjugate(verb, language) which is the main method of the module.

    :param language: string.
        Language of the conjugator. The default language is 'fr' for french.
    :param model: string.
        A user provided model if the user has trained his own model.

     Console script for mlconjug. The language for the conjugation model. The values can be fr, en, es, it, pt or ro. The default value is fr. The split proportion must be between 0 and 1. The supplied word: {0} is not a valid verb in {1}. Unsupported language.
The allowed languages are fr, en, es, it, pt, ro. Project-Id-Version: 
POT-Creation-Date: 2018-06-15 21:51+0200
PO-Revision-Date: 2018-06-16 18:32+0200
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
X-Generator: Poedit 2.0.8
Last-Translator: SekouD <sekoud.python@gmail.com>
Plural-Forms: nplurals=2; plural=(n != 1);
Language: pt
 
        Atribui o modelo scikit-learn pré-treinado fornecido para poder conjugar verbos desconhecidos.

        :param model: scikit-learn Classifier or Pipeline.

         
        Obtém informações de conjugação correspondentes ao modelo fornecido.

        :param template: string.
            Nome do padrão final do verbo.
        :return: OrderedDict or None.
            OrderedDict contendo os sufixos conjugados do modelo.

         
        Obtém informações verbais e retorna uma instância de VerbInfo.

        :param verb: string.
            Verbo para conjugar.
        :return: VerbInfo object or None.

         
        Carregue e analise as conjugações do arquivo xml.

        :param conjugations_file: string or path object.
            Caminho para o arquivo xml de conjugação.

         
        Carregue e analise os formulários flexionados do tempo do arquivo xml.

        :param tense: string.
            O tempo atual sendo processado.
        :return: list.
            Lista de sufixos conjugados.

         
        Carregue e analise os verbos do arquivo xml.

        :param verbs_file: string or path object.
            Caminho para o arquivo xml de verbos.

         
        Analisa o arquivo XML

        :param file: FileObject.
            Arquivo XML contendo os modelos de conjugação
        :return: OrderedDict.
            Um OrderedDict contendo todos os modelos de conjugação no arquivo.

         
        Analisa o arquivo XML

        :param file: FileObject.
            Arquivo XML contendo os verbos.
        :return: OrderedDict.
            Um OrderedDict contendo o verbo e seu modelo para todos os verbos no arquivo.

         
        Analisa um verbo e retorna os n-grams finais.

        :param verb: string.
            Verbo para vetorizar.
        :return: list.
            N-grams finais do verbo.
         
        Prevê a classe de conjugação da lista de verbos fornecida.

        :param verbs: list.
            Lista de verbos
        :return: list.
            Lista de grupos de conjugação previstos.

         
        Divide os dados em um treinamento e um conjunto de testes.

        :param threshold: int.
            Tamanho mínimo da classe de conjugação a ser dividida.
        :param proportion: float.
            Proporção de amostras no conjunto de treinamento.
            Deve estar entre 0 e 1.

         
        Treina o modelo nas amostras e rótulos fornecidos.

        :param samples: list.
            Lista de verbos
        :param labels: list.
            Lista de modelos de verbos.

         
        | Verifica se o verbo é um verbo válido no idioma dado.
        | As palavras inglesas são sempre tratadas como verbos possíveis.
        | Verbos em outros idiomas são filtrados por seus finais.

        :param verb: string.
            O verbo conjugado
        :return: bool.
            True se o verbo for um verbo válido no idioma. False em contrário.

         
        | Detecta as terminações permitidas para verbos nos idiomas suportados.
        | Todos os idiomas suportados, exceto o inglês, restringem a forma que um verbo pode receber.
        | Como o inglês é muito mais produtivo e variado na morfologia de seus verbos, qualquer palavra é permitida como verbo.

        :return: set.
            Um conjunto contendo as terminações permitidas de verbos no idioma de destino.

         
        | Preenche o dicionário que contém os modelos de conjugação.
        | Preenche as listas que contêm os verbos e seus modelos.

         
        | Popula as formas flexionadas do verbo.
        | Adiciona pronomes pessoais aos verbos flexionados.

         
        | Popula as formas flexionadas do verbo.
        | Esta é a versão genérica desse método.
        | Não adiciona pronomes pessoais às formas conjugadas.
        | Esse método pode manipular qualquer novo idioma se a estrutura de conjugação estiver em conformidade com o Esquema XML da Verbiste.

         
        | Este é o método principal desta classe.
        | Primeiro, verifica se o verbo está em Verbiste.
        | Se não for, e um modelo de scikit-learn pré-treinado foi fornecido, o método chama o modelo
        para prever a classe de conjugação do verbo fornecido.

        | Retorna um objeto Verb ou None.

        :param verb: string.
            Verbo para conjugar.
        :param subject: string.
            Ativa os pronomes abreviados ou completos.
            O valor padrão é 'abrev'.
            Selecione 'pronome' para pronomes completos.
        :return: Verb object or None.

         
    Esta classe define o Objeto Verb em Inglês.

     
    Esta classe define o Objeto Verb Francês.

     
    Esta classe define o Objeto Verb Italiano.

     
    Esta classe define o Objeto Verb português.

     
    Esta classe define o Objeto Verbo romeno.

     
    Esta classe define o Objeto Verb Espanhol.

     
    Esta classe define o Objeto Verb.

    :param verb_info: VerbInfo Object.
    :param conjug_info: OrderedDict.
    :param subject: string.
        Ativa os pronomes abreviados ou completos.
        O valor padrão é 'abrev'.
        Selecione 'pronome' para pronomes completos.

     
    Essa classe define a estrutura de informações verbais do Verbiste.

    :param infinitive: string.
        Forma Infinitiva do Verbo.
    :param root: string.
        Raiz lexical do verbo.
    :param template: string.
        Nome do padrão final do verbo.

     
    Esta é a classe que manipula os arquivos xml da Verbiste.

    :param language: string.
    | A linguagem do conjugador. O valor padrão é fr para francês.
    | Os valores permitidos são: fr, en, es, pt, ro.

     
    | Vectorizer personalizado otimizado para extrair recursos de verbos.
    | O vetorizador subclasse sklearn.feature_extraction.text.CountVectorizer.
    | Como nas línguas indo-européias os verbos são flexionados pela adição de um sufixo morfológico,
    o vetorizador extrai terminações verbais e produz uma representação vetorial do verbo com características binárias.

    | As características são os verbos ngrams. (n-gram_range é definido no instanciation de classe).

     
    | Esta classe mantém e gerencia o conjunto de dados.
    | Define funções auxiliares para gerenciar tarefas de Aprendizado de Máquina, como a construção de um conjunto de treinamento e teste.

    :param VerbisteObj:
        Instância de um objeto Verbiste.

     
    | Esta classe gerencia o modelo scikit-learn.
     | O Pipeline inclui um vetorizador de recursos, um seletor de recursos e um classificador.
     | Se algum vetorizador, seletor de recurso ou classificador não for fornecido na declaração de instância,
     o método __init__ fornecerá bons valores padrão que obtêm mais de 92% de precisão de previsão.

    :param vectorizer: scikit-learn Vectorizer.
    :param feature_selector: scikit-learn Classifier with a fit_transform() method
    :param classifier: scikit-learn Classifier with a predict() method

     
    | Esta é a classe principal do projeto.
    | A classe gerencia o conjunto de dados Verbiste e fornece uma interface com o modelo scikit-learn.
    | Se nenhum parâmetro for fornecido, o idioma padrão é definido para francês e o modelo de conjugação francês pré-treinado é usado.
    | A classe define o método conjugado (verbo, idioma) que é o método principal do módulo.

    :param language: string.
        Linguagem do conjugador. O idioma padrão é 'fr' para francês.
    :param model: string.
        Um modelo fornecido pelo usuário se o usuário tiver treinado seu próprio modelo.

     Script de console para o mlconjug. A linguagem para o modelo de conjugação. Os valores podem ser fr, en, es, pt ou ro. O valor padrão é fr. A proporção dividida deve estar entre 0 e 1. A palavra fornecida: {0} não é um verbo válido em {1}. Idioma não suportado.
Os idiomas permitidos são fr, en, es, pt, ro. 