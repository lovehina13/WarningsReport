# WarningsReport

WarningsReport est une application console permettant la récupération des avertissements de compilation et des diagnostics pour les sources C++ d'un projet CMake et la génération d'un rapport au format HTML.

Les fonctionnalités de l'application sont les suivantes :
 - Compilation fictive des sources C++ d'un projet CMake avec le compilateur `Clang++` et l'outil `Clang-tidy`.
 - Récupération des avertissements de compilation et des diagnostics.
 - Génération d'un rapport au format HTML.
 - Paramétrage des critères d'analyse et de compte-rendu.

L'application est réalisée en bash et [Python 3.7.3](https://www.python.org/downloads/release/python-373/) et nécessite l'outil [CMake](https://cmake.org/) et le compilateur [Clang++](https://clang.llvm.org/).

Un exemple de rapport au format HTML est disponible [ici](http://alexis.foerster.free.fr/github/warnings-report.html).
