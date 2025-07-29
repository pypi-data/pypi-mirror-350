import torch
import torch.nn as nn
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Union, Optional
import requests
from torch.nn import Sequential as Seq, Linear as Lin, ReLU
from torch_geometric.utils import scatter
from torch_geometric.nn import MetaLayer
from torch_geometric.loader import DataLoader
from torch_geometric.data import Data


def run_gql(url, api_key, gql, variables):
    headers = {"x-api-key": api_key}
    payload = {"query": gql, "variables": variables}
    return requests.post(url, headers=headers, json=payload).json()


@dataclass(frozen=True)
class MultipointModelDomainConfig:
    figtagidx2uuid: List[str]
    figtaguuid2idx: Dict[str, int]
    figactionidx2uuid: List[str]
    figactionuuid2idx: Dict[str, int]
    actionuuid2idx: Dict[str, int]
    signatureuuid2idx: Dict[str, int]
    measurementuuid2idx: Dict[str, int]
    systemuuid2idx: Dict[Optional[str], int]  # Union[None, str] in Python < 3.10
    makeuuid2idx: Dict[Optional[str], int]    # Union[None, str] in Python < 3.10


def getsefanin(s: MultipointModelDomainConfig) -> int:
    return 152


def getevalfanin(s: MultipointModelDomainConfig) -> int:
    return 5


def getsignaturefanin(s: MultipointModelDomainConfig) -> int:
    return len(set(s.signatureuuid2idx.values()))


def getactionfanin(s: MultipointModelDomainConfig) -> int:
    return len(set(s.actionuuid2idx.values()))


def getsystemfanin(s: MultipointModelDomainConfig) -> int:
    return len(set(s.systemuuid2idx.values()))


def getglobalfanin(s: MultipointModelDomainConfig) -> int:
    return getmakefanin(s) + getsystemfanin(s)


def getnodefanin(s: MultipointModelDomainConfig) -> int:
    return (
        getsefanin(s)
        + getevalfanin(s)
        + getmeasurementfanin(s)
        + getsignaturefanin(s)
        + getactionfanin(s)
    )


def getnodefanout(s: MultipointModelDomainConfig) -> int:
    return getevalfanout(s) + gettagfanout(s) + getactionfanout(s)


def getglobalfanout(s: MultipointModelDomainConfig) -> int:
    return getevalfanout(s) + gettagfanout(s) + getactionfanout(s)


def getmakefanin(s: MultipointModelDomainConfig) -> int:
    return len(set(s.makeuuid2idx.values()))


def getmeasurementfanin(s: MultipointModelDomainConfig) -> int:
    return len(set(s.measurementuuid2idx.values()))


def getevalfanout(config: MultipointModelDomainConfig) -> int:
    return 5

def gettagfanout(config: MultipointModelDomainConfig) -> int:
    return len(set(config.figtaguuid2idx.values()))

def getactionfanout(config: MultipointModelDomainConfig) -> int:
    return len(set(config.figactionuuid2idx.values()))


def getevaloutrange(s):
    n = getevalfanout(s)
    return list(range(1, n + 1))


def getuuid2idx(uuids):
    return {uuid: i + 1 for i, uuid in enumerate(uuids)}


def getuuid2idx(uuids):
    return {uuid: i + 1 for i, uuid in enumerate(uuids)}

    
def getgroupeduuid2idx(grouped_uuids):
    return {x["uuid"]: x["groupIdx"] for x in grouped_uuids}


def getmultipointmodeldomainconfig(json):
    return MultipointModelDomainConfig(
        figtagidx2uuid=json['outputTagUuids'],
        figtaguuid2idx=getuuid2idx(json['outputTagUuids']),
        figactionidx2uuid=json['outputActionUuids'],
        figactionuuid2idx=getuuid2idx(json['outputActionUuids']),
        actionuuid2idx=getgroupeduuid2idx(json['inputActionUuids']),
        signatureuuid2idx=getgroupeduuid2idx(json['inputSignatureUuids']),
        measurementuuid2idx=getgroupeduuid2idx(json['inputMeasurementUuids']),
        systemuuid2idx=getgroupeduuid2idxallownothing(json['inputSystemUuids']),
        makeuuid2idx=getgroupeduuid2idxallownothing(json['inputMakeUuids']),
    )


