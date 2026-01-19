"""
Créé par OrangeGrenadine
17/01/2026

Sans utiliser SageMath, on essaie de se défaire de Numpy et donc
on essaie de 'recoder' l'algèbre héhé :)
"""

"""
On veut recréer les opérations sur les octets.

Ici on manipule directement des entiers modulo 2.
On les écrit sous la forme 0b..., soit les coefficients 
du polynôme associés vus dans Z/2Z.

Par exemple X^3 + X^2 + 1 s'écrira 0b1101
Où 1101 correspond bien à 13 en base 2.
"""


def ADD(a, b):
	"""'a' et 'b' sont vus comme des polynômes dans Z/2Z[X].

	Renvoie l'addition entre 'a' et 'b'.
	Correspond à la porte logique XOR
	ou encore l'addition sans retenue.

	"""
	return(a ^ b)

def DOT(a, b):
	"""'a' et 'b' sont vus comme des polynômes dans Z/2Z[X].

	Renvoie la multiplication entre 'a' et 'b'.
	"""
	resultat = 0
	while b:
		if b & 1:
			resultat = ADD(resultat, a)
		a <<= 1 
		b >>= 1
	return(resultat)

	
def MOD(a, q):
	"""'a' et 'q' sont vus comme des polynômes dans Z/2Z[X].

	Renvoie le modulo de 'a' par 'q'.
	"""		
	deg_q = q.bit_length() - 1
	while a.bit_length() - 1 >= deg_q:
		shift = (a.bit_length() - 1) - deg_q
		a ^= q << shift
	return(a)

def POWER(a, p):
	"""'a' et 'p' sont vus comme des polynômes dans Z/2Z[X].

	Renvoie 'a' élevé à la puissance 'p'.
	"""	
	resultat = 1
	while p:
		if p & 1:
			resultat = DOT(resultat, a)
		a = DOT(a ,a)
		p >>= 1
	return(resultat)

# - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - -

def LAMBDA(f):
	"""Correspond à la fonction lambda :

	Lambda(f) = (X^4+X^3+X^2+X+1)*f + (X^6+X^5+X+1) [X^8+1]

	f : polynôme vu dans Z/2Z[X] de degré strictement
	inférieur à 8.
	"""
	return(MOD(ADD(DOT(0b11111, f), 0b1100011), 0b100000001))

def invLAMBDA(f):
	"""Correspond à la fonction lambda^{-1} :

	Lambda^{-1}(f) = (X^6+X^3+X)*f + (X^2+1) [X^8+1]

	f : polynôme vu dans Z/2Z[X] de degré strictement
	inférieur à 8.
	"""
	return(MOD(ADD(DOT(0b1001010, f), 0b101), 0b100000001))

"""
On affirme qu'un octet est un polynôme vu dans F256 de degré 
strictement inférieur à 8 !

Dans notre cas, cette conversion dans F256 ne sera pas nécessaire
car le modulo par m = X^8 + X^4 + X^3 + X + 1 sera inclus 
dans les fonctions qui suivent par souci de stabilité !

Mais pour rendre un élément écrit sous la forme 0b... toujours 
valable comme octet, on peut l'évaluer modulo m (= 0b100011011).

-> NB: m est irréductible dans Z/2Z[X], donc on sera assurement 
placé dans un corps !
"""

def F256(f):
	"""Permet d'évaluer un certain polynôme dans F_256.

	f : polynôme vu dans Z/2Z[X] de degré strictement
	inférieur à 8.
	"""
	return(MOD(f, 0b100011011))

def DOT256(a, b):
	"""'a' et 'b' sont vus comme des octets dans F_256.

	Renvoie la multiplication entre 'a' et 'b'.
	"""
	return F256(DOT(a, b))

def SIGMA(o):
	"""Correspond à la fonction sigma.

	o : polynôme vu dans F256 de degré strictement
	inférieur à 8.
	"""
	return(LAMBDA(MOD(POWER(o, 0b11111110), 0b100011011)))

def invSIGMA(o):
	"""Correspond à la fonction sigma^{-1}.
	
	o : polynôme vu dans F256 de degré strictement
	inférieur à 8.
	"""
	return(MOD(POWER(invLAMBDA(o), 0b11111110), 0b100011011))

