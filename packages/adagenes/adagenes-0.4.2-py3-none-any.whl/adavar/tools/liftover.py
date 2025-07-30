import os
from pathlib import Path


def check_liftover_files(liftover_dir):
    """
    Checks if the liftover files exist. Downloads them if the files cannot be found

    :param liftover_dir: Directory in the host file system where the liftover files are to be stored
    """

    # HG19 -> HG38
    path = Path(liftover_dir + "/hg19ToHg38.over.chain.gz")
    if not os.path.exists(path):
        print("Could not find Liftover file: ",path,". Downloading file...")
        os.system("wget -v https://hgdownload.cse.ucsc.edu/goldenpath/hg19/liftOver/hg19ToHg38.over.chain.gz -P " + liftover_dir)
    else:
        print("Liftover file located: ",path)

    # HG38 -> HG19
    path = Path(liftover_dir + "/hg38ToHg19.over.chain.gz")
    if not os.path.exists(path):
        print("Could not find Liftover file: ", path, ". Downloading file...")
        os.system("wget -v https://hgdownload.cse.ucsc.edu/goldenpath/hg38/liftOver/hg38ToHg19.over.chain.gz -P " + liftover_dir)
    else:
        #print("Liftover file located: ",path)
        pass

    # T2T -> HG38
    path = Path(liftover_dir + "/hs1ToHg38.over.chain.gz")
    if not os.path.exists(path):
        print("Could not find Liftover file: ", path, ". Downloading file...")
        os.system("wget -v https://hgdownload.soe.ucsc.edu/goldenPath/hs1/liftOver/hs1ToHg38.over.chain.gz -P " + liftover_dir)
    else:
        print("Liftover file located: ",path)

    # HG38 -> T2T
    path = Path(liftover_dir + "/hg38ToGCA_009914755.4.over.chain.gz")
    if not os.path.exists(path):
        print("Could not find Liftover file: ", path, ". Downloading file...")
        os.system("wget -v https://hgdownload.soe.ucsc.edu/goldenPath/hg38/liftOver/hg38ToGCA_009914755.4.over.chain.gz -P " + liftover_dir)
    else:
        print("Liftover file located: ",path)