def getuuid2idxallownothing(args):
    original = getuuid2idx(args)
    return original

    d = dict(original)
    # Assign None the maximum value plus 1
    d[None] = max(original.values()) + 1
    return d


def getgroupeduuid2idxallownothing(args):
    original = getgroupeduuid2idx(args)
    return original
    # Create a new dict with Union[None, str] keys, copying original
    d = dict(original)
    # Assign None the maximum value plus 1
    d[None] = max(original.values()) + 1
    return d


def getmodelnumvocab():
    letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    digits = [chr(i) for i in range(ord('0'), ord('9') + 1)]
    return ['|'] + letters + digits + ['-', ' ', '.']


def getmodelnumchar2vocabidx():
    vocab = getmodelnumvocab()
    # Enumerate starts at 0, so add 1 for 1-based indexing like Julia
    return {str(c): i + 1 for i, c in enumerate(vocab)}


def getvocabidxs(max_chars, text, char2vocabidx):
    text = "" if text is None else text
    return [
        char2vocabidx[uppercase_char] if i < len(text) and (uppercase_char := text[i].upper()) in char2vocabidx
        else char2vocabidx["|"]
        for i in range(max_chars)
    ]


def getmodelnumembedlen():
    """Return the embedding length for model numbers."""
    return 4


def getnummodelmaxchars():
    """Return the maximum number of characters for model numbers."""
    return 5


def get_net_version(url, api_key, net_version_uuid):
    query = """query GetNetVersion($uuid: ID!) {
      getNetVersion(uuid: $uuid){
        uuid
        net_uuid
        net {
            feed {
                targeta_uuid
                targetb_uuid
            }
        }
        config {
          context
          architecture
          domain_config_json
        }
      }
    }"""
    variables = {
        "uuid": net_version_uuid
    }
    net_version = run_gql(url, api_key, query, variables)
    return net_version['data']['getNetVersion']


def get_raw_samples(url, api_key, uuids):
    query = """query GetMultipointSamples($uuids: [ID]!){
        getNetSamples(uuids:$uuids){
            uuid
            x_json
            y_json
          }
        }"""
    variables = {
        "uuids": uuids
    }
    res = run_gql(url, api_key, query, variables)
    return res['data']['getNetSamples']


# def get_dataset(url, api_key, dataset_uuid):
#     query = """query GetNetSamplesByDataset($uuid: ID!) {
#         getNetSamplesByDataset(uuid: $uuid) {
#             multipoint {
#                 uuid
#                 y {
#                     nodes {
#                         evalLevel
#                         tagUuids
#                         actionUuids
#                     }
#                 }
#                 x {
#                     nodes {
#                         makeUuid
#                         systemUuid
#                         modelNum
#                         readings {
#                             se
#                             evalLevel
#                             measurementUuid
#                             signatureUuids
#                             actionUuids
#                         }
#                     }
#                 }
#             }
#         }
#     }"""
#     variables = {
#         "uuid": dataset_uuid
#     }
#     res = run_gql(url, api_key, query, variables)
#     return [item['multipoint'] for item in res['data']['getNetSamplesByDataset']]


def get_dataset(url, api_key, dataset_uuid):
    query = """query GetNetSamplesByDataset($uuid: ID!) {
        getNetSamplesByDataset(uuid: $uuid) {
            uuid
            x_json
            y_json
        }
    }"""
    variables = {"uuid": dataset_uuid}
    res = run_gql(url, api_key, query, variables)
    return res["data"]["getNetSamplesByDataset"]


def forceminmax(x, min_se=0, max_se=150):
    """Clamp a value between min_se and max_se."""
    return min(max_se, max(min_se, x))


