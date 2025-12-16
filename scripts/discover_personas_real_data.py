import pandas as pd
from src.features.persona_discovery import LLMPersonaDiscovery


def main():
    print("🔹 Loading master_featured.csv ...")
    df = pd.read_csv("src/data/full_realistic_dataset/master_featured.csv")

    print("Dataset shape:", df.shape)

    # To reduce cost, sample subset
    sample_df = df.sample(n=min(400, len(df)))

    print("🔹 Running LLM Persona Discovery...")
    discovery = LLMPersonaDiscovery()

    personas_json = discovery.discover_personas(sample_df)

    print("\n✅ Personas Discovered:")
    print(personas_json)

    # Save
    with open("src/features/discovered_personas.json", "w", encoding="utf-8") as f:
        f.write(personas_json)

    print("\n📁 Saved to src/features/discovered_personas.json")


if __name__ == "__main__":
    main()
