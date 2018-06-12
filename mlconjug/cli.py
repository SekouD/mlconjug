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
@click.option('-m', '--mood',
              default=None,
              help='The mood to conjugate. By default displays all moods.',
              type=click.STRING)
@click.option('-t', '--tense',
              default=None,
              help='The tense to conjugate. By default displays all tense.',
              type=click.STRING)
def main(verb, language):
    """Console script for mlconjug."""
    conjugator = mlconjug.Conjugator(language)
    result = conjugator.conjugate(verb)
    pprint(result.conjug_info)


if __name__ == "__main__":
    main()
