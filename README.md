# pydantic-ui
Pydantic UI is a way to see and edit your Pydantic models using auto generated forms and table views. Inspired by Django admin

# Dependencies

### Javascript
[JSON Editor](https://github.com/json-editor/json-editor): JSON Editor takes a JSON Schema and uses it to generate an HTML form.


# Autocomplete Fields

Define a model with an autocomplete field
```python
from pydantic_ui.datatables import DataTableModel


class MyModelClassName(DataTableModel):
    my_id_field: int
    name: str

    @classmethod
    def autocomplete_fields(cls):
        return {"name"}  # the name field is autocompleted
```

Now, some static JS is expected at the location: `static/js/{model_class_name}/{model_field_name}.js`. In our case, our model class is `MyModelClassName` and field is `name`, so our javascript must be located at `static/js/MyModelClassName/related_wikipedia_title.js`.

The contents of the javascript must be a variable referencing an associative array, that must have at least one key - `search`. The value of which is a function that returns search results based on a search parameter. Let's create a very simple function that returns a few names to choose from.

The name of the variable holding the array is important, as it must be unique. The function name must be `{model_class_name}_{model_field_name}_search`. All lower case.

```javascript
// contents of static/js/MyModelClassName/related_wikipedia_title.js
const mymodelclassname_name_search = {
    "search": (parameter) => {
        const possibleResults = [
            "Jack Sparrow",
            "Jack Frost",
            "Jack Flash",
            "Something else"
        ];
        const searchLower = parameter.toLowerCase();
        const results = possibleResults.filter(possible => possible.toLowerCase().includes(searchLower))
        return results;
    }
}
```

This javascript function will check the input of the user, convert it to lower case and compare it against the possibleResults in lower case. If the current input characters match a substring of the input list, those results are returned.

For more detail on using autocomplete, including an example using Wikipedia search results, take a look at the documentation for [autocomplete-js](https://autocomplete.trevoreyre.com/#/javascript-component)
