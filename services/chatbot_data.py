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
    },
    
    "bénédiction": {
        "versets": [
            {"reference": "Nombres 6:24-26", "text": "Que l'Éternel te bénisse, et qu'il te garde! Que l'Éternel fasse luire sa face sur toi, et qu'il t'accorde sa grâce! Que l'Éternel tourne sa face vers toi, et qu'il te donne la paix!"},
            {"reference": "Éphésiens 1:3", "text": "Béni soit Dieu, le Père de notre Seigneur Jésus-Christ, qui nous a bénis de toute sorte de bénédictions spirituelles dans les lieux célestes en Christ!"},
            {"reference": "Genèse 12:2", "text": "Je ferai de toi une grande nation, et je te bénirai; je rendrai ton nom grand, et tu seras une source de bénédiction."},
            {"reference": "Psaume 67:1", "text": "Que Dieu ait pitié de nous et qu'il nous bénisse, Qu'il fasse luire sur nous sa face!"},
            {"reference": "Deutéronome 28:2", "text": "Voici toutes les bénédictions qui se répandront sur toi et qui seront ton partage, lorsque tu obéiras à la voix de l'Éternel, ton Dieu"}
        ],
        "interpretations": [
            "Historique: Les bénédictions étaient centrales dans l'alliance de Dieu avec son peuple.",
            "Spirituelle: Dieu désire nous bénir et nous rendre bénis pour les autres.",
            "Pratique: Reconnaître et partager les bénédictions de Dieu transforme nos vies."
        ]
    },
    
    "crainte": {
        "versets": [
            {"reference": "Proverbes 1:7", "text": "La crainte de l'Éternel est le commencement de la science"},
            {"reference": "Psaume 111:10", "text": "La crainte de l'Éternel est le commencement de la sagesse"},
            {"reference": "Ecclésiaste 12:13", "text": "Écoutons la fin du discours: Crains Dieu et observe ses commandements. C'est là ce que doit faire tout homme."},
            {"reference": "Psaume 34:11", "text": "Venez, mes fils, écoutez-moi! Je vous enseignerai la crainte de l'Éternel."},
            {"reference": "Proverbes 14:27", "text": "La crainte de l'Éternel est une source de vie, Pour détourner des pièges de la mort."}
        ],
        "interpretations": [
            "Historique: La crainte de Dieu était la base de la sagesse dans l'Ancien Testament.",
            "Spirituelle: La crainte révérencielle de Dieu est le début de toute vraie connaissance.",
            "Pratique: Respecter Dieu nous guide vers des choix sages dans la vie."
        ]
    },
    
    "louange": {
        "versets": [
            {"reference": "Psaume 150:6", "text": "Que tout ce qui respire loue l'Éternel! Louez l'Éternel!"},
            {"reference": "Psaume 34:1", "text": "Je bénirai l'Éternel en tout temps; Sa louange sera toujours dans ma bouche."},
            {"reference": "Hébreux 13:15", "text": "Par lui, offrons sans cesse à Dieu un sacrifice de louange"},
            {"reference": "Psaume 22:3", "text": "Pourtant tu es le Saint, Tu sièges au milieu des louanges d'Israël."},
            {"reference": "Actes 16:25", "text": "Vers le milieu de la nuit, Paul et Silas priaient et chantaient les louanges de Dieu"}
        ],
        "interpretations": [
            "Historique: La louange était au cœur du culte israélite et des premiers chrétiens.",
            "Spirituelle: La louange nous connecte à la présence de Dieu et transforme notre perspective.",
            "Pratique: Louer Dieu régulièrement élève notre esprit et renforce notre foi."
        ]
    },
    
    "servir": {
        "versets": [
            {"reference": "Marc 10:43-44", "text": "Il n'en est pas de même au milieu de vous. Mais quiconque veut être grand parmi vous, qu'il soit votre serviteur; et quiconque veut être le premier parmi vous, qu'il soit l'esclave de tous."},
            {"reference": "Galates 5:13", "text": "Frères, vous avez été appelés à la liberté, seulement ne faites pas de cette liberté un prétexte de vivre selon la chair; mais rendez-vous, par la charité, serviteurs les uns des autres."},
            {"reference": "1 Pierre 4:10", "text": "Comme de bons dispensateurs des diverses grâces de Dieu, que chacun de vous mette au service des autres le don qu'il a reçu"},
            {"reference": "Josué 24:15", "text": "Et si vous ne trouvez pas bon de servir l'Éternel, choisissez aujourd'hui qui vous voulez servir"}
        ],
        "interpretations": [
            "Historique: Servir Dieu et les autres était central dans l'éthique biblique.",
            "Spirituelle: Le service est l'expression naturelle de l'amour chrétien.",
            "Pratique: Servir les autres nous rend semblables à Jésus et apporte la joie."
        ]
    },
    
    "justice": {
        "versets": [
            {"reference": "Michée 6:8", "text": "On t'a fait connaître, ô homme, ce qui est bien; Et ce que l'Éternel demande de toi, C'est que tu pratiques la justice, Que tu aimes la miséricorde, Et que tu marches humblement avec ton Dieu."},
            {"reference": "Ésaïe 1:17", "text": "Apprenez à faire le bien, recherchez la justice, Protégez l'opprimé; Faites droit à l'orphelin, Défendez la veuve."},
            {"reference": "Psaume 37:28", "text": "Car l'Éternel aime la justice, Et il n'abandonne pas ses fidèles"},
            {"reference": "Proverbes 21:3", "text": "La pratique de la justice et de l'équité, Voilà ce que l'Éternel préfère aux sacrifices."}
        ],
        "interpretations": [
            "Historique: La justice était un pilier de la loi divine et des prophètes.",
            "Spirituelle: Dieu est juste et appelle son peuple à pratiquer la justice.",
            "Pratique: Défendre les faibles et pratiquer l'équité reflète le caractère de Dieu."
        ]
    },
    
    "miséricorde": {
        "versets": [
            {"reference": "Lamentations 3:22-23", "text": "Les bontés de l'Éternel ne sont pas épuisées, Ses compassions ne sont pas à leur terme; Elles se renouvellent chaque matin. Oh! que ta fidélité est grande!"},
            {"reference": "Psaume 103:8", "text": "L'Éternel est miséricordieux et compatissant, Lent à la colère et riche en bonté."},
            {"reference": "Matthieu 5:7", "text": "Heureux les miséricordieux, car ils obtiendront miséricorde!"},
            {"reference": "Éphésiens 2:4", "text": "Mais Dieu, qui est riche en miséricorde, à cause du grand amour dont il nous a aimés"}
        ],
        "interpretations": [
            "Historique: La miséricorde de Dieu était célébrée dans tout l'Ancien Testament.",
            "Spirituelle: La miséricorde divine est la source de notre salut et de notre espoir.",
            "Pratique: Montrer la miséricorde aux autres reflète la miséricorde que nous avons reçue."
        ]
    },
    
    "protection": {
        "versets": [
            {"reference": "Psaume 91:1-2", "text": "Celui qui demeure sous l'abri du Très-Haut Repose à l'ombre du Tout-Puissant. Je dis à l'Éternel: Mon refuge et ma forteresse, Mon Dieu en qui je me confie!"},
            {"reference": "Psaume 23:4", "text": "Quand je marche dans la vallée de l'ombre de la mort, Je ne crains aucun mal, car tu es avec moi"},
            {"reference": "Proverbes 18:10", "text": "Le nom de l'Éternel est une tour forte; Le juste s'y réfugie, et se trouve en sûreté."},
            {"reference": "Psaume 121:7-8", "text": "L'Éternel te gardera de tout mal, Il gardera ton âme; L'Éternel gardera ton départ et ton arrivée, Dès maintenant et à jamais."}
        ],
        "interpretations": [
            "Historique: Dieu était le protecteur d'Israël dans toutes les circonstances.",
            "Spirituelle: La protection divine s'étend à tous les aspects de notre vie.",
            "Pratique: Nous pouvons avoir confiance en la protection de Dieu dans l'adversité."
        ]
    },
    
    "pureté": {
        "versets": [
            {"reference": "Psaume 51:10", "text": "O Dieu! crée en moi un cœur pur, Et renouvelle en moi un esprit bien disposé."},
            {"reference": "Matthieu 5:8", "text": "Heureux ceux qui ont le cœur pur, car ils verront Dieu!"},
            {"reference": "1 Jean 3:3", "text": "Quiconque a cette espérance en lui se purifie, comme lui-même est pur."},
            {"reference": "Proverbes 20:9", "text": "Qui dira: J'ai purifié mon cœur, Je suis net de mon péché?"}
        ],
        "interpretations": [
            "Historique: La pureté était requise pour s'approcher de Dieu dans l'Ancien Testament.",
            "Spirituelle: La pureté du cœur est le résultat de l'œuvre de l'Esprit en nous.",
            "Pratique: Rechercher la pureté dans nos pensées et actions nous rapproche de Dieu."
        ]
    },
    
    "obéissance": {
        "versets": [
            {"reference": "1 Samuel 15:22", "text": "Samuel dit: L'Éternel trouve-t-il du plaisir dans les holocaustes et les sacrifices, comme dans l'obéissance à la voix de l'Éternel? Voici, l'obéissance vaut mieux que les sacrifices"},
            {"reference": "Jean 14:15", "text": "Si vous m'aimez, gardez mes commandements."},
            {"reference": "Actes 5:29", "text": "Pierre et les apôtres répondirent: Il faut obéir à Dieu plutôt qu'aux hommes."},
            {"reference": "Deutéronome 11:27", "text": "la bénédiction, si vous obéissez aux commandements de l'Éternel, votre Dieu, que je vous prescris en ce jour"}
        ],
        "interpretations": [
            "Historique: L'obéissance à Dieu était la condition des bénédictions dans l'alliance.",
            "Spirituelle: L'obéissance est l'expression de notre amour et de notre confiance en Dieu.",
            "Pratique: Obéir à Dieu nous garde dans sa volonté et nous protège du mal."
        ]
    },
    
    "persévérance": {
        "versets": [
            {"reference": "Hébreux 12:1", "text": "Nous donc aussi, puisque nous sommes environnés d'une si grande nuée de témoins, rejetons tout fardeau, et le péché qui nous enveloppe si facilement, et courons avec persévérance dans la carrière qui nous est ouverte"},
            {"reference": "Galates 6:9", "text": "Ne nous lassons pas de faire le bien; car nous moissonnerons au temps convenable, si nous ne nous relâchons pas."},
            {"reference": "1 Corinthiens 15:58", "text": "Ainsi, mes frères bien-aimés, soyez fermes, inébranlables, travaillant de mieux en mieux à l'œuvre du Seigneur"},
            {"reference": "Apocalypse 2:10", "text": "Ne crains pas ce que tu vas souffrir. Voici, le diable jettera quelques-uns de vous en prison, afin que vous soyez éprouvés, et vous aurez une tribulation de dix jours. Sois fidèle jusqu'à la mort, et je te donnerai la couronne de vie."}
        ],
        "interpretations": [
            "Historique: La persévérance était nécessaire pour les premiers chrétiens face à la persécution.",
            "Spirituelle: Persévérer dans la foi nous assure de recevoir les récompenses éternelles.",
            "Pratique: La persévérance dans les difficultés développe notre caractère et notre foi."
        ]
    },
    
    "joie": {
        "versets": [
            {"reference": "Néhémie 8:10", "text": "Ne vous affligez pas, car la joie de l'Éternel sera votre force."},
            {"reference": "Psaume 16:11", "text": "Tu me feras connaître le sentier de la vie; Il y a d'abondantes joies devant ta face, Des délices éternelles à ta droite."},
            {"reference": "Philippiens 4:4", "text": "Réjouissez-vous toujours dans le Seigneur; je le répète, réjouissez-vous."},
            {"reference": "Jean 15:11", "text": "Je vous ai dit ces choses, afin que ma joie soit en vous, et que votre joie soit parfaite."}
        ],
        "interpretations": [
            "Historique: La joie était un signe de la présence de Dieu parmi son peuple.",
            "Spirituelle: La joie chrétienne transcende les circonstances et trouve sa source en Dieu.",
            "Pratique: Cultiver la joie nous rend témoins de la bonté de Dieu dans notre monde."
        ]
    },
    
    "confiance": {
        "versets": [
            {"reference": "Proverbes 3:5-6", "text": "Confie-toi en l'Éternel de tout ton cœur, Et ne t'appuie pas sur ta sagesse; Reconnais-le dans toutes tes voies, Et il aplanira tes sentiers."},
            {"reference": "Psaume 37:3", "text": "Confie-toi en l'Éternel, et pratique le bien; Aie le pays pour demeure et la fidélité pour pâture."},
            {"reference": "Ésaïe 26:4", "text": "Confiez-vous en l'Éternel à perpétuité, Car l'Éternel, l'Éternel est le rocher des siècles."},
            {"reference": "Psaume 56:3", "text": "Quand je suis dans la crainte, En toi je me confie."}
        ],
        "interpretations": [
            "Historique: La confiance en Dieu était la base de la survie du peuple d'Israël.",
            "Spirituelle: Faire confiance à Dieu nous libère de l'anxiété et de la peur.",
            "Pratique: Développer la confiance en Dieu nous aide à prendre de meilleures décisions."
        ]
    },
    
    "courage": {
        "versets": [
            {"reference": "Josué 1:9", "text": "Ne t'ai-je pas donné cet ordre: Fortifie-toi et prends courage? Ne t'effraie point et ne t'épouvante point, car l'Éternel, ton Dieu, est avec toi dans tout ce que tu entreprendras."},
            {"reference": "Psaume 27:14", "text": "Espère en l'Éternel! Fortifie-toi et que ton cœur s'affermisse! Espère en l'Éternel!"},
            {"reference": "1 Corinthiens 16:13", "text": "Veillez, demeurez fermes dans la foi, soyez des hommes, fortifiez-vous."},
            {"reference": "Deutéronome 31:6", "text": "Fortifiez-vous et ayez du courage! Ne craignez point et ne soyez point effrayés devant eux; car l'Éternel, ton Dieu, marchera lui-même avec toi"}
        ],
        "interpretations": [
            "Historique: Le courage était nécessaire pour conquérir la Terre Promise et résister aux ennemis.",
            "Spirituelle: Le courage chrétien vient de la certitude que Dieu est avec nous.",
            "Pratique: Avoir du courage nous permet de faire ce qui est juste même dans l'adversité."
        ]
    },
    
    "liberté": {
        "versets": [
            {"reference": "Jean 8:36", "text": "Si donc le Fils vous affranchit, vous serez réellement libres."},
            {"reference": "Galates 5:1", "text": "C'est pour la liberté que Christ nous a affranchis. Demeurez donc fermes, et ne vous laissez pas mettre de nouveau sous le joug de la servitude."},
            {"reference": "2 Corinthiens 3:17", "text": "Or, le Seigneur c'est l'Esprit; et là où est l'Esprit du Seigneur, là est la liberté."},
            {"reference": "Romains 8:2", "text": "En effet, la loi de l'esprit de vie en Jésus-Christ m'a affranchi de la loi du péché et de la mort."}
        ],
        "interpretations": [
            "Historique: La liberté était promise par Dieu à travers l'histoire du salut.",
            "Spirituelle: Christ nous libère du péché et de la mort pour une vie nouvelle.",
            "Pratique: Vivre dans la liberté chrétienne signifie servir Dieu et les autres avec joie."
        ]
    },
    
    "transformation": {
        "versets": [
            {"reference": "2 Corinthiens 5:17", "text": "Si quelqu'un est en Christ, il est une nouvelle créature. Les choses anciennes sont passées; voici, toutes choses sont devenues nouvelles."},
            {"reference": "Romains 12:2", "text": "Ne vous conformez pas au siècle présent, mais soyez transformés par le renouvellement de l'intelligence"},
            {"reference": "2 Corinthiens 3:18", "text": "Nous tous qui, le visage découvert, contemplons comme dans un miroir la gloire du Seigneur, nous sommes transformés en la même image, de gloire en gloire"},
            {"reference": "Éphésiens 4:22-24", "text": "à vous dépouiller, eu égard à votre vie passée, du vieil homme qui se corrompt par les convoitises trompeuses, à être renouvelés dans l'esprit de votre intelligence, et à revêtir l'homme nouveau"}
        ],
        "interpretations": [
            "Historique: La transformation était promise par les prophètes et accomplie en Christ.",
            "Spirituelle: L'Esprit Saint nous transforme progressivement à l'image de Christ.",
            "Pratique: Accepter la transformation divine change radicalement notre manière de vivre."
        ]
    },
    
    "compassion": {
        "versets": [
            {"reference": "Matthieu 9:36", "text": "Voyant la foule, il fut ému de compassion pour elle, parce qu'elle était languissante et abattue, comme des brebis qui n'ont point de berger."},
            {"reference": "Colossiens 3:12", "text": "Ainsi donc, comme des élus de Dieu, saints et bien-aimés, revêtez-vous d'entrailles de miséricorde, de bonté, d'humilité, de douceur, de patience."},
            {"reference": "1 Pierre 3:8", "text": "Enfin, soyez tous animés des mêmes pensées et des mêmes sentiments, pleins d'amour fraternel, de compassion, d'humilité."},
            {"reference": "Lamentations 3:32", "text": "Mais, lorsqu'il afflige, Il a compassion selon sa grande miséricorde"}
        ],
        "interpretations": [
            "Historique: La compassion de Dieu était manifestée envers Israël malgré leur infidélité.",
            "Spirituelle: La compassion divine nous pousse à avoir pitié des autres dans leurs souffrances.",
            "Pratique: Développer la compassion nous rend plus humains et plus proches de Dieu."
        ]
    },
    
    "force": {
        "versets": [
            {"reference": "Ésaïe 40:31", "text": "Mais ceux qui se confient en l'Éternel renouvellent leur force. Ils prennent le vol comme les aigles; Ils courent, et ne se lassent point, Ils marchent, et ne se fatiguent point."},
            {"reference": "Philippiens 4:13", "text": "Je puis tout par celui qui me fortifie."},
            {"reference": "2 Corinthiens 12:9", "text": "et il m'a dit: Ma grâce te suffit, car ma puissance s'accomplit dans la faiblesse."},
            {"reference": "Psaume 46:1", "text": "Dieu est pour nous un refuge et un appui, Un secours qui ne manque jamais dans la détresse."}
        ],
        "interpretations": [
            "Historique: La force de Dieu se manifestait dans la faiblesse humaine tout au long de l'histoire biblique.",
            "Spirituelle: Notre force vient de notre relation avec Dieu, pas de nos capacités propres.",
            "Pratique: Compter sur la force divine nous permet d'affronter les défis les plus difficiles."
        ]
    },
    
    "lumière": {
        "versets": [
            {"reference": "Jean 8:12", "text": "Jésus leur parla de nouveau, et dit: Je suis la lumière du monde; celui qui me suit ne marchera pas dans les ténèbres, mais il aura la lumière de la vie."},
            {"reference": "Matthieu 5:14", "text": "Vous êtes la lumière du monde. Une ville située sur une montagne ne peut être cachée"},
            {"reference": "Psaume 119:105", "text": "Ta parole est une lampe à mes pieds, Et une lumière sur mon sentier."},
            {"reference": "1 Jean 1:5", "text": "La nouvelle que nous avons apprise de lui, et que nous vous annonçons, c'est que Dieu est lumière, et qu'il n'y a point en lui de ténèbres."}
        ],
        "interpretations": [
            "Historique: La lumière était un symbole de la présence divine dans le temple et les Écritures.",
            "Spirituelle: Christ est la lumière qui éclaire notre chemin et révèle la vérité.",
            "Pratique: Être lumière pour les autres signifie refléter l'amour et la vérité de Dieu."
        ]
    },
    
    "vérité": {
        "versets": [
            {"reference": "Jean 14:6", "text": "Jésus lui dit: Je suis le chemin, la vérité, et la vie. Nul ne vient au Père que par moi."},
            {"reference": "Jean 8:32", "text": "vous connaîtrez la vérité, et la vérité vous affranchira."},
            {"reference": "Psaume 119:160", "text": "Le fondement de ta parole est la vérité, Et toutes les lois de ta justice sont éternelles."},
            {"reference": "Éphésiens 4:15", "text": "mais que, professant la vérité dans la charité, nous croissions à tous égards en celui qui est le chef, Christ"}
        ],
        "interpretations": [
            "Historique: La vérité de Dieu était révélée progressivement à travers sa Parole.",
            "Spirituelle: Jésus-Christ est la vérité incarnée qui nous révèle parfaitement Dieu.",
            "Pratique: Vivre dans la vérité nous libère du mensonge et de la tromperie."
        ]
    },
    
    "résurrection": {
        "versets": [
            {"reference": "Jean 11:25", "text": "Jésus lui dit: Je suis la résurrection et la vie. Celui qui croit en moi vivra, quand même il serait mort"},
            {"reference": "1 Corinthiens 15:20", "text": "Mais maintenant, Christ est ressuscité des morts, il est les prémices de ceux qui sont morts."},
            {"reference": "Romains 6:4", "text": "Nous avons donc été ensevelis avec lui par le baptême en sa mort, afin que, comme Christ est ressuscité des morts par la gloire du Père, de même nous aussi nous marchions en nouveauté de vie."},
            {"reference": "1 Thessaloniciens 4:16", "text": "Car le Seigneur lui-même, à un signal donné, à la voix d'un archange, et au son de la trompette de Dieu, descendra du ciel, et les morts en Christ ressusciteront premièrement."}
        ],
        "interpretations": [
            "Historique: La résurrection était espérée par les juifs et accomplie en Jésus-Christ.",
            "Spirituelle: La résurrection de Christ garantit notre propre résurrection future.",
            "Pratique: L'espoir de la résurrection transforme notre vision de la mort et de la vie."
        ]
    },
    
    "unité": {
        "versets": [
            {"reference": "Éphésiens 4:3", "text": "vous efforçant de conserver l'unité de l'esprit par le lien de la paix."},
            {"reference": "Jean 17:21", "text": "afin que tous soient un, comme toi, Père, tu es en moi, et comme je suis en toi, afin qu'eux aussi soient un en nous"},
            {"reference": "1 Corinthiens 12:12", "text": "Car, comme le corps est un et a plusieurs membres, et comme tous les membres du corps, malgré leur nombre, ne forment qu'un seul corps, ainsi en est-il de Christ."},
            {"reference": "Psaume 133:1", "text": "Voici, oh! qu'il est agréable, qu'il est doux Pour des frères de demeurer ensemble!"}
        ],
        "interpretations": [
            "Historique: L'unité du peuple de Dieu était un objectif constant malgré les divisions.",
            "Spirituelle: L'unité chrétienne reflète l'unité divine et témoigne de l'amour de Dieu.",
            "Pratique: Rechercher l'unité dans l'Église nécessite humilité, patience et amour mutuel."
        ]
    },
    
    "repos": {
        "versets": [
            {"reference": "Matthieu 11:28", "text": "Venez à moi, vous tous qui êtes fatigués et chargés, et je vous donnerai du repos."},
            {"reference": "Psaume 23:2", "text": "Il me fait reposer dans de verts pâturages, Il me dirige près des eaux paisibles."},
            {"reference": "Hébreux 4:9", "text": "Il y a donc un repos de sabbat réservé au peuple de Dieu."},
            {"reference": "Exode 20:8", "text": "Souviens-toi du jour du repos, pour le sanctifier."}
        ],
        "interpretations": [
            "Historique: Le repos sabbatique était institué par Dieu dès la création.",
            "Spirituelle: Le repos en Christ libère de l'agitation et des soucis du monde.",
            "Pratique: Prendre du temps de repos honore Dieu et restaure notre âme."
        ]
    },
    
    "réconciliation": {
        "versets": [
            {"reference": "2 Corinthiens 5:18", "text": "Et tout cela vient de Dieu, qui nous a réconciliés avec lui par Christ, et qui nous a donné le ministère de la réconciliation."},
            {"reference": "Romains 5:10", "text": "Car si, lorsque nous étions ennemis, nous avons été réconciliés avec Dieu par la mort de son Fils, à plus forte raison, étant réconciliés, serons-nous sauvés par sa vie."},
            {"reference": "Matthieu 5:24", "text": "laisse là ton offrande devant l'autel, et va d'abord te réconcilier avec ton frère; puis, viens présenter ton offrande."},
            {"reference": "Éphésiens 2:16", "text": "et de les réconcilier, l'un et l'autre en un seul corps, avec Dieu par la croix, en détruisant par elle l'inimitié."}
        ],
        "interpretations": [
            "Historique: La réconciliation était le but du système sacrificiel de l'Ancien Testament.",
            "Spirituelle: Christ a accompli la réconciliation parfaite entre Dieu et l'humanité.",
            "Pratique: Nous sommes appelés à être des agents de réconciliation dans nos relations."
        ]
    },
    
    "fidélité": {
        "versets": [
            {"reference": "Lamentations 3:23", "text": "Elles se renouvellent chaque matin. Oh! que ta fidélité est grande!"},
            {"reference": "Psaume 89:1", "text": "Je chanterai toujours les bontés de l'Éternel; Ma bouche fera connaître ta fidélité de génération en génération."},
            {"reference": "1 Corinthiens 4:2", "text": "Du reste, ce qu'on demande des dispensateurs, c'est que chacun soit trouvé fidèle."},
            {"reference": "Apocalypse 2:10", "text": "Sois fidèle jusqu'à la mort, et je te donnerai la couronne de vie."}
        ],
        "interpretations": [
            "Historique: La fidélité de Dieu envers ses promesses traverse toute l'histoire biblique.",
            "Spirituelle: La fidélité divine est la garantie de notre espérance et de notre salut.",
            "Pratique: Être fidèle dans les petites choses nous prépare pour de plus grandes responsabilités."
        ]
    },
    
    "sanctification": {
        "versets": [
            {"reference": "1 Thessaloniciens 4:3", "text": "Ce que Dieu veut, c'est votre sanctification"},
            {"reference": "Hébreux 12:14", "text": "Recherchez la paix avec tous, et la sanctification, sans laquelle personne ne verra le Seigneur."},
            {"reference": "1 Pierre 1:15", "text": "Mais, puisque celui qui vous a appelés est saint, vous aussi soyez saints dans toute votre conduite"},
            {"reference": "Jean 17:17", "text": "Sanctifie-les par ta vérité: ta parole est la vérité."}
        ],
        "interpretations": [
            "Historique: La sainteté était requise pour s'approcher de Dieu dans l'Ancien Testament.",
            "Spirituelle: La sanctification est l'œuvre de l'Esprit qui nous rend semblables à Christ.",
            "Pratique: Poursuivre la sanctification transforme progressivement notre caractère."
        ]
    },
    
    "baptême": {
        "versets": [
            {"reference": "Matthieu 28:19", "text": "Allez, faites de toutes les nations des disciples, les baptisant au nom du Père, du Fils et du Saint-Esprit"},
            {"reference": "Romains 6:3-4", "text": "Ignorez-vous que nous tous qui avons été baptisés en Jésus-Christ, c'est en sa mort que nous avons été baptisés? Nous avons donc été ensevelis avec lui par le baptême en sa mort"},
            {"reference": "Actes 2:38", "text": "Pierre leur dit: Repentez-vous, et que chacun de vous soit baptisé au nom de Jésus-Christ"}
        ],
        "interpretations": [
            "Historique: Le baptême était pratiqué par Jean-Baptiste et institué par Jésus.",
            "Spirituelle: Le baptême symbolise notre mort au péché et notre résurrection avec Christ.",
            "Pratique: Le baptême est un acte d'obéissance et de témoignage public de notre foi."
        ]
    },
    
    "communion": {
        "versets": [
            {"reference": "1 Corinthiens 11:24-25", "text": "et, après avoir rendu grâces, le rompit, et dit: Ceci est mon corps, qui est rompu pour vous; faites ceci en mémoire de moi. De même, après avoir soupé, il prit la coupe, et dit: Cette coupe est la nouvelle alliance en mon sang"},
            {"reference": "Matthieu 26:26-28", "text": "Pendant qu'ils mangeaient, Jésus prit du pain; et, après avoir rendu grâces, il le rompit, et le donna aux disciples, en disant: Prenez, mangez, ceci est mon corps."},
            {"reference": "1 Corinthiens 10:16", "text": "La coupe de bénédiction que nous bénissons, n'est-elle pas la communion au sang de Christ? Le pain que nous rompons, n'est-il pas la communion au corps de Christ?"}
        ],
        "interpretations": [
            "Historique: La communion fut instituée par Jésus lors de la dernière Cène.",
            "Spirituelle: La communion nous unit à Christ et à son sacrifice sur la croix.",
            "Pratique: Participer à la communion nous rappelle l'amour de Christ et fortifie notre foi."
        ]
    },
    
    "péché": {
        "versets": [
            {"reference": "Romains 3:23", "text": "Car tous ont péché et sont privés de la gloire de Dieu"},
            {"reference": "1 Jean 1:8", "text": "Si nous disons que nous n'avons pas de péché, nous nous séduisons nous-mêmes, et la vérité n'est point en nous."},
            {"reference": "Romains 6:23", "text": "Car le salaire du péché, c'est la mort; mais le don gratuit de Dieu, c'est la vie éternelle en Jésus-Christ notre Seigneur."}
        ],
        "interpretations": [
            "Historique: Le péché est entré dans le monde par la désobéissance d'Adam et Ève.",
            "Spirituelle: Le péché nous sépare de Dieu et nécessite la rédemption par Christ.",
            "Pratique: Reconnaître notre péché est le premier pas vers la repentance et le salut."
        ]
    },
    
    "évangélisation": {
        "versets": [
            {"reference": "Matthieu 28:19-20", "text": "Allez, faites de toutes les nations des disciples, les baptisant au nom du Père, du Fils et du Saint-Esprit, et enseignez-leur à observer tout ce que je vous ai prescrit."},
            {"reference": "Marc 16:15", "text": "Puis il leur dit: Allez par tout le monde, et prêchez la bonne nouvelle à toute la création."},
            {"reference": "Romains 10:14", "text": "Comment donc invoqueront-ils celui en qui ils n'ont pas cru? Et comment croiront-ils en celui dont ils n'ont pas entendu parler?"}
        ],
        "interpretations": [
            "Historique: L'évangélisation était le mandat donné par Jésus à ses disciples.",
            "Spirituelle: Partager l'Évangile est un privilège et une responsabilité pour tous les chrétiens.",
            "Pratique: L'évangélisation peut se faire par nos paroles, nos actions et notre témoignage de vie."
        ]
    },
    
    "repentance": {
        "versets": [
            {"reference": "Actes 3:19", "text": "Repentez-vous donc et convertissez-vous, pour que vos péchés soient effacés"},
            {"reference": "Luc 13:3", "text": "Non, je vous le dis. Mais si vous ne vous repentez, vous périrez tous également."},
            {"reference": "2 Corinthiens 7:10", "text": "En effet, la tristesse selon Dieu produit une repentance à salut dont on ne se repent jamais"}
        ],
        "interpretations": [
            "Historique: La repentance était prêchée par Jean-Baptiste et Jésus comme préparation au royaume.",
            "Spirituelle: La repentance implique un changement de cœur et de direction dans notre vie.",
            "Pratique: Se repentir signifie abandonner le péché et se tourner vers Dieu."
        ]
    },
    
    "grâce": {
        "versets": [
            {"reference": "Éphésiens 2:8-9", "text": "Car c'est par la grâce que vous êtes sauvés, par le moyen de la foi. Et cela ne vient pas de vous, c'est le don de Dieu. Ce n'est point par les œuvres, afin que personne ne se glorifie."},
            {"reference": "2 Corinthiens 12:9", "text": "et il m'a dit: Ma grâce te suffit, car ma puissance s'accomplit dans la faiblesse."},
            {"reference": "Romains 5:20", "text": "Or, là où le péché a abondé, la grâce a surabondé"}
        ],
        "interpretations": [
            "Historique: La grâce de Dieu se manifeste tout au long de l'histoire du salut.",
            "Spirituelle: La grâce est la faveur imméritée de Dieu envers nous malgré nos péchés.",
            "Pratique: Vivre par la grâce nous libère de la culpabilité et nous permet de grandir."
        ]
    },
    
    "éternité": {
        "versets": [
            {"reference": "Jean 3:16", "text": "Car Dieu a tant aimé le monde qu'il a donné son Fils unique, afin que quiconque croit en lui ne périsse point, mais qu'il ait la vie éternelle."},
            {"reference": "1 Jean 5:13", "text": "Je vous ai écrit ces choses, afin que vous sachiez que vous avez la vie éternelle, vous qui croyez au nom du Fils de Dieu."},
            {"reference": "Apocalypse 21:4", "text": "Il essuiera toute larme de leurs yeux, et la mort ne sera plus, et il n'y aura plus ni deuil, ni cri, ni douleur, car les premières choses ont disparu."}
        ],
        "interpretations": [
            "Historique: L'espoir de l'éternité avec Dieu a toujours été au cœur de la foi biblique.",
            "Spirituelle: L'éternité commence maintenant dans notre relation avec Dieu par Christ.",
            "Pratique: La perspective éternelle donne un sens et une espérance à notre vie présente."
        ]
    },
    
    "royaume": {
        "versets": [
            {"reference": "Matthieu 6:33", "text": "Cherchez premièrement le royaume et la justice de Dieu; et toutes ces choses vous seront données par-dessus."},
            {"reference": "Marc 1:15", "text": "Il disait: Le temps est accompli, et le royaume de Dieu est proche. Repentez-vous, et croyez à la bonne nouvelle."},
            {"reference": "Luc 17:21", "text": "On ne dira point: Il est ici, ou: Il est là. Car voici, le royaume de Dieu est au milieu de vous."}
        ],
        "interpretations": [
            "Historique: Le royaume de Dieu était le thème central de l'enseignement de Jésus.",
            "Spirituelle: Le royaume représente la souveraineté de Dieu dans nos cœurs et dans le monde.",
            "Pratique: Vivre selon les principes du royaume transforme notre manière d'être et d'agir."
        ]
    },
    
    "saint-esprit": {
        "versets": [
            {"reference": "Jean 14:26", "text": "Mais le consolateur, l'Esprit-Saint, que le Père enverra en mon nom, vous enseignera toutes choses"},
            {"reference": "Actes 1:8", "text": "Mais vous recevrez une puissance, le Saint-Esprit survenant sur vous, et vous serez mes témoins"},
            {"reference": "1 Corinthiens 6:19", "text": "Ne savez-vous pas que votre corps est le temple du Saint-Esprit qui est en vous"}
        ],
        "interpretations": [
            "Historique: L'Esprit Saint était promis par Jésus et donné à la Pentecôte.",
            "Spirituelle: L'Esprit Saint nous guide, nous console et nous donne la puissance pour vivre chrétiennement.",
            "Pratique: Être rempli de l'Esprit transforme notre vie et notre témoignage."
        ]
    },
    
    "discernement": {
        "versets": [
            {"reference": "1 Jean 4:1", "text": "Bien-aimés, n'ajoutez pas foi à tout esprit; mais éprouvez les esprits, pour savoir s'ils sont de Dieu"},
            {"reference": "Hébreux 5:14", "text": "Mais la nourriture solide est pour les hommes faits, pour ceux dont le jugement est exercé par l'usage à discerner ce qui est bien et ce qui est mal."},
            {"reference": "1 Thessaloniciens 5:21", "text": "Mais examinez toutes choses; retenez ce qui est bon"}
        ],
        "interpretations": [
            "Historique: Le discernement était nécessaire pour distinguer les vrais prophètes des faux.",
            "Spirituelle: L'Esprit Saint nous donne le discernement pour reconnaître la vérité.",
            "Pratique: Développer le discernement nous aide à faire de bons choix spirituels."
        ]
    },
    
    "providence": {
        "versets": [
            {"reference": "Romains 8:28", "text": "Nous savons, du reste, que toutes choses concourent au bien de ceux qui aiment Dieu"},
            {"reference": "Matthieu 6:26", "text": "Regardez les oiseaux du ciel: ils ne sèment ni ne moissonnent, et ils n'amassent rien dans des greniers; et votre Père céleste les nourrit."},
            {"reference": "Psaume 23:1", "text": "L'Éternel est mon berger: je ne manquerai de rien."}
        ],
        "interpretations": [
            "Historique: La providence divine s'est manifestée dans la protection et la provision pour son peuple.",
            "Spirituelle: Dieu veille sur nous et pourvoit à nos besoins selon sa sagesse parfaite.",
            "Pratique: Faire confiance à la providence divine nous libère de l'anxiété et de l'inquiétude."
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
