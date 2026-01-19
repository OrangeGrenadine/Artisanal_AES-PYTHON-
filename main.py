"""
Créé par OrangeGrenadine
19/01/2026

Bien que ce fichier soit nommé 'main', il n'est pas le coeur du projet entier !
Le but était de réécrire tout le code fait sur SageMath... sans Sage... et sans Numpy aussi !

(vu que sur un autre poste que j'ai tendance à utiliser, il n'y est pas... moee bizarre oe :O) 

Le but ici est donc d'utiliser le moteur algèbre pour crypter/décrypter des fichiers.
"""

#Bibliothèques
import os
import argparse
from Biblio.MoteurAlgebre import AES_cryptage, AES_decryptage

"""
Je tiens à dire que la suite du fichier 'main.py' a été VibeCodé 

0: - - (c'est vraiment génial ce qu'on peut faire juste en Python) - - :0

(et oui os et argparse sont bien sur mon autre poste, pour une raison que j'ignore :0)
"""
def pad(data):
    """Ajoute du padding PKCS#7 pour arriver à un multiple de 16 octets."""
    padding_len = 16 - (len(data) % 16)
    return data + bytes([padding_len] * padding_len)

def unpad(data):
    """Retire le padding PKCS#7."""
    padding_len = data[-1]
    return data[:-padding_len]

def process_file(input_path, output_path, key_int, rounds, mode='encrypt'):
    with open(input_path, 'rb') as f:
        data = f.read()

    if mode == 'encrypt':
        data = pad(data)
        processed_data = bytearray()

        for i in range(0, len(data), 16):
            block = int.from_bytes(data[i:i+16], 'big')
            encrypted_block = AES_cryptage(block, key_int, rounds)
            processed_data.extend(encrypted_block.to_bytes(16, 'big'))
    else:
        processed_data = bytearray()
        for i in range(0, len(data), 16):
            block = int.from_bytes(data[i:i+16], 'big')
            decrypted_block = AES_decryptage(block, key_int, rounds)
            processed_data.extend(decrypted_block.to_bytes(16, 'big'))
        processed_data = unpad(processed_data)

    with open(output_path, 'wb') as f:
        f.write(processed_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Outil de cryptage AES artisanal")
    parser.add_argument("action", choices=['enc', 'dec'], help="Encrypter ou Décrypter")
    parser.add_argument("file", help="Fichier cible")
    parser.add_argument("-k", "--key", required=True, help="Clé en hexadécimal (ex: 0xb4c1...)")
    parser.add_argument("-p", "--profondeur", type=int, default=11, help="Nombre de rounds")

    args = parser.parse_args()
    
    key_int = int(args.key, 16)
    output = args.file + (".enc" if args.action == 'enc' else ".dec")
    
    print(f"Traitement de {args.file} en cours...")
    process_file(args.file, output, key_int, args.profondeur, 'encrypt' if args.action == 'enc' else 'decrypt')
    print(f"Terminé ! Fichier généré : {output}")