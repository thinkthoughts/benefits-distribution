from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from .paths import ROOT


def create_outputs_archive(
    zip_name: str,
    folders: tuple[str, ...] = (
        "figures",
        "results",
        "data",
    ),
) -> Path:
    zip_path = ROOT / zip_name

    with ZipFile(
        zip_path,
        "w",
        ZIP_DEFLATED,
    ) as archive:
        for folder_name in folders:
            folder = ROOT / folder_name

            if not folder.exists():
                continue

            for file in folder.rglob("*"):
                if file.is_file():
                    archive.write(
                        file,
                        file.relative_to(ROOT),
                    )

    print(
        f"Created outputs archive: {zip_path}"
    )
    return zip_path


def display_download_links(
    zip_path: Path,
    notebook: str,
) -> None:
    notebook_path = (
        ROOT
        / "notebooks"
        / notebook
    )

    try:
        from IPython.display import (
            FileLink,
            display,
        )

        if notebook_path.exists():
            print("Notebook:")
            display(
                FileLink(
                    str(notebook_path)
                )
            )

        print("Generated outputs:")
        display(
            FileLink(
                str(zip_path)
            )
        )

    except Exception:
        print(
            "Notebook:",
            notebook_path,
        )
        print(
            "Generated outputs:",
            zip_path,
        )


def download_in_colab(
    path: Path,
    notebook: str,
) -> None:
    try:
        from google.colab import files

        files.download(
            str(path)
        )

    except Exception:
        display_download_links(
            path,
            notebook,
        )


def finalize_notebook(
    notebook: str = (
        "00_engineering_context.ipynb"
    ),
    zip_name: str = (
        "benefits-distribution-"
        "00-engineering-context-outputs.zip"
    ),
    folders: tuple[str, ...] = (
        "figures",
        "results",
        "data",
    ),
    download: bool = True,
) -> Path:
    zip_path = create_outputs_archive(
        zip_name=zip_name,
        folders=folders,
    )

    if download:
        download_in_colab(
            zip_path,
            notebook,
        )
    else:
        display_download_links(
            zip_path,
            notebook,
        )

    return zip_path
