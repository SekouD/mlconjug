# -*- coding: utf-8 -*-

"""Console script for mlconjug."""

import click
import mlconjug
from pprint import pprint


@click.command()
@click.argument('verb')
@click.option('-l', '--language',
              default='fr',
              help='The language for the conjugation model.',
              type=click.STRING)
def main(verb, language):
    """Console script for mlconjug."""
    conjugator = mlconjug.Conjugator(language)
    result = conjugator.conjugate(verb)
    pprint(result.conjug_info)


if __name__ == "__main__":
    main()
