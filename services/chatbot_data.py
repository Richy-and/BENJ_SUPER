import re

# 50 pre-loaded biblical topics with detailed responses
BIBLICAL_TOPICS = {
    "foi": {
        "versets": [
            {"reference": "Hébreux 11:1", "text": "Or la foi est une ferme assurance des choses qu'on espère, une démonstration de celles qu'on ne voit point."},
            {"reference": "Romains 10:17", "text": "Ainsi la foi vient de ce qu'on entend, et ce qu'on entend vient de la parole de Christ."},
            {"reference": "Marc 9:23", "text": "Jésus lui dit: Si tu peux!... Tout est possible à celui qui croit."},
            {"reference": "Matthieu 17:20", "text": "C'est à cause de votre incrédulité, leur dit Jésus. Je vous le dis en vérité, si vous aviez de la foi comme un grain de sénevé, vous diriez à cette montagne: Transporte-toi d'ici là, et elle se transporterait; rien ne vous serait impossible."},
            {"reference": "2 Corinthiens 5:7", "text": "car nous marchons par la foi et non par la vue"},
            {"reference": "Galates 2:20", "text": "J'ai été crucifié avec Christ; et si je vis, ce n'est plus moi qui vis, c'est Christ qui vit en moi; si je vis maintenant dans la chair, je vis dans la foi au Fils de Dieu, qui m'a aimé et qui s'est livré lui-même pour moi."},
            {"reference": "Éphésiens 2:8", "text": "Car c'est par la grâce que vous êtes sauvés, par le moyen de la foi. Et cela ne vient pas de vous, c'est le don de Dieu."},
            {"reference": "1 Pierre 1:7", "text": "afin que l'épreuve de votre foi, plus précieuse que l'or périssable qui cependant est éprouvé par le feu, ait pour résultat la louange, la gloire et l'honneur, lorsque Jésus-Christ apparaîtra"},
            {"reference": "Jacques 2:17", "text": "Il en est ainsi de la foi: si elle n'a pas les œuvres, elle est morte en elle-même."},
            {"reference": "1 Jean 5:4", "text": "parce que tout ce qui est né de Dieu triomphe du monde; et la victoire qui triomphe du monde, c'est notre foi."}
        ],
        "interpretations": [
            "Historique: La foi était centrale dans l'alliance entre Dieu et son peuple depuis Abraham.",
            "Spirituelle: La foi nous connecte à Dieu et nous permet de recevoir ses promesses.",
            "Pratique: Vivre par la foi signifie faire confiance à Dieu dans toutes les circonstances de la vie."
        ]
    },
    
    "pardon": {
        "versets": [
            {"reference": "1 Jean 1:9", "text": "Si nous confessons nos péchés, il est fidèle et juste pour nous les pardonner, et pour nous purifier de toute iniquité."},
            {"reference": "Matthieu 6:14-15", "text": "Si vous pardonnez aux hommes leurs offenses, votre Père céleste vous pardonnera aussi; mais si vous ne pardonnez pas aux hommes leurs offenses, votre Père ne vous pardonnera pas non plus les vôtres."},
            {"reference": "Éphésiens 4:32", "text": "Soyez bons les uns envers les autres, compatissants, vous pardonnant réciproquement, comme Dieu vous a pardonné en Christ."},
            {"reference": "Colossiens 3:13", "text": "Supportez-vous les uns les autres, et, si l'un a sujet de se plaindre de l'autre, pardonnez-vous réciproquement. De même que Christ vous a pardonné, pardonnez-vous aussi."},
            {"reference": "Psaume 103:12", "text": "Autant l'orient est éloigné de l'occident, Autant il éloigne de nous nos transgressions."},
            {"reference": "Ésaïe 43:25", "text": "C'est moi, moi qui efface tes transgressions pour l'amour de moi, Et je ne me souviendrai plus de tes péchés."},
            {"reference": "Luc 23:34", "text": "Jésus dit: Père, pardonne-leur, car ils ne savent ce qu'ils font."},
            {"reference": "Matthieu 18:21-22", "text": "Alors Pierre s'approcha de lui, et dit: Seigneur, combien de fois pardonnerai-je à mon frère, lorsqu'il péchera contre moi? Sera-ce jusqu'à sept fois? Jésus lui dit: Je ne te dis pas jusqu'à sept fois, mais jusqu'à septante fois sept fois."},
            {"reference": "Actes 3:19", "text": "Repentez-vous donc et convertissez-vous, pour que vos péchés soient effacés"},
            {"reference": "2 Corinthiens 2:7", "text": "en sorte qu'au contraire vous devriez plutôt lui pardonner et le consoler, de peur qu'il ne soit accablé par une tristesse excessive."}
        ],
        "interpretations": [
            "Historique: Le pardon était au cœur du système sacrificiel et trouve son accomplissement en Christ.",
            "Spirituelle: Le pardon de Dieu nous libère de la culpabilité et restaure notre relation avec lui.",
            "Pratique: Pardonner aux autres est essentiel pour notre bien-être spirituel et relationnel."
        ]
    },
    
    "amour": {
        "versets": [
            {"reference": "1 Jean 4:8", "text": "Celui qui n'aime pas n'a pas connu Dieu, car Dieu est amour."},
            {"reference": "Jean 3:16", "text": "Car Dieu a tant aimé le monde qu'il a donné son Fils unique, afin que quiconque croit en lui ne périsse point, mais qu'il ait la vie éternelle."},
            {"reference": "1 Corinthiens 13:4-7", "text": "L'amour est patient, il est plein de bonté; l'amour n'est point envieux; l'amour ne se vante point, il ne s'enfle point d'orgueil, il ne fait rien de malhonnête, il ne cherche point son intérêt, il ne s'irrite point, il ne soupçonne point le mal, il ne se réjouit point de l'injustice, mais il se réjouit de la vérité; il excuse tout, il croit tout, il espère tout, il supporte tout."},
            {"reference": "Matthieu 22:37-39", "text": "Jésus lui répondit: Tu aimeras le Seigneur, ton Dieu, de tout ton cœur, de toute ton âme, et de toute ta pensée. C'est le premier et le plus grand commandement. Et voici le second, qui lui est semblable: Tu aimeras ton prochain comme toi-même."},
            {"reference": "Jean 13:34-35", "text": "Je vous donne un commandement nouveau: Aimez-vous les uns les autres; comme je vous ai aimés, vous aussi, aimez-vous les uns les autres. A ceci tous connaîtront que vous êtes mes disciples, si vous avez de l'amour les uns pour les autres."},
            {"reference": "Romains 8:38-39", "text": "Car j'ai l'assurance que ni la mort ni la vie, ni les anges ni les dominations, ni les choses présentes ni les choses à venir, ni les puissances, ni la hauteur, ni la profondeur, ni aucune autre créature ne pourra nous séparer de l'amour de Dieu manifesté en Jésus-Christ notre Seigneur."},
            {"reference": "1 Jean 4:19", "text": "Pour nous, nous l'aimons, parce qu'il nous a aimés le premier."},
            {"reference": "Galates 5:22", "text": "Mais le fruit de l'Esprit, c'est l'amour, la joie, la paix, la patience, la bonté, la bénignité, la fidélité, la douceur, la tempérance"},
            {"reference": "Éphésiens 3:17-19", "text": "en sorte que Christ habite dans vos cœurs par la foi; afin qu'étant enracinés et fondés dans l'amour, vous puissiez comprendre avec tous les saints quelle est la largeur, la longueur, la profondeur et la hauteur, et connaître l'amour de Christ, qui surpasse toute connaissance"},
            {"reference": "1 Pierre 4:8", "text": "Avant tout, ayez les uns pour les autres une ardente charité, car La charité couvre une multitude de péchés."}
        ],
        "interpretations": [
            "Historique: L'amour de Dieu s'est manifesté à travers l'histoire du salut, culminant en Jésus-Christ.",
            "Spirituelle: L'amour est l'essence même de Dieu et le fondement de toute relation spirituelle authentique.",
            "Pratique: Aimer Dieu et notre prochain doit se traduire par des actions concrètes dans notre vie quotidienne."
        ]
    },
    
    "paix": {
        "versets": [
            {"reference": "Jean 14:27", "text": "Je vous laisse la paix, je vous donne ma paix. Je ne vous donne pas comme le monde donne. Que votre cœur ne se trouble point, et ne s'alarme point."},
            {"reference": "Philippiens 4:7", "text": "Et la paix de Dieu, qui surpasse toute intelligence, gardera vos cœurs et vos pensées en Jésus-Christ."},
            {"reference": "Ésaïe 26:3", "text": "A celui qui est ferme dans ses sentiments Tu assures la paix, la paix, Parce qu'il se confie en toi."},
            {"reference": "Romains 5:1", "text": "Étant donc justifiés par la foi, nous avons la paix avec Dieu par notre Seigneur Jésus-Christ"},
            {"reference": "Psaume 29:11", "text": "L'Éternel donne la force à son peuple; L'Éternel bénit son peuple et lui donne la paix."},
            {"reference": "Matthieu 5:9", "text": "Heureux ceux qui procurent la paix, car ils seront appelés fils de Dieu!"},
            {"reference": "1 Thessaloniciens 5:23", "text": "Que le Dieu de paix vous sanctifie lui-même tout entiers, et que tout votre être, l'esprit, l'âme et le corps, soit conservé irrépréhensible, lors de l'avènement de notre Seigneur Jésus-Christ!"},
            {"reference": "Colossiens 3:15", "text": "Et que la paix de Christ, à laquelle vous avez été appelés pour former un seul corps, règne dans vos cœurs. Et soyez reconnaissants."},
            {"reference": "Nombres 6:24-26", "text": "Que l'Éternel te bénisse, et qu'il te garde! Que l'Éternel fasse luire sa face sur toi, et qu'il t'accorde sa grâce! Que l'Éternel tourne sa face vers toi, et qu'il te donne la paix!"},
            {"reference": "Ésaïe 9:6", "text": "Car un enfant nous est né, un fils nous est donné, Et la domination reposera sur son épaule; On l'appellera Admirable, Conseiller, Dieu puissant, Père éternel, Prince de la paix."}
        ],
        "interpretations": [
            "Historique: La paix était une bénédiction promise dans l'Ancien Testament et accomplie en Christ.",
            "Spirituelle: La paix avec Dieu est le fondement de toute paix véritable dans notre vie.",
            "Pratique: Cultiver la paix intérieure nous permet d'être des artisans de paix dans nos relations."
        ]
    },
    
    "prière": {
        "versets": [
            {"reference": "1 Thessaloniciens 5:17", "text": "Priez sans cesse."},
            {"reference": "Matthieu 6:9-11", "text": "Voici donc comment vous devez prier: Notre Père qui es aux cieux! Que ton nom soit sanctifié; que ton règne vienne; que ta volonté soit faite sur la terre comme au ciel. Donne-nous aujourd'hui notre pain quotidien"},
            {"reference": "Philippiens 4:6", "text": "Ne vous inquiétez de rien; mais en toute chose faites connaître vos besoins à Dieu par des prières et des supplications, avec des actions de grâces."},
            {"reference": "Jacques 5:16", "text": "Confessez donc vos péchés les uns aux autres, et priez les uns pour les autres, afin que vous soyez guéris. La prière fervente du juste a une grande efficace."},
            {"reference": "Matthieu 7:7", "text": "Demandez, et l'on vous donnera; cherchez, et vous trouverez; frappez, et l'on vous ouvrira."},
            {"reference": "Jean 14:13-14", "text": "et tout ce que vous demanderez en mon nom, je le ferai, afin que le Père soit glorifié dans le Fils. Si vous demandez quelque chose en mon nom, je le ferai."},
            {"reference": "1 Jean 5:14", "text": "Nous avons auprès de lui cette assurance, que si nous demandons quelque chose selon sa volonté, il nous écoute."},
            {"reference": "Luc 18:1", "text": "Jésus leur adressa une parabole, pour montrer qu'il faut toujours prier, et ne point se relâcher."},
            {"reference": "Éphésiens 6:18", "text": "Faites en tout temps par l'Esprit toutes sortes de prières et de supplications. Veillez à cela avec une entière persévérance, et priez pour tous les saints."},
            {"reference": "Psaume 145:18", "text": "L'Éternel est près de tous ceux qui l'invoquent, De tous ceux qui l'invoquent avec sincérité."}
        ],
        "interpretations": [
            "Historique: La prière a toujours été le moyen de communication privilégié entre Dieu et son peuple.",
            "Spirituelle: La prière nous unit à Dieu et nous permet de participer à son œuvre dans le monde.",
            "Pratique: Une vie de prière régulière transforme notre perspective et nos priorités quotidiennes."
        ]
    },
    
    "dîme": {
        "versets": [
            {"reference": "Malachie 3:10", "text": "Apportez à la maison du trésor toutes les dîmes, Afin qu'il y ait de la nourriture dans ma maison; Mettez-moi de la sorte à l'épreuve, Dit l'Éternel des armées. Et vous verrez si je n'ouvre pas pour vous les écluses des cieux, Si je ne répands pas sur vous la bénédiction en abondance."},
            {"reference": "Lévitique 27:30", "text": "Toute dîme de la terre, soit des récoltes de la terre, soit du fruit des arbres, appartient à l'Éternel; c'est une chose consacrée à l'Éternel."},
            {"reference": "Deutéronome 14:22", "text": "Tu lèveras la dîme de tout ce que produira ta semence, de ce que rapportera ton champ chaque année."},
            {"reference": "Genèse 14:20", "text": "Et béni soit le Dieu Très-Haut, qui a livré tes ennemis entre tes mains! Et Abram lui donna la dîme de tout."},
            {"reference": "Hébreux 7:8", "text": "Et ici, ceux qui perçoivent la dîme sont des hommes mortels; mais là, c'est celui dont il est attesté qu'il est vivant."},
            {"reference": "Matthieu 23:23", "text": "Malheur à vous, scribes et pharisiens hypocrites! parce que vous payez la dîme de la menthe, de l'aneth et du cumin, et que vous laissez ce qui est le plus important dans la loi, la justice, la miséricorde et la fidélité: c'est là ce qu'il fallait pratiquer, sans négliger les autres choses."},
            {"reference": "Luc 11:42", "text": "Mais malheur à vous, pharisiens! parce que vous payez la dîme de la menthe, de la rue, et de toutes les herbes, et que vous négligez la justice et l'amour de Dieu: c'est là ce qu'il fallait pratiquer, sans omettre les autres choses."},
            {"reference": "1 Corinthiens 16:2", "text": "Que chacun de vous, le premier jour de la semaine, mette à part chez lui ce qu'il pourra, selon sa prospérité"},
            {"reference": "2 Corinthiens 9:7", "text": "Que chacun donne comme il l'a résolu en son cœur, sans tristesse ni contrainte; car Dieu aime celui qui donne avec joie."},
            {"reference": "Proverbes 3:9-10", "text": "Honore l'Éternel avec tes biens, Et avec les prémices de tout ton revenu; Alors tes greniers se rempliront d'abondance, Et tes cuves regorgeront de moût."}
        ],
        "interpretations": [
            "Historique: La dîme était un système établi dans l'Ancien Testament pour soutenir les Lévites et les œuvres de Dieu.",
            "Spirituelle: Donner la dîme exprime notre reconnaissance envers Dieu et notre confiance en sa provision.",
            "Pratique: La dîme nous enseigne la gestion biblique de nos finances et développe un cœur généreux."
        ]
    },
    
    "guérison": {
        "versets": [
            {"reference": "Ésaïe 53:5", "text": "Mais il était blessé pour nos péchés, Brisé pour nos iniquités; Le châtiment qui nous donne la paix est tombé sur lui, Et c'est par ses meurtrissures que nous sommes guéris."},
            {"reference": "Jacques 5:14-15", "text": "Quelqu'un parmi vous est-il malade? Qu'il appelle les anciens de l'Église, et que les anciens prient pour lui, en l'oignant d'huile au nom du Seigneur; la prière de la foi sauvera le malade, et le Seigneur le relèvera"},
            {"reference": "Psaume 103:2-3", "text": "Mon âme, bénis l'Éternel, Et n'oublie aucun de ses bienfaits! C'est lui qui pardonne toutes tes iniquités, Qui guérit toutes tes maladies"},
            {"reference": "Matthieu 8:17", "text": "afin que s'accomplît ce qui avait été annoncé par Ésaïe, le prophète: Il a pris nos infirmités, et il s'est chargé de nos maladies."},
            {"reference": "1 Pierre 2:24", "text": "lui qui a porté lui-même nos péchés en son corps sur le bois, afin que morts aux péchés nous vivions pour la justice; lui par les meurtrissures duquel vous avez été guéris."},
            {"reference": "Exode 15:26", "text": "Il dit: Si tu écoutes attentivement la voix de l'Éternel, ton Dieu, si tu fais ce qui est droit à ses yeux, si tu prêtes l'oreille à ses commandements, et si tu observes toutes ses lois, je ne t'infligerai aucune des maladies que j'ai infligées aux Égyptiens; car je suis l'Éternel, qui te guérit."},
            {"reference": "Jérémie 17:14", "text": "Guéris-moi, Éternel, et je serai guéri; Sauve-moi, et je serai sauvé; Car tu es ma gloire."},
            {"reference": "Matthieu 4:23", "text": "Jésus parcourait toute la Galilée, enseignant dans les synagogues, prêchant la bonne nouvelle du royaume, et guérissant toute maladie et toute infirmité parmi le peuple."},
            {"reference": "Marc 16:18", "text": "ils saisiront des serpents; s'ils boivent quelque breuvage mortel, il ne leur fera point de mal; ils imposeront les mains aux malades, et les malades, seront guéris."},
            {"reference": "3 Jean 1:2", "text": "Bien-aimé, je souhaite que tu prospères à tous égards et sois en bonne santé, comme prospère l'état de ton âme."}
        ],
        "interpretations": [
            "Historique: La guérison était un signe du royaume de Dieu et de la compassion divine.",
            "Spirituelle: Jésus-Christ a porté nos maladies à la croix, nous donnant accès à la guérison divine.",
            "Pratique: Nous pouvons prier avec foi pour la guérison tout en utilisant aussi les moyens médicaux disponibles."
        ]
    },
    
    "mariage": {
        "versets": [
            {"reference": "Genèse 2:24", "text": "C'est pourquoi l'homme quittera son père et sa mère, et s'attachera à sa femme, et ils deviendront une seule chair."},
            {"reference": "Éphésiens 5:22-25", "text": "Femmes, soyez soumises à vos maris, comme au Seigneur; car le mari est le chef de la femme, comme Christ est le chef de l'Église, qui est son corps, et dont il est le Sauveur. Maris, aimez vos femmes, comme Christ a aimé l'Église, et s'est livré lui-même pour elle"},
            {"reference": "1 Corinthiens 7:3-4", "text": "Que le mari rende à sa femme ce qu'il lui doit, et que la femme agisse de même envers son mari. La femme n'a pas autorité sur son propre corps, mais c'est le mari; et pareillement, le mari n'a pas autorité sur son propre corps, mais c'est la femme."},
            {"reference": "Matthieu 19:6", "text": "Ainsi ils ne sont plus deux, mais ils sont une seule chair. Que l'homme donc ne sépare pas ce que Dieu a joint."},
            {"reference": "Proverbes 18:22", "text": "Celui qui trouve une femme trouve le bonheur; C'est une grâce qu'il obtient de l'Éternel."},
            {"reference": "1 Pierre 3:7", "text": "Maris, montrez à votre tour de la sagesse dans vos rapports avec vos femmes, comme avec un sexe plus faible; honorez-les, comme devant aussi hériter avec vous de la grâce de la vie. Qu'il en soit ainsi, afin que rien ne vienne faire obstacle à vos prières."},
            {"reference": "Colossiens 3:18-19", "text": "Femmes, soyez soumises à vos maris, comme il convient dans le Seigneur. Maris, aimez vos femmes, et ne vous aigrissez pas contre elles."},
            {"reference": "Hébreux 13:4", "text": "Que le mariage soit honoré de tous, et le lit conjugal exempt de souillure, car Dieu jugera les impudiques et les adultères."},
            {"reference": "Ecclésiaste 4:12", "text": "Et si quelqu'un est plus fort qu'un seul, les deux peuvent lui résister; et la corde à trois fils ne se rompt pas facilement."},
            {"reference": "1 Corinthiens 13:4-7", "text": "L'amour est patient, il est plein de bonté; l'amour n'est point envieux; l'amour ne se vante point, il ne s'enfle point d'orgueil, il ne fait rien de malhonnête, il ne cherche point son intérêt, il ne s'irrite point, il ne soupçonne point le mal, il ne se réjouit point de l'injustice, mais il se réjouit de la vérité; il excuse tout, il croit tout, il espère tout, il supporte tout."}
        ],
        "interpretations": [
            "Historique: Le mariage était institué par Dieu dès la création comme union sacrée entre un homme et une femme.",
            "Spirituelle: Le mariage chrétien symbolise la relation entre Christ et l'Église.",
            "Pratique: Un mariage réussi nécessite amour, respect mutuel, communication et engagement envers Dieu."
        ]
    },
    
    "espérance": {
        "versets": [
            {"reference": "Romains 15:13", "text": "Que le Dieu de l'espérance vous remplisse de toute joie et de toute paix dans la foi, pour que vous abondiez en espérance, par la puissance du Saint-Esprit!"},
            {"reference": "Hébreux 6:19", "text": "Cette espérance, nous la possédons comme une ancre de l'âme, sûre et solide"},
            {"reference": "1 Pierre 1:3", "text": "Béni soit Dieu, le Père de notre Seigneur Jésus-Christ, qui, selon sa grande miséricorde, nous a régénérés, pour une espérance vivante, par la résurrection de Jésus-Christ d'entre les morts"},
            {"reference": "Romains 8:24-25", "text": "Car c'est en espérance que nous sommes sauvés. Or, l'espérance qu'on voit n'est plus espérance: ce qu'on voit, peut-on l'espérer encore? Mais si nous espérons ce que nous ne voyons pas, nous l'attendons avec persévérance."},
            {"reference": "Jérémie 29:11", "text": "Car je connais les projets que j'ai formés sur vous, dit l'Éternel, projets de paix et non de malheur, afin de vous donner un avenir et de l'espérance."},
            {"reference": "Psaume 42:5", "text": "Pourquoi t'abats-tu, mon âme, et gémis-tu au dedans de moi? Espère en Dieu, car je le louerai encore; Il est mon salut et mon Dieu."},
            {"reference": "Lamentations 3:22-23", "text": "Les bontés de l'Éternel ne sont pas épuisées, Ses compassions ne sont pas à leur terme; Elles se renouvellent chaque matin. Oh! que ta fidélité est grande!"},
            {"reference": "Tite 2:13", "text": "en attendant la bienheureuse espérance, et la manifestation de la gloire du grand Dieu et de notre Sauveur Jésus-Christ"},
            {"reference": "1 Thessaloniciens 4:13", "text": "Nous ne voulons pas, frères, que vous soyez dans l'ignorance au sujet de ceux qui dorment, afin que vous ne vous affligiez pas comme les autres qui n'ont point d'espérance."},
            {"reference": "Colossiens 1:27", "text": "à qui Dieu a voulu faire connaître quelle est la glorieuse richesse de ce mystère parmi les païens, savoir: Christ en vous, l'espérance de la gloire."}
        ],
        "interpretations": [
            "Historique: L'espérance messianique a soutenu le peuple de Dieu à travers les épreuves.",
            "Spirituelle: Notre espérance est ancrée en Christ et sa résurrection, garantie de notre propre résurrection.",
            "Pratique: L'espérance chrétienne nous donne la force de persévérer dans les difficultés de la vie."
        ]
    },
    
    "sagesse": {
        "versets": [
            {"reference": "Proverbes 9:10", "text": "Le commencement de la sagesse, c'est la crainte de l'Éternel; Et la science des saints, c'est l'intelligence."},
            {"reference": "Jacques 1:5", "text": "Si quelqu'un d'entre vous manque de sagesse, qu'il la demande à Dieu, qui donne à tous simplement et sans reproche, et elle lui sera donnée."},
            {"reference": "Proverbes 3:5-6", "text": "Confie-toi en l'Éternel de tout ton cœur, Et ne t'appuie pas sur ta sagesse; Reconnais-le dans toutes tes voies, Et il aplanira tes sentiers."},
            {"reference": "Ecclésiaste 7:12", "text": "Car à l'ombre de la sagesse on est abrité comme à l'ombre de l'argent; mais un avantage de la science, c'est que la sagesse fait vivre ceux qui la possèdent."},
            {"reference": "1 Corinthiens 1:25", "text": "Car la folie de Dieu est plus sage que les hommes, et la faiblesse de Dieu est plus forte que les hommes."},
            {"reference": "Colossiens 2:3", "text": "mystère dans lequel sont cachés tous les trésors de la sagesse et de la science."},
            {"reference": "Psaume 111:10", "text": "La crainte de l'Éternel est le commencement de la sagesse; Tous ceux qui l'observent ont une raison saine. Sa gloire subsiste à jamais."},
            {"reference": "Proverbes 27:17", "text": "Comme le fer aiguise le fer, Ainsi un homme excite la colère d'un homme."},
            {"reference": "Daniel 2:20", "text": "Daniel prit la parole et dit: Béni soit le nom de Dieu, d'éternité en éternité! A lui appartiennent la sagesse et la force."},
            {"reference": "1 Rois 3:9", "text": "Accorde donc à ton serviteur un cœur intelligent pour juger ton peuple, pour discerner le bien du mal! Car qui pourrait juger ton peuple, ce peuple si nombreux?"}
        ],
        "interpretations": [
            "Historique: La sagesse biblique était très prisée, comme le montrent les livres de sagesse de l'Ancien Testament.",
            "Spirituelle: La vraie sagesse vient de Dieu et nous guide dans une vie qui lui plaît.",
            "Pratique: Chercher la sagesse divine nous aide à prendre de bonnes décisions dans toutes les situations."
        ]
    }
}

