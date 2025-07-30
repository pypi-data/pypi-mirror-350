from .rx import LoRaReceiver
from .tx import LoRaTransmitter


def load_yaml_config(file_path: str) -> tuple[LoRaTransmitter, LoRaReceiver, dict[str, str | float | int | bool]]:
    """
    Load a YAML configuration file and return the transmitter and receiver objects.

    Parameters
    ----------
    file_path : str
        Path to the YAML configuration file.
    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("Parsing YAML config files requires the 'pyyaml' package. "
                          "Please install it with 'pip install pyyaml'") from e
    with open(file_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    rf_freq = float(config["fc"])
    sample_rate = float(config["fs"])
    spreading_factor = int(config["lora_sf"])
    bandwidth = float(config["lora_bw"])
    coding_rate = int(config["lora_cr"]) if "lora_cr" in config else 4
    has_header = bool(config["lora_has_header"]
                      ) if "lora_has_header" in config else True
    payload_len = int(config["payload_len"]) if "payload_len" in config else 0
    tx = LoRaTransmitter(spreading_factor, bandwidth, sample_rate,
                         has_header=has_header, coding_rate=coding_rate)
    rx = LoRaReceiver(rf_freq, spreading_factor, bandwidth, sample_rate, has_header=has_header,
                      implicit_header_coding_rate=coding_rate, implicit_header_payload_len=payload_len)

    config["num_symbols"] = 1 << spreading_factor
    config["seconds_per_symbol"] = config["num_symbols"] / bandwidth
    config["samples_per_symbol"] = round(
        sample_rate * config["num_symbols"] / bandwidth)

    return tx, rx, config
