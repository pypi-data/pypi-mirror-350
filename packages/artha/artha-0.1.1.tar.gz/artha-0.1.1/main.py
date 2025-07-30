import os


def main():
    folder_path = "data-final"  # Replace with the actual folder path
    data = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                lines = []
                for line in file:
                    if not line.startswith("#"):
                        if line.strip():
                            lines.append(line.strip())
                            if len(lines) == 3:
                                data.append(
                                    {
                                        "shloka_id": lines[0],
                                        "latin": lines[1],
                                        "sn": lines[2].replace("'", "ऽ"),
                                    }
                                )
                                lines = []

    print(f"Total entries: {len(data)}")
    print(data[0])
    full_sn = " ".join([entry["sn"] for entry in data])
    print("Total chars:", len(full_sn))


if __name__ == "__main__":
    main()
