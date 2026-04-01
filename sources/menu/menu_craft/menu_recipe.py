import arcade
import json
from entity.item import Item

path_to_recipe = "craft/recipes.json"
path_to_img = "textures/UI/recipe.png"
img_recipe = arcade.load_texture(path_to_img)

class MenuRecipe(arcade.View):

    def __init__(self, gameview):
        self.gameview = gameview
        super().__init__()

        self.background_color = arcade.color.LIGHT_BLUE

        with open(path_to_recipe, "r") as f:
            self.recipes = json.load(f)

        self.text_list = []
        self.base_positions = []
        self.icon_list = arcade.SpriteList()
        self.title_list = arcade.SpriteList()
        self.scroll_offset = 0

        self.title_sprite = arcade.Sprite()
        self.title_sprite.texture = img_recipe
        self.title_sprite.center_x = self.window.width // 2
        self.title_sprite.center_y = self.window.height - 100
        self.title_base_y = self.title_sprite.center_y
        self.title_list.append(self.title_sprite)

        start_y = self.window.height - 250
        spacing = 170

        for i, (item, data) in enumerate(self.recipes.items()):
            ingredients, result_qty = data

            text = f"{item.upper()}\n"

            for ing, qty in ingredients.items():
                text += f"- {ing} x{qty}\n"

            text += f"=> x{result_qty}"

            y_pos = start_y - i * spacing

            recipe_text = arcade.Text(
                text=text,
                x=self.window.width // 2 + 50,
                y=y_pos,
                color=(0, 0, 0),
                font_size=16,
                anchor_x="left",
                multiline=True,
                width=self.window.width - 200,
                align="left"
            )

            self.text_list.append(recipe_text)
            self.base_positions.append(y_pos)

            item_class = self.get_item_class(item)

            if item_class:
                sprite = arcade.Sprite()

                tex_input = item_class.path_or_texture

                try:
                    if isinstance(tex_input, list):
                        sprite.texture = tex_input[0]
                    elif isinstance(tex_input, str):
                        sprite.texture = arcade.load_texture(tex_input)
                    else:
                        sprite.texture = tex_input
                except Exception:
                    continue

                sprite.center_x = self.window.width // 2 - 200
                sprite.center_y = y_pos
                sprite.scale = 0.8

                self.icon_list.append(sprite)

    def get_item_class(self, name: str):
        for cls in Item.__subclasses__():
            if cls.type == name:
                return cls
        return None

    def on_draw(self):
        self.clear()

        self.title_sprite.center_y = self.title_base_y + self.scroll_offset
        self.title_list.draw()

        for i, text in enumerate(self.text_list):
            text.y = self.base_positions[i] + self.scroll_offset
            text.draw()

        for i, sprite in enumerate(self.icon_list):
            sprite.center_y = self.base_positions[i] + self.scroll_offset
        self.icon_list.draw()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.scroll_offset = min(max(self.scroll_offset - scroll_y * 40, -self.window.height * 0.4), self.window.height * 1.5)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from sources.menu.menu_craft.menu_craft import MenuCraft
            self.window.show_view(MenuCraft(gameview=self.gameview))
