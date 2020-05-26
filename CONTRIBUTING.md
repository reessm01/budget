# Guidelines:

## Front-end
1. Unless they are components, all pages should extend `base.page.html`
2. Whenever possible make components [reusable components](https://pypi.org/project/django-reusable-components/)
3. Page or component level js files should be in the same directory as its matching html file unless its a core or common script.
4. Minimize global scope whenever possible.
5. Bootstrap should be used extensively.
6. Inline scripts or styles need to be ported to their own respective files whenever possible.
7. SASS for styling
8. Javascript for scripts (typescript integrations TBD)
9. Based on how the compiler works static/compiled/ folder follows the directory hierarchy.
Example:
- `templates/common/main.scss` can be found in
- `static/compiled/common/main.css`
- django template syntax looks like:
`{% static 'compiled/common/main.css' %}` or `{% static 'js/common/main.js' %}`
10. Attach all css & js tags to block tags:
- {% addtoblock 'css' %} <link></link>{% endaddtoblock %}
- {% addtoblock 'js' %}<script></script>{% endaddtoblock %}
11. Naming conventions:
- pages (direct extensions of `base.page.html`) to be named `pageName.page.html`
- components to be named `componentName.component.html`
12. File directory:
- first order children inside of `templates` represent pages
- folder children to pages should be named components
- folder children of components should be named per component
Example:
- `templates/dashboard/` page level files here
- `templates/dashboard/components/` components directories here
- `template/dashboard/components/someComponent` component level files here
