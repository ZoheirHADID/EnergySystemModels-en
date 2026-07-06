.. _gui_tools:

Graphical Interfaces and Visual Tools
=======================================

EnergySystemModels contains several visual building blocks to build, test and
present energy models. This page is a working guide: it explains how to launch
the PyQt simulator, read a graph, add a new node and document results with the
figures actually produced by the library.

Overview
--------------

The main graphical simulator is ``PyqtSimulator``. It relies on the
``NodeEditor`` engine to manipulate nodes and connections, then calls the
library's physical models: compressor, exchanger, pump, coil, humidifier,
heater, etc.

.. figure:: images/gui_pyqtsimulator_architecture.svg
   :alt: PyQt simulator architecture
   :align: center

   General architecture: the PyQt window hosts a NodeEditor scene, registered
   nodes call EnergySystemModels models, then values are displayed or saved.

The usage principle is always the same:

1. Launch the interface.
2. Create a new scene.
3. Drag nodes from the palette.
4. Connect outputs to inputs.
5. Fill in the parameters.
6. Evaluate the graph or the output node.
7. Save the project in ``.json`` format.

Installation and Launch
-------------------------

The graphical interfaces require ``PyQt5``. In a development environment, also
install the library in editable mode or add the ``src`` folder to
``PYTHONPATH``.

.. code-block:: console

   pip install -e .
   pip install PyQt5

From the source repository:

.. code-block:: powershell

   cd A:\OneDrive\_Github_\EnergySystemModels
   $env:PYTHONPATH = "$PWD\src"
   python -m PyqtSimulator.main

The script creates a ``QApplication``, applies the ``Fusion`` style, then opens
``CalculatorWindow``. The window contains an MDI workspace and a node palette.
Each palette item comes from the ``CALC_NODES`` registry.

PyqtSimulator Interface
-----------------------

The main window groups the following elements:

``Nodes``
   Side palette. It lists the classes registered with ``@register_node(...)``.
   Dragging an item creates a node in the scene.

``Workspace``
   NodeEditor scene. Nodes are placed, moved and connected there.

``File menu``
   Creation, opening and saving of graphs. Projects are stored as JSON by the
   NodeEditor engine.

``Context menu``
   Right-click a node to evaluate it, mark it invalid, or force recalculation
   of its descendants. Right-click a connection to choose the curve type.

``Output node``
   Final display node. It triggers upstream evaluation and presents the fluid,
   flow rate, pressure, enthalpy, temperature and volumetric flow rate.

Port Convention
--------------------

Connections exchange des listes Python courtes. This convention makes les
graphs faciles à sérialiser in les fichiers ``.json``.

.. list-table::
   :header-rows: 1

   * - Type de flux
     - Format échangé
     - Unités
   * - Fluid thermodynamique
     - ``[fluid, F, P, h]``
     - ``fluid`` en chaîne, ``F`` en kg/s, ``P`` en bar, ``h`` en kJ/kg
   * - Air humide
     - ``[w, F, P, h]``
     - ``w`` en g/kg d'air sec, ``F`` en kg/s, ``P`` en bar, ``h`` en kJ/kg

Les helpers de ``PyqtSimulator.nodes.esm_node_helpers`` assurent la conversion
between these lists and the objects de the library :

``make_fluid_port(arr)``
   Convertit ``[fluid, F, P, h]`` to un ``FluidPort``.

``fluid_out(port)``
   Convertit un ``FluidPort`` de output to la liste standard.

``make_air_port(arr)`` et ``air_out(port)``
   Appliquent la même logique aux ports d'air humide.

Reading a Graph
-------------------

Pour un graph simple ``Source -> Heater -> Output`` :

.. figure:: images/gui_node_declaratif_heater.svg
   :alt: Graphe source, réchauffeur, output
   :align: center

   Le node source fournit le fluid. Le réchauffeur convertit la liste d'input
   en ``FluidPort``, appelle le model ``Heater.Object`` then renvoie une liste
   de output compatible with ``Output``.

Example d'usage :

1. Ajouter un node ``Source``.
2. Choisir le fluid, for example ``Water`` ou ``R134a``.
3. Définir le flow rate, la temperature et la pressure.
4. Ajouter un node ``Heater``.
5. Renseigner ``Power nominale`` et ``Taux de charge``.
6. Ajouter un node ``Output``.
7. Relier ``Source`` to ``Heater``, then ``Heater`` vers
   ``Output``.
8. Évaluer ``Output``.

Result attendu : ``Output`` affiche l'état de output, tandis que le node
``Heater`` affiche directement la power transférée et la temperature
de output.

