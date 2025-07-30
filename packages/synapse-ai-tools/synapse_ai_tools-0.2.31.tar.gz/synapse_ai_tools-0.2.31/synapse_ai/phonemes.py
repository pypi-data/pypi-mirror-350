import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd






def phoneme(text:str, punctuation:bool=False) -> str:
    """
    Transforms Spanish text into a simplified phonetic representation based on predefined rules.

    This function applies a series of transformations to approximate the phonetic structure 
    of Spanish words. It normalizes input text by removing punctuation, converting to lowercase, 
    and replacing specific character patterns with their phonetic equivalents.

    Args:
        text (str): The input Spanish text to be transformed.
        punctuation (bool, optinal): If it is True, only deletes characters "¿" and "¡". If it is False, deletes all special characters. Defaults to False.
        

    Returns:
        str: A string containing the transformed phonetic representation.

    Transformations include:
        - Normalization: Converts text to lowercase and removes non-alphanumeric characters.
        - Removes silent "h" characters that do not affect pronunciation.
        - Phonetic rules for "c", "x", "qu", "g", "j", "v", "z", etc., to approximate pronunciation.
        - Substitutes certain clusters, e.g., "xc" → "ks", "ca" → "ka", "qu" → "k".
        - Handles soft and hard "g" sounds ("ge", "gi", "j" → "x").
        - Replaces double consonants or ambiguous vowels for simplicity, e.g., "rr" → "r".
        - Marks the flap "r" with `chr(638)` to distinguish it from other "r" cases.
        - Converts "ñ" to "ni", "z" to "s", and adjusts "y" depending on its position.

    Examples:
        >>> phoneme("Canción y jardín.")
        'kansión i xardín'
        >>> phoneme("El que quiso jugar.")
        'el ke kiso xugar'
    """

    if punctuation:
        text = text.lower().replace('¿', '').replace('¡', '').replace('.', ' .').replace(',', ' ,').replace('?', ' ?').replace(':', ' :')
    else:
        text = re.sub('[^\w\s]', '', text.lower())
    text = text.replace('\n', ' ')
    split_text = text.split(" ")
    new_text = ""
    temp_text = ""
    for word in split_text:
        temp_text = word     
        if 'h' in temp_text:
            if temp_text[0] == 'h':
                temp_text = temp_text.replace('h', '')
            if not 'sh' in temp_text and not 'ch' in temp_text:
                temp_text = temp_text.replace('h', '')
        if "xc" in temp_text:
            temp_text = temp_text.replace("x", "k")
        if "ca" in temp_text: 
            temp_text = temp_text.replace("ca", "ka")
        if "cá" in temp_text:
            temp_text = temp_text.replace("cá", "ká")
        if "co" in temp_text:
            temp_text = temp_text.replace("co", "ko")
        if "có" in temp_text:
            temp_text = temp_text.replace("có", "kó")
        if "cu" in temp_text:
            temp_text = temp_text.replace("cu", "ku")
        if "cú" in temp_text:
            temp_text = temp_text.replace("cú", "kú")
        if "que" in temp_text or "qué" in temp_text:
            temp_text = temp_text.replace("qu", "k")
        if "qui" in temp_text or "quí" in temp_text:
            temp_text = temp_text.replace("qu", "k")
        if "cr" in temp_text: 
            temp_text = temp_text.replace("cr", "kr")
        if "ct" in temp_text: 
            temp_text = temp_text.replace("ct", "kt")
        if "cl" in temp_text: 
            temp_text = temp_text.replace("cl", "kl")
        if "cd" in temp_text:
            temp_text = temp_text.replace("cd", "kd")
        if "x" in temp_text:
            temp_text = temp_text.replace("x", "ks")
        if "ge" in temp_text or "gé" in temp_text or "gi" in temp_text or "gí" in temp_text:
            temp_text = temp_text.replace("g", "x")
        if "j" in temp_text:
            temp_text = temp_text.replace("j", "x")
        if "gue" in temp_text or "gué" in temp_text or "gui" in temp_text or "guí" in temp_text:
            temp_text = temp_text.replace("gu", "g")
        if "bv" in temp_text:
            temp_text = temp_text.replace("bv", "b")
        if "v" in temp_text:
            temp_text = temp_text.replace("v", "b")
        if "cc" in temp_text:
            temp_text = temp_text.replace("cc", "ks")
        if "ce" in temp_text:
            temp_text = temp_text.replace("ce", "se")
        if "cé" in temp_text: 
            temp_text = temp_text.replace("cé", "sé")
        if "ci" in temp_text: 
            temp_text = temp_text.replace("ci", "si")
        if "cí" in temp_text:
            temp_text = temp_text.replace("cí", "sí")
        if "z" in temp_text:
            temp_text = temp_text.replace("z", "s")
        if "ñ" in temp_text:
            temp_text = temp_text.replace("ñ", "ni")
        if "r" in temp_text:
            temp_text = re.sub(r'(?<!^)(?<!r)r(?!r)', chr(638), temp_text)
        if "rr" in temp_text:
            temp_text = temp_text.replace("rr", "r")
        if "y" in temp_text:
            if len(temp_text) == 1 or temp_text.endswith("y"):
                temp_text = temp_text.replace("y", "i")
            else:
                temp_text = temp_text.replace("y", "ll")
        if "sh" in temp_text:
            temp_text = temp_text.replace("sh", chr(643))
        if "ll" in temp_text:
            if temp_text.endswith('ll'):
                temp_text = temp_text.replace("ll", 'l')
            else:
                temp_text = temp_text.replace("ll", chr(669))
        if "ch" in temp_text:
            temp_text = temp_text.replace("ch", chr(679))
        if "w" in temp_text:
            if temp_text[0] == "w":
                temp_text = temp_text.replace("w", "gu")
            else:
                temp_text = temp_text.replace("w", "u")
        new_text += temp_text + " "
    return new_text



