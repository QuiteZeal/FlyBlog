# NewLog 
> Design for Spring FLY

## Structure
- `blueprints/`(Use Blueprint)
    - `__init__.py`
    - `admin.py`
    - `auth.py`
    - `blog.py`

- `templates/`
    - `admin/`
    - `auth/`
    - `blog/`
    - `base.html`
    - `macros.html`
    
- `static/`
    - `css/`
    - `js/`

- `forms.py`
- `models.py`
- `emails.py`
- `utils.py`
- `fakes.py`
    - generate demo information
- `extensions.py`

## Pages
- admin
    - manage_category.html
    - new_category.html
    - edit_category.html
    - manage_post.html
    - new_post.html
    - edit_post.html
    - manage_comment.html
    - settings.html
- auth
    - login.html
- errors
    - 400.html
    - 404.html
    - 500.html
- blog
    - index.html 
    - about.html
    - category.html
    - post.html
    - _post.html
    - _sidebar.html
