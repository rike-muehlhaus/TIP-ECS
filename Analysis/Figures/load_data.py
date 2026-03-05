# data_utils.py
import requests
from pathlib import Path

def download_from_zenodo(filename, record_id = "18511488", outdir="data"):
    Path(outdir).mkdir(exist_ok=True)
    url = f"https://zenodo.org/record/{record_id}/files/{filename}"

    print(f"Downloading {filename} from Zenodo...")
    r = requests.get(url)

    outpath = Path(outdir) / filename
    outpath.write_bytes(r.content)

    print(f"Saved to {outpath}")
    return outpath



import zipfile

def download_and_extract(zipname, record_id="18511488", outdir="data"):
    Path(outdir).mkdir(exist_ok=True)
    url = f"https://zenodo.org/record/{record_id}/files/{zipname}"

    r = requests.get(url)
    zpath = Path(outdir) / zipname
    zpath.write_bytes(r.content)

    with zipfile.ZipFile(zpath, "r") as z:
        z.extractall(outdir)

    return outdir