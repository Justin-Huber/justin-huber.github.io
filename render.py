"""Build static HTML site from directory of HTML templates and plain files."""
import shutil
import json
import os
import jinja2


def main():
    """Templated static website generator."""

    base_path = os.getcwd()
    config_path = os.path.join(base_path, 'config.json')

    try:
        config = json.load(open(config_path))
    except FileNotFoundError:
        print('Error_FileNotFound: failed to parse config.json')
        exit(1)
    except ValueError:
        print('Error_JSON: failed to parse config.json')
        exit(1)

    template_path = os.path.join(
            base_path,
            'templates/')
    for config_dict in config:
        try:
            template_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_path),
                autoescape=jinja2.select_autoescape(['html', 'xml'])
            )

            template = template_env.get_template(config_dict['template'])

            # template filled with data
            output = template.render(config_dict['context'])
        except jinja2.TemplateError:
            print('Error_Jinja: jinja2 template ' + config_dict['template'])
            exit(1)

        output_path = os.path.join(base_path, config_dict['template'])  # full path including filename

        with open(output_path, 'w') as file:  # write to output file
            file.write(output)


if __name__ == "__main__":
    main()