def accent(text:str, punctuation:bool=False) -> str:
    """
    Applies prosodic accentuation to Spanish text based on predefined phonetic and grammatical rules.

    This function processes text to add appropriate diacritical marks (accents) to vowels 
    following Spanish accentuation rules. It handles various word structures and considers 
    the length, position of vowels, and terminal characters to determine where to place accents.

    Args:
        text (str): The input Spanish text to be accented.
        punctuation (bool, optinal): If it is True, only deletes characters "¿" and "¡". If it is False, deletes all special characters. Defaults to False.

    Returns:
        str: A string with words accented based on Spanish prosodic rules.

    Main Features:
        - Normalizes text: Converts to lowercase and removes punctuation.
        - Applies accentuation rules:
            - Words already containing accents are left unchanged.
            - Single-character words and two-character vowel-only words are handled explicitly.
            - Longer words are processed to identify vowels requiring accents based on syllable 
            structure and terminal characters.
        - Considers word endings:
            - Words ending in consonants (not "n", "s", or vowels) are likely acute.
            - Words ending in vowels or "n" or "s" follow standard stress patterns.
        - Multi-syllable words are processed iteratively, accentuating vowels in stressed syllables.

    Examples:
        >>> accent("camino farol pasear resumen")
        'camíno faról paseár resúmen'

        >>> accent("canción sin acento alguno")
        'canción sin acénto algúno'

    Limitations:
        - Assumes input text adheres to standard Spanish orthography.
        - May not handle edge cases for compound or irregularly stressed words.
    """

    if punctuation:
        text = text.lower().replace('¿', '').replace('¡', '').replace('.', ' .').replace(',', ' ,').replace('?', ' ?').replace(':', ' :')
    else:
        text = re.sub('[^\w\s]', '', text.lower())
    text = text.replace('\n', ' ')
    split_text = text.split(" ")
    new_text = ""
    temp_text = ""
    accents_dictionary = {'a':'á', 'e':'é', 'i':'í', 'o':'ó', 'u':'ú'}
    for word in split_text:
        temp_text = word
        try:
            if len(word) == 1:
                temp_text = word
            elif any(letter in 'áéíóú' for letter in word):
                temp_text = word
            elif len(word) == 2:
                if word[0] in 'aeiou' and word[1] in 'aeiou':
                    temp_text = word
                elif word[0] in "aeiou" and word[1] in "aeiou":
                    temp_text = word.replace(word[0], accents_dictionary[word[0]])
                else:
                    temp_text = word
            elif len(word) == 3:
                if word[0] in 'aeiou' and word[1] in 'aeiou' and word[2] in 'aeiou':
                    temp_text = word
                elif word[1] not in "aeiou":
                    word_without_vowel = word[1:] 
                    accented_vowel = accents_dictionary[word[0]]
                    temp_text = accented_vowel + word_without_vowel  
                elif word[-1] in "aeiou" and word[-2] == "e":
                    accented_vowel = accents_dictionary[word[-2]]
                    temp_text = word[0] + accented_vowel + word[-1]
                else: 
                    temp_text = word
            elif word[-1] not in 'aeouns' and word[-1] != chr(643): 
                if word[-2] in 'aeiou':
                    word_without_vowel = word[:-2] 
                    accented_vowel = accents_dictionary[word[-2]] 
                    temp_text =  word_without_vowel + accented_vowel + word[-1] 
                else:
                    word_without_vowel = word[:-3] 
                    accented_vowel = accents_dictionary[word[-3]] 
                    temp_text =  word_without_vowel + accented_vowel + word[-2:]
            else: 
                if 'ai' in word:
                    temp_text = word.replace('ai', 'ái')
                elif word[-1] in 'aeiou' and word[-2] in 'aeiou': 
                    if word[-2:] != 'ia' and word[-2:] != 'io': 
                        if word[-4] in 'aeiou':
                            word_without_vowel = word[:-4]
                            accented_vowel = accents_dictionary[word[-4]]
                            temp_text =  word_without_vowel + accented_vowel + word[-3:]
                    else:  
                        if word[-4] in 'aeiou': 
                            word_without_vowel = word[:-4] 
                            accented_vowel = accents_dictionary[word[-4]] 
                            temp_text =  word_without_vowel + accented_vowel + word[-3:] 
                        elif word[-5] in 'aeiou':
                            word_without_vowel = word[:-5]
                            accented_vowel = accents_dictionary[word[-5]]
                            temp_text =  word_without_vowel + accented_vowel + word[-4:] 
                        else:
                            word_without_vowel = word[:-6]
                            accented_vowel = accents_dictionary[word[-6]]
                            temp_text =  word_without_vowel + accented_vowel + word[-5:]
                elif len(word) == 4 and word[-1] == 'n' and word[-2] in 'aeiou' and word[-3] in 'aeiou':
                    word_without_vowel = word[:-2]
                    accented_vowel = accents_dictionary[word[-2]]
                    temp_text =  word_without_vowel + accented_vowel + word[-1]
                elif word[-1] in 'aeiou' and word[-2] not in 'aeiou':
                    if len(word) > 6 and 'ei' in word[-6:]:
                         temp_text = temp_text.replace('ei', 'éi') 
                    elif word[-3] in 'aeiou':
                        word_without_vowel = word[:-3]
                        accented_vowel = accents_dictionary[word[-3]]
                        temp_text =  word_without_vowel + accented_vowel + word[-2:]
                    elif word[-4] in 'aeiou':
                        word_without_vowel = word[:-4]
                        accented_vowel = accents_dictionary[word[-4]]
                        temp_text =  word_without_vowel + accented_vowel + word[-3:]
                    elif word[-5] in 'aeiou':
                        word_without_vowel = word[:-5]
                        accented_vowel = accents_dictionary[word[-5]]
                        temp_text =  word_without_vowel + accented_vowel + word[-4:]
                    else:
                        word_without_vowel = word[:-6]
                        accented_vowel = accents_dictionary[word[-6]]
                        temp_text =  word_without_vowel + accented_vowel + word[-5:]
                elif word[-1] not in 'aeiou' and word[-2] in 'aeiou':
                    if len(word) > 6 and 'ei' in word[-6:]:
                         temp_text = temp_text.replace('ei', 'éi') 
                    elif word[-3] in 'aeiou':
                        word_without_vowel = word[:-3]
                        accented_vowel = accents_dictionary[word[-3]]
                        temp_text =  word_without_vowel + accented_vowel + word[-2:]
                    elif word[-4] in 'aeiou':
                        word_without_vowel = word[:-4]
                        accented_vowel = accents_dictionary[word[-4]]
                        temp_text =  word_without_vowel + accented_vowel + word[-3:]
                    elif word[-5] in 'aeiou':
                        word_without_vowel = word[:-5]
                        accented_vowel = accents_dictionary[word[-5]]
                        temp_text =  word_without_vowel + accented_vowel + word[-4:]
                    else:
                        word_without_vowel = word[:-6]
                        accented_vowel = accents_dictionary[word[-6]]
                        temp_text =  word_without_vowel + accented_vowel + word[-5:]
            new_text += temp_text + " "
        except:
            new_text += word + " "
            continue
    return new_text




