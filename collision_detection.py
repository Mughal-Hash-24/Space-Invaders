import pygame


def get_mask(image):
    return pygame.mask.from_surface(image)


def check_collision(enemy, bullet):
    enemy_mask = get_mask(enemy.img)
    bullet_mask = get_mask(bullet.img)

    offset_x = enemy.x - bullet.x + 20
    offset_y = enemy.y - bullet.y + 10

    return enemy_mask.overlap(bullet_mask, (offset_x, offset_y)) is not None


def check_collision_drop(obj, drop):
    obj_mask = get_mask(obj.img)
    drop_mask = get_mask(drop.img)

    offset_x = drop.x - obj.x + 32
    offset_y = drop.y - obj.y

    return obj_mask.overlap(drop_mask, (offset_x, offset_y)) is not None


def handle_list_collision(enemies, bullets, score):
    collided_bullets = []
    collided_enemies = []
    collided = False
    x = 0
    y = 0

    for enemy in enemies:
        for bullet in bullets:
            if check_collision(enemy, bullet):
                collided_bullets.append(bullet)
                enemy.health -= 1

                if enemy.health <= 0:
                    collided_enemies.append(enemy)

                    collided = True
                    x = bullet.x
                    y = bullet.y
                    score += enemy.enemy_type * 10

                break

    for bullet in collided_bullets:
        bullets.remove(bullet)

    for enemy in collided_enemies:
        enemies.remove(enemy)

    return collided, x, y, score


def handle_obj_with_drop_collision(obj, drops, is_bullet):
    collided_drops = []

    for drop in drops:
        if check_collision_drop(obj, drop):
            collided_drops.append(drop)
            if not is_bullet:
                if drop.type == 1:
                    obj.bullet_count += 1
                elif drop.type == 2:
                    obj.bullet_count -= 1

                if obj.bullet_count > 3:
                    obj.bullet_count = 3
                elif obj.bullet_count < 1:
                    obj.bullet_count = 1

            else:
                obj.health -= 20

    for drop in collided_drops:
        drops.remove(drop)
