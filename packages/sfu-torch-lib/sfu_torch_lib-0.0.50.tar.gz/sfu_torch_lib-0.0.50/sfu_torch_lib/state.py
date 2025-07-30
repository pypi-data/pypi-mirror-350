import logging
import os
from typing import Any

import mlflow.artifacts as artifacts
import torch
from pytorch_lightning import LightningModule

import sfu_torch_lib.io as io
import sfu_torch_lib.utils as utils

logger = logging.getLogger(__name__)


def localize_artifact(
    run_id: str,
    filename: str,
    directory: str | None = io.get_data_path(),
    basename: str | None = None,
    overwrite: bool = True,
) -> str:
    basename = os.path.basename(filename) if basename is None else basename

    target = io.generate_path(basename) if directory is None else io.generate_path(basename, directory)

    if not overwrite and io.exists(target):
        return target

    artifacts.download_artifacts(run_id=run_id, artifact_path=filename, dst_path=target)

    return target


def localize_artifact_cached(
    run_id: str,
    filename: str,
    basename: str | None = None,
    overwrite: bool = False,
    cache: bool = True,
    data_cache_path: str | None = io.get_data_cache_path(),
) -> str:
    if cache:
        assert data_cache_path is not None

    if cache:
        path_local = localize_artifact(run_id, filename, data_cache_path, basename, overwrite)
        path_local = io.localize_file(path_local, basename=basename, overwrite=overwrite)

    else:
        path_local = localize_artifact(run_id, filename, basename=basename, overwrite=overwrite)

    return path_local


def checkpoint_exists(run_id: str, filename: str = 'last.ckpt') -> bool:
    return filename in (artifact.path for artifact in artifacts.list_artifacts(run_id=run_id))


def get_localized_checkpoint_path(
    run_id: str,
    filename: str = 'last.ckpt',
    overwrite: bool = True,
    cache: bool = False,
) -> str | None:
    if not checkpoint_exists(run_id, filename):
        return None

    checkpoint_path = localize_artifact_cached(run_id, filename, f'{run_id}_{filename}', overwrite, cache)

    return checkpoint_path


def get_resumable_checkpoint_path(
    run_id: str | None,
    run_id_pretrained: str | None,
    filename: str = 'last.ckpt',
    overwrite: bool = True,
    cache: bool = False,
) -> tuple[str | None, bool]:
    if run_id:
        checkpoint_path = get_localized_checkpoint_path(run_id, filename, overwrite, cache)

        if checkpoint_path:
            return checkpoint_path, False

    if run_id_pretrained:
        checkpoint_path = get_localized_checkpoint_path(run_id_pretrained, filename, overwrite, cache)

        if checkpoint_path:
            return checkpoint_path, True

    return None, True


def get_checkpoint(run_id: str, filename: str = 'last.ckpt') -> dict[str, Any] | None:
    checkpoint_path = get_localized_checkpoint_path(run_id, filename)

    if checkpoint_path is None:
        return None

    with io.open(checkpoint_path) as checkpoint_file:
        checkpoint = torch.load(checkpoint_file)

    return checkpoint


def load_model[T: LightningModule](
    run_id: str,
    module_class: T | None = None,
    filename: str = 'last.ckpt',
    overwrite: bool = True,
    cache: bool = False,
    **kwargs,
) -> T:
    checkpoint_path = get_localized_checkpoint_path(run_id, filename, overwrite, cache)

    assert checkpoint_path

    if module_class is not None:
        module_class_asserted = module_class

    else:
        module_class_asserted = utils.get_run_class(run_id)
        assert isinstance(module_class_asserted, T.__class__)

    with io.open(checkpoint_path) as checkpoint_file:
        model = module_class_asserted.load_from_checkpoint(checkpoint_file, **kwargs)

    return model


def load_checkpoint_state(checkpoint_path: str, model: LightningModule, strict: bool = True) -> None:
    device = torch.device('cuda') if torch.cuda.device_count() else torch.device('cpu')

    with io.open(checkpoint_path) as checkpoint_file:
        checkpoint = torch.load(checkpoint_file, device)

    model.load_state_dict(checkpoint['state_dict'], strict)


def load_run_state(run_id: str, model: LightningModule, filename: str = 'last.ckpt', strict: bool = True) -> None:
    checkpoint_path = get_localized_checkpoint_path(run_id, filename)

    assert checkpoint_path

    load_checkpoint_state(checkpoint_path, model, strict)
