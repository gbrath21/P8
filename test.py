def run_gml(code):
    lines = code.strip().split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        if line.strip().startswith("loop"):
            loop_header = line.strip()
            loop_indent = len(line) - len(line.lstrip())
            block_lines = []
            i += 1

            while i < len(lines):
                block_line = lines[i]
                indent = len(block_line) - len(block_line.lstrip())
                if not block_line.strip() or indent <= loop_indent:
                    break
                block_lines.append(block_line)
                i += 1

            full_block = loop_header + "\n" + "\n".join(block_lines)
            try:
                ast = parser.parse(full_block)
                execute(ast)
            except Exception as e:
                print(f"Parse error in loop block: {e}")
        else:
            try:
                ast = parser.parse(line.strip())
                execute(ast)
            except Exception as e:
                print(f"Parse error: {e}")
            i += 1
