import os
from pathlib import Path
import json
from typing import Optional, Union

import numpy as np

from numpy import ndarray

import torch
from torch.utils.data import DataLoader, SequentialSampler


from tqdm import tqdm

from scdrakex.tokenize.experiments import GeneVocab
# from scdrakex.tokenize.tokenizer import GeneVocab
from scdrakex.data.data_collator import DataCollator
from scdrakex.model.transformer import TransformerModel
from scdrakex.utils import load_pretrained

PathLike = Union[str, os.PathLike]

def r_embed_data(

    count_matrix: Union[list, np.ndarray],
    genes: list,
    model_dir: PathLike,
    max_length=1200,
    batch_size=64,
    use_batch_labels: Optional[bool] = False,
    obs_to_save: Optional[list] = None,
    device: Union[str, torch.device] = "cuda",
    use_fast_transformer: bool = True,
    fast_transformer_backend: str = "Linear",
) -> ndarray:
    
    """
    Embeds single-cell gene expression data using a pretrained transformer model.
    Args:
        count_matrix (Union[list, np.ndarray]): The gene expression count matrix (cells x genes).
        genes (list): List of gene names corresponding to columns in count_matrix.
        model_dir (PathLike): Path to the directory containing the pretrained model and configuration files.
        max_length (int, optional): Maximum sequence length for the transformer model. Defaults to 1200.
        batch_size (int, optional): Number of cells per batch during embedding. Defaults to 64.
        use_batch_labels (Optional[bool], optional): Whether to use batch labels for domain adaptation. Defaults to False.
        obs_to_save (Optional[list], optional): List of observation fields to save (unused in current implementation). Defaults to None.
        device (Union[str, torch.device], optional): Device to run the model on ("cuda" or "cpu"). Defaults to "cuda".
        use_fast_transformer (bool, optional): Whether to use a fast transformer backend. Defaults to True.
        fast_transformer_backend (str, optional): Backend to use for fast transformer ("Linear", etc.). Defaults to "Linear".
    Returns:
        np.ndarray: Array of shape (num_cells, embedding_dim) containing the cell embeddings.
    Notes:
        - The function loads model configuration and vocabulary from the specified model directory.
        - Only genes present in the model vocabulary are used for embedding.
        - The function normalizes the resulting embeddings to unit norm.
        - Requires the model files: "args.json", "vocab.json", and "best_model.pt" in model_dir.
    """

    print(type(count_matrix))
    print(count_matrix.shape)
    print(type(genes))
    print(len(genes))

    count_matrix = (
        count_matrix if isinstance(count_matrix, np.ndarray) else count_matrix.toarray()
    )
    
    
    if device == "cuda":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if not torch.cuda.is_available():
            print("WARNING: CUDA is not available. Using CPU instead.")
    
    # Model directory & Model files
    model_dir = Path(model_dir)
    model_config_file = model_dir / "args.json"
    vocab_file = model_dir / "vocab.json"
    model_file = model_dir / "best_model.pt"

    # Load model configs from Model directory
    with open(model_config_file, "r") as f:
        model_configs = json.load(f)

    # Load vocabulary from Model directory
    pad_token = "<pad>"
    special_tokens = [pad_token, "<cls>", "<eoc>"]
    vocab = GeneVocab.from_file(vocab_file)
    for s in special_tokens:
        if s not in vocab:
            vocab.append_token(s)
    vocab.set_default_index(vocab["<pad>"])

    # remove non indexed genes
    id_in_vocab = np.array([
        vocab[gene] if gene in vocab else -1 for gene in genes
    ])
    gene_in_vocab = list(np.array(genes)[id_in_vocab >= 0])

    gene_ids = np.array(vocab(gene_in_vocab), dtype=int)

    count_matrix = count_matrix[:, id_in_vocab >= 0]

    print(type(count_matrix))
    print(count_matrix.shape)
    print(type(gene_in_vocab))
    print(len(gene_in_vocab))

    class Dataset(torch.utils.data.Dataset):
        def __init__(self, count_matrix, gene_ids, batch_ids=None):
            self.count_matrix = count_matrix
            self.gene_ids = gene_ids
            self.batch_ids = batch_ids

        def __len__(self):
            return len(self.count_matrix)

        def __getitem__(self, idx):
            row = self.count_matrix[idx]
            nonzero_idx = np.nonzero(row)[0]
            values = row[nonzero_idx]
            genes = self.gene_ids[nonzero_idx]
            # append <cls> token at the beginning
            genes = np.insert(genes, 0, vocab["<cls>"])
            values = np.insert(values, 0, model_configs["pad_value"])
            genes = torch.from_numpy(genes).long()
            values = torch.from_numpy(values).float()
            output = {
                "id": idx,
                "genes": genes,
                "expressions": values,
            }
            if self.batch_ids is not None:
                output["batch_labels"] = self.batch_ids[idx]
            return output
    
    # create dataset
    dataset = Dataset(
        count_matrix, gene_ids, use_batch_labels if use_batch_labels else None
    )

    collator = DataCollator(
        do_padding=True,
        pad_token_id=vocab[model_configs["pad_token"]],
        pad_value=model_configs["pad_value"],
        do_mlm=False,
        do_binning=True,
        max_length=max_length,
        sampling=True,
        keep_first_n_tokens=1,
    )

    data_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        sampler=SequentialSampler(dataset),
        collate_fn=collator,
        drop_last=False,
        # num_workers=min(len(os.sched_getaffinity(0)), batch_size),
        pin_memory=True,
    )


    # Prepare model

    model = TransformerModel(
        ntoken=len(vocab),
        d_model=model_configs["embsize"],
        nhead=model_configs["nheads"],
        d_hid=model_configs["d_hid"],
        nlayers=model_configs["nlayers"],
        nlayers_cls=model_configs["n_layers_cls"],
        n_cls=1,
        vocab=vocab,
        dropout=model_configs["dropout"],
        pad_token=model_configs["pad_token"],
        pad_value=model_configs["pad_value"],
        do_mvc=True,
        do_dab=False,
        use_batch_labels=False,
        domain_spec_batchnorm=False,
        explicit_zero_prob=False,
        use_fast_transformer=use_fast_transformer,
        fast_transformer_backend=fast_transformer_backend,
        pre_norm=False,
    )
    load_pretrained(model, torch.load(model_file, map_location=device), verbose=False)
    model.to(device)
    model.eval()

    print(model)

    device = next(model.parameters()).device
    
    cell_embeddings = np.zeros(
        (len(dataset), model_configs["embsize"]), dtype=np.float32
    )

    with torch.no_grad(), torch.cuda.amp.autocast(enabled=True):
        count = 0
        for data_dict in tqdm(data_loader, desc="Embedding cells"):
            input_gene_ids = data_dict["gene"].to(device)
            src_key_padding_mask = input_gene_ids.eq(
                vocab[model_configs["pad_token"]]
            )
            embeddings = model._encode(
                input_gene_ids,
                data_dict["expr"].to(device),
                src_key_padding_mask=src_key_padding_mask,
                batch_labels=data_dict["batch_labels"].to(device)
                if use_batch_labels
                else None,
            )

            embeddings = embeddings[:, 0, :]  # get the <cls> position embedding
            embeddings = embeddings.cpu().numpy()
            cell_embeddings[count : count + len(embeddings)] = embeddings
            count += len(embeddings)
        cell_embeddings = cell_embeddings / np.linalg.norm(
            cell_embeddings, axis=1, keepdims=True
        )
    return cell_embeddings


