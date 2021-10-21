from ru_soundex.soundex import RussianSoundex
from ru_soundex.distance import SoundexDistance

soundex = RussianSoundex(delete_first_letter=True)
print(soundex.transform('ёлочка'))

soundex = RussianSoundex(delete_first_letter=True)
soundex_distance = SoundexDistance(soundex)
print(soundex_distance.distance('ёлочка', 'йолочка'))

from Levenshtein import distance as lev
print(lev('ёлочка', 'йолочка'))