# Python_Course_Project
Yksinkertainen "tasohyppely" -peli käyttäen Pygame-nimistä python-kirjastoa, joka on luotu auttamaan pelien ja "kuvien" luontia erilaisiin, mutta yksinkertaisiin käyttötarkoituksiin. On hyvä huomioida, ettei Pygamea ole tarkoitettu suuriin, AAA-peleihin verrattaviin projekteihin, mutta tästäkin huolimatta Pygamen on hyvä valinta henkilölle, joka haluaa haastaa itseään ja oppia hieman syvällisemmin Python-kielen käyttöä, mikä onkin yksi syy miksi päätin ottaa tämän projektikseni.

Pelin idea on yksinkertainen tasohyppely, jossa pelaajan hahmo "pysyy paikallaan" liikkuvalla taustalla, hyppien ja väistäen esteitä/vihollisia, keräten pisteitä kerryttäviä objekteja tiettyyn määrään saakka.
Peli alkaa ikkunasta, jossa on mahdollisuus valita pelimuoto, tarkistaa aikaisempien pelikertojen ajat ja tulokset sekä mahdollisuus sulkea peli.  

Pelissä olisi kaksi pelimuotoa; Single Run, eli yksisuoritus, jossa pelisessio loppuu pelaajan kerättyä 100 pistettä, ja Endless, eli ikuinen, jossa pelaajaan sessio ei koskaan lopu, vaan hänen täytyy manuaalisesti lopettaa sessios painamalla X-kirjainta. Molemmissa muodoissa peli loppuu loppunäkymään, joka kertoo pelaajalle kerrytetyt pisteet ja käytetyn ajan, sekä kysyy haluatko aloittaa uuden pelin. Mikäli onnistun siinä, luon myös tiedoston, joka pitää yllä tilastoa aikaisemmista pelikerroista, jota olisi mahdollista tutkia myöhemmillä pelisessioilla.

The game idea is a simplistic platformer, akin to Geometry Dash and games such as that, where the player "stays in place" in a moving game map, avoiding enemies/obstacles by jumping and slightly horizontal movements, while collecting items that provide points. 

The game would begin in a start menu with three options, allowing you to choose between a "single run" -mode, where the run lasts until you collect 100 points, and an "endless" -mode, that continues until the player decides  to quit the game. When the player begins the game, they will be greeted by an "empty" moving map and in a moment the enemies will start spawning from the right. When the player sprite hits an enemy sprite, they lose one health point, resulting in a game over if they lose all three of their health points.

There would be two kinds of enemies. One is a "snail" that is at ground level and the other a "fly" which, as you might imagine, flies. 

When the player finishes their run and depending if the game ended in a success or a game over, they will receive an appropriately titled screen that displays the time spent and collected points, giving them the option to return to the start menu or quit the game.

For player movement I think the space + left & right keys will be enough. Ther must also be a gravity variable that brings the player down to ground level when they jump, and something that stops them from going below ground level.