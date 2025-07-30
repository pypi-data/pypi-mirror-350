def sort_file(input_file, output_file):
    with open(input_file) as f:
        with open(output_file, "w") as o:
            o.write("\n".join(sorted(f.read().splitlines())))

sort_file("intermap.txt", "new-intermap.txt")