Graphs with Multiple Outputs
------------------------------

Certains composants possèdent plusieurs outputs physiques. C'est le cas du
``Splitter``, du ``Séparateur liq/vap`` et du ``Ballon de flash``. Dans ces
cas, le node renvoie une liste de valeurs, une by socket de output.

.. figure:: images/gui_node_splitter_multisortie.svg
   :alt: Example de node Splitter with deux outputs
   :align: center

   Le ``Splitter`` conserve le même fluid, la même pressure et la même
   enthalpy on les deux branches. Seul le flow rate est réparti between les deux
   outputs according to le ratio saisi.

Example d'usage du ``Splitter`` :

1. Ajouter une ``Source`` with un flow rate de ``1.0 kg/s``.
2. Ajouter un node ``Splitter``.
3. Régler ``Fraction to output 1`` à ``0.30``.
4. Ajouter deux nodes ``Output``.
5. Relier la première output du ``Splitter`` to ``Output 1``.
6. Relier la deuxième output du ``Splitter`` to ``Output 2``.
7. Évaluer les deux outputs.

Result attendu :

.. list-table::
   :header-rows: 1

   * - Branche
     - Flow rate attendu
     - Commentaire
   * - Output 1
     - ``0.30 kg/s``
     - Fraction ``Ratio`` du flow rate d'input
   * - Output 2
     - ``0.70 kg/s``
     - Fraction ``1 - Ratio`` du flow rate d'input

Le routage est assuré by ``CalcNode.getOutputValue(index)``. Pour un node à
une seule output, la valeur est directement ``[fluid, F, P, h]``. Pour un node
multiple outputs, la valeur devient ``[[fluid, F1, P, h], [fluid, F2, P, h]]`` et
l'index du socket allows choisir la bonne branche.

Storage and Step-by-Step Calculation
------------------------------------

Le node ``Storage tank`` expose le model ``MixedStorage``. Il estime la
temperature d'un ballon mélangé after un time step, from la
temperature initiale, du volume, du flow rate entrant et des pertes vers
l'ambiance.

.. figure:: images/gui_node_mixed_storage_pas_temps.svg
   :alt: Example de ballon de stockage in PyqtSimulator
   :align: center

   Le node reçoit un flux entrant, calculates l'état du ballon after ``dt`` then
   renvoie un flux de output dont l'enthalpy correspond à la temperature du
   ballon.

Main Parameters :

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Signification
     - Unité
   * - ``Volume``
     - Volume d'eau ou de fluid in le ballon
     - m³
   * - ``T° initiale``
     - Temperature du ballon au début du time step
     - °C
   * - ``T° ambiante``
     - Temperature extérieure for le calcul des pertes
     - °C
   * - ``Coeff U pertes``
     - Coefficient global de pertes thermiques
     - W/m²/K
   * - ``Surface pertes``
     - Surface d'échange to l'ambiance
     - m²
   * - ``Pas de temps``
     - Durée du calcul élémentaire
     - s

Example d'usage :

1. Créer une ``Source`` with un fluid compatible CoolProp, for example
   ``Water``.
2. Définir une temperature d'input supérieure à la temperature initiale du
   ballon for simulatesr une charge, ou inférieure for simulatesr une décharge.
3. Ajouter ``Storage tank``.
4. Renseigner ``Volume``, ``T° initiale``, ``T° ambiante`` et ``Pas de temps``.
5. Ajouter ``Output`` en output.
6. Évaluer le graph.

Results affichés localement :

``T° ballon``
   Temperature du volume mélangé after le time step.

``Power stockage``
   Power moyenne stockée ou restituée during le time step.

Limite importante : in l'interface actuelle, le node crée une nouvelle
instance du model à chaque évaluation. Il représente donc un time step
isolé from ``T° initiale``. Pour simulatesr une série temporelle complète, il
faut mettre à jour ``T° initiale`` between les pas ou utiliser un script Python
qui conserve l'objet ``MixedStorage`` between deux appels à ``calculate()``.

Evaluation Cycle
------------------

Lorsqu'un paramètre est modifié, le node est marqué comme sale et ses
descendants doivent être recalculés. L'évaluation d'un node de output remonte
le graph jusqu'aux sources, then propage les valeurs to l'aval.

.. figure:: images/gui_evaluation_flow.svg
   :alt: Evaluation Cycle d'un graph
   :align: center

   Les champs Qt déclenchent ``onInputChanged``. Le node aval demande ensuite
   l'évaluation des nodes amont, retrieves leurs valeurs et appelle son model
   physique.

Les points importants for l'utilisateur sont :