def dictionaries(text:str) -> tuple[dict[str, int], dict[str, int]]:
    """
    Generates two dictionaries from the input text: a phoneme-to-index dictionary and a phoneme frequency dictionary.

    This function processes the input text to create:
    1. A mapping of unique characters (phonemes) to indices, with an additional "pad" token for padding.
    2. A dictionary counting the frequency of each phoneme in the text.

    Args:
        text (str): Input text to process for phoneme mapping and frequency counting.

    Returns:
        tuple[dict[str, int], dict[str, int]]: A tuple containing:
            - phonemes_dictionary (dict[str, int]): A dictionary where keys are unique characters (phonemes) 
              from the text and values are their respective indices. The special key "pad" maps to 0.
            - phonemes_quantity (dict[str, int]): A dictionary where keys are unique characters (phonemes) 
              and values are the counts of their occurrences in the text.

    Features:
        - Creates a unique index for each phoneme based on their sorted order in the text.
        - Includes a "pad" token for compatibility with padding operations, assigned to index 0.
        - Calculates the frequency of each phoneme in the input text.

    Examples:
        >>> text = "hola mundo"
        >>> dictionaries(text)
        ({' ': 1, 'a': 2, 'd': 3, 'h': 4, 'l': 5, 'm': 6, 'n': 7, 'o': 8, 'u': 9, 'pad': 0},
        {' ': 1, 'a': 1, 'd': 1, 'h': 1, 'l': 1, 'm': 1, 'n': 1, 'o': 2, 'u': 1, 'pad': 0})

    Limitations:
        - Does not handle special characters or non-standard inputs explicitly; it processes all characters as-is.
        - Assumes text is pre-processed (e.g., lowercased and stripped of punctuation) if necessary.

    Notes:
        - The function creates an index starting at 1 for phonemes, reserving 0 for "pad".
        - Frequencies in `phonemes_quantity` are initialized to 0 and updated iteratively for each character in the text.
    """

    phonemes_dictionary = {k:v+1 for v,k in enumerate(sorted(set(text)))}
    phonemes_dictionary['pad'] = 0
    phonemes_quantity = {}
    for k in phonemes_dictionary.keys():
        phonemes_quantity[k] = 0
    for letter in text:
        phonemes_quantity[letter] += 1
    return (phonemes_dictionary, phonemes_quantity)
    