def createSBOX():
	"""Permet de générer la S-box sous
	la forme d'un dictionnaire.
	"""
	HEX = '0123456789abcdef'
	SBOX = {h: {} for h in HEX}
	for o in range(256):
		h = HEX[o >> 4]
		l = HEX[o & 0xF]
		SBOX[h][l] = SIGMA(o)
	return(SBOX)

def createInvSBOX():
	"""Permet de générer la Inv_S-box sous
	la forme d'un dictionnaire.
	"""
	HEX = '0123456789abcdef'
	SBOX = {h: {} for h in HEX}
	for o in range(256):
		h = HEX[o >> 4]
		l = HEX[o & 0xF]
		SBOX[h][l] = invSIGMA(o)
	return(SBOX)

"""
On n'utilisera ni createSBOX ni createInvSBOX par souci de vitesse.
On pré-calcule la S-box et la Inv_S-Box en tant qu'hexa-digits, à l'aide
de la fonction getHexSBOX et getHexINVSBOX.
On n'a qu'à les sauvegarder dans la rubrique
'constantes' qui suit, sous forme chacune d'un hexadécimal.
"""

def getHexSBOX(): # Même principe pour getHexINVSBOX qu'on n'écrit pas ici !
	"""
	Cette fonction génère la S-box sous
	forme d'un hexadécimal.
	"""
	SBOX = ""
	for o in range(256):
		SBOX += f"{SIGMA(o):02x}"
	return SBOX

# -- -- Constantes -- --
SBOX = 0x637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b27509832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cfd0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdbe0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9ee1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16
INV_SBOX = 0x52096ad53036a538bf40a39e81f3d7fb7ce339829b2fff87348e4344c4dee9cb547b9432a6c2233dee4c950b42fac34e082ea16628d924b2765ba2496d8bd12572f8f66486689816d4a45ccc5d65b6926c704850fdedb9da5e154657a78d9d8490d8ab008cbcd30af7e45805b8b34506d02c1e8fca3f0f02c1afbd0301138a6b3a9111414f67dcea97f2cfcef0b4e67396ac7422e7ad3585e2f937e81c75df6e47f11a711d29c5896fb7620eaa18be1bfc563e4bc6d279209adbc0fe78cd5af41fdda8338807c731b11210592780ec5f60517fa919b54a0d2de57a9f93c99cefa0e03b4dae2af5b0c8ebbb3c83539961172b047eba77d626e169146355210c7d

"""
À présent, appliquer SubBytes est beaucoup plus rapide
grâce à la fonction suivante :
"""

def sigma(index, S_BOX):
	"""Évalue un hexa dans la S-Box (ou la Inv_S-Box)

	index : c'est un octet qu'on preférera écrire sous forme hexa.
	S_BOX : correspond à un long hexa qu'on aura placé dans 'Constates'
	"""
	return((S_BOX >> 8*(255 - index) & 0xFF))


"""
Ici, on souhaite réécrire nos opérations sur les mots.
Pour rappel, un mot ('w' pour word) est 
un vecteur de 4 octets [w = (a_0, ..., a_3)].

On l'écrit de la façon suivante sous une forme
hexadécimale 0x... (donc de 2*4 hexa-digits).

Par exemple w = 0xae6c06db.
Python permet de directement l'évaluer comme un 
ensemble de 4 octets (w = 0xae6c06db = 0b10101110011011000000011011011011).
"""


def bytesFromWord(w):
	"""Renvoie un à un les octets du mot w
	sous la forme de tuple.

	w : Polynôme vu dans F_2^{32} de degré strictement
	inférieur à 4 (4*2 hexa-digits).
	"""
	return((w >> 24) & 0xFF, (w >> 16) & 0xFF, (w >> 8) & 0xFF, w & 0xFF)

def wordFromBytes(a_0, a_1, a_2, a_3):
	"""Renvoie le mot associé aux différents octets spécifiés.

	a_i : polynôme vu dans F256 de degré strictement
	inférieur à 8.
	"""
	return( (a_0 << 24) | (a_1 << 16) | (a_2 << 8) | a_3 )

def xsi(w, S_Box):
	"""Correspond à la fonction xsi... bruh logique :)

	w : Polynôme vu dans F_2^{32} de degré strictement
	inférieur à 4 (4*2 hexa-digits).

	Renvoie un mot !
	"""
	word = bytesFromWord(w)
	return(wordFromBytes(sigma(word[1], S_Box), sigma(word[2], S_Box), sigma(word[3], S_Box), sigma(word[0], S_Box)))

