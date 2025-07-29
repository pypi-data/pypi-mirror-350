import yaml


def parse_config(config_file_path: str = "config.yaml") -> dict:
    with open(config_file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def get_vector_db_type():
    config = parse_config()
    vector_db_type = config.get("vector_db").get("type")
    return vector_db_type


def get_embedding_type() -> str:
    config = parse_config()
    embedding_type = config.get("embedding").get("type")
    if embedding_type not in ['OpenAI/ada-002', 'OctoAI/gte-large', "OpenAI/text-embedding-3-large", "OpenAI/text-embedding-3-small"]:
        raise ValueError("invalid embedding type")
    return embedding_type


def get_embedding_size() -> int:
    config = parse_config()
    embedding_type = config.get("embedding").get("type")
    if embedding_type in ['OpenAI/ada-002', "OpenAI/text-embedding-3-small"]:
        return 1536
    elif embedding_type == "OpenAI/text-embedding-3-large":
        if get_vector_db_type() == "Pinecone":
            raise Exception("Pinecone with OpenAI/text-embedding-3-large not supported")
        return 3072
    else:
        return 1024