1. Un node without input connectée devient invalide.
2. Une saisie numérique invalide doit être corrigée before d'obtenir un result
   fiable.
3. Le node ``Output`` est le meilleur point de contrôle : il force le calcul
   de toute la chaîne amont.
4. Les unités affichées ne sont pas toujours celles useds en interne. Par
   example, la pressure circule en bar in le graph mais les models peuvent
   utiliser le pascal.

Creating a New Node
---------------------

Pour exposer un model EnergySystemModels in l'interface, utiliser de
préférence la classe ``ESMNode``. Elle évite de réécrire l'interface Qt, la
sérialisation et les labels de results.

Un node déclaratif contient :

``op_code``
   Identifiant numérique unique in ``PyqtSimulator.calc_conf``.

``op_title``
   Nom affiché in la palette.

``icon``
   Chemin de l'icône affichée in la liste.

``INPUTS`` et ``OUTPUTS``
   Sockets d'input et de output.

   Pour un composant simple, ``OUTPUTS = [1]`` suffit. Pour un composant à
   deux outputs, utiliser ``OUTPUTS = [1, 1]`` et retourner une liste de deux
   ports in le même ordre que les sockets.

   .. code-block:: python

      OUTPUTS = [1, 1]

      def evalOperation(self, input1, input2):
          ...
          self.value = [fluid_out(model.Outlet_b), fluid_out(model.Outlet_c)]
          return self.value

``FIELDS``
   Champs numériques affichés under forme de ``QLineEdit``.

``CHOICES``
   Listes déroulantes affichées under forme de ``QComboBox``.

``RESULTS``
   Labels de output mis à jour by le calcul.

``evalOperation(...)``
   Code métier : lecture des inputs, appel du model, affichage des results,
   retour de la valeur de output.

Real Example: Heater Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le node ``Heater`` illustre la structure recommandée.

.. code-block:: python

   from ThermodynamicCycles.Components import Heater
   from ThermodynamicCycles.FluidPort.FluidPort import Fluid_connect
   from PyqtSimulator.calc_conf import register_node, OP_NODE_HEATER
   from PyqtSimulator.nodes.esm_node_helpers import ESMNode, make_fluid_port, fluid_out


   @register_node(OP_NODE_HEATER)
   class CalcNode_Heater(ESMNode):
       icon = "icons/heating_coil.png"
       op_code = OP_NODE_HEATER
       op_title = "Réchauffeur"
       content_label_objname = "calc_node_heater"

       INPUTS = [2]
       OUTPUTS = [1]
       HEIGHT = 300

       FIELDS = [
           ("q_nom", "Puissance nominale (kW)", 100.0),
           ("u", "Taux de charge (0-1)", 1.0),
       ]
       RESULTS = [
           ("q", "Puissance transférée (kW)"),
           ("to", "T° sortie (°C)"),
       ]

       def evalOperation(self, input1, input2):
           a = make_fluid_port(input1)
           model = Heater.Object()
           Fluid_connect(model.Inlet, a)
           model.Q_flow_nominal = self.num("q_nom") * 1000.0
           model.u = self.num("u")
           model.calculate()

           self.show_result("q", "%.3f" % (model.Q_flow / 1000.0))
           self.show_result("to", "%.2f" % model.To_degC)

           self.value = fluid_out(model.Outlet)
           return self.value

Ce model donne une règle générale : les champs affichés en kW ou en bar sont
convertis in les unités attendues by le model, then reconvertis for les
ports ou les labels utilisateur.

Registering the Node in the Palette
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Ajouter un code unique in ``PyqtSimulator.calc_conf``.
2. Décorer la classe with ``@register_node(OP_NODE_...)``.
3. Placer le fichier in ``PyqtSimulator/nodes``.
4. Vérifier que le module est importé. Le fichier ``nodes/__init__.py`` importe
   automatiquement les fichiers ``.py`` du dossier.
5. Relancer ``PyqtSimulator``. Le node doit apparaître in la palette.

Example de réservation d'opcode :

.. code-block:: python

   OP_NODE_HEATER = 280

Development Best Practices
---------------------------------

Utiliser des noms de champs explicites
   Le libellé doit contenir l'unité : ``Power nominale (kW)``,
   ``Pressure output (bar)``, ``Rendement (-)``.

Limiter la logique Qt in les nodes
   Pour les nouveaux models, préférer ``ESMNode`` et garder le code métier
   dans ``evalOperation``.

Valider les unités à chaque conversion
   Les ports internes des models utilisent souvent le pascal et le joule par
   kilogramme. Les graphs utilisent plutôt le bar et le kJ/kg.

