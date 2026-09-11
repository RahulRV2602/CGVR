import matplotlib.pyplot as plt

# Region codes
INSIDE = 0   # 0000
LEFT   = 1   # 0001
RIGHT  = 2   # 0010
BOTTOM = 4   # 0100
TOP    = 8   # 1000


def compute_code(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE

    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT

    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP

    return code


def cohen_sutherland_clip(x1, y1, x2, y2,
                          xmin, ymin, xmax, ymax):

    code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
    code2 = compute_code(x2, y2, xmin, ymin, xmax, ymax)

    accept = False

    while True:

        # Case 1: Both points are inside
        if code1 == 0 and code2 == 0:
            accept = True
            break

        # Case 2: Both points are outside in the same region
        elif (code1 & code2) != 0:
            break

        # Case 3: Line needs clipping
        else:

            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

            # Find intersection with TOP boundary
            if code_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax

            # Find intersection with BOTTOM boundary
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin

            # Find intersection with RIGHT boundary
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax

            # Find intersection with LEFT boundary
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Replace the outside point
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(
                    x1, y1, xmin, ymin, xmax, ymax
                )
            else:
                x2, y2 = x, y
                code2 = compute_code(
                    x2, y2, xmin, ymin, xmax, ymax
                )

    if accept:
        return x1, y1, x2, y2
    else:
        return None


# -------------------------------
# Main Program
# -------------------------------

# Clipping window
xmin, ymin = 2, 2
xmax, ymax = 8, 6

# Original line
x1, y1 = 1, 1
x2, y2 = 10, 7

# Perform clipping
result = cohen_sutherland_clip(
    x1, y1, x2, y2,
    xmin, ymin, xmax, ymax
)

# Plotting
plt.figure(figsize=(8, 6))

# Clipping window
plt.plot(
    [xmin, xmax, xmax, xmin, xmin],
    [ymin, ymin, ymax, ymax, ymin],
    'k-',
    linewidth=2,
    label="Clipping Window"
)

# Original line
plt.plot(
    [x1, x2],
    [y1, y2],
    'r--',
    linewidth=2,
    label="Original Line"
)

# Clipped line
if result:
    cx1, cy1, cx2, cy2 = result

    plt.plot(
        [cx1, cx2],
        [cy1, cy2],
        'b-',
        linewidth=3,
        label="Clipped Line"
    )

    print("Line accepted.")
    print("Clipped Line:")
    print(f"({cx1:.2f}, {cy1:.2f}) to ({cx2:.2f}, {cy2:.2f})")

else:
    print("Line rejected completely.")

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Cohen–Sutherland Line Clipping Algorithm")
plt.grid(True)
plt.legend()
plt.axis("equal")
plt.show()