def phoneme_graphs(tokens:dict, quantity:dict, fig_size:tuple[int]=(8,8), color:str='violet') -> None:
    """
    Visualizes the frequency of phonemes in a bar chart.

    This function generates a bar chart displaying the frequency of phonemes in the input data. 
    The phonemes are ordered based on their indices in the provided token dictionary.

    Args:
        tokens (dict): A dictionary mapping phonemes to their indices, used to define the order of phonemes in the plot.
        quantity (dict): A dictionary where keys are phonemes and values are their frequencies.
        fig_size (tuple[int], optional): A tuple specifying the size of the figure in inches (width, height). Defaults to (8, 8).
        color (str, optional): The color of the bars in the chart, specified as a valid Matplotlib color. Defaults to 'violet'.

    Returns:
        None: The function directly displays the plot.

    Features:
        - Creates a DataFrame to combine phoneme frequencies, their corresponding indices, and their labels.
        - Sorts the phonemes by their order in the `tokens` dictionary to ensure consistent visualization.
        - Uses Seaborn for bar chart creation, with customization for layout.

    Examples:
        >>> quantity = {'a': 10, 'e': 15, 'i': 8, 'o': 20, 'u': 5}
        >>> tokens = {'a': 1, 'e': 2, 'i': 3, 'o': 4, 'u': 5, 'pad': 0}
        >>> phoneme_graphs(quantity, tokens)

        This example will display a bar chart with the phonemes "a", "e", "i", "o", "u" sorted in the order 
        defined by the `tokens` dictionary, with frequencies as heights.

    Notes:
        - The x-axis represents phonemes, and the y-axis represents their frequencies.
        - Phonemes are sorted according to the `tokens` dictionary before plotting.
        - A tight layout ensures the chart fits well within the figure dimensions.

    Dependencies:
        - Requires Matplotlib, Seaborn, and Pandas for visualization and data handling.

    Limitations:
        - Assumes that all phonemes in the `quantity` dictionary have corresponding indices in `tokens`.
        - Does not handle missing or mismatched keys between `quantity` and `tokens`.

    Customizations:
        - You can modify `fig_size` to change the dimensions of the figure.
        - You can modify `color` to use any Matplotlib-compatible color for the bars.
    """

    data = pd.DataFrame({'phoneme': quantity.keys(), 'frequency': quantity.values(), 'order': [tokens[fonema] for fonema in quantity.keys()]})
    data = data.sort_values(by='order')
    plt.figure(figsize=fig_size)
    sns.barplot(data=data, x='phoneme', y='frequency', color=color)
    plt.title('Phoneme Frequency', fontsize=16)
    plt.xlabel('Phoneme', fontsize=10)
    plt.ylabel('Frequency', fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