def mu(w):
	"""Correspond à la fonction mu... ça va bien l'faire oe XD

	w : Polynôme vu dans F_2^{32} de degré strictement
	inférieur à 4 (4*2 hexa-digits).

	Cette fonction correspond à une des étapes de MixColumns, à savoir
	le produit d'un mot par la matrice obtenue après permutations
	circulaires du mot c = (X, 1, 1, X+1).

	Les permutations circulaires du mot c dans la 
	matrice sont dues au module Y^4+1, on 
	détaille le produit matriciel,
	d'où l'absence de MOD(..., 0x0100000001) dans la fonction.
	"""
	word = bytesFromWord(w)
	mu0 = ADD(ADD(DOT256(0x02, word[0]), DOT256(0x03, word[1])), ADD(word[2], word[3]))
	mu1 = ADD(ADD(word[0], DOT256(0x02, word[1])), ADD(DOT256(0x03, word[2]), word[3]))
	mu2 = ADD(ADD(word[0], word[1]), ADD(DOT256(0x02, word[2]), DOT256(0x03, word[3])))
	mu3 = ADD(ADD(DOT256(0x03, word[0]), word[1]), ADD(word[2], DOT256(0x02, word[3])))
	return(wordFromBytes(mu0, mu1, mu2, mu3))

def nu(w):
	"""Correspond à la fonction nu... :/ moe trop cool les commentaires !

	w : Polynôme vu dans F_2^{32} de degré strictement
	inférieur à 4 (4*2 hexa-digits).

	"""
	word = bytesFromWord(w)
	nu0 = ADD(ADD(DOT256(0x0e, word[0]), DOT256(0x0b, word[1])), ADD(DOT256(0x0d, word[2]), DOT256(0x09, word[3])))
	nu1 = ADD(ADD(DOT256(0x09, word[0]), DOT256(0x0e, word[1])), ADD(DOT256(0x0b, word[2]), DOT256(0x0d, word[3])))
	nu2 = ADD(ADD(DOT256(0x0d, word[0]), DOT256(0x09, word[1])), ADD(DOT256(0x0e, word[2]), DOT256(0x0b, word[3])))
	nu3 = ADD(ADD(DOT256(0x0b, word[0]), DOT256(0x0d, word[1])), ADD(DOT256(0x09, word[2]), DOT256(0x0e, word[3])))
	return(wordFromBytes(nu0, nu1, nu2, nu3))

"""
À présent, on veut réécrire les opérations sur les états !

Pour rappel, un état ('S' pour state) est 
un vecteur de 4 mots [S = (w_0, ..., w_3)].

On l'écrit de la façon suivante sous une forme
hexadécimale 0x... (donc de 2*(2*4) hexa-digits).

Par exemple w = 0xac1c289af15123a98cecaf167c27160e.
"""

def wordsFromState(S):
	"""Renvoie un à un les mots de l'état S
	sous la forme de tuple.

	S : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	"""
	return((S >> 96) & 0xFFFFFFFF, (S >> 64) & 0xFFFFFFFF, (S >> 32) & 0xFFFFFFFF, S & 0xFFFFFFFF)


def stateFromWords(w_0, w_1, w_2, w_3):
	"""Renvoie l'état associé aux différents mots spécifiés.

	w_i : Polynômes vus dans F_2^{32} de degré strictement
	inférieur à 4 (4*2 hexa-digits).
	"""
	return( (w_0 << 96) | (w_1 << 64) | (w_2 << 32) | w_3 )

def MixColumns(S):
	"""Correspond à appliquer mu à l'ensemble
	des mots de S.

	S : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	"""
	State = wordsFromState(S)
	return(stateFromWords(mu(State[0]), mu(State[1]), mu(State[2]), mu(State[3])))

def InvMixColumns(S):
	"""Correspond à appliquer nu à l'ensemble
	des mots de S.

	S : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	"""
	State = wordsFromState(S)
	return(stateFromWords(nu(State[0]), nu(State[1]), nu(State[2]), nu(State[3])))

