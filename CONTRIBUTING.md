# Guidelines:

## Front-end
- Unless they are components, all pages should extend `base.page.html`
- Page or component level js files should be in the same directory as its matching html file unless its a core or common script.
- Minimize global scope whenever possible.
- Bootstrap should be used extensively.
- Inline scripts or styles need to be ported to their own respective files whenever possible.
- SASS for styling
- Javascript for scripts (typescript integrations TBD)
- Based on how the compiler works static/compiled/ folder follows the directory hierarchy.
Example:
-- `templates/common/main.scss` can be found in
-- `static/compiled/common/main.css`
- django template syntax looks like:
`{% static 'compiled/common/main.css' %}` or `{% static 'js/common/main.js' %}`
- Attach all css & js tags to block tags:
-- {% addtoblock 'css' %} <link></link>{% endaddtoblock %}
-- {% addtoblock 'js' %}<script></script>{% endaddtoblock %}
- Naming conventions:
-- pages (direct extensions of `base.page.html`) to be named `pageName.page.html`
-- components to be named `componentName.component.html`-. File directory:
-- first order children inside of `templates` represent pages
-- folder children to pages should be named components
-- folder children of components should be named per component
Example:
-- `templates/dashboard/` page level files here
-- `templates/dashboard/components/` components directories here
-- `template/dashboard/components/someComponent` component level files here