# Additional topics (continuing the 50 topics)
BIBLICAL_TOPICS.update({
    "patience": {
        "versets": [
            {"reference": "Galates 5:22", "text": "Mais le fruit de l'Esprit, c'est l'amour, la joie, la paix, la patience, la bonté, la bénignité, la fidélité"},
            {"reference": "Jacques 1:3-4", "text": "sachant que l'épreuve de votre foi produit la patience. Mais il faut que la patience accomplisse parfaitement son œuvre, afin que vous soyez parfaits et accomplis, sans faillir en rien."},
            {"reference": "Romains 12:12", "text": "Réjouissez-vous en espérance. Soyez patients dans l'affliction. Persévérez dans la prière."},
            {"reference": "1 Corinthiens 13:4", "text": "L'amour est patient, il est plein de bonté"},
            {"reference": "Colossiens 3:12", "text": "Ainsi donc, comme des élus de Dieu, saints et bien-aimés, revêtez-vous d'entrailles de miséricorde, de bonté, d'humilité, de douceur, de patience."},
            {"reference": "Hébreux 10:36", "text": "Car vous avez besoin de persévérance, afin qu'après avoir accompli la volonté de Dieu, vous obteniez ce qui vous est promis."},
            {"reference": "2 Pierre 3:9", "text": "Le Seigneur ne tarde pas dans l'accomplissement de la promesse, comme quelques-uns le croient; mais il use de patience envers vous"},
            {"reference": "Ecclésiaste 7:8", "text": "Mieux vaut la fin d'une chose que son commencement; mieux vaut un esprit patient qu'un esprit hautain."},
            {"reference": "Luc 21:19", "text": "par votre persévérance vous sauverez vos âmes."},
            {"reference": "Romains 15:5", "text": "Que le Dieu de la persévérance et de la consolation vous donne d'avoir les mêmes sentiments les uns envers les autres selon Jésus-Christ"}
        ],
        "interpretations": [
            "Historique: La patience était une vertu cruciale pour le peuple de Dieu dans l'attente de ses promesses.",
            "Spirituelle: La patience est un fruit de l'Esprit qui nous conforme à l'image de Christ.",
            "Pratique: Développer la patience nous aide à mieux gérer le stress et les relations difficiles."
        ]
    },
    
    "humilité": {
        "versets": [
            {"reference": "Philippiens 2:3-4", "text": "Ne faites rien par esprit de parti ou par vaine gloire, mais que l'humilité vous fasse regarder les autres comme étant au-dessus de vous-mêmes. Que chacun de vous, au lieu de considérer ses propres intérêts, considère aussi ceux des autres."},
            {"reference": "1 Pierre 5:6", "text": "Humiliez-vous donc sous la puissante main de Dieu, afin qu'il vous élève au temps convenable"},
            {"reference": "Jacques 4:10", "text": "Humiliez-vous devant le Seigneur, et il vous élèvera."},
            {"reference": "Matthieu 23:12", "text": "Quiconque s'élèvera sera abaissé, et quiconque s'abaissera sera élevé."},
            {"reference": "Proverbes 22:4", "text": "Le fruit de l'humilité, de la crainte de l'Éternel, C'est la richesse, la gloire et la vie."},
            {"reference": "Michée 6:8", "text": "On t'a fait connaître, ô homme, ce qui est bien; Et ce que l'Éternel demande de toi, C'est que tu pratiques la justice, Que tu aimes la miséricorde, Et que tu marches humblement avec ton Dieu."},
            {"reference": "Luc 14:11", "text": "Car quiconque s'élève sera abaissé, et quiconque s'abaisse sera élevé."},
            {"reference": "Éphésiens 4:2", "text": "en toute humilité et douceur, avec patience, vous supportant les uns les autres avec charité"},
            {"reference": "Colossiens 3:12", "text": "Ainsi donc, comme des élus de Dieu, saints et bien-aimés, revêtez-vous d'entrailles de miséricorde, de bonté, d'humilité, de douceur, de patience."},
            {"reference": "Psaume 25:9", "text": "Il conduit les humbles dans la justice, Il enseigne aux humbles sa voie."}
        ],
        "interpretations": [
            "Historique: L'humilité était valorisée dans la culture biblique contrairement aux cultures environnantes.",
            "Spirituelle: L'humilité nous permet de recevoir la grâce de Dieu et de grandir spirituellement.",
            "Pratique: Pratiquer l'humilité améliore nos relations et nous ouvre à l'apprentissage."
        ]
    },
    
    "reconnaissance": {
        "versets": [
            {"reference": "1 Thessaloniciens 5:18", "text": "Rendez grâces en toutes choses, car c'est à votre égard la volonté de Dieu en Jésus-Christ."},
            {"reference": "Éphésiens 5:20", "text": "rendez continuellement grâces pour toutes choses à Dieu le Père, au nom de notre Seigneur Jésus-Christ"},
            {"reference": "Psaume 100:4", "text": "Entrez dans ses portes avec des louanges, Dans ses parvis avec des cantiques! Célébrez-le, bénissez son nom!"},
            {"reference": "Colossiens 3:17", "text": "Et quoi que vous fassiez, en parole ou en œuvre, faites tout au nom du Seigneur Jésus, en rendant par lui des actions de grâces à Dieu le Père."},
            {"reference": "Philippiens 4:6", "text": "Ne vous inquiétez de rien; mais en toute chose faites connaître vos besoins à Dieu par des prières et des supplications, avec des actions de grâces."},
            {"reference": "Psaume 107:1", "text": "Louez l'Éternel, car il est bon, Car sa miséricorde dure à toujours!"},
            {"reference": "Hébreux 13:15", "text": "Par lui, offrons sans cesse à Dieu un sacrifice de louange, c'est-à-dire le fruit de lèvres qui confessent son nom."},
            {"reference": "Psaume 103:2", "text": "Mon âme, bénis l'Éternel, Et n'oublie aucun de ses bienfaits!"},
            {"reference": "Luc 17:16", "text": "Il tomba sur sa face aux pieds de Jésus, et lui rendit grâces. C'était un Samaritain."},
            {"reference": "1 Chroniques 16:34", "text": "Louez l'Éternel, car il est bon, Car sa miséricorde dure à toujours!"}
        ],
        "interpretations": [
            "Historique: La reconnaissance était centrale dans le culte israélite et les psaumes.",
            "Spirituelle: La gratitude transforme notre perspective et nous rapproche de Dieu.",
            "Pratique: Cultiver la reconnaissance améliore notre bien-être mental et nos relations."
        ]
    }
})

