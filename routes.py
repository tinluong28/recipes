from config import app
from controller_functions import index, register, login, dashboard, logout, create, create_recipe, review, all_users_review, display_instruction, delete_recipe, verify_username

app.add_url_rule('/', view_func=index)
app.add_url_rule('/register', view_func=register, methods=['POST'])
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/dashboard', view_func=dashboard)
app.add_url_rule('/logout', view_func=logout)
app.add_url_rule('/create', view_func=create)
app.add_url_rule('/create_recipe', view_func=create_recipe, methods=['POST'])
app.add_url_rule('/review', view_func=review)
app.add_url_rule('/all_recipes', view_func=all_users_review)
app.add_url_rule('/instruction/<recipe_id>', view_func=display_instruction)
app.add_url_rule('/<recipe_id>/delete', view_func=delete_recipe)
app.add_url_rule('/username', view_func=verify_username, methods=['POST'])
