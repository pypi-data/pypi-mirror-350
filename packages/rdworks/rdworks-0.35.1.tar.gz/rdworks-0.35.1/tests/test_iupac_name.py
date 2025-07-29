# Note: This example requires internet connectivity to use the NCI resolver.
# and may not always return a result, due to the nature of external services.

import pandas as pd

def smiles_to_iupac_nci(smiles:str) -> str:
    from urllib.request import urlopen
    from urllib.parse import quote
    from rdkit import Chem
    try:
        m = Chem.MolFromSmiles(smiles)
        if m is not None:
            url = 'https://cactus.nci.nih.gov/chemical/structure/' + quote(smiles) + '/iupac_name'
            iupac_name = urlopen(url).read().decode('utf-8')
            return iupac_name
        else:
            return "Invalid SMILES"
    except Exception as e:
        return f"Error: {e}"

def smiles_to_iupac_stout(smiles:str) -> str:
    from STOUT import translate_forward, translate_reverse

    return translate_forward(smiles)


if __name__ == '__main__':

    df = pd.read_csv('aromatic_and_heterocyclic_derivative.csv')
    names = []
    for i, row in df.iterrows():
        smiles_string = row['structure (smiles)']
        #iupac_name = smiles_to_iupac_nci(smiles_string)
        iupac_name = smiles_to_iupac_stout(smiles_string)
        print(f"The IUPAC name for {smiles_string} is: {iupac_name}")
        names.append(iupac_name)

    df['IUPAC name'] = names
    df.to_csv('aromatic_and_heterocyclic_derivative_IUPAC_name.csv')
