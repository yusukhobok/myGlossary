from glossary import Text

def importMany():
    directory = "data\\new\\"
    print(directory)
    import os
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            FileName = os.path.join(directory, file)
            print(FileName[:-3] + "gls")

            glossary = Text(FileName)
            glossary.calculate()

            import pickle

            f = open(FileName[:-3]+"gls", "wb")
            pickle.dump(glossary, f)


if __name__ == '__main__':
    importMany()