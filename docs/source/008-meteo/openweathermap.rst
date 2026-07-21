OpenWeatherMap API
==================

Configuration
-------------

1. Create an account on https://openweathermap.org
2. Récupérer la clé API (plan gratuit : 1000 appels/jour)
3. Renseigner la clé in le fichier ``config.ini`` lu by le module
   (fonction ``get_weather.get_api_key()``).

Usage (par GPS coordinates)
---------------------------------

.. code-block:: python

   from OpenWeatherMap import OpenWeatherMap_call_location

   # Paris (Tour Eiffel) — latitude et longitude en chaînes de caractères
   latitude = "48.858370"
   longitude = "2.294481"

   # Appel API : renvoie un DataFrame d'une ligne
   df = OpenWeatherMap_call_location.API_call_location(latitude, longitude)

   print(df)

DataFrame retourné (colonnes) :

* **Timestamp** : date/heure de la mesure ;
* **T(°C)** : temperature ;
* **RH(%)** : humidité relative.

.. note::
   ``API_call_location`` effectue un appel network to l'API OpenWeatherMap et
   requires une clé valide in ``config.ini``. The module exposes **only**
   l'appel by coordata (il n'existe pas d'appel by nom de ville).

Limites
-------

* **1000 appels/jour** (plan gratuit) ;
* ne pas interroger plus d'une fois toutes les 10-15 minutes ;
* for les data historiques, utiliser :doc:`meteociel`.
