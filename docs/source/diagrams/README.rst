:orphan:

Diagrammes de documentation
===========================

Ce dossier contient les descriptions ``JSON`` useds for générer les
figures de principe de la documentation.

Each file describes :

* des ``nodes`` : composants, sources, usages, pertes, utilités ;
* des ``edges`` : flux de chaleur, fluid, électricité, économie ou calcul ;
* une ``column`` by node for contrôler l'ordre gauche-droite du diagram.

Pour régénérer les figures ``SVG`` :

.. code-block:: console

   python docs/generate_diagrams.py

Les images générées sont écrites in ``docs/source/images`` et can be
référencées in les pages ``.rst`` with la directive ``figure``.