def encodecomponentfeatures(domain_config, component, augmentation=False):
    """
    Encode features for a component's readings in a multipoint context, version 2 using PyTorch.
    
    Parameters:
    - domain_config: Object containing configuration data, including UUID-to-index mappings and fan-in values.
    - component: Dictionary with 'readings', a list of reading dictionaries.
    - augmentation: Boolean flag to enable sound energy augmentation (default: False).
    
    Returns:
    - A PyTorch tensor where each row corresponds to a reading and columns are concatenated feature encodings.
    """
    # Process sound energies with optional augmentation
    soundenergies = []
    for r in component['readings']:
        if r['se'] is None:
            se = -1
        elif augmentation:
            capped_se = forceminmax(r['se'])
            se_min = forceminmax(capped_se * 0.95)
            se_max = forceminmax(capped_se * 1.05)
            # PyTorch triangular distribution (left, mode, right)
            se = torch.distributions.Triangular(
                torch.tensor(se_min),
                torch.tensor(capped_se),
                torch.tensor(se_max)
            ).sample()
        else:
            se = forceminmax(r['se'])
        soundenergies.append(int(round(se.item() if torch.is_tensor(se) else se))+1)
        
    
    # Extract evaluation levels
    eval_levels = [r['evalLevel'] for r in component['readings']]
    
    # Encode measurement indices, using None for missing UUIDs
    encoded_measurement_idxs = [
        domain_config.measurementuuid2idx.get(r['measurementUuid'], None)
        for r in component['readings']
    ]

    
    # Encode signatures as lists of indices
    encoded_reading_signatures = [
        [
            domain_config.signatureuuid2idx[x] 
            for x in reading['signatureUuids'] 
            if x in domain_config.signatureuuid2idx
        ] 
        for reading in component['readings']
    ]
    
    
    # Encode actions as lists of indices
    encoded_reading_actions = [
        [domain_config.actionuuid2idx[x] for x in reading['actionUuids']
         if x in domain_config.actionuuid2idx]
        for reading in component['readings']
    ]
    
    
    # Get fan-in values from domain_config (assuming they are attributes; adjust if they are methods)
    se_fanin = getsefanin(domain_config)  # e.g., 151 for sound energies 0-150
    eval_fanin = getevalfanin(domain_config)
    measurement_fanin = getmeasurementfanin(domain_config)
    signature_fanin = getsignaturefanin(domain_config)
    action_fanin = getactionfanin(domain_config)
    
    # Convert lists to PyTorch tensors
    soundenergies = torch.tensor(soundenergies, dtype=torch.long)
    eval_levels = torch.tensor(eval_levels, dtype=torch.long) - 1  # Shift to 0-based indexing
    
    # One-hot encode sound energies (0 to se_fanin-1)
    soundenergies_onehot = torch.nn.functional.one_hot(soundenergies, num_classes=se_fanin).float()
    
    # One-hot encode evaluation levels (1 to eval_fanin, already shifted)
    eval_levels_onehot = torch.nn.functional.one_hot(eval_levels, num_classes=eval_fanin).float()
    
    # One-hot encode measurement indices, with zeros for None
    measurement_onehot = torch.zeros(len(encoded_measurement_idxs), measurement_fanin)
    for i, idx in enumerate(encoded_measurement_idxs):
        if idx is not None:
            measurement_onehot[i, idx - 1] = 1  # Indices are 1-based
    
    # Multi-hot encode signatures and actions
    def multihotbatch(lists, num_classes):
        """Convert lists of indices into a multi-hot encoded tensor."""
        matrix = torch.zeros(len(lists), num_classes)
        for i, idxs in enumerate(lists):
            for idx in idxs:
                matrix[i, idx - 1] = 1  # Indices are 1-based
        return matrix
    
    signatures_multihot = multihotbatch(encoded_reading_signatures, signature_fanin)
    actions_multihot = multihotbatch(encoded_reading_actions, action_fanin)
    
    # Concatenate all feature tensors horizontally
    features = torch.cat([
        soundenergies_onehot,
        eval_levels_onehot,
        measurement_onehot,
        signatures_multihot,
        actions_multihot
    ], dim=1)
    
    return features


