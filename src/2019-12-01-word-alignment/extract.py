import re
import argparse

# count = 0
# all_sen, x = [], []
# with open("ch-en-giza.A3.final", "r", encoding="utf-8") as f:
#     x.append(f.readline())
#     for line in f:
#         if line.startswith("# Sentence pair"):
#             all_sen.append(x)
#             x = []
#             x.append(line)
#         else:
#             x.append(line)
#     if len(x) > 0:
#         all_sen.append(x)

# print(len(all_sen))

# with open("ch-en.alignment", "w", encoding="utf-8") as f:
#     for x in all_sen[-8780:]:
#         for y in x:
#             f.write(y.strip())
#             f.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="extract")
    parser.add_argument(
        "--in_file", "-i", default="./toy.A3.final", help="input file"
    )
    parser.add_argument(
        "--out_file", "-o", default="./toy.A3.final.extract", help="output file"
    )

    args = parser.parse_args()
    pattern = re.compile(r'\(\{[\d, ]*\}\)')
    final_result = []
    with open(args.in_file, "r", encoding="utf-8") as f:
        for line in f:
            find_all = pattern.findall(line)
            if len(find_all) > 0:
                result = []
                for i,p in enumerate(find_all):
                    if i == 0:
                        continue
                    p = p[3:-3]
                    if p:
                        p = p.split(" ")
                        for a in p:
                            result.append(str(int(a)-1)+"-"+str(i-1))
                final_result.append(" ".join(result))
    with open(args.out_file, "w", encoding="utf-8") as f:
        for x in final_result:
            f.write(x)
            f.write("\n")
