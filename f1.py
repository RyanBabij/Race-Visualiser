import pygame
import sys
import math
import time

# Settings
LOGICAL_SIZE = (1000, 1000)
DOT_RADIUS = 5
COORD_FILE = 'coordinates.txt'
TIMES_FILE = 'times.txt'

def load_coordinates(filename):
    with open(filename, 'r') as file:
        coords = []
        for line in file:
            line = line.strip()
            if line:
                x, y = map(float, line.split(','))
                coords.append((x, y))
    return coords

def load_times(filename):
    with open(filename, 'r') as file:
        times = []
        for line in file:
            line = line.strip()
            if line:
                times.append(float(line))
    return times

def calculate_path_length(coords):
    total_length = 0
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        total_length += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return total_length

def scale_point(point, surf_size):
    surf_w, surf_h = surf_size
    logical_w, logical_h = LOGICAL_SIZE
    scale = min(surf_w / logical_w, surf_h / logical_h)
    x, y = point
    offset_x = (surf_w - logical_w * scale) / 2
    offset_y = (surf_h - logical_h * scale) / 2
    return (int(x * scale + offset_x), int(y * scale + offset_y))

def draw_start_finish_line(screen, coords, surf_size):
    x1, y1 = coords[0]
    x2, y2 = coords[1]
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return
    perp_dx, perp_dy = -dy / length, dx / length
    p1 = (x1 + perp_dx * 8, y1 + perp_dy * 8)
    p2 = (x1 - perp_dx * 8, y1 - perp_dy * 8)
    p1_screen = scale_point(p1, surf_size)
    p2_screen = scale_point(p2, surf_size)
    pygame.draw.line(screen, (0, 0, 255), p1_screen, p2_screen, 3)

def format_time(total_seconds):
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    millis = int((total_seconds - int(total_seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
    pygame.display.set_caption("Race visualiser")

    coords = load_coordinates(COORD_FILE)
    lap_times = load_times(TIMES_FILE)

    if len(coords) < 2 or len(lap_times) == 0:
        print("Please provide at least two coordinates and one lap time.")
        sys.exit()

    path_length = calculate_path_length(coords)
    current_lap = 0
    speed = path_length / (lap_times[current_lap] * 60)

    current_point = 0
    next_point = 1
    x, y = coords[current_point]

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20, bold=False)
    lap_start_time = time.perf_counter()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        elapsed_time = time.perf_counter() - lap_start_time

        target_x, target_y = coords[next_point]
        dx = target_x - x
        dy = target_y - y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < speed:
            x, y = target_x, target_y
            current_point = next_point
            next_point = (next_point + 1) % len(coords)
            if next_point == 1:
                current_lap = (current_lap + 1) % len(lap_times)
                speed = path_length / (lap_times[current_lap] * 60)
                lap_start_time = time.perf_counter()
        else:
            x += speed * dx / distance
            y += speed * dy / distance

        surf_size = screen.get_size()
        screen.fill((255, 255, 255))

        # Draw path in black
        scaled_coords = [scale_point(pt, surf_size) for pt in coords]
        pygame.draw.lines(screen, (0, 0, 0), True, scaled_coords, 3)

        # Draw start/finish line
        draw_start_finish_line(screen, coords, surf_size)

        # Draw moving dot in red
        dot_pos = scale_point((x, y), surf_size)
        pygame.draw.circle(screen, (255, 0, 0), dot_pos, DOT_RADIUS)

        # Draw timer
        timer_str = format_time(elapsed_time)
        timer_surf = font.render(timer_str, True, (0, 0, 0))
        screen.blit(timer_surf, (10, 10))

        # Draw lap counter
        lap_str = f"Lap: {current_lap + 1}"
        lap_surf = font.render(lap_str, True, (0, 0, 0))
        screen.blit(lap_surf, (10, 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