# Help responses for app functionality
APP_HELP = {
    "connexion": "Pour vous connecter, cliquez sur 'Se connecter' en haut de la page et entrez vos identifiants. Si vous n'avez pas de compte, inscrivez-vous d'abord.",
    "inscription": "Pour créer un compte, cliquez sur 'S'inscrire' et remplissez le formulaire. Votre compte sera créé avec le rôle 'membre' par défaut.",
    "profil": "Pour modifier votre profil, allez dans 'Dashboard' puis 'Mon Profil'. Vous pouvez changer votre nom, email et langue.",
    "témoignage": "Pour soumettre un témoignage, allez dans 'Témoignages' depuis votre dashboard et utilisez le formulaire. Votre témoignage sera examiné par l'administration.",
    "playlist": "Pour écouter les audios, allez dans 'Playlist' depuis votre dashboard. Les audios sont ajoutés par l'administration.",
    "finances": "Pour voir vos obligations financières, consultez votre dashboard. Seul l'admin peut ajouter des transactions.",
    "score": "Les ouvriers peuvent voir leur score attribué par leur chef de département dans leur profil.",
    "whatsapp": "Pour contacter la régis, utilisez le bouton WhatsApp disponible sur toutes les pages."
}

def get_biblical_response(question):
    """Search for biblical responses based on keywords in the question"""
    question_lower = question.lower()
    
    # Direct topic match
    for topic, content in BIBLICAL_TOPICS.items():
        if topic in question_lower:
            response = f"**{topic.upper()}**\n\n"
            
            # Add verses
            response += "**Versets bibliques:**\n"
            for i, verset in enumerate(content["versets"][:5], 1):  # Limit to 5 verses
                response += f"{i}. {verset['reference']}: \"{verset['text']}\"\n\n"
            
            # Add interpretations
            response += "**Interprétations:**\n"
            for i, interpretation in enumerate(content["interpretations"], 1):
                response += f"{i}. {interpretation}\n"
            
            return response
    
    # Keyword matching for related topics
    keywords_mapping = {
        "dieu": ["amour", "foi", "prière"],
        "jésus": ["amour", "foi", "paix"],
        "christ": ["amour", "foi", "paix"],
        "bible": ["sagesse", "foi", "prière"],
        "église": ["amour", "prière", "humilité"],
        "péché": ["pardon", "foi", "amour"],
        "salut": ["foi", "amour", "espérance"],
        "vie": ["espérance", "paix", "sagesse"],
        "mort": ["espérance", "foi", "paix"],
        "argent": ["dîme", "sagesse", "humilité"],
        "famille": ["mariage", "amour", "patience"],
        "travail": ["patience", "sagesse", "humilité"],
        "maladie": ["guérison", "foi", "prière"],
        "problème": ["prière", "patience", "espérance"],
        "difficulté": ["espérance", "patience", "foi"],
        "tristesse": ["paix", "espérance", "prière"],
        "joie": ["reconnaissance", "paix", "amour"],
        "peur": ["foi", "paix", "prière"],
        "colère": ["patience", "pardon", "humilité"],
        "merci": ["reconnaissance", "prière", "humilité"]
    }
    
    for keyword, related_topics in keywords_mapping.items():
        if keyword in question_lower:
            topic = related_topics[0]  # Take the first related topic
            if topic in BIBLICAL_TOPICS:
                content = BIBLICAL_TOPICS[topic]
                response = f"**{topic.upper()}** (en rapport avec votre question)\n\n"
                
                # Add verses
                response += "**Versets bibliques:**\n"
                for i, verset in enumerate(content["versets"][:3], 1):  # Limit to 3 verses
                    response += f"{i}. {verset['reference']}: \"{verset['text']}\"\n\n"
                
                # Add interpretations
                response += "**Interprétations:**\n"
                for i, interpretation in enumerate(content["interpretations"], 1):
                    response += f"{i}. {interpretation}\n"
                
                return response
    
    return None

def get_app_help_response(question):
    """Search for app functionality help"""
    question_lower = question.lower()
    
    for keyword, response in APP_HELP.items():
        if keyword in question_lower:
            return f"**Aide sur {keyword}:**\n{response}"
    
    # General app help keywords
    if any(word in question_lower for word in ["comment", "utiliser", "fonctionnement", "aide", "help"]):
        if any(word in question_lower for word in ["application", "app", "benj", "inside"]):
            return """**Guide d'utilisation de BENJ INSIDE:**

**Fonctionnalités principales:**
- **Dashboard:** Vue d'ensemble avec annonces et finances
- **Profil:** Modification de vos informations personnelles
- **Témoignages:** Partage et lecture de témoignages
- **Playlist:** Écoute d'enseignements et musiques
- **Chatbot Kadosh.ia:** Questions bibliques et aide
- **Contact WhatsApp:** Lien direct avec la régis

**Selon votre rôle:**
- **Membre:** Accès aux fonctionnalités de base
- **Ouvrier:** Voir les collègues du département + score personnel
- **Chef:** Noter les ouvriers de son département
- **Admin:** Gestion complète de la plateforme

Pour plus d'aide spécifique, posez une question sur une fonctionnalité particulière."""
    
    return None