def gensampleinput(config, sample_raw, augmentation=False):
    """
    Generate sample input for a multipoint context, converting Julia code to Python.
    
    Parameters:
    - config: Configuration object containing domain_config and architecture.
    - sample: Dictionary containing input data with nested structure.
    - augmentation: Boolean flag for data augmentation (default: False).
    
    Returns:
    - Dictionary containing processed features and adjacency matrices.
    """
    print("*********** ^^^^^ ***** ^^^^^ gensampleinput.sample_raw: ", json.dumps(sample_raw))
    x_json = sample_raw["x_json"]
    x = json.loads(json.loads(x_json))

    domain_config = config['domain_config']

    print("*********** ^^^^^ ***** ^^^^^ x2: ", json.dumps(x))
    
    # Encode reading features for the first node
    reading_features = encodecomponentfeatures(
        domain_config,
        x['nodes'][0],
        augmentation=augmentation
    )
    
    # Determine number of components from reading features
    n = reading_features.shape[1]
    
    # Create adjacency matrices
    # Fully connected graph for readings
    reading_adj_mat = torch.ones((n, n), dtype=torch.float32)
    # 1x1 adjacency matrix for component (hard-coded for 1-component equipment)
    component_adj_mat = torch.ones((1, 1), dtype=torch.float32)
    
    # Get model number character to vocabulary index mapping
    modelnumchar2vocabidx = getmodelnumchar2vocabidx()
    
    # Convert model number to vocabulary indices
    model_num_idxs = getvocabidxs(
        getnummodelmaxchars(),
        x['nodes'][0]['modelNum'],
        modelnumchar2vocabidx
    )
    model_num_idxs = torch.tensor(model_num_idxs, dtype=torch.long)
    
    # Retrieve system and make indices from domain configuration
    system_idx = domain_config.systemuuid2idx.get(
        x['nodes'][0]['systemUuid'],
        None
    )
    make_idx = domain_config.makeuuid2idx.get(
        x['nodes'][0]['makeUuid'],
        None
    )
    
    # Get fan-in sizes for systems and makes
    system_fanin = getsystemfanin(domain_config)
    make_fanin = getmakefanin(domain_config)

    
    # Create one-hot encodings for system_idx
    system_onehot = torch.zeros(system_fanin)
    if system_idx is not None:
        system_onehot[system_idx - 1] = 1  # Adjust for 0-based indexing
    else:
        system_onehot[-1] = 1  # Set last element for default case
    
    # Create one-hot encodings for make_idx
    make_onehot = torch.zeros(make_fanin)
    if make_idx is not None:
        make_onehot[make_idx - 1] = 1
    else:
        make_onehot[-1] = 1
    
    # Concatenate one-hot encodings and reshape to column vector
    component_x = torch.concatenate([system_onehot, make_onehot])
    component_x = torch.tensor(component_x, dtype=torch.float32).unsqueeze(1)
    
    # Return processed data as a dictionary
    return {
        'reading_adj_mat': reading_adj_mat,
        'component_adj_mat': component_adj_mat,
        'model_num_idxs': model_num_idxs,
        'component_x': component_x.t(),
        'reading_features': reading_features,
    }