Afficher les results utiles localement
   Un node de composant peut afficher ses indicateurs propres : power,
   rendement, temperature de output, humidité relative, COP, pressure drop.

Tester with un graph minimal
   Avant d'intégrer un composant complexe, tester ``Source -> composant ->
   Output``. Ajouter ensuite les branches multiples.

Documenter le comportement
   Each important new node must have an example in the documentation :
   diagram du graph, paramètres, results attendus, limites et figure si une
   method ``plot()`` existe.

Results and Figures in the Documentation
------------------------------------------

La documentation doit distinguer trois types de visuels :

``Diagram de graph``
   Figure pédagogique montrant les nodes et les connexions. Ces diagrams sont
   générés from ``docs/source/diagrams/*.json`` par
   ``docs/generate_diagrams.py``.

``Table de results``
   Valeurs numériques issues d'un example reproductible. Les unités doivent
   être visibles in l'en-tête ou in la première colonne.

``Plot du model``
   Figure produite by une method realle de the library : for example
   ``ch.plot()``, ``calc.plot()`` ou ``calc.plot_detail()``. Il ne faut pas
   remplacer ces methods by un tracé manuel arbitraire lorsque le model
   fournit déjà sa propre fonction de visualisation.

Workflow recommandé for une page d'example :

1. Décrire le cas étudié et les hypothèses.
2. Afficher le diagram des nodes connectés.
3. Donner le code minimal reproductible.
4. Afficher les results in une table.
5. Afficher les plots actually générés by les fonctions du model.
6. Ajouter une courte interprétation métier.

Generating Diagrams and Plots
-----------------------------

Dethen le dépôt ``EnergySystemModels-fr`` :

.. code-block:: powershell

   cd A:\OneDrive\_Github_\EnergySystemModels-fr
   python docs\generate_diagrams.py

Pour les plots actually exposés by les models :

.. code-block:: powershell

   cd A:\OneDrive\_Github_\EnergySystemModels-fr
   $env:PYTHONPATH = "A:\OneDrive\_Github_\EnergySystemModels\src"
   $env:PYTHONIOENCODING = "utf-8"
   python docs\generate_model_plots.py

Le fichier ``generate_model_plots.py`` doit rester strict : il appelle les
methods de plot de the library and saves the figures dans
``docs/source/images``. Les figures de remplacement ne sont acceptables que
pour les examples without method graphique déterministe, et elles doivent être
signalées comme telles in le script.

Building the Documentation
---------------------------

.. code-block:: powershell

   cd A:\OneDrive\_Github_\EnergySystemModels-fr
   python -m sphinx -b html docs\source docs\_build\html

Ouvrir ensuite ``docs\_build\html\gui_tools.html`` for vérifier la mise en
forme. Contrôler en particulier :

1. Les chemins ``.. figure:: images/...``.
2. Les unités in les tableaux.
3. La lisibilité des diagrams on une largeur réduite.
4. La présence des plots lorsque l'example appelle une method ``plot``.

Troubleshooting
---------------

``ModuleNotFoundError: PyqtSimulator``
   Ajouter ``EnergySystemModels/src`` au ``PYTHONPATH`` ou installer le paquet
   en mode éditable.

``QApplication`` ou ``PyQt5`` introuvable
   Install ``PyQt5`` in l'environnement actif.

``CoolProp`` introuvable
   Install les dépendances scientifiques useds by les composants
   thermodynamiques.

Un node n'apparaît pas in la palette
   Vérifier l'opcode, le décorateur ``@register_node``, le nom du fichier dans
   ``PyqtSimulator/nodes`` et les erreurs d'import au démarrage.

Un result ne se met pas à jour
   Vérifier que les champs sont connectés à ``onInputChanged``. Avec
   ``ESMNode``, cette connexion est automatique for ``FIELDS`` et ``CHOICES``.

Une connexion est refusée
   Le moteur empêche de relier deux inputs, deux outputs ou un node à lui-même.
   Repartir de la output du node amont to l'input du node aval.

Un plot manque in ReadTheDocs
   Vérifier que la figure est générée in ``docs/source/images`` before le build
   et que le document référence exactement le bon nom de fichier.

Checklist for Finalizing an Example
-----------------------------------

Avant de considérer une page comme complète :

1. Le scénario est compréhensible without lire le code source.
2. Les nodes et connexions sont diagramtisés.
3. Les paramètres d'input sont listés with unités.
4. Les results sont affichés in une table lisible.
5. Les plots existants du model sont affichés.
6. Les limites de validité sont indiquées.
7. Le code est reproductible from un environnement propre.
8. Le build Sphinx passe without erreur liée à la page.
