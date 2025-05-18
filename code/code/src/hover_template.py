'''
    Provides the template for the hover tooltips.
'''
from modes import MODES


def get_hover_template(name, mode):
    '''
        Sets the template for the hover tooltips.

        The template contains:
            * A title stating player name with:
                - Font family: Grenze Gotish
                - Font size: 24px
                - Font color: Black
            * The number of lines spoken by the player, formatted as:
                - The number of lines if the mode is 'Count ("X lines").
                - The percent of lines fomatted with two
                    decimal points followed by a '%' symbol
                    if the mode is 'Percent' ("Y% of lines").

        Args:
            name: The hovered element's player's name
            mode: The current display mode
        Returns:
            The hover template with the elements descibed above
    '''
    #Si le mode est count on affiche la valeur
    if mode == MODES['count']:
        hover_sentence = "%{y} lines" 
    #si le mode est percent, on affiche le pourcentage formaté
    elif mode == MODES['percent']:
        hover_sentence = "%{y:.2f}% of lines" 
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    #on associe le message formaté à l'evenement hover_template et on supprime l'anciènne trace du over pour éviter l'effet de dédoublement
    hover_template = (
        f"<span style='font-family: Grenze Gotisch; font-size: 24px; color: black;'>"
        f"{name}</span><br>{hover_sentence}<extra></extra>"
    )
    return hover_template
