"""
Fonctions utilitaires :
- fitness.py : Calculs de fitness avancés
- visualization.py : Outils de visualisation
"""

from .fitness import normalize
from .visualization import plot_evolution

__all__ = [
    'normalize',
    'plot_evolution'
]