def shiftRows(S):
	"""Correspond à la fonction ShiftRows (WHAOUU).

	S : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).

	"""
	State = wordsFromState(S)
	State = (bytesFromWord(State[0]), bytesFromWord(State[1]), bytesFromWord(State[2]), bytesFromWord(State[3]))

	#Ième colonne (noté row_i)
	row_0 = wordFromBytes(State[0][0], State[1][1], State[2][2], State[3][3])
	row_1 = wordFromBytes(State[1][0], State[2][1], State[3][2], State[0][3])
	row_2 = wordFromBytes(State[2][0], State[3][1], State[0][2], State[1][3])
	row_3 = wordFromBytes(State[3][0], State[0][1], State[1][2], State[2][3])
	return(stateFromWords(row_0, row_1, row_2, row_3))

def INVshiftRows(S):
	"""Correspond à la fonction InvShiftRows... (y'en a vrm ils lisent ça ?)

	S : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).

	"""
	State = wordsFromState(S)
	State = (bytesFromWord(State[0]), bytesFromWord(State[1]), bytesFromWord(State[2]), bytesFromWord(State[3]))

	#Ième colonne (noté row_i)
	row_0 = wordFromBytes(State[0][0], State[3][1], State[2][2], State[1][3])
	row_1 = wordFromBytes(State[1][0], State[0][1], State[3][2], State[2][3])
	row_2 = wordFromBytes(State[2][0], State[1][1], State[0][2], State[3][3])
	row_3 = wordFromBytes(State[3][0], State[2][1], State[1][2], State[0][3])
	return(stateFromWords(row_0, row_1, row_2, row_3))

def SubBytes(S, S_BOX):
	"""Correspond à la fonction SubBytes, mais peut aussi
	selon le choix de la SBOX correspondre à INVSubBytes.

	S : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).

	"""
	State = wordsFromState(S)
	State = (bytesFromWord(State[0]), bytesFromWord(State[1]), bytesFromWord(State[2]), bytesFromWord(State[3]))

	#Ième colonne (noté row_i)
	row_0 = wordFromBytes(sigma(State[0][0], S_BOX), sigma(State[0][1], S_BOX), sigma(State[0][2], S_BOX), sigma(State[0][3], S_BOX))
	row_1 = wordFromBytes(sigma(State[1][0], S_BOX), sigma(State[1][1], S_BOX), sigma(State[1][2], S_BOX), sigma(State[1][3], S_BOX))
	row_2 = wordFromBytes(sigma(State[2][0], S_BOX), sigma(State[2][1], S_BOX), sigma(State[2][2], S_BOX), sigma(State[2][3], S_BOX))
	row_3 = wordFromBytes(sigma(State[3][0], S_BOX), sigma(State[3][1], S_BOX), sigma(State[3][2], S_BOX), sigma(State[3][3], S_BOX))
	return(stateFromWords(row_0, row_1, row_2, row_3))

def AddRoundKey(S_1, S_2):
	"""Correspond à la simple addition entre deux
	états.

	S_1 et S_2 : Polynômes vus dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	"""
	return(ADD(S_1, S_2))

"""
À partir de là, on a toutes les opérations de l'AES.
Il ne nous manque plus qu'à générer les RoundKeys.
C'est ce que l'on fait dans le paragraphe suivant !
"""

def Rcon(itt):
	"""Renvoie la constante associée au tour n° 'itt'.
	On l'appelle la Rcon_{itt}.

	itt : entier positif.
	"""
	j = 0x01
	for i in range((itt-1)):
		j = DOT256(j, 0x02)
	return(j)

def RconWord(itt):
	"""Renvoie le mot associé à la Rcon_{itt}, où le premier
	octet du mot est la Rcon_{itt} et le reste 0x00.

	itt : entier positif.
	"""
	return(Rcon(itt) << 24)

def getNextRoundKey(S, itt, S_Box=SBOX):
	"""Renvoie la RoundKey numéro 'itt', on aura besoin de la SBOX et aussi
	de la précédente RoundKey (si c'est la première, on aura besoin de la clé de cryptage).

	S : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	itt : entier positif (correspond au n° de la RoundKey que l'on souhaite).
	"""
	State = wordsFromState(S)

	#Ième colonne (notée row_i)
	row_0 = ADD(ADD(xsi(State[3], S_Box), RconWord(itt)), State[0])
	row_1 = ADD(row_0, State[1])
	row_2 = ADD(row_1, State[2])
	row_3 = ADD(row_2, State[3])
	return(stateFromWords(row_0, row_1, row_2, row_3))

