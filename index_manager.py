import argparse
import json
import hashlib
import sys

def calc_sha512(filepath):
    sha = hashlib.sha512()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True)
    parser.add_argument("--src-file", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--stable", action="store_true", default=False)
    parser.add_argument("--api-version", type=int, choices=[1,2], default=2)
    parser.add_argument("--repository-type", required=False)
    parser.add_argument("--toolchain-version", required=False)
    args = parser.parse_args()

    if args.api_version == 2 and not args.repository_type:
        print("Error: --repository-type is required for api-version 2", file=sys.stderr)
        sys.exit(1)

    with open(args.index) as f:
        data = json.load(f)

    selected_toolchain_version = args.toolchain_version or args.version
    sha512 = calc_sha512(args.src_file)
    bundle = {
        "version": args.version,
        "sha512": sha512,
        "toolchain": {"versions": [selected_toolchain_version]}
    }

    if args.api_version == 1:
        if not args.stable:
            bundle["tags"] = ["unstable"]
            # Hide all previous unstable entries
            for b in data["versions"]["1"]["bundles"]:
                tags = b.get("tags")
                if tags and "unstable" in tags and "hidden" not in tags:
                    tags.append("hidden")
                    b["tags"] = tags

        data["versions"]["1"]["bundles"].insert(0, bundle)
    else:
        # Validate repository-type exists in types
        valid_types = [t["type"] for t in data["versions"]["2"]["types"]]
        if args.repository_type not in valid_types:
            print(f"Error: repository-type '{args.repository_type}' not found in index.json types", file=sys.stderr)
            sys.exit(1)

        bundle["type"] = args.repository_type

        if not args.stable:
            bundle["tags"] = ["unstable"]
            # Hide all previous unstable entries for this type
            for b in data["versions"]["2"]["bundles"]:
                if b.get("type") == args.repository_type:
                    tags = b.get("tags")
                    if tags and "unstable" in tags and "hidden" not in tags:
                        tags.append("hidden")
                        b["tags"] = tags

        data["versions"]["2"]["bundles"].insert(0, bundle)

    with open(args.index, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
