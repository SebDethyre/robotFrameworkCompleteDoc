import sys
import re

def parse_robot_file(file_path):
    """
    Analyse un fichier .robot et extrait les sections `*** Test Cases ***`.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return

    test_cases = {}
    current_test = None
    current_content = []

    in_test_case_section = False

    for line in lines:
        # Détecte la section des cas de test
        if re.match(r'^\*\*\* Test Cases \*\*\*', line):
            in_test_case_section = True
            continue

        if in_test_case_section:
            # Identifie le début d'un nouveau cas de test
            if re.match(r'^[^\s#].*', line):
                if current_test:
                    # Sauvegarde le précédent test case
                    test_cases[current_test] = ''.join(current_content).strip()
                # Initialise un nouveau cas de test
                current_test = line.strip()
                current_content = []
            elif current_test:
                # Ajoute les lignes au contenu du cas de test courant
                current_content.append(line)

    # Sauvegarde le dernier test case
    if current_test:
        test_cases[current_test] = ''.join(current_content).strip()

    return test_cases


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python script.py <path_to_robot_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    test_cases = parse_robot_file(file_path)

    if test_cases:
        # print("Test Cases extraits :\n")
        for name, content in test_cases.items():
            # print(f"=== {name} ===\n{content}\n")
            print(f"=== {name} ===\n")
