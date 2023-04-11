import csv
import argparse

def read_pubchem(path):
    titles = {}
    inchis = {}
    smiles = {}
    with open(path) as infile:
        reader = csv.DictReader(infile, delimiter=",")
        for i, row in enumerate(reader):
            cid = row["CID"]
            if row["Title"]:
                titles[cid] = row["Title"]
            if row["Title"]:
                inchis[cid] = row["InChIKey"]
            if row["Title"]:
                smiles[cid] = row["CanonicalSMILES"]
    return (titles, inchis, smiles)


def add_info(path, titles, inchis, smiles):
    path2 = path.replace(".csv", "_2.csv")
    with open(path) as infile:
        with open(path2, "w") as outfile:
            reader = csv.DictReader(infile, delimiter=",")
            writer = csv.DictWriter(outfile, delimiter=",", fieldnames=reader.fieldnames)
            writer.writeheader()
            for i, row in enumerate(reader):
                if row["Compound PubChem CID"]:
                    cid = row["Compound PubChem CID"]
                    if cid in titles:
                        row["Compound Name"] = titles[cid]
                    if cid in inchis:
                        row["Compound InChIKey"] = inchis[cid]
                    if cid in smiles:
                        row["Compound SMILES"] = smiles[cid]
                writer.writerow(row)


def main(args):
    titles, inchis, smiles = read_pubchem(args.pubchem)
    add_info(args.annos, titles, inchis, smiles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill in compounds info. Needs a csv with pubchem info, retrieved via e.g. https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/7641,7642/property/Title,InChIKey,CanonicalSMILES/CSV")
    parser.add_argument("pubchem", help="Path to the pubchem csv")
    parser.add_argument("annos", help="Path to the annotation csv")
    args = parser.parse_args()
    main(args)