"""
On appelle 'profondeur' le nombre de tours de notre boucle AES. On fera attention à
ce qu'elle soit >= 1.
Par souci de vitesse, on veut de la même manière qu'avec les mots et les états,
obtenir toutes les RoundKeys sous UNE forme hexadécimale.
Ce que l'on fait, c'est qu'on génère une 'roundKeys' (avec un 's').


En gros 'roundKeys' est un polynôme vu dans F_2^{128 * {profondeur}}. Sous une forme 
hexadécimale, c'est la concaténation de toutes les RoundKeys.
On crée alors 'selectRoundKey_i' qui permet de récupérer la RoundKey_{itt} 
destinée à un tour de l'AES, ainsi que "keySchedule" qui génère l'hexa 'roundKeys'.
"""

def selectRoundKey_i(S, itt, profondeur):
	"""Permet de récupérer sous forme hexadécimale la RoundKey_{itt}
	dans notre 'roundKeys'.

	S : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	-> Ici S correspond à notre hexa : 'roundKeys'.

	itt : entier positif >=1 (correspond au n° de la RoundKey que l'on souhaite récupérer).

	profondeur : entier positif (>=1) correspondant au nombre de tours de l'AES.
	"""
	roundKey = profondeur - itt
	return (S >> (roundKey*128)) & (1 << 128) - 1

def keySchedule(M, profondeur, S_BOX=SBOX):
	"""

	M : Polynôme vu dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	-> Ici M correspond à l'état de la clé secrète.

	Ici on fait attention que la profondeur soit bien un entier >=1,
	vu que ce nombre est choisi par l'utilisateur, c'est important de faire des vérifications !
	(Même si on ne le fait que dans les fonctions de cryptage et décryptage).
	"""

	roundKeys = getNextRoundKey(M, 1, S_BOX)
	for i in range(2, profondeur+1):
		roundKeys = (roundKeys << 128) | getNextRoundKey(selectRoundKey_i(roundKeys, i-1, i-1), i, S_BOX)
	return(roundKeys)


"""
À présent, on a tout pour réaliser l'AES !
On le fera sur deux états : notons S le message à crypter et M la clé secrète.

Je note :
- Epsilon_1 la fonction AddRoundKey(S, M)
- Epsilon_2 : La boucle AES -> SubBytes into ShiftRows into MixColumns into AddRoundKey
- Epsilon_3 : SubBytes into ShiftRows into AddRoundKey
"""

def AES_cryptage(S, M, profondeur, S_BOX=SBOX):
	""" Permet le cryptage d'un état par un autre !

	S et M : Polynômes vus dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	-> (S correspond au message et M la clé secrète).

	profondeur : entier positif (>=1) correspondant au nombre de tours de l'AES.
	"""

	if int(profondeur) < 1:
		return(S)

	#On génère les RoundKeys
	roundKeys = keySchedule(M, profondeur, S_BOX)

	#Epsilon 1
	S = AddRoundKey(S, M)

	#Epsilon 2
	for i in range(1, profondeur):
		S = AddRoundKey(MixColumns(shiftRows(SubBytes(S, S_BOX))), selectRoundKey_i(roundKeys, i, profondeur))

	#Epsilon 3
	S = AddRoundKey(shiftRows(SubBytes(S, S_BOX)), selectRoundKey_i(roundKeys, profondeur, profondeur))

	return(S)

def AES_decryptage(S, M, profondeur, S_BOX=SBOX, Inv_S_BOX=INV_SBOX):
	""" Permet le décryptage d'un état par un autre !

	S et M : Polynômes vus dans F_2^{128} de degré strictement
	inférieur à 4 (2*(4*2) hexa-digits).
	-> (S correspond au message crypté et M la même clé secrète que pour le cryptage de S).

	profondeur : entier positif (>=1) correspondant au nombre de tours de l'AES.
	"""

	if int(profondeur) < 1:
		return(S)

	#On génère les RoundKeys
	roundKeys = keySchedule(M, profondeur, S_BOX)

	#Epsilon_3^{-1}
	S = SubBytes(INVshiftRows(AddRoundKey(S, selectRoundKey_i(roundKeys, profondeur, profondeur))), Inv_S_BOX)

	#Epsilon_2^{-1}
	for i in range(profondeur-1, 0, -1):
		S = SubBytes(INVshiftRows(InvMixColumns(AddRoundKey(S, selectRoundKey_i(roundKeys, i, profondeur)))), Inv_S_BOX)

	#Epsilon_1^{-1}
	S = AddRoundKey(S, M)

	return(S)