def gensampletarget(config, sample_raw):
    y_json = sample_raw["y_json"]
    y = json.loads(json.loads(y_json))

    print("*********** ^^^^^ ***** ^^^^^ y2: ", json.dumps(y))

    domain_config = config['domain_config']
    
    actionUuids = y['nodes'][0]['actionUuids']
    tagUuids = y['nodes'][0]['tagUuids']
    evalLevel = y['nodes'][0]['evalLevel']

    
    # Filter and map actionUuids to indices
    # In Julia: filter then map; in Python: list comprehension
    action_idxs = [
        domain_config.figactionuuid2idx[x]
        for x in actionUuids
        if x in domain_config.figactionuuid2idx
    ]
    
    # Filter and map tagUuids to indices
    tag_idxs = [
        domain_config.figtaguuid2idx[x]
        for x in tagUuids
        if x in domain_config.figtaguuid2idx
    ]
    
    # One-hot encoding for evalLevel
    eval_range = getevaloutrange(domain_config)  # List of possible eval levels
    eval_index = eval_range.index(evalLevel)     # Find 0-based index
    onehot_vec = torch.nn.functional.one_hot(
        torch.tensor(eval_index),
        num_classes=len(eval_range)
    ).float()  # Convert to float32 as in Julia
    
    # Multi-hot encoding for tags
    n_tags = len(domain_config.figtaguuid2idx)
    multihot_tag = torch.zeros(n_tags, dtype=torch.float32)
    tag_indices = torch.tensor(
        [i - 1 for i in tag_idxs],  # Convert 1-based to 0-based indices
        dtype=torch.long
    )
    multihot_tag[tag_indices] = 1  # Set positions to 1
    
    # Multi-hot encoding for actions
    n_actions = len(domain_config.figactionuuid2idx)
    multihot_action = torch.zeros(n_actions, dtype=torch.float32)
    action_indices = torch.tensor(
        [i - 1 for i in action_idxs],  # Convert 1-based to 0-based indices
        dtype=torch.long
    )
    multihot_action[action_indices] = 1  # Set positions to 1
    
    # Concatenate all vectors and reshape to column vector (n, 1)
    nf = torch.cat([onehot_vec, multihot_tag, multihot_action], dim=0).unsqueeze(1)
    
    # Create ef as a 1x1 tensor (kept despite TODO note in Julia code)
    ef = torch.ones(1, 1, dtype=torch.float32)
    
    # Return as a dictionary (Python equivalent of Julia's named tuple)
    return {'nf': nf.t(), 'ef': ef.t()}


def create_edge_index_with_self_loops(n):
    sources = [i for i in range(n) for _ in range(n)]
    targets = [j for j in range(n) for j in range(n)]
    edge_index = torch.tensor([sources, targets], dtype=torch.int64)
    return edge_index


def gensample(config, sample_raw, augmentation=False):
    print("*********** ^^^^^ ***** ^^^^^ gensample.sample_raw: ", json.dumps(sample_raw))
    domain_config = config['domain_config']
    gnn_input = gensampleinput(config, sample_raw, augmentation=augmentation)
    x_readings = gnn_input['reading_features']
    target = gensampletarget(config, sample_raw)
    num_nodes = x_readings.shape[0]
    edge_index = create_edge_index_with_self_loops(num_nodes)
    num_edges = edge_index.size()[1]
    return Data(
        x=x_readings,
        y=target['nf'],
        edge_attr=torch.ones(num_edges,1),
        edge_index=edge_index,
        global_attr=gnn_input['component_x'],
    )


class EdgeModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.edge_mlp = Seq(Lin(2 * 13 + 4 + 1, 32), ReLU(), Lin(32, 32))

    def forward(self, src, dst, edge_attr, u, batch):
        out = torch.cat([src, dst, edge_attr, u[batch]], 1)
        return self.edge_mlp(out)

class NodeModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.node_mlp_1 = Seq(Lin(32 + 13, 32), ReLU(), Lin(32, 32))
        self.node_mlp_2 = Seq(Lin(32 + 13 + 1, 64), ReLU(), Lin(64, 64))

    def forward(self, x, edge_index, edge_attr, u, batch):
        row, col = edge_index
        out = torch.cat([x[row], edge_attr], dim=1)
        out = self.node_mlp_1(out)
        out = scatter(out, col, dim=0, dim_size=x.size(0),
                      reduce='mean')
        out = torch.cat([x, out, u[batch]], dim=1)
        return self.node_mlp_2(out)

class GlobalModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.global_mlp = Seq(Lin(1 + 64, 512), ReLU(), Lin(512, 300))

    def forward(self, x, edge_index, edge_attr, u, batch):
        out = torch.cat([
            u,
            scatter(x, batch, dim=0, reduce='mean'),
        ], dim=1)
        return self.global_mlp(out)


class EdgeModel(torch.nn.Module):
    def __init__(self, node_fan_in, node_fan_out, edge_fan_in, edge_fan_out, global_fan_in, global_fan_out):
        super().__init__()
        self.edge_mlp = Seq(Lin(2*node_fan_in + edge_fan_in + global_fan_in, 32), ReLU(), Lin(32, 32))

    def forward(self, src, dst, edge_attr, u, batch):
        out = torch.cat([src, dst, edge_attr, u[batch]], 1)
        return self.edge_mlp(out)


class NodeModel(torch.nn.Module):
    def __init__(self, node_fan_in, node_fan_out, edge_fan_in, edge_fan_out, global_fan_in, global_fan_out):
        super().__init__()
        self.node_mlp_1 = Seq(Lin(32 + node_fan_in, 32), ReLU(), Lin(32, 32))
        self.node_mlp_2 = Seq(Lin(32 + node_fan_in + global_fan_in, 64), ReLU(), Lin(64, node_fan_out))

    def forward(self, x, edge_index, edge_attr, u, batch):
        row, col = edge_index
        out = torch.cat([x[row], edge_attr], dim=1)
        out = self.node_mlp_1(out)
        out = scatter(out, col, dim=0, dim_size=x.size(0),
                      reduce='mean')
        out = torch.cat([x, out, u[batch]], dim=1)
        return self.node_mlp_2(out)


class GlobalModel(torch.nn.Module):
    def __init__(self, node_fan_in, node_fan_out, edge_fan_in, edge_fan_out, global_fan_in, global_fan_out):
        super().__init__()
        self.global_mlp = Seq(Lin(global_fan_in + node_fan_out, 512), ReLU(), Lin(512, global_fan_out))

    def forward(self, x, edge_index, edge_attr, u, batch):
        out = torch.cat([
            u,
            scatter(x, batch, dim=0, reduce='mean'),
        ], dim=1)
        return self.global_mlp(out)


def parse_mat(d, mat_name, dims_name):
    return torch.tensor(d[mat_name]).reshape(d[dims_name][::-1]).t()


def parse_real_data(json_item):
    x = parse_mat(json_item, "x", "x_dims")
    y = parse_mat(json_item, "y", "y_dims")
    edge_attr = parse_mat(json_item, "edge_attr", "edge_attr_dims")
    edge_index = parse_mat(json_item, "edge_index", "edge_index_dims")
    x = parse_mat(json_item, "x", "x_dims")
    return Data(x=x, y=y, edge_attr=edge_attr, edge_index=edge_index)


def get_gnn_data(sample):
    return Data(
        x=sample['x'],
        y=sample['y']['nf'],
        edge_attr=torch.ones(1,1),
        edge_index=torch.ones(2,1).int(),
        x_readings_adj_mat=sample['x_readings_adj_mat'],
        x_readings=sample['x_readings'],
    )


def gen_samples_from_uuids(url, api_key, uuids, model_config):
    raw_samples = get_raw_samples(url, api_key, uuids)
    return [gensample(model_config, item, augmentation=False) for item in raw_samples]


# def gen_samples_from_dataset(url, api_key, dataset_uuid, model_config):
#     return load_dataset(url, api_key, dataset_uuid, model_config)


# def load_dataset(url, api_key, dataset_uuid, model_config):
#     dataset = get_dataset(url, api_key, dataset_uuid)
#     return [gensample(model_config, item, augmentation=False) for item in dataset]


def gen_samples_from_dataset(url, api_key, dataset_uuid, model_config):
    raw_samples = get_dataset(url, api_key, dataset_uuid)
    return load_dataset(url, api_key, raw_samples, model_config)


