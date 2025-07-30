import os
from pathlib import Path


def get_pretrained_folder() -> Path | None:
    if os.environ.get("PRETRAINED_ROOT"):
        pretrained_path = Path(os.environ["PRETRAINED_ROOT"])
        if pretrained_path.is_dir():
            return pretrained_path
    return None


def get_pretrained_ckpt_folder(model_name) -> Path:
    pretrained_folder = get_pretrained_folder()
    if pretrained_folder is None:
        raise ValueError("PRETRAINED_ROOT is not set")
    return pretrained_folder.joinpath(f"checkpoints/{model_name}/pretrained")


def get_ckpt_path(model_name, ckpt_version) -> Path:
    return get_pretrained_ckpt_folder(model_name).joinpath(f"{ckpt_version}.ckpt")
