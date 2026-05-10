from pygame import*

init()
window_size = 1200, 700
window = display.set_mode(window_size)
player = Rect(50, 500, 70, 70)

class soul():# створення гравця у режимі битви
    pass
class button(): #
    pass
class fight(): #відкриває вікно битви та логіка
    pass
class enemy: #створення вогора та його атак хп та інше
    pass
class labirint: #створення самої локації
    pass
class boss_good_ending: #створення босса та його атак хп та інше на пацифісті
    pass
class boss_bad_ending: #створення босса та його атак і хп на геноциді(більш складна версія)
    pass
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
    window.fill((30, 255, 255))
    draw.rect(window, (200, 200, 200), player)


    display.update()
    keys = key.get_pressed()
    if keys[K_w]: player.y -= 1
    if keys[K_s]: player.y += 1
    if keys[K_d]: player.x += 1
    if keys[K_a]: player.x -= 1