def load_dataset(url, api_key, raw_samples, model_config):
    return [
        gensample(model_config, item, augmentation=False)
        for item in raw_samples
    ]


def run_update_net_version(url, api_key, net_version_input):
    query = """mutation UpdateNetVersion($input: UpdateNetVersionInput!){
        updateNetVersion(input: $input){
            id
            uuid
            name
            created_at
            updated_at
            trained_at
            queued_at
            net_uuid
            training_failed_at
            training_started_at
            context
            train_checksum
            test_checksum
            source_size
            train_loss
            test_loss
            train_acc
            test_acc
            architecture    
            config_checksum
            needs_testing
            is_latest
            is_default
            is_dev_default
        }
    }"""
    variables = {"input": net_version_input}
    print("*********** ^^^^^ ***** ^^^^^ run_update_net_version.net_version_input: ", json.dumps(net_version_input))
    run_gql(url, api_key, query, variables)


def run_net_version_training_started_gql(url, api_key, net_version_uuid):
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    net_version_input = {
        "uuid": net_version_uuid,
        "training_started_at": formatted_time
    }
    return run_update_net_version(url, api_key, net_version_input)


def run_net_version_training_ended_gql(url, api_key, net_version_uuid, train_loss, train_acc, test_acc):
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    net_version_input = {
        "uuid": net_version_uuid,
        "trained_at": formatted_time,
        "train_loss": 5.0,
        "train_acc": 6.0,
        "test_acc": 7.0,
    }
    # print the values and types of the variables
    print("run_net_version_training_ended_gql .............................*** ")
    print("train_loss:", train_loss, type(train_loss))
    print("train_acc:", train_acc, type(train_acc))
    print("test_acc:", test_acc, type(test_acc))
    return run_update_net_version(url, api_key, net_version_input)


def run_alert_training_progress_gql(url, api_key, net_uuid, net_version_uuid, progress):
    percentage = int(progress * 100)
    run_alert_training_msg_gql(
        url, 
        api_key, 
        net_uuid, 
        net_version_uuid, 
        f"Training progress: {percentage}%"
    )


def run_alert_training_msg_gql(url, api_key, net_uuid, net_version_uuid, msg):
    net_version_input = {
        "net_uuid": net_uuid,
        "net_version_uuid": net_version_uuid,
        "msg": msg,
    }
    query = """mutation AlertTrainingMsg($input: TrainingMsgInput!){
        alertTrainingMsg(input: $input){
            net_uuid
            net_version_uuid
            msg
        }
    }"""
    variables = {"input": net_version_input}
    run_gql(url, api_key, query, variables)


def hello(url, api_key):
    node_fan_in = 5
    node_fan_out = 27
    edge_fan_in = 1
    edge_fan_out = 32
    global_fan_in = 1
    global_fan_out = 64
    component_model = MetaLayer(
        EdgeModel(node_fan_in, node_fan_out, edge_fan_in, edge_fan_out, global_fan_in, global_fan_out),
        NodeModel(node_fan_in, node_fan_out, edge_fan_in, edge_fan_out, global_fan_in, global_fan_out),
        GlobalModel(node_fan_in, node_fan_out, edge_fan_in, edge_fan_out, global_fan_in, global_fan_out)
    )
    x = torch.randn(20, node_fan_in)
    edge_attr = torch.randn(40, edge_fan_in)
    u = torch.randn(2, global_fan_in)
    batch = torch.tensor([0] * 10 + [1] * 10)
    edge_index = torch.randint(0, high=10, size=(2, 20), dtype=torch.long)
    edge_index = torch.cat([edge_index, 10 + edge_index], dim=1)
    x_out, edge_attr_out, u_out = component_model(x, edge_index, edge_attr, u, batch)
    assert x_out.size() == (20, node_fan_out)
    assert edge_attr_out.size() == (40, edge_fan_out)
    assert u_out.size() == (2, global_fan_out)
    print(u_out[0].tolist())
    print("hello world7")