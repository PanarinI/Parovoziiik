class InputHandler:
    @staticmethod
    def handle_input(hero):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            hero.jump()
