from query_expansion.utils import Utils
from query_expansion.query import Query
import click


@click.command()
@click.option("--index", default="data/title_pos_index.json", type=str, help="Path to index file.")
@click.option("--documents", default="data/documents.json", type=str, help="Path to documents file.")
@click.option("--query", default="casting dans le monde du divertissement", type=str, help="Type your query.")
@click.option("--path", default=".", type=str, help="Path to ouput results of the query.")
@click.option("--file", default="results.json", type=str, help="File name to ouput results of the query.")
@click.option("--lang", default="fr", type=click.Choice(['fr', 'en']), help="Language of the query.")
def main(
    index,
    documents,
    query,
    path,
    file,
    lang
):
    utils = Utils()
    my_index = utils.read_json_file(index)
    my_docs = utils.read_json_file(documents)

    user_query = Query(
        query=str(query),
        index=my_index,
        documents=my_docs,
        path=path,
        file=file,
        lang=lang
    )
    user_query.rank()


if __name__ == "__main__":
    main()
