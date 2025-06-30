def normalize_coordinates(input_file, output_file):
    # Read and parse coordinates from input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
        coordinates = [tuple(map(int, line.strip().split(','))) for line in lines if line.strip()]

    # Find min and max for both axes
    min_x = min(x for x, y in coordinates)
    max_x = max(x for x, y in coordinates)
    min_y = min(y for x, y in coordinates)
    max_y = max(y for x, y in coordinates)

    # Target normalization range
    target_min = 10
    target_max = 990
    scale = target_max - target_min

    # Normalize coordinates to range 10–990
    normalized = []
    for x, y in coordinates:
        norm_x = int(((x - min_x) / (max_x - min_x)) * scale + target_min)
        norm_y = int(((y - min_y) / (max_y - min_y)) * scale + target_min)
        normalized.append((norm_x, norm_y))

    # Write normalized coordinates to output file
    with open(output_file, 'w') as f:
        for x, y in normalized:
            f.write(f"{x},{y}\n")

# Example usage:
if __name__ == "__main__":
    normalize_coordinates("input_coordinates.txt", "output_normalized.txt")
