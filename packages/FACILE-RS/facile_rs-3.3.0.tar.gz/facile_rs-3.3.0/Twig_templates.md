# Twig templates

The following [Twig](https://twig.symfony.com/doc/3.x/) templates can be used to display the metadata that the `run_markdown_pipeline` scripts extracts from `codemeta.json` and includes in the YAML frontmatter of the [GRAV pages](https://getgrav.org). We use a theme derived from [quark](https://github.com/getgrav/grav-theme-quark).

## Modular
### citation.twig.html
Based on the `text` modular. See [here](https://opencarp.org/download/citation) for an example.
````
{% set grid_size = theme_var('grid-size') %}

{% set grid_size = theme_var('grid-size') %}

<section class="section modular-text {{ page.header.class}}">
    <section class="container {{ grid_size }}">
        <div class="columns {{ page.header.image_align|default('align-right') }}">
            <div class="column col-12">
                {{ content|raw }}{% markdown %}
		! *{% for author in page.header.codemeta.referencePublication.author|slice(0, 3) %}{{ author.givenName }} {{ author.familyName|replace({'*': "&ast;"}) }}{% if not loop.last %}, {% endif %}{% endfor %} {% if page.header.codemeta.referencePublication.author|length > 3 %} et al{% endif %}. {{ page.header.codemeta.referencePublication.name }}. {{ page.header.codemeta.referencePublication.isPartOf.isPartOf.name }} {{ page.header.codemeta.referencePublication.isPartOf.datePublished }};{{page.header.codemeta.referencePublication.isPartOf.volumeNumber }}:{{page.header.codemeta.referencePublication.pageStart}}{% if page.header.codemeta.referencePublication.pageEnd %}{{ page.header.codemeta.referencePublication.pageEnd }}{% endif %}. [doi:{{ page.header.codemeta.referencePublication['@id']|replace({'https://doi.org/': ""}) }}]({{ page.header.codemeta.referencePublication['@id'] }})*

		```bibtex
@article{{ '{' }}{{ page.header.codemeta.name }}-paper,
	author = {{ '{' }}{% for author in page.header.codemeta.referencePublication.author %}{{ author.familyName }}, {{ author.givenName }}{% if not loop.last %} and {% endif %}{% endfor %}},
	title = {{ '{' }}{{ page.header.codemeta.referencePublication.name|replace({'openCARP': "{openCARP}"}) }}},
	journal = {{ '{' }}{{ page.header.codemeta.referencePublication.isPartOf.isPartOf.name }}},
	year = {{ '{' }}{{ page.header.codemeta.referencePublication.isPartOf.datePublished }}},
	pages = {{ '{' }}{{ page.header.codemeta.referencePublication.pageStart }}{% if page.header.codemeta.referencePublication.pageEnd %}{{ page.header.codemeta.referencePublication.pageEnd }}{% endif %}},
	volume = {{ '{' }}{{ page.header.codemeta.referencePublication.isPartOf.volumeNumber }}},
	doi = {{ '{' }}{{ page.header.codemeta.referencePublication['@id']|replace({'https://doi.org/': ""}) }}}
}
@software{{ '{' }}{{ page.header.codemeta.name }}-sw,
	author = {{ '{' }}{% for author in page.header.codemeta.author %}{% if author.familyName %}{{ author.familyName }}, {{ author.givenName }}{% if not loop.last %} and {% endif %}{% endif %}{% endfor %}},
	title = {{ '{' }}{{ page.header.codemeta.name|replace({'openCARP': "{openCARP}"}) }}},
	year = {{ '{' }}{{ page.header.codemeta.dateModified|substr(0,4) }}},
	doi = {{ '{' }}{{ page.header.codemeta.identifier[0].value }}},
	version = {{ '{' }}{{ page.header.codemeta.version }}},
	license = {{ '{' }}{{ page.header.codemeta.license.name }}},
	url	= {{ '{' }}{{ page.header.codemeta.codeRepository }}}
}
		```
		{% endmarkdown %}
            </div>
        </div>
    </section>
</section>
````

### contributors.twig.html
Based on the `text` modular. See [here](https://opencarp.org/community/contributors) for an example.
```
{% set grid_size = theme_var('grid-size') %}

<section class="section modular-text {{ page.header.class}}">
    <section class="container {{ grid_size }}">
        <div class="columns {{ page.header.image_align|default('align-right') }}">
            <div class="column col-12">
                {{ content|raw }}

                <ul>
                    {% for author in page.header.codemeta.author %}
                    {% if author['@type'] != 'Organization' %}
                    <li>
                        <span>{{ author.givenName }} {{ author.familyName }}</span>

                        {% if author['@id'] and str_starts_with(author['@id'], 'https://orcid.org/') %}
                        <a href="{{ author['@id'] }}">
                            <img src="{{ url('theme://images/orcid_16x16.png') }}" alt="ORCID" class="orcid-logo"/>
                        </a>
                        {% endif %}
                    </li>
                    {% endif %}
                    {% endfor %}
                </ul>
            </div>
        </div>
    </section>
</section>
